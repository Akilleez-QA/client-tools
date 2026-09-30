#ifndef CLIENT_MILES_STARTUP_SAMPLE_H
#define CLIENT_MILES_STARTUP_SAMPLE_H
#include "../ClientMiles.h"

struct StartupObservations {
    ClientMiles::OwnedText version, dot, directory, firstError, secondError;
    int32_t startupResult;
    intptr_t mixerChannels, initialFragments, previous16, read16, previous64, read64;
    intptr_t finalFragments;
    bool driverOpened;
    int32_t speakerSpec;
    StartupObservations()
        : startupResult(0), mixerChannels(0), initialFragments(0), previous16(0), read16(0),
          previous64(0), read64(0), finalFragments(0), driverOpened(false), speakerSpec(0) {
    }
};

// Game-facing source sample: independent of backend selection and transport.
// It preserves startup23's valid call order; raw negative probes stay in fixtures.
StartupObservations startupCalls();
#endif
