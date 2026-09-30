#include "../pipe/LiveChannel.h"
#include "../pipe/Session.h"
#include "../sample/startup_calls.h"
#include <cstdio>

namespace {
void require(bool value, const char *message) {
    if (!value)
        throw std::runtime_error(message);
}

// Fixture-only negative requests preserve the frozen host23 oracle's IDs.
// This decorator is never part of game-facing policy or the native backend.
class NegativeControls : public ClientMilesPipe::Channel {
  public:
    explicit NegativeControls(std::unique_ptr<ClientMilesPipe::Channel> channel)
        : channel_(std::move(channel)), next_(2) {
    } // Hello was private bootstrap.
    StartupBridge::OwnedReply call(uint32_t opcode, const MilesWire::Call &fields,
                                   MilesTransport::Bytes text) override {
        const unsigned request = next_++;
        StartupBridge::OwnedReply out = channel_->call(opcode, fields, text);
        if (out.result.transport_status != StartupBridge::Success)
            return out;
        if (request == 4) {
            const char malformed[] = {'m', 'i', 'l', 'e', 's', 0, 'x', 0};
            reject(MilesWire::AIL_set_redist_directory, MilesWire::Call(),
                   MilesTransport::Bytes(malformed, sizeof malformed),
                   StartupBridge::InvalidFields);
        } else if (request == 14) {
            MilesWire::Call invalid = {};
            invalid.value[0] = 42;
            invalid.value[1] = 0xffffffffu;
            reject(MilesWire::AIL_set_preference, invalid, MilesTransport::Bytes(),
                   StartupBridge::InvalidFields);
        } else if (request == 17) {
            MilesWire::Call invalid = {};
            invalid.target = out.result.resource;
            invalid.output_mask = 24;
            reject(MilesWire::AIL_speaker_configuration, invalid, MilesTransport::Bytes(),
                   StartupBridge::InvalidFields);
            invalid.output_mask = 8;
            ++invalid.target.slot;
            reject(MilesWire::AIL_speaker_configuration, invalid, MilesTransport::Bytes(),
                   StartupBridge::InvalidResource);
        } else if (request == 21) {
            MilesWire::Call invalid = {};
            invalid.value[0] = 42;
            reject(MilesWire::AIL_get_preference, invalid, MilesTransport::Bytes(),
                   StartupBridge::LifecycleRefused);
        }
        return out;
    }
    void finish() override {
        require(next_ == 24, "fixture must retain all23 requests");
        channel_->finish();
    }

  private:
    std::unique_ptr<ClientMilesPipe::Channel> channel_;
    unsigned next_;
    void reject(uint32_t opcode, const MilesWire::Call &fields, MilesTransport::Bytes text,
                uint32_t expected) {
        ++next_;
        require(channel_->call(opcode, fields, text).result.transport_status == expected,
                "raw negative fixture status");
    }
    NegativeControls(const NegativeControls &);
    NegativeControls &operator=(const NegativeControls &);
};
} // namespace

int main(int argc, char **argv) {
    try {
        require(argc == 3, "host and original DLL paths required");
        std::unique_ptr<ClientMilesPipe::Channel> channel =
            ClientMilesPipe::connect(argv[1], argv[2]);
        std::unique_ptr<ClientMilesPipe::Channel> checked(new NegativeControls(std::move(channel)));
        ClientMilesPipe::Session session(std::move(checked));
        const StartupObservations out = startupCalls();
        require(out.startupResult != 0 && out.driverOpened && out.speakerSpec == 2,
                "real startup/driver prerequisites");
        require(!out.version.isNull && out.version.value == "7.2a", "actual bounded version");
        require(!out.dot.isNull && out.dot.value.empty() && out.directory.value == "miles/",
                "owned directory results");
        require(out.firstError.value == "startup bridge23 first" &&
                    out.secondError.value == "startup bridge23 changed",
                "owned controlled errors survive later replies");
        require(out.previous16 == out.initialFragments && out.read16 == 16 &&
                    out.previous64 == 16 && out.read64 == 64 && out.finalFragments == 64,
                "separate signed preference readbacks");
        session.close();
        puts("PASS source-facade23 framed requests; no samples/playback");
        return 0;
    } catch (const std::exception &error) {
        printf("FAIL %s\n", error.what());
        return 1;
    }
}
