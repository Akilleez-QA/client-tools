#include "../pipe/Session.h"
#include "../sample/startup_calls.h"
#include <cstring>
#include <iostream>
#include <limits>
#include <utility>
#include <vector>

namespace {
unsigned checks = 0;
void require(bool value, const char *message) {
    ++checks;
    if (!value)
        throw std::runtime_error(message);
}

template <class Function>
void fails(Function function, ClientMiles::FailureReason expected, const char *message) {
    try {
        function();
    } catch (const ClientMiles::Failure &failure) {
        require(failure.reason() == expected, message);
        return;
    }
    require(false, message);
}

struct Step {
    uint32_t opcode;
    MilesWire::Call call;
    std::string input;
    MilesWire::Result result;
    std::vector<unsigned char> text;
    bool corrupt, throwTransport, bypassDecoder;
    explicit Step(uint32_t op)
        : opcode(op), call(), result(), corrupt(false), throwTransport(false),
          bypassDecoder(false) {
    }
    Step &scalar(uint32_t value) {
        result.return_bits = value;
        return *this;
    }
    Step &string(const char *value) {
        text.assign(value, value + std::strlen(value) + 1);
        return *this;
    }
};

class ScriptedChannel : public ClientMilesPipe::Channel {
  public:
    std::vector<Step> steps;
    size_t next;
    bool finished, failFinish;
    ScriptedChannel() : next(0), finished(false), failFinish(false) {
    }
    Step &add(uint32_t opcode) {
        steps.push_back(Step(opcode));
        return steps.back();
    }
    StartupBridge::OwnedReply call(uint32_t opcode, const MilesWire::Call &fields,
                                   MilesTransport::Bytes input) override {
        require(next < steps.size(), "unexpected adapter call");
        const Step &step = steps[next++];
        require(opcode == step.opcode, "exact operation order");
        require(!std::memcmp(&fields, &step.call, sizeof fields), "exact typed argument mapping");
        const std::string actual =
            input.size ? std::string(reinterpret_cast<const char *>(input.data), input.size)
                       : std::string();
        require(actual == step.input, "exact input extent");
        if (step.throwTransport)
            throw std::runtime_error("test-only transport failure");
        StartupBridge::OwnedReply out;
        if (step.bypassDecoder) {
            out.result = step.result;
            return out;
        }
        MilesWire::Header expected = {};
        expected.magic = MilesWire::Magic;
        expected.version = MilesWire::Version;
        expected.kind = MilesWire::Request;
        expected.opcode = opcode;
        expected.request = next;
        expected.lane = 1;
        MilesWire::Header reply = expected;
        reply.kind = MilesWire::Reply;
        std::vector<unsigned char> encoded;
        require(MilesTransport::encodeResult(
                    reply, step.result, MilesTransport::Bytes(),
                    MilesTransport::Bytes(step.text.empty() ? 0 : &step.text[0], step.text.size()),
                    encoded),
                "test reply codec encode");
        if (step.corrupt)
            encoded[16] ^= 1; // Wrong request identity, not vendor data.
        if (!StartupBridge::decodeReply(MilesTransport::Bytes(&encoded[0], encoded.size()),
                                        expected, out))
            throw std::runtime_error("test-only decoded reply refusal");
        std::fill(encoded.begin(), encoded.end(), 0xcd);
        return out;
    }
    void finish() override {
        if (failFinish)
            throw std::runtime_error("test-only finish failure");
        require(next == steps.size(), "all scripted operations consumed");
        finished = true;
    }
};

void preference(ScriptedChannel &channel, uint32_t opcode, uint32_t value, uint32_t result) {
    Step &step = channel.add(opcode).scalar(result);
    step.call.value[0] = 42;
    if (opcode == MilesWire::AIL_set_preference)
        step.call.value[1] = value;
}

void validSample() {
    std::unique_ptr<ScriptedChannel> owned(new ScriptedChannel);
    ScriptedChannel &channel = *owned;
    channel.add(MilesWire::SessionVersion).string("TEST-ONLY version");
    Step &dot = channel.add(MilesWire::AIL_set_redist_directory).string("");
    dot.input.assign(".", 2);
    Step &directory = channel.add(MilesWire::AIL_set_redist_directory).string("test directory");
    directory.input.assign("miles", 6);
    channel.add(MilesWire::AIL_startup).scalar(1);
    Step &mixer = channel.add(MilesWire::AIL_get_preference).scalar(64);
    mixer.call.value[0] = 1;
    preference(channel, MilesWire::AIL_get_preference, 0, 0xffffffffu);
    channel.add(MilesWire::AIL_last_error).result.null_mask = MilesStartup::TextNull;
    channel.add(MilesWire::AIL_last_error).string("");
    preference(channel, MilesWire::AIL_set_preference, 16, 0x80000000u);
    preference(channel, MilesWire::AIL_get_preference, 0, 16);
    preference(channel, MilesWire::AIL_set_preference, 64, 16);
    preference(channel, MilesWire::AIL_get_preference, 0, 64);
    preference(channel, MilesWire::AIL_get_preference, 0, 64);
    Step &open = channel.add(MilesWire::AIL_open_digital_driver);
    open.call.value[0] = 22050;
    open.call.value[1] = 16;
    open.call.value[2] = 2;
    MilesWire::Handle driver = {MilesWire::Driver, 7, 3};
    open.result.resource = driver;
    Step &speaker = channel.add(MilesWire::AIL_speaker_configuration);
    speaker.call.target = driver;
    speaker.call.output_mask = 8;
    speaker.result.value[3] = 2;
    channel.add(MilesWire::AIL_shutdown);
    channel.add(MilesWire::SessionClose);
    ClientMilesPipe::Session session(std::move(owned));
    const StartupObservations out = startupCalls();
    require(out.startupResult == 1 && out.driverOpened && out.speakerSpec == 2,
            "typed lifecycle results");
    require(out.initialFragments == -1 && out.previous16 == (std::numeric_limits<int32_t>::min)(),
            "signed32 results extend to intptr_t");
    require(out.read16 == 16 && out.previous64 == 16 && out.read64 == 64 &&
                out.finalFragments == 64,
            "separate preference effects/readbacks");
    require(!out.version.isNull && out.version.value == "TEST-ONLY version" &&
                out.directory.value == "test directory",
            "owned text survives all subsequent replies");
    require(!out.dot.isNull && out.dot.value.empty() && out.firstError.isNull &&
                !out.secondError.isNull && out.secondError.value.empty(),
            "null versus nonnull empty preserved");
    session.close();
    require(channel.finished, "explicit protocol teardown remains private");
}

void refusalsAndRealValueShapes() {
    std::unique_ptr<ScriptedChannel> owned(new ScriptedChannel);
    ScriptedChannel &channel = *owned;
    channel.add(MilesWire::AIL_startup).scalar(1);
    preference(channel, MilesWire::AIL_get_preference, 0, 0);
    Step &knownError = channel.add(MilesWire::AIL_get_preference);
    knownError.call.value[0] = 42;
    knownError.result.transport_status = StartupBridge::InvalidFields;
    preference(channel, MilesWire::AIL_get_preference, 0, 0);
    Step &open = channel.add(MilesWire::AIL_open_digital_driver);
    open.call.value[0] = 22050;
    open.call.value[1] = 16;
    open.call.value[2] = 2;
    channel.add(MilesWire::AIL_shutdown);
    channel.add(MilesWire::SessionClose);
    ClientMilesPipe::Session session(std::move(owned));
    fails([] { ClientMiles::get_preference(42); }, ClientMiles::FailureReason::WrongState,
          "prestartup refusal");
    require(ClientMiles::startup() == 1, "startup result separate from failure");
    const size_t before = channel.next;
    fails([] { ClientMiles::startup(); }, ClientMiles::FailureReason::WrongState,
          "duplicate startup refused");
    fails([] { ClientMiles::set_preference(42, (std::numeric_limits<intptr_t>::max)()); },
          ClientMiles::FailureReason::InvalidArgument, "wide preference rejected before narrowing");
    fails([] { ClientMiles::set_preference(42, -1); }, ClientMiles::FailureReason::InvalidArgument,
          "unsupported negative rejected before channel");
    fails([] { ClientMiles::get_preference(99); }, ClientMiles::FailureReason::InvalidArgument,
          "unsupported ID rejected");
    fails([] { ClientMiles::set_redist_directoryOwned(0); },
          ClientMiles::FailureReason::InvalidArgument, "null input rejected");
    fails(
        [] {
            ClientMiles::speaker_configuration_spec(
                reinterpret_cast<ClientMiles::HDIGDRIVER>(uintptr_t(1)));
        },
        ClientMiles::FailureReason::InvalidDriver,
        "opaque foreign handle rejected without dereference");
    require(channel.next == before, "local refusals do not issue requests");
    require(ClientMiles::get_preference(42) == 0, "valid zero preference preserved");
    fails([] { ClientMiles::get_preference(42); }, ClientMiles::FailureReason::InvalidArgument,
          "known operation error distinguished");
    require(ClientMiles::get_preference(42) == 0, "known refusal remains recoverable");
    require(!ClientMiles::open_digital_driver(22050, 16, 2, 0), "valid vendor null preserved");
    ClientMiles::shutdown();
    session.close();
}

void terminalFailures() {
    for (unsigned mode = 0; mode != 3; ++mode) {
        std::unique_ptr<ScriptedChannel> owned(new ScriptedChannel);
        ScriptedChannel &channel = *owned;
        channel.add(MilesWire::AIL_startup).scalar(1);
        Step &failure = channel.add(MilesWire::AIL_get_preference);
        failure.call.value[0] = 42;
        failure.throwTransport = mode == 0;
        failure.corrupt = mode == 1;
        failure.bypassDecoder = mode == 2;
        if (mode == 2)
            failure.result.transport_status = 4;
        ClientMilesPipe::Session session(std::move(owned));
        ClientMiles::startup();
        fails([] { ClientMiles::get_preference(42); }, ClientMiles::FailureReason::BackendFailed,
              "terminal uncertain outcome");
        const size_t after = channel.next;
        fails([] { ClientMiles::get_preference(42); }, ClientMiles::FailureReason::BackendFailed,
              "no ordinary retry after fault");
        fails([] { ClientMiles::shutdown(); }, ClientMiles::FailureReason::BackendFailed,
              "no shutdown replay after fault");
        fails([&session] { session.close(); }, ClientMiles::FailureReason::BackendFailed,
              "no close retry after fault");
        require(channel.next == after, "fault latch blocks all further channel calls");
    }
    std::unique_ptr<ScriptedChannel> owned(new ScriptedChannel);
    ScriptedChannel &channel = *owned;
    channel.add(MilesWire::AIL_startup).scalar(1);
    channel.add(MilesWire::AIL_shutdown);
    channel.add(MilesWire::SessionClose);
    channel.failFinish = true;
    ClientMilesPipe::Session session(std::move(owned));
    ClientMiles::startup();
    ClientMiles::shutdown();
    fails([&session] { session.close(); }, ClientMiles::FailureReason::BackendFailed,
          "finish failure is terminal");
    const size_t after = channel.next;
    fails([&session] { session.close(); }, ClientMiles::FailureReason::BackendFailed,
          "finish failure cannot replay close");
    require(channel.next == after, "close was issued exactly once");
}
} // namespace

int main() {
    try {
        validSample();
        refusalsAndRealValueShapes();
        terminalFailures();
        std::cout << "PASS " << checks << " explicit portable checks; scripted test-only replies\n";
        return 0;
    } catch (const std::exception &error) {
        std::cerr << "FAIL " << error.what() << '\n';
        return 1;
    }
}
