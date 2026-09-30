#include "startup_calls.h"

StartupObservations startupCalls() {
    StartupObservations out;
    out.version = ClientMiles::MSS_versionOwned();
    out.dot = ClientMiles::set_redist_directoryOwned(".");
    out.directory = ClientMiles::set_redist_directoryOwned("miles");
    out.startupResult = ClientMiles::startup();
    if (!out.startupResult)
        return out;
    out.mixerChannels = ClientMiles::get_preference(1);
    out.initialFragments = ClientMiles::get_preference(42);
    out.firstError = ClientMiles::last_errorOwned();
    out.secondError = ClientMiles::last_errorOwned();
    out.previous16 = ClientMiles::set_preference(42, 16);
    out.read16 = ClientMiles::get_preference(42);
    out.previous64 = ClientMiles::set_preference(42, 64);
    out.read64 = ClientMiles::get_preference(42);
    out.finalFragments = ClientMiles::get_preference(42);
    ClientMiles::HDIGDRIVER driver = ClientMiles::open_digital_driver(22050, 16, 2, 0);
    out.driverOpened = driver != 0;
    if (driver)
        out.speakerSpec = ClientMiles::speaker_configuration_spec(driver);
    ClientMiles::shutdown();
    return out;
}
