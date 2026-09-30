#ifndef CLIENT_MILES_INSTALL_ORDER25_H
#define CLIENT_MILES_INSTALL_ORDER25_H
#include "../ClientMilesStartup.h"
namespace Startup25 {
struct Inputs {
    int32_t configuredProvider;
    float position[3], face[3], up[3], rolloff;
    ClientMiles::FileOpenCallback open;
    ClientMiles::FileCloseCallback close;
    ClientMiles::FileSeekCallback seek;
    ClientMiles::FileReadCallback read;
};
struct Observations {
    int32_t startupResult;
    intptr_t mixerChannels;
    ClientMiles::HDIGDRIVER driver;
    ClientMiles::OwnedText directory, firstOpenError, secondOpenError;
    bool usedStereoFallback;
    int32_t speakerSpec;
    Observations() : startupResult(0), mixerChannels(0), driver(0),
                     usedStereoFallback(false), speakerSpec(0) {}
};
// Compile-only operation-order excerpt, not Audio::install or a runnable engine
// integration. Caller owns observations even after Failure. No hidden cleanup.
// Preconditions: fresh selected native lifetime; actual configured callbacks.
// Existing Audio options/cache setup precedes this excerpt. Mixer int narrowing,
// logging, provider-string update and music table work stay in actual Audio.
void installOrder(Inputs const &input, Observations &out);
} // namespace Startup25
#endif
