#include "stream_calls.h"

namespace StreamCalls28
{
Observations showCallShapes(ClientMiles::HDIGDRIVER driver, const char *filename,
                            int32_t streamMem, int32_t loopStartOffset,
                            int32_t loopEndOffset, int32_t loopCount,
                            int32_t milliseconds)
{
    Observations result;
    ClientMiles::HSTREAM stream = ClientMiles::open_stream(driver, filename, streamMem);
    if (!stream)
        return result;

    result.opened = true;
    ClientMiles::set_stream_loop_block(stream, loopStartOffset, loopEndOffset);
    ClientMiles::set_stream_loop_count(stream, loopCount);
    ClientMiles::start_stream(stream);
    result.status = ClientMiles::stream_status(stream);
    ClientMiles::set_stream_ms_position(stream, milliseconds);
    ClientMiles::stream_ms_position(stream, &result.totalMilliseconds,
                                    &result.currentMilliseconds);
    // Normal-return ownership only. No callback, wait-for-completion, automatic
    // retry or transport-exception cleanup policy is implied by this excerpt.
    ClientMiles::close_stream(stream);
    return result;
}
}
