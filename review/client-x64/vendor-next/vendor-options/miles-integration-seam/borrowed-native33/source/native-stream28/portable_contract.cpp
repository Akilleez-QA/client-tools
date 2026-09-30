#include "ClientMilesStream.h"
#include "../native-sample27/ClientMilesSample.h"
#include <type_traits>

namespace
{
using namespace ClientMiles;
static_assert(!std::is_convertible<HSTREAM, HDIGDRIVER>::value, "stream is not a driver");
static_assert(!std::is_convertible<HDIGDRIVER, HSTREAM>::value, "driver is not a stream");
static_assert(!std::is_convertible<HSTREAM, HSAMPLE>::value, "stream is not an allocated sample");
static_assert(!std::is_convertible<HSAMPLE, HSTREAM>::value, "allocated sample is not a stream");

static_assert(std::is_same<decltype(&open_stream),
    HSTREAM (*)(HDIGDRIVER, const char *, int32_t)>::value, "open declaration");
static_assert(std::is_same<decltype(&close_stream), void (*)(HSTREAM)>::value,
    "close declaration");
static_assert(std::is_same<decltype(&start_stream), void (*)(HSTREAM)>::value,
    "start declaration");
static_assert(std::is_same<decltype(&set_stream_loop_count),
    void (*)(HSTREAM, int32_t)>::value, "signed loop count");
static_assert(std::is_same<decltype(&set_stream_loop_block),
    void (*)(HSTREAM, int32_t, int32_t)>::value, "signed native offsets");
static_assert(std::is_same<decltype(&stream_status), int32_t (*)(HSTREAM)>::value,
    "signed status declaration");
static_assert(std::is_same<decltype(&set_stream_ms_position),
    void (*)(HSTREAM, int32_t)>::value, "signed milliseconds");
static_assert(std::is_same<decltype(&stream_ms_position),
    void (*)(HSTREAM, int32_t *, int32_t *)>::value, "nullable signed output pointers");
}

// Compile-only shapes, never linked or executed. Null outputs are not converted
// to temporary required storage; signed values remain signed at this boundary.
void compileNullableStreamOutputs(ClientMiles::HSTREAM stream, int32_t *output)
{
    ClientMiles::stream_ms_position(stream, output, 0);
    ClientMiles::stream_ms_position(stream, 0, output);
    ClientMiles::stream_ms_position(stream, 0, 0);
    ClientMiles::set_stream_loop_block(stream, 0, -1);
    ClientMiles::set_stream_loop_count(stream, 0);
}
