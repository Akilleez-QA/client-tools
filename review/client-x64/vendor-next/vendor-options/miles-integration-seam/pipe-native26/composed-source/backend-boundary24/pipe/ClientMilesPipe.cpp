#include "Session.h"
#include "../../native-startup25/ClientMilesStartup.h"
#include <cstring>
#include <limits>

namespace ClientMiles {
struct DigitalDriver {
    MilesWire::Handle wire;
    const ClientMilesPipe::Session *owner;
};
} // namespace ClientMiles

namespace {
ClientMilesPipe::Session *selectedSession = 0;

void fail(ClientMiles::FailureReason reason, const char *message) {
    throw ClientMiles::Failure(reason, message);
}

void checkStatus(uint32_t status) {
    using ClientMiles::FailureReason;
    switch (status) {
    case StartupBridge::Success:
        return;
    case StartupBridge::Unsupported:
        fail(FailureReason::Unsupported, "unsupported Miles operation");
        break;
    case StartupBridge::InvalidResource:
        fail(FailureReason::InvalidDriver, "invalid Miles driver");
        break;
    case StartupBridge::InvalidFields:
        fail(FailureReason::InvalidArgument, "invalid Miles arguments");
        break;
    case StartupBridge::LifecycleRefused:
        fail(FailureReason::WrongState, "Miles lifecycle refused operation");
        break;
    case StartupBridge::TextTooLong:
        fail(FailureReason::ResultLimit, "Miles result exceeds text limit");
        break;
    case StartupBridge::InputBudgetExceeded:
        fail(FailureReason::InputLimit, "Miles retained input limit");
        break;
    case StartupBridge::VersionQueryFailed:
        fail(FailureReason::QueryFailed, "Miles version query failed");
        break;
    default:
        fail(FailureReason::BackendFailed, "unknown backend result");
    }
}

ClientMiles::OwnedText ownedText(const StartupBridge::OwnedReply &reply) {
    ClientMiles::OwnedText out;
    out.isNull = reply.result.null_mask == MilesStartup::TextNull;
    if (!out.isNull) {
        if (reply.text.empty() || reply.text.back() ||
            std::memchr(&reply.text[0], 0, reply.text.size() - 1))
            fail(ClientMiles::FailureReason::BackendFailed, "invalid owned backend text");
        out.value.assign(reinterpret_cast<const char *>(&reply.text[0]), reply.text.size() - 1);
    } else if (!reply.text.empty()) {
        fail(ClientMiles::FailureReason::BackendFailed, "null backend text contains bytes");
    }
    return out;
}

uint32_t floatBits(float value) {
    static_assert(sizeof(float) == sizeof(uint32_t), "wire F32 width");
    uint32_t bits;
    std::memcpy(&bits, &value, sizeof bits);
    return bits;
}

MilesWire::Call driverCall(ClientMilesPipe::Session &session, ClientMiles::HDIGDRIVER driver) {
    session.requireRunning();
    // Compare the opaque identity before inspecting any pointed-to bytes.
    if (!driver || driver != session.driver.get() || driver->owner != &session)
        fail(ClientMiles::FailureReason::InvalidDriver, "driver does not belong to selected Miles session");
    MilesWire::Call fields = {};
    fields.target = driver->wire;
    return fields;
}

intptr_t preferenceResult(const StartupBridge::OwnedReply &reply) {
    return static_cast<intptr_t>(MilesStartup::signedValue(reply.result.return_bits));
}
} // namespace

namespace ClientMilesPipe {
Session::Session(std::unique_ptr<Channel> channel)
    : started(false), stopped(false), channel_(std::move(channel)), closed_(false),
      faulted_(false) {
    if (selectedSession || !channel_)
        fail(ClientMiles::FailureReason::WrongState, "one Miles session must be selected");
    selectedSession = this;
}

Session::~Session() {
    // No implicit vendor calls, retry or success claim on abandonment. The
    // concrete channel owns process termination if normal close was incomplete.
    if (selectedSession == this)
        selectedSession = 0;
}

Session &Session::selected() {
    if (!selectedSession)
        fail(ClientMiles::FailureReason::WrongState, "Miles implementation not selected");
    return *selectedSession;
}

void Session::requireAvailable() const {
    if (faulted_)
        fail(ClientMiles::FailureReason::BackendFailed, "Miles session has an uncertain outcome");
    if (stopped || closed_)
        fail(ClientMiles::FailureReason::WrongState, "Miles session already stopped");
}

void Session::requireRunning() const {
    requireAvailable();
    if (!started)
        fail(ClientMiles::FailureReason::WrongState, "Miles is not started");
}

StartupBridge::OwnedReply Session::request(uint32_t opcode, const MilesWire::Call &fields,
                                           MilesTransport::Bytes text) {
    if (faulted_ || closed_)
        fail(ClientMiles::FailureReason::BackendFailed,
             "Miles session cannot issue another request");
    StartupBridge::OwnedReply reply;
    try {
        reply = channel_->call(opcode, fields, text);
    } catch (...) {
        faulted_ = true;
        fail(ClientMiles::FailureReason::BackendFailed, "Miles channel failed");
    }
    if (!StartupBridge::knownStatus(reply.result.transport_status)) {
        faulted_ = true;
        fail(ClientMiles::FailureReason::BackendFailed, "unknown Miles channel status");
    }
    // Known, validated operation refusals are distinguishable from an uncertain
    // transport outcome. They do not manufacture a successful SDK return value.
    checkStatus(reply.result.transport_status);
    return reply;
}

void Session::close() {
    if (faulted_)
        fail(ClientMiles::FailureReason::BackendFailed, "cannot retry an uncertain Miles close");
    if (!stopped || started || closed_)
        fail(ClientMiles::FailureReason::WrongState, "Miles shutdown must precede close");
    request(MilesWire::SessionClose, MilesWire::Call());
    try {
        channel_->finish();
    } catch (...) {
        faulted_ = true;
        fail(ClientMiles::FailureReason::BackendFailed, "Miles channel teardown failed");
    }
    closed_ = true;
}
} // namespace ClientMilesPipe

namespace ClientMiles {
int32_t startup() {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    session.requireAvailable();
    if (session.started)
        fail(FailureReason::WrongState, "Miles startup already completed");
    StartupBridge::OwnedReply reply = session.request(MilesWire::AIL_startup, MilesWire::Call());
    const int32_t value = static_cast<int32_t>(MilesStartup::signedValue(reply.result.return_bits));
    session.started = value != 0;
    return value;
}

void shutdown() {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    session.requireRunning();
    session.request(MilesWire::AIL_shutdown, MilesWire::Call());
    session.started = false;
    session.stopped = true;
}

intptr_t get_preference(uint32_t number) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    session.requireRunning();
    if (number != 1 && number != 42)
        fail(FailureReason::InvalidArgument, "unsupported preference identifier");
    MilesWire::Call fields = {};
    fields.value[0] = number;
    return preferenceResult(session.request(MilesWire::AIL_get_preference, fields));
}

intptr_t set_preference(uint32_t number, intptr_t value) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    session.requireRunning();
    if (value < (std::numeric_limits<int32_t>::min)() ||
        value > (std::numeric_limits<int32_t>::max)() || number != 42 ||
        (value != 16 && value != 64))
        fail(FailureReason::InvalidArgument, "unsupported preference value");
    MilesWire::Call fields = {};
    fields.value[0] = number;
    fields.value[1] = static_cast<uint32_t>(value);
    return preferenceResult(session.request(MilesWire::AIL_set_preference, fields));
}

OwnedText last_errorOwned() {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    session.requireRunning();
    return ownedText(session.request(MilesWire::AIL_last_error, MilesWire::Call()));
}

OwnedText set_redist_directoryOwned(const char *directory) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    session.requireAvailable();
    if (!directory)
        fail(FailureReason::InvalidArgument, "null redistribution directory");
    const size_t size = std::strlen(directory) + 1;
    if (size > MilesStartup::RequestTextLimit)
        fail(FailureReason::InputLimit, "redistribution directory exceeds limit");
    return ownedText(session.request(MilesWire::AIL_set_redist_directory, MilesWire::Call(),
                                     MilesTransport::Bytes(directory, size)));
}

OwnedText MSS_versionOwned() {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    session.requireAvailable();
    return ownedText(session.request(MilesWire::SessionVersion, MilesWire::Call()));
}

HDIGDRIVER open_digital_driver(uint32_t frequency, int32_t bits, int32_t channels, uint32_t flags) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    session.requireRunning();
    if (session.driver || frequency != 22050 || bits != 16 || channels != 2 || flags)
        fail(FailureReason::InvalidArgument, "unsupported digital driver request");
    MilesWire::Call fields = {};
    fields.value[0] = frequency;
    fields.value[1] = static_cast<uint32_t>(bits);
    fields.value[2] = static_cast<uint32_t>(channels);
    fields.value[3] = flags;
    // Obtain caller-visible storage before the side-effecting vendor request.
    std::unique_ptr<DigitalDriver> driver(new DigitalDriver);
    StartupBridge::OwnedReply reply = session.request(MilesWire::AIL_open_digital_driver, fields);
    if (StartupBridge::nullHandle(reply.result.resource))
        return 0;
    driver->wire = reply.result.resource;
    driver->owner = &session;
    session.driver = std::move(driver);
    return session.driver.get();
}

int32_t speaker_configuration_spec(HDIGDRIVER driver) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    session.requireRunning();
    // Compare identity before dereferencing an opaque caller-provided pointer.
    if (!driver || driver != session.driver.get() || driver->owner != &session)
        fail(FailureReason::InvalidDriver, "driver does not belong to selected Miles session");
    MilesWire::Call fields = {};
    fields.target = driver->wire;
    fields.output_mask = 8;
    StartupBridge::OwnedReply reply = session.request(MilesWire::AIL_speaker_configuration, fields);
    return static_cast<int32_t>(MilesStartup::signedValue(reply.result.value[3]));
}
// File callback registration is deliberately absent: no pipe implementation.
void set_listener_3D_position(HDIGDRIVER driver, float x, float y, float z) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = driverCall(session, driver);
    fields.value[0] = floatBits(x); fields.value[1] = floatBits(y); fields.value[2] = floatBits(z);
    session.request(MilesWire::AIL_set_listener_3D_position, fields);
}
void set_listener_3D_velocity_vector(HDIGDRIVER driver, float x, float y, float z) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = driverCall(session, driver);
    fields.value[0] = floatBits(x); fields.value[1] = floatBits(y); fields.value[2] = floatBits(z);
    session.request(MilesWire::AIL_set_listener_3D_velocity_vector, fields);
}
void set_listener_3D_orientation(HDIGDRIVER driver, float x, float y, float z,
                                 float upX, float upY, float upZ) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = driverCall(session, driver);
    fields.value[0] = floatBits(x); fields.value[1] = floatBits(y); fields.value[2] = floatBits(z);
    fields.value[3] = floatBits(upX); fields.value[4] = floatBits(upY); fields.value[5] = floatBits(upZ);
    session.request(MilesWire::AIL_set_listener_3D_orientation, fields);
}
void set_3D_rolloff_factor(HDIGDRIVER driver, float factor) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = driverCall(session, driver);
    fields.value[0] = floatBits(factor);
    session.request(MilesWire::AIL_set_3D_rolloff_factor, fields);
}
void serve() {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    session.requireRunning();
    session.request(MilesWire::AIL_serve, MilesWire::Call());
}
int32_t room_type(HDIGDRIVER driver) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    return static_cast<int32_t>(MilesStartup::signedValue(
        session.request(MilesWire::AIL_room_type, driverCall(session, driver)).result.return_bits));
}
void set_room_type(HDIGDRIVER driver, int32_t room) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = driverCall(session, driver);
    fields.value[0] = static_cast<uint32_t>(room);
    session.request(MilesWire::AIL_set_room_type, fields);
}
} // namespace ClientMiles
