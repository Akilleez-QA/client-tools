#ifndef STREAM_CALLS28_H
#define STREAM_CALLS28_H

#include "ClientMilesStream.h"

namespace StreamCalls28
{
struct Observations
{
    bool opened;
    int32_t status;
    int32_t totalMilliseconds;
    int32_t currentMilliseconds;

    Observations()
        : opened(false), status(0), totalMilliseconds(0), currentMilliseconds(0)
    {
    }
};

// Compile-only usage excerpt; never linked or executed in this candidate.
// A false opened flag leaves all other fields unobserved, not vendor results.
Observations showCallShapes(ClientMiles::HDIGDRIVER driver, const char *filename,
                            int32_t streamMem, int32_t loopStartOffset,
                            int32_t loopEndOffset, int32_t loopCount,
                            int32_t milliseconds);
}
#endif
