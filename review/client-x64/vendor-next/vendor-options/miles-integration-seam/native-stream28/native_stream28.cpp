#include "ClientMilesStream.h"
#include <Mss.h>
#include <type_traits>

#if !defined(_WIN64) || _MSC_VER != 1800
#error Requires actual v120 x64 and the pinned private Miles 7.2a header.
#endif

static_assert(std::is_same<int32_t, S32>::value, "exact native signed scalar type");
static_assert(std::is_same<char, C8>::value, "exact native filename character type");

// Handles intentionally differ. Bind all other facade arguments/results to the
// possessed SDK types, and separately assert each actual native declaration.
static_assert(std::is_same<decltype(&ClientMiles::open_stream),
    ClientMiles::HSTREAM (*)(ClientMiles::HDIGDRIVER, const char *, S32)>::value,
    "facade open shape");
static_assert(std::is_same<decltype(&::AIL_open_stream),
    ::HSTREAM (AILCALL *)(::HDIGDRIVER, const char *, S32)>::value,
    "actual open signature");

static_assert(std::is_same<decltype(&ClientMiles::close_stream),
    void (*)(ClientMiles::HSTREAM)>::value, "facade close shape");
static_assert(std::is_same<decltype(&::AIL_close_stream),
    void (AILCALL *)(::HSTREAM)>::value, "actual close signature");

static_assert(std::is_same<decltype(&ClientMiles::start_stream),
    void (*)(ClientMiles::HSTREAM)>::value, "facade start shape");
static_assert(std::is_same<decltype(&::AIL_start_stream),
    void (AILCALL *)(::HSTREAM)>::value, "actual start signature");

static_assert(std::is_same<decltype(&ClientMiles::set_stream_loop_count),
    void (*)(ClientMiles::HSTREAM, S32)>::value, "facade signed loop count");
static_assert(std::is_same<decltype(&::AIL_set_stream_loop_count),
    void (AILCALL *)(::HSTREAM, S32)>::value, "actual loop count signature");

static_assert(std::is_same<decltype(&ClientMiles::set_stream_loop_block),
    void (*)(ClientMiles::HSTREAM, S32, S32)>::value, "facade signed native offsets");
static_assert(std::is_same<decltype(&::AIL_set_stream_loop_block),
    void (AILCALL *)(::HSTREAM, S32, S32)>::value, "actual loop block signature");

static_assert(std::is_same<decltype(&ClientMiles::stream_status),
    S32 (*)(ClientMiles::HSTREAM)>::value, "facade signed status");
static_assert(std::is_same<decltype(&::AIL_stream_status),
    S32 (AILCALL *)(::HSTREAM)>::value, "actual status signature");

static_assert(std::is_same<decltype(&ClientMiles::set_stream_ms_position),
    void (*)(ClientMiles::HSTREAM, S32)>::value, "facade signed milliseconds");
static_assert(std::is_same<decltype(&::AIL_set_stream_ms_position),
    void (AILCALL *)(::HSTREAM, S32)>::value, "actual set position signature");

static_assert(std::is_same<decltype(&ClientMiles::stream_ms_position),
    void (*)(ClientMiles::HSTREAM, S32 *, S32 *)>::value, "facade nullable signed outputs");
static_assert(std::is_same<decltype(&::AIL_stream_ms_position),
    void (AILCALL *)(::HSTREAM, S32 *, S32 *)>::value, "actual position signature");

namespace ClientMiles
{
HSTREAM open_stream(HDIGDRIVER driver, const char *filename, int32_t streamMem)
{
    return reinterpret_cast<HSTREAM>(::AIL_open_stream(
        reinterpret_cast<::HDIGDRIVER>(driver), filename, streamMem));
}

void close_stream(HSTREAM stream)
{
    ::AIL_close_stream(reinterpret_cast<::HSTREAM>(stream));
}

void start_stream(HSTREAM stream)
{
    ::AIL_start_stream(reinterpret_cast<::HSTREAM>(stream));
}

void set_stream_loop_count(HSTREAM stream, int32_t count)
{
    ::AIL_set_stream_loop_count(reinterpret_cast<::HSTREAM>(stream), count);
}

void set_stream_loop_block(HSTREAM stream, int32_t loopStartOffset, int32_t loopEndOffset)
{
    ::AIL_set_stream_loop_block(reinterpret_cast<::HSTREAM>(stream),
                                loopStartOffset, loopEndOffset);
}

int32_t stream_status(HSTREAM stream)
{
    return ::AIL_stream_status(reinterpret_cast<::HSTREAM>(stream));
}

void set_stream_ms_position(HSTREAM stream, int32_t milliseconds)
{
    ::AIL_set_stream_ms_position(reinterpret_cast<::HSTREAM>(stream), milliseconds);
}

void stream_ms_position(HSTREAM stream, int32_t *totalMilliseconds,
                        int32_t *currentMilliseconds)
{
    ::AIL_stream_ms_position(reinterpret_cast<::HSTREAM>(stream),
                             totalMilliseconds, currentMilliseconds);
}
}
