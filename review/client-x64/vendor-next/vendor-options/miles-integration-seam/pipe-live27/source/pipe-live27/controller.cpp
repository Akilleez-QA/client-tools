#include "../backend-boundary24/pipe/LiveChannel.h"
#include "../backend-boundary24/pipe/Session.h"
#include "../native-startup25/ClientMilesStartup.h"
#include "sequence.h"
#include <cstdio>
namespace {
void require27(bool value, const char *message) {
    if (!value) throw std::runtime_error(message);
}
class Controls27 : public ClientMilesPipe::Channel {
  public:
    explicit Controls27(std::unique_ptr<ClientMilesPipe::Channel> channel)
        : channel_(std::move(channel)), next_(2), driver_() {}
    StartupBridge::OwnedReply call(uint32_t opcode, const MilesWire::Call &fields,
                                   MilesTransport::Bytes text) override {
        const unsigned request = next_;
        StartupBridge::OwnedReply out = exchange(opcode, fields, text);
        if (request == 5) driver_ = out.result.resource;
        if (request == 15) {
            MilesWire::Call invalid = {};
            invalid.target = driver_;
            invalid.value[3] = 1;
            exchange(MilesWire::AIL_set_listener_3D_position, invalid, MilesTransport::Bytes());
            invalid = MilesWire::Call();
            invalid.target = driver_;
            ++invalid.target.slot;
            exchange(MilesWire::AIL_room_type, invalid, MilesTransport::Bytes());
            invalid.target = driver_;
            exchange(MilesWire::AIL_serve, invalid, MilesTransport::Bytes());
        } else if (request == 20) {
            exchange(MilesWire::AIL_serve, MilesWire::Call(), MilesTransport::Bytes());
        }
        return out;
    }
    void finish() override {
        require27(next_ == 23, "controller exact22 requests");
        channel_->finish();
    }
  private:
    std::unique_ptr<ClientMilesPipe::Channel> channel_;
    unsigned next_;
    MilesWire::Handle driver_;
    StartupBridge::OwnedReply exchange(uint32_t opcode, const MilesWire::Call &fields,
                                       MilesTransport::Bytes text) {
        require27(next_ >= 2 && next_ <= 22, "controller request bound");
        const Expected27 &expected = expected27[next_ - 1];
        require27(opcode == expected.opcode, "controller precommitted opcode");
        ++next_;
        StartupBridge::OwnedReply out = channel_->call(opcode, fields, text);
        require27(out.result.transport_status == expected.status, "controller expected status");
        return out;
    }
    Controls27(const Controls27 &);
    Controls27 &operator=(const Controls27 &);
};
}
int main(int argc, char **argv) {
    try {
        require27(argc == 3, "host and original DLL paths required");
        std::unique_ptr<ClientMilesPipe::Channel> channel = ClientMilesPipe::connect(argv[1], argv[2]);
        std::unique_ptr<ClientMilesPipe::Channel> checked(new Controls27(std::move(channel)));
        ClientMilesPipe::Session session(std::move(checked));
        const ClientMiles::OwnedText version = ClientMiles::MSS_versionOwned();
        require27(!version.isNull && version.value == "7.2a", "actual bounded version");
        ClientMiles::set_redist_directoryOwned("miles");
        require27(ClientMiles::startup() != 0, "real startup");
        ClientMiles::HDIGDRIVER driver = ClientMiles::open_digital_driver(22050, 16, 2, 0);
        require27(driver != 0, "real driver");
        require27(ClientMiles::speaker_configuration_spec(driver) == 2, "stereo speaker");
        ClientMiles::set_listener_3D_position(driver, -1.25f, 2.5f, -3.75f);
        ClientMiles::set_listener_3D_velocity_vector(driver, .001f, -.002f, .003f);
        ClientMiles::set_listener_3D_orientation(driver, 1.f, 0.f, 0.f, 0.f, 1.f, 0.f);
        ClientMiles::set_3D_rolloff_factor(driver, .5f);
        ClientMiles::set_room_type(driver, 2);
        require27(ClientMiles::room_type(driver) == 2, "facade ROOM readback");
        ClientMiles::set_room_type(driver, 0);
        require27(ClientMiles::room_type(driver) == 0, "facade GENERIC readback");
        ClientMiles::serve();
        require27(ClientMiles::room_type(driver) == 0, "generic room after negative controls");
        ClientMiles::shutdown();
        session.close();
        puts("PASS pipe-live27 exact22; seven operations; no playback/callbacks");
        return 0;
    } catch (const std::exception &error) {
        printf("FAIL %s\n", error.what());
        return 1;
    }
}
