#include "../../backend-boundary24/pipe/Session.h"
#include "../../native-startup25/ClientMilesStartup.h"
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
        MilesWire::Header sent = {};
        sent.magic = MilesWire::Magic; sent.version = MilesWire::Version;
        sent.kind = MilesWire::Request; sent.opcode = opcode; sent.request = next; sent.lane = 1;
        std::vector<unsigned char> requestFrame;
        require(MilesTransport::encodeCall(sent, fields, MilesTransport::Bytes(), input, requestFrame),
                "encode actual request");
        MilesWire::Header decodedHeader = {};
        MilesWire::Call decodedCall = {};
        require(MilesTransport::decodeCall(MilesTransport::Bytes(&requestFrame[0], requestFrame.size()),
                                           decodedHeader, decodedCall), "decode request");
        require(decodedHeader.opcode == step.opcode &&
                !std::memcmp(&decodedCall, &step.call, sizeof decodedCall), "framed request mapping");
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

const uint32_t ops[] = {
    MilesWire::AIL_set_listener_3D_position, MilesWire::AIL_set_listener_3D_velocity_vector,
    MilesWire::AIL_set_listener_3D_orientation, MilesWire::AIL_set_3D_rolloff_factor,
    MilesWire::AIL_serve, MilesWire::AIL_room_type, MilesWire::AIL_set_room_type
};
float fromBits(uint32_t bits) { float out; std::memcpy(&out, &bits, 4); return out; }
MilesWire::Handle wireDriver() { MilesWire::Handle out = {MilesWire::Driver, 7, 3}; return out; }
void prepare(ScriptedChannel &c) {
    c.add(MilesWire::AIL_startup).scalar(1);
    Step &s = c.add(MilesWire::AIL_open_digital_driver);
    s.call.value[0] = 22050; s.call.value[1] = 16; s.call.value[2] = 2;
    s.result.resource = wireDriver();
}
ClientMiles::HDIGDRIVER begin() {
    require(ClientMiles::startup() == 1, "startup value");
    return ClientMiles::open_digital_driver(22050, 16, 2, 0);
}
void invoke(unsigned i, ClientMiles::HDIGDRIVER d) {
    switch (i) {
    case 0: ClientMiles::set_listener_3D_position(d, 0, 0, 0); break;
    case 1: ClientMiles::set_listener_3D_velocity_vector(d, 0, 0, 0); break;
    case 2: ClientMiles::set_listener_3D_orientation(d, 0, 0, 0, 0, 0, 0); break;
    case 3: ClientMiles::set_3D_rolloff_factor(d, 0); break;
    case 4: ClientMiles::serve(); break;
    case 5: (void)ClientMiles::room_type(d); break;
    case 6: ClientMiles::set_room_type(d, 0); break;
    }
}
Step &operation(ScriptedChannel &c, unsigned i) {
    Step &s = c.add(ops[i]);
    if (i != 4) s.call.target = wireDriver();
    return s;
}
void validMappings() {
    std::unique_ptr<ScriptedChannel> owned(new ScriptedChannel); ScriptedChannel &c = *owned;
    prepare(c);
    const uint32_t bits[] = {0x80000000u, 0xbf800000u, 0, 0x7f800000u, 0x7fc12345u, 1};
    for (unsigned i = 0; i < 4; ++i) {
        Step &s = operation(c, i);
        const unsigned count = i == 2 ? 6 : i == 3 ? 1 : 3;
        for (unsigned j = 0; j < count; ++j) s.call.value[j] = bits[j];
    }
    operation(c, 4);
    operation(c, 5).scalar(0xffffffffu);
    operation(c, 5).scalar(0x80000000u);
    operation(c, 5).scalar(0);
    operation(c, 6).call.value[0] = 0xffffffffu;
    operation(c, 6).call.value[0] = 0x80000000u;
    operation(c, 6);
    c.add(MilesWire::AIL_shutdown); c.add(MilesWire::SessionClose);
    ClientMilesPipe::Session session(std::move(owned));
    ClientMiles::HDIGDRIVER d = begin();
    ClientMiles::set_listener_3D_position(d, fromBits(bits[0]), fromBits(bits[1]), fromBits(bits[2]));
    ClientMiles::set_listener_3D_velocity_vector(d, fromBits(bits[0]), fromBits(bits[1]), fromBits(bits[2]));
    ClientMiles::set_listener_3D_orientation(d, fromBits(bits[0]), fromBits(bits[1]), fromBits(bits[2]),
                                           fromBits(bits[3]), fromBits(bits[4]), fromBits(bits[5]));
    ClientMiles::set_3D_rolloff_factor(d, fromBits(bits[0]));
    ClientMiles::serve();
    require(ClientMiles::room_type(d) == -1, "negative room is a vendor value");
    require(ClientMiles::room_type(d) == (std::numeric_limits<int32_t>::min)(), "minimum room");
    require(ClientMiles::room_type(d) == 0, "zero room is a vendor value");
    ClientMiles::set_room_type(d, -1);
    ClientMiles::set_room_type(d, (std::numeric_limits<int32_t>::min)());
    ClientMiles::set_room_type(d, 0);
    const size_t before = c.next;
    for (unsigned i = 0; i != 7; ++i) if (i != 4) {
        fails([&] { invoke(i, 0); }, ClientMiles::FailureReason::InvalidDriver, "null identity");
        fails([&] { invoke(i, reinterpret_cast<ClientMiles::HDIGDRIVER>(uintptr_t(1))); },
              ClientMiles::FailureReason::InvalidDriver, "foreign identity before dereference");
    }
    require(c.next == before, "bad drivers never reach channel");
    ClientMiles::shutdown();
    const size_t stopped = c.next;
    for (unsigned i = 0; i != 7; ++i)
        fails([&] { invoke(i, d); }, ClientMiles::FailureReason::WrongState, "postshutdown rejected");
    require(c.next == stopped, "postshutdown no requests");
    session.close(); require(c.finished, "ordered normal close");
}
void refusals() {
    for (unsigned i = 0; i != 7; ++i) {
        std::unique_ptr<ScriptedChannel> owned(new ScriptedChannel); ScriptedChannel &c = *owned;
        prepare(c); operation(c, i).result.transport_status = StartupBridge::InvalidFields;
        operation(c, i); c.add(MilesWire::AIL_shutdown); c.add(MilesWire::SessionClose);
        ClientMilesPipe::Session session(std::move(owned));
        fails([&] { invoke(i, 0); }, ClientMiles::FailureReason::WrongState, "prestartup refusal");
        require(c.next == 0, "prestartup no channel");
        ClientMiles::HDIGDRIVER d = begin();
        fails([&] { invoke(i, d); }, ClientMiles::FailureReason::InvalidArgument, "validated refusal distinct");
        invoke(i, d); ClientMiles::shutdown(); session.close();
    }
}
void uncertainty() {
    for (unsigned i = 0; i != 7; ++i) for (unsigned mode = 0; mode != 3; ++mode) {
        std::unique_ptr<ScriptedChannel> owned(new ScriptedChannel); ScriptedChannel &c = *owned;
        prepare(c); Step &s = operation(c, i); s.throwTransport = mode == 0; s.corrupt = mode == 1;
        if (mode == 2) { if (i == 5) s.result.value[0] = 1; else s.result.return_bits = 1; }
        ClientMilesPipe::Session session(std::move(owned)); ClientMiles::HDIGDRIVER d = begin();
        fails([&] { invoke(i, d); }, ClientMiles::FailureReason::BackendFailed, "uncertain result terminal");
        const size_t count = c.next;
        for (unsigned j = 0; j != 7; ++j)
            fails([&] { invoke(j, d); }, ClientMiles::FailureReason::BackendFailed, "no replay/new op after fault");
        fails([] { ClientMiles::shutdown(); }, ClientMiles::FailureReason::BackendFailed, "no shutdown replay");
        fails([&] { session.close(); }, ClientMiles::FailureReason::BackendFailed, "no close replay");
        require(c.next == count, "terminal fault blocks channel");
    }
}
} // namespace
int main() {
    try { validMappings(); refusals(); uncertainty();
          std::cout << "PASS " << checks << " scripted-framed checks; no vendor execution\n";
    } catch (std::exception const &e) { std::cerr << e.what() << "\n"; return 1; }
}
