#ifndef CLIENT_MILES_SAMPLE_TIME27_H
#define CLIENT_MILES_SAMPLE_TIME27_H
#include "ClientMilesSample.h"

namespace SampleTime27
{
struct Observations
{
    bool allocated;
    int32_t bindingResult;
    int32_t totalMilliseconds;
    int32_t currentMilliseconds;
    Observations() : allocated(false), bindingResult(0),
        totalMilliseconds(0), currentMilliseconds(0) {}
};

// Compile-only native usage excerpt. The caller supplies a live driver, the
// existing extension bytes, and a complete image kept stable through return.
// This models normal SDK returns only, not future uncertain transport failures.
Observations inspectDuration(ClientMiles::HDIGDRIVER driver, const char *extension,
                             const void *fileImage, int32_t signedFileBytes);
}
#endif
