#include "../native-stream28/ClientMilesStream.h"
#include "../native-playback28/ClientMilesPlayback.h"
#include <type_traits>
// Intended for a future composed overlay check; not compiled or executed here.
static_assert(std::is_same<decltype(&ClientMiles::stream_sample_handle),
    ClientMiles::HSAMPLE (*)(ClientMiles::HSTREAM)>::value, "one common sample result");
// Mirrors the five actual stream branches without a public ownership cast or
// duplicate borrowed-control API. Inputs/policy/lifetime remain caller concerns.
void streamControlShapes32(ClientMiles::HSTREAM stream, float left, float right,
                           int32_t rate, float *leftOut, float *rightOut, int32_t *rateOut)
{
    ClientMiles::set_sample_volume_levels(ClientMiles::stream_sample_handle(stream), left, right);
    ClientMiles::set_sample_reverb_levels(ClientMiles::stream_sample_handle(stream), 1.0f, 0.0f);
    ClientMiles::set_sample_playback_rate(ClientMiles::stream_sample_handle(stream), rate);
    ClientMiles::sample_volume_levels(ClientMiles::stream_sample_handle(stream), leftOut, rightOut);
    *rateOut = ClientMiles::sample_playback_rate(ClientMiles::stream_sample_handle(stream));
}
