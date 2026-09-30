#include "../backend-boundary24/pipe/LiveChannel.h"
#include "../backend-boundary24/pipe/Session.h"
#include "../native-sample27/ClientMilesSample.h"
#include "sequence.h"
#include <cstdio>
namespace {
void require30(bool value, const char *message) {
    if (!value) throw std::runtime_error(message);
}
class Controls30 : public ClientMilesPipe::Channel {
  public:
    explicit Controls30(std::unique_ptr<ClientMilesPipe::Channel> channel)
        : channel_(std::move(channel)), next_(2), sample_(), allocations_(0) {}
    StartupBridge::OwnedReply call(uint32_t opcode, const MilesWire::Call &fields,
                                   MilesTransport::Bytes text) override {
        const unsigned request = next_;
        StartupBridge::OwnedReply out = exchange(opcode, fields, text);
        if (opcode == MilesWire::AIL_allocate_sample_handle) {
            sample_ = out.result.resource;
            ++allocations_;
            require30(sample_.kind == MilesWire::OwnedSample && sample_.slot == 2 &&
                      sample_.generation == allocations_, "owned slot reuse/generation");
            printf("sample_identity allocation=%u kind=%u slot=%u generation=%u\n",
                   allocations_, sample_.kind, sample_.slot, sample_.generation);
        }
        if (request == 9 || request == 777) {
            MilesWire::Call invalid = {};
            invalid.target = sample_;
            exchange(MilesWire::AIL_end_sample, invalid, MilesTransport::Bytes());
            if (request == 777)
                exchange(MilesWire::AIL_serve, MilesWire::Call(), MilesTransport::Bytes());
        }
        return out;
    }
    void finish() override {
        require30(next_ == 781, "controller exact780 requests");
        channel_->finish();
    }
  private:
    std::unique_ptr<ClientMilesPipe::Channel> channel_;
    unsigned next_;
    MilesWire::Handle sample_;
    unsigned allocations_;
    StartupBridge::OwnedReply exchange(uint32_t opcode, const MilesWire::Call &fields,
                                       MilesTransport::Bytes text) {
        require30(next_ >= 2 && next_ <= 780, "controller request bound");
        const Expected30 &expected = expected30[next_ - 1];
        require30(opcode == expected.opcode, "controller precommitted opcode");
        ++next_;
        StartupBridge::OwnedReply out = channel_->call(opcode, fields, text);
        require30(out.result.transport_status == expected.status, "controller expected status");
        return out;
    }
    Controls30(const Controls30 &);
    Controls30 &operator=(const Controls30 &);
};
}
int main(int argc, char **argv) {
    try {
        require30(argc == 3, "host and original DLL paths required");
        std::unique_ptr<ClientMilesPipe::Channel> channel = ClientMilesPipe::connect(argv[1], argv[2]);
        std::unique_ptr<ClientMilesPipe::Channel> checked(new Controls30(std::move(channel)));
        ClientMilesPipe::Session session(std::move(checked));
        const ClientMiles::OwnedText version = ClientMiles::MSS_versionOwned();
        require30(!version.isNull && version.value == "7.2a", "actual bounded version");
        ClientMiles::set_redist_directoryOwned("miles");
        require30(ClientMiles::startup() != 0, "real startup");
        ClientMiles::HDIGDRIVER driver = ClientMiles::open_digital_driver(22050, 16, 2, 0);
        require30(driver != 0, "real driver");
        require30(ClientMiles::speaker_configuration_spec(driver) == 2, "stereo speaker");
        for (unsigned i = 0; i < 256; ++i) {
            ClientMiles::HSAMPLE sample = ClientMiles::allocate_sample_handle(driver);
            require30(sample != 0 && session.sampleProxyCount() == 1, "allocated owned proxy");
            ClientMiles::end_sample(sample);
            ClientMiles::release_sample_handle(sample);
            require30(session.sampleProxyCount() == 0, "released proxy reclaimed");
        }
        require30(ClientMiles::allocate_sample_handle(driver) != 0 &&
                  session.sampleProxyCount() == 1, "live sample before shutdown");
        ClientMiles::shutdown();
        require30(session.sampleProxyCount() == 0, "confirmed shutdown clears local samples");
        session.close();
        puts("PASS sample-live31 exact780;257 allocations256 releases; no query/binding/playback/callbacks");
        return 0;
    } catch (const std::exception &error) {
        printf("FAIL %s\n", error.what());
        return 1;
    }
}
