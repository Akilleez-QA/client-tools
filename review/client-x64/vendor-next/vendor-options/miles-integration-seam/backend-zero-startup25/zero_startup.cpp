#include "../backend-boundary24/pipe/Session.h"
#include <iostream>

namespace {
struct Trace {
    unsigned requests, finishes;
    bool destroyed;
    Trace() : requests(0), finishes(0), destroyed(false) {
    }
};

void require(bool value, const char *message) {
    if (!value)
        throw std::runtime_error(message);
}

class TestOnlyZeroChannel : public ClientMilesPipe::Channel {
  public:
    explicit TestOnlyZeroChannel(Trace &trace) : trace_(trace) {
    }
    ~TestOnlyZeroChannel() {
        trace_.destroyed = true;
    }

    StartupBridge::OwnedReply call(uint32_t opcode, const MilesWire::Call &,
                                   MilesTransport::Bytes text) override {
        ++trace_.requests;
        require(trace_.requests == 1 && opcode == MilesWire::AIL_startup && !text.size,
                "only the scripted startup request may reach this channel");
        MilesWire::Header expected = {};
        expected.magic = MilesWire::Magic;
        expected.version = MilesWire::Version;
        expected.kind = MilesWire::Request;
        expected.opcode = opcode;
        expected.request = 1;
        expected.lane = 1;
        MilesWire::Header header = expected;
        header.kind = MilesWire::Reply;
        MilesWire::Result result = {}; // Test-only known zero, no SDK call.
        std::vector<unsigned char> frame;
        require(MilesTransport::encodeResult(header, result, MilesTransport::Bytes(),
                                             MilesTransport::Bytes(), frame),
                "encode zero reply");
        StartupBridge::OwnedReply reply;
        require(StartupBridge::decodeReply(MilesTransport::Bytes(&frame[0], frame.size()), expected,
                                           reply),
                "decode known zero reply");
        return reply;
    }

    void finish() override {
        ++trace_.finishes;
    }

  private:
    Trace &trace_;
    TestOnlyZeroChannel(const TestOnlyZeroChannel &);
    TestOnlyZeroChannel &operator=(const TestOnlyZeroChannel &);
};

template <class Function> bool wrongState(Function function) {
    try {
        function();
    } catch (const ClientMiles::Failure &failure) {
        return failure.reason() == ClientMiles::FailureReason::WrongState;
    }
    return false;
}
} // namespace

int main() {
    try {
        Trace trace;
        int32_t returned = -1;
        bool shutdownRefused = false, closeRefused = false;
        {
            std::unique_ptr<ClientMilesPipe::Channel> channel(new TestOnlyZeroChannel(trace));
            ClientMilesPipe::Session session(std::move(channel));
            returned = ClientMiles::startup();
            require(returned == 0 && !session.started && !session.stopped,
                    "known zero remains zero and leaves the current state unstarted");
            shutdownRefused = wrongState([] { ClientMiles::shutdown(); });
            closeRefused = wrongState([&session] { session.close(); });
            require(shutdownRefused && closeRefused,
                    "current zero-startup close gap must remain visible");
            require(trace.requests == 1 && trace.finishes == 0,
                    "refused cleanup sends no request and never finishes the channel");
        }
        require(trace.destroyed && trace.requests == 1 && trace.finishes == 0,
                "scope destruction only abandons this test channel");
        std::cout << "{\"startup_return\":0,\"shutdown_wrong_state\":true,"
                     "\"close_wrong_state\":true,\"channel_requests\":1,"
                     "\"finish_calls\":0,\"channel_destroyed\":true,"
                     "\"vendor_called\":false,\"graceful_close_demonstrated\":false}\n";
        return 0;
    } catch (const std::exception &error) {
        std::cerr << "FAIL " << error.what() << '\n';
        return 1;
    }
}
