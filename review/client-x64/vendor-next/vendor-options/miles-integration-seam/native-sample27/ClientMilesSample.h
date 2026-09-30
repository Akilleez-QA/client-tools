#ifndef CLIENT_MILES_SAMPLE27_H
#define CLIENT_MILES_SAMPLE27_H

#include "../backend-boundary24/ClientMiles.h"

namespace ClientMiles
{
// Allocated sample identity, local to the selected backend and owning driver.
// Copies alias one allocation; release exactly once. No borrowed stream samples.
struct OwnedSample;
typedef OwnedSample *HSAMPLE;

HSAMPLE allocate_sample_handle(HDIGDRIVER driver);
int32_t set_named_sample_file(HSAMPLE sample, const char *suffix,
                             const void *fileImage, uint32_t fileBytes, int32_t block);
void sample_ms_position(HSAMPLE sample, int32_t *totalMilliseconds,
                        int32_t *currentMilliseconds);
void end_sample(HSAMPLE sample);
void release_sample_handle(HSAMPLE sample);

// Allocation null and named-file scalar returns stay actual SDK values. Output
// pointers preserve nullability and millisecond units. No image ownership moves:
// the caller retains suffix/image storage through the documented vendor lifetime;
// this candidate's usage excerpt conservatively keeps both stable through release.
// This subset does not expose start/playback or a borrowed-sample conversion.
}

#endif
