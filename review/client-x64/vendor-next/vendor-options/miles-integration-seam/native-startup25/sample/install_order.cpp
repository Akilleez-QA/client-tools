#include "install_order.h"
namespace Startup25 {
void installOrder(Inputs const &in, Observations &out) {
    out.directory = ClientMiles::set_redist_directoryOwned("miles");
    out.startupResult = ClientMiles::startup();
    // Actual Audio does not branch on startup's return; do not import the old
    // startup fixture's early-exit policy into this operation-order excerpt.
    ClientMiles::set_file_callbacks(in.open, in.close, in.seek, in.read);
    out.mixerChannels = ClientMiles::get_preference(1);
    // Actual Audio validates int range before storing the mixer count.
    out.driver = ClientMiles::open_digital_driver(22050, 16, in.configuredProvider, 0);
    if (!out.driver) {
        out.firstOpenError = ClientMiles::last_errorOwned(); // actual Audio logs here
        out.driver = ClientMiles::open_digital_driver(22050, 16, in.stereoProvider, 0);
        out.usedStereoFallback = true; // actual Audio updates its provider string here
        if (!out.driver) {
            out.secondOpenError = ClientMiles::last_errorOwned();
            // Actual Audio calls remove/disable here. Partial-startup cleanup is
            // unresolved in source; this excerpt must not invent SDK shutdown.
            return;
        }
    }
    ClientMiles::set_listener_3D_position(out.driver, in.position[0], in.position[1], in.position[2]);
    ClientMiles::set_listener_3D_velocity_vector(out.driver, 0.0f, 0.0f, 0.0f);
    ClientMiles::set_listener_3D_orientation(out.driver, in.face[0], in.face[1], in.face[2],
                                           in.up[0], in.up[1], in.up[2]);
    ClientMiles::set_3D_rolloff_factor(out.driver, in.rolloff);
    out.speakerSpec = ClientMiles::speaker_configuration_spec(out.driver);
    // Audio's install-time setRoomType is gated off by s_installed==false.
    // Actual Audio loads its music table here; no engine work is copied here.
    ClientMiles::set_preference(42, 16);
    ClientMiles::serve();
    // Actual Audio now installs AbstractFile's serve hook, creates its timer,
    // and sets s_installed. No room setter or automatic shutdown belongs here.
}
} // namespace Startup25
