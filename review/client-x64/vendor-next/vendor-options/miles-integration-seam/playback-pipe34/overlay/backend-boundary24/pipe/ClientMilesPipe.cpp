#include "Session.h"
#include "../../native-playback28/ClientMilesPlayback.h"
#include <list>
#include "../../native-startup25/ClientMilesStartup.h"
#include <cstring>
#include <limits>

namespace ClientMiles {
struct DigitalDriver {
    MilesWire::Handle wire;
    const ClientMilesPipe::Session *owner;
};
struct Sample {
    MilesWire::Handle wire;
    bool live;
    Sample() : wire(), live(false) {}
};
} // namespace ClientMiles

namespace ClientMilesPipe {
struct SampleState {
    typedef std::list<std::unique_ptr<ClientMiles::Sample> > Proxies;
    Proxies proxies;
};
}

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
    : started(false), stopped(false), samples(new SampleState), channel_(std::move(channel)), closed_(false),
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

size_t Session::sampleProxyCount() const { return samples->proxies.size(); }

void Session::rejectResult() {
    faulted_ = true;
    fail(ClientMiles::FailureReason::BackendFailed, "invalid sample reply; outcome uncertain");
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
    session.samples->proxies.clear(); // confirmed vendor shutdown, local handles expire
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
// Private helper compares identity without dereferencing caller-provided pointers.
static Sample &ownedSample(ClientMilesPipe::Session &session, HSAMPLE sample) {
    session.requireRunning();
    for (ClientMilesPipe::SampleState::Proxies::iterator i=session.samples->proxies.begin();
         i!=session.samples->proxies.end(); ++i) {
        Sample *candidate = i->get();
        if (sample == candidate && candidate->live && candidate->wire.kind == MilesWire::OwnedSample) return *candidate;
    }
    fail(FailureReason::InvalidArgument, "sample is not live in this selected Session");
    throw std::logic_error("unreachable");
}

HSAMPLE allocate_sample_handle(HDIGDRIVER driver) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = driverCall(session, driver);
    // Both proxy allocation and container publication precede remote side effects.
    std::unique_ptr<Sample> local(new Sample);
    Sample *sample = local.get();
    session.samples->proxies.push_back(std::move(local));
    StartupBridge::OwnedReply reply;
    try {
        reply = session.request(MilesWire::AIL_allocate_sample_handle, fields);
    } catch (...) {
        // Only an observed refusal permits discarding the unpublished proxy.
        if (!session.uncertain()) session.samples->proxies.pop_back();
        throw;
    }
    if (StartupBridge::nullHandle(reply.result.resource)) {
        session.samples->proxies.pop_back(); // never exposed, so cannot alias a stale handle
        return 0;
    }
    sample->wire = reply.result.resource;
    sample->live = true;
    return sample;
}

void sample_ms_position(HSAMPLE sample, int32_t *total, int32_t *current) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = {};
    fields.target = ownedSample(session, sample).wire;
    fields.output_mask = (total ? 1u : 0u) | (current ? 2u : 0u);
    StartupBridge::OwnedReply reply = session.request(MilesWire::AIL_sample_ms_position, fields);
    // Decoder knows the opcode; only this layer knows which outputs were requested.
    if ((!total && reply.result.value[0]) || (!current && reply.result.value[1]))
        session.rejectResult();
    const int32_t a = static_cast<int32_t>(MilesStartup::signedValue(reply.result.value[0]));
    const int32_t b = static_cast<int32_t>(MilesStartup::signedValue(reply.result.value[1]));
    if (total) *total = a;
    if (current) *current = b;
}

void end_sample(HSAMPLE sample) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = {};
    fields.target = ownedSample(session, sample).wire;
    session.request(MilesWire::AIL_end_sample, fields);
}

void release_sample_handle(HSAMPLE sample) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    Sample &owned = ownedSample(session, sample);
    MilesWire::Call fields = {};
    fields.target = owned.wire;
    session.request(MilesWire::AIL_release_sample_handle, fields);
    // Native HSAMPLE lifetime ends here. Caller reuse of that raw pointer is invalid.
    // Wire generations are a separate host/callback obligation, not pointer tokens.
    for (ClientMilesPipe::SampleState::Proxies::iterator i=session.samples->proxies.begin();
         i!=session.samples->proxies.end(); ++i) {
        if (i->get()==&owned) { session.samples->proxies.erase(i); break; }
    }
}

// Owned-only playback slice. The host independently enforces OwnedSample kind.
static MilesWire::Call sampleCall(ClientMilesPipe::Session &session, HSAMPLE sample) {
    MilesWire::Call fields = {};
    fields.target = ownedSample(session, sample).wire;
    return fields;
}
static void sampleFloatPair(uint32_t opcode, HSAMPLE sample, float *first, float *second) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = sampleCall(session, sample);
    fields.output_mask = (first ? 1u : 0u) | (second ? 2u : 0u);
    const StartupBridge::OwnedReply reply = session.request(opcode, fields);
    if ((!first && reply.result.value[0]) || (!second && reply.result.value[1]))
        session.rejectResult();
    float a, b;
    std::memcpy(&a, &reply.result.value[0], sizeof a);
    std::memcpy(&b, &reply.result.value[1], sizeof b);
    if (first) *first = a;
    if (second) *second = b;
}
void start_sample(HSAMPLE sample) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = sampleCall(session, sample);
    session.request(MilesWire::AIL_start_sample, fields);
}
void stop_sample(HSAMPLE sample) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = sampleCall(session, sample);
    session.request(MilesWire::AIL_stop_sample, fields);
}
uint32_t sample_status(HSAMPLE sample) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = sampleCall(session, sample);
    return session.request(MilesWire::AIL_sample_status, fields).result.return_bits;
}
void set_sample_loop_count(HSAMPLE sample, int32_t count) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = sampleCall(session, sample);
    fields.value[0] = static_cast<uint32_t>(count);
    session.request(MilesWire::AIL_set_sample_loop_count, fields);
}
void set_sample_loop_block(HSAMPLE sample, int32_t startByte, int32_t endByte) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = sampleCall(session, sample);
    fields.value[0] = static_cast<uint32_t>(startByte);
    fields.value[1] = static_cast<uint32_t>(endByte);
    session.request(MilesWire::AIL_set_sample_loop_block, fields);
}
void set_sample_ms_position(HSAMPLE sample, int32_t milliseconds) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = sampleCall(session, sample);
    fields.value[0] = static_cast<uint32_t>(milliseconds);
    session.request(MilesWire::AIL_set_sample_ms_position, fields);
}
void set_sample_position(HSAMPLE sample, uint32_t byteOffset) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = sampleCall(session, sample);
    fields.value[0] = static_cast<uint32_t>(byteOffset);
    session.request(MilesWire::AIL_set_sample_position, fields);
}
uint32_t sample_position(HSAMPLE sample) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = sampleCall(session, sample);
    return session.request(MilesWire::AIL_sample_position, fields).result.return_bits;
}
void set_sample_playback_rate(HSAMPLE sample, int32_t rate) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = sampleCall(session, sample);
    fields.value[0] = static_cast<uint32_t>(rate);
    session.request(MilesWire::AIL_set_sample_playback_rate, fields);
}
int32_t sample_playback_rate(HSAMPLE sample) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = sampleCall(session, sample);
    return static_cast<int32_t>(MilesStartup::signedValue(session.request(MilesWire::AIL_sample_playback_rate, fields).result.return_bits));
}
void set_sample_volume_levels(HSAMPLE sample, float left, float right) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = sampleCall(session, sample);
    fields.value[0] = floatBits(left);
    fields.value[1] = floatBits(right);
    session.request(MilesWire::AIL_set_sample_volume_levels, fields);
}
void sample_volume_levels(HSAMPLE sample, float * left, float * right) {
    sampleFloatPair(MilesWire::AIL_sample_volume_levels, sample, left, right);
}
void set_sample_reverb_levels(HSAMPLE sample, float dry, float wet) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = sampleCall(session, sample);
    fields.value[0] = floatBits(dry);
    fields.value[1] = floatBits(wet);
    session.request(MilesWire::AIL_set_sample_reverb_levels, fields);
}
void sample_reverb_levels(HSAMPLE sample, float * dry, float * wet) {
    sampleFloatPair(MilesWire::AIL_sample_reverb_levels, sample, dry, wet);
}
void set_sample_3D_position(HSAMPLE sample, float x, float y, float z) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = sampleCall(session, sample);
    fields.value[0] = floatBits(x);
    fields.value[1] = floatBits(y);
    fields.value[2] = floatBits(z);
    session.request(MilesWire::AIL_set_sample_3D_position, fields);
}
void set_sample_3D_velocity_vector(HSAMPLE sample, float xPerMs, float yPerMs, float zPerMs) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = sampleCall(session, sample);
    fields.value[0] = floatBits(xPerMs);
    fields.value[1] = floatBits(yPerMs);
    fields.value[2] = floatBits(zPerMs);
    session.request(MilesWire::AIL_set_sample_3D_velocity_vector, fields);
}
void set_sample_3D_distances(HSAMPLE sample, float maximum, float minimum, int32_t autoWetAttenuation) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = sampleCall(session, sample);
    fields.value[0] = floatBits(maximum);
    fields.value[1] = floatBits(minimum);
    fields.value[2] = static_cast<uint32_t>(autoWetAttenuation);
    session.request(MilesWire::AIL_set_sample_3D_distances, fields);
}
void set_sample_occlusion(HSAMPLE sample, float value) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = sampleCall(session, sample);
    fields.value[0] = floatBits(value);
    session.request(MilesWire::AIL_set_sample_occlusion, fields);
}
void set_sample_obstruction(HSAMPLE sample, float value) {
    ClientMilesPipe::Session &session = ClientMilesPipe::Session::selected();
    MilesWire::Call fields = sampleCall(session, sample);
    fields.value[0] = floatBits(value);
    session.request(MilesWire::AIL_set_sample_obstruction, fields);
}

// set_named_sample_file is deliberately not defined: native rebind and failed-bind
// input-lifetime rules plus actual sealed-upload/host ownership must be resolved.
} // namespace ClientMiles
