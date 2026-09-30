#ifndef CLIENT_MILES_TEST_DOUBLE
#error This implementation is only for the deletion build check, never a vendor replacement.
#endif
#include "../ClientMiles.h"

namespace ClientMiles {
struct DigitalDriver {};
int32_t startup() {
    return 0;
}
void shutdown() {
}
intptr_t get_preference(uint32_t) {
    return 0;
}
intptr_t set_preference(uint32_t, intptr_t) {
    return 0;
}
OwnedText last_errorOwned() {
    return OwnedText();
}
OwnedText set_redist_directoryOwned(const char *) {
    return OwnedText();
}
OwnedText MSS_versionOwned() {
    return OwnedText();
}
HDIGDRIVER open_digital_driver(uint32_t, int32_t, int32_t, uint32_t) {
    return 0;
}
int32_t speaker_configuration_spec(HDIGDRIVER) {
    return 0;
}
} // namespace ClientMiles
