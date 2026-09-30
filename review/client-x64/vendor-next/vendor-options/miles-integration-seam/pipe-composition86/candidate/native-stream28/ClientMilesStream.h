#ifndef CLIENT_MILES_STREAM_FACADE_H
#define CLIENT_MILES_STREAM_FACADE_H

#include "../native-sample27/ClientMilesSample.h"

namespace ClientMiles
{
// Owned by the caller after a nonnull open; close once before driver teardown.
// Copies alias one stream. This is an opaque identity, not an RAII owner.
struct OwnedStream;
typedef OwnedStream *HSTREAM;

HSTREAM open_stream(HDIGDRIVER driver, const char *filename, int32_t streamMem);
// Closing invalidates every borrowed sample obtained from this stream.
void close_stream(HSTREAM stream);
// Borrowed: do not release_sample_handle; invalid after parent close/shutdown.
HSAMPLE stream_sample_handle(HSTREAM stream);
void start_stream(HSTREAM stream);
void set_stream_loop_count(HSTREAM stream, int32_t count);
void set_stream_loop_block(HSTREAM stream, int32_t loopStartOffset, int32_t loopEndOffset);
int32_t stream_status(HSTREAM stream);
void set_stream_ms_position(HSTREAM stream, int32_t milliseconds);
void stream_ms_position(HSTREAM stream, int32_t *totalMilliseconds,
                        int32_t *currentMilliseconds);

// Signed SDK values, native offsets and nullable output pointers pass unchanged.
// Use the existing shared sample control names for borrowed samples; see
// ClientMilesPlayback.h for this subset. No callback/EOS lifetime is promised.
}
#endif
