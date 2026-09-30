#ifndef CLIENT_MILES_SAMPLE27_H
#define CLIENT_MILES_SAMPLE27_H

#include "../backend-boundary24/ClientMiles.h"

namespace ClientMiles
{
// Common sample identity. Copies alias; they never transfer ownership.
// allocate_sample_handle owns; stream_sample_handle borrows from its live stream.
struct Sample;
typedef Sample *HSAMPLE;

// Nonnull allocation is owned: release exactly once before driver teardown.
HSAMPLE allocate_sample_handle(HDIGDRIVER driver);
int32_t set_named_sample_file(HSAMPLE sample, const char *suffix,
                             const void *fileImage, uint32_t fileBytes, int32_t block);
void sample_ms_position(HSAMPLE sample, int32_t *totalMilliseconds,
                        int32_t *currentMilliseconds);
void end_sample(HSAMPLE sample);
// Owned allocation only; never release a borrowed stream sample.
void release_sample_handle(HSAMPLE sample);

// Allocation null and named-file scalar returns stay actual SDK values. Output
// pointers preserve nullability and millisecond units. No image ownership moves:
// the caller retains suffix/image storage through the documented vendor lifetime;
// this candidate's usage excerpt conservatively keeps both stable through release.
// Binding, millisecond query and end in this subset require an owned allocation.
// The common type also supports the explicitly documented shared stream controls.
}

#endif
