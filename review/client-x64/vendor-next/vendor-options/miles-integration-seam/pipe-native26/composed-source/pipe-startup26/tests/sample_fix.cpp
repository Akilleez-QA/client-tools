#ifndef PIPE26_TEST_ONLY
#error This is a portable test double, never a production implementation.
#endif
#include "../../native-startup25/sample/install_order.h"
#include <stdexcept>
#include <iostream>
namespace { bool failDirectory = false; unsigned opens = 0; }
namespace ClientMiles {
OwnedText set_redist_directoryOwned(char const *) {
    if (failDirectory) throw Failure(FailureReason::BackendFailed, "test-only fault");
    OwnedText t; t.isNull = false; t.value = "test"; return t;
}
int32_t startup() { return 1; }
void set_file_callbacks(FileOpenCallback, FileCloseCallback, FileSeekCallback, FileReadCallback) {}
intptr_t get_preference(uint32_t) { return 64; }
HDIGDRIVER open_digital_driver(uint32_t, int32_t, int32_t spec, uint32_t) {
    ++opens;
    if (opens == 1) { if (spec != 99) throw std::runtime_error("configured request changed"); return 0; }
    if (spec != 2) throw std::runtime_error("fallback must use fixed stereo");
    return reinterpret_cast<HDIGDRIVER>(uintptr_t(1));
}
OwnedText last_errorOwned() { OwnedText t; t.isNull=false; t.value="vendor-null"; return t; }
void set_listener_3D_position(HDIGDRIVER, float, float, float) {}
void set_listener_3D_velocity_vector(HDIGDRIVER, float, float, float) {}
void set_listener_3D_orientation(HDIGDRIVER, float, float, float, float, float, float) {}
void set_3D_rolloff_factor(HDIGDRIVER, float) {}
int32_t speaker_configuration_spec(HDIGDRIVER) { return 2; }
intptr_t set_preference(uint32_t, intptr_t) { return 0; }
void serve() {}
}
int main() {
    Startup25::Inputs in = {}; in.configuredProvider=99;
    Startup25::Observations out;
    Startup25::installOrder(in,out);
    if (!out.driver || !out.usedStereoFallback || opens != 2) return 1;
    failDirectory=true;
    try { Startup25::installOrder(in,out); return 2; }
    catch (ClientMiles::Failure const &) {}
    if (out.driver || out.usedStereoFallback || out.startupResult || out.mixerChannels ||
        out.speakerSpec || !out.directory.isNull || !out.directory.value.empty() ||
        !out.firstOpenError.isNull || !out.firstOpenError.value.empty() ||
        !out.secondOpenError.isNull || !out.secondOpenError.value.empty()) return 3;
    std::cout << "PASS fixed stereo and fresh observations after second-attempt fault\n";
}
