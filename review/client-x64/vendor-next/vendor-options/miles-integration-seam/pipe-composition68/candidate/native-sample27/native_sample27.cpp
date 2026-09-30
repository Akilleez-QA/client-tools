#include "ClientMilesSample.h"
#include <Mss.h>
#include <type_traits>

#if !defined(_WIN64) || _MSC_VER != 1800
#error Requires actual v120 x64 and the pinned private Miles 7.2a header.
#endif

static_assert(std::is_same<uint32_t, U32>::value, "exact native image byte count");
static_assert(std::is_same<int32_t, S32>::value, "exact native block/result/millisecond type");
static_assert(std::is_same<char, C8>::value, "exact native suffix element type");

// Opaque facade handles intentionally differ. Bind every remaining argument and
// result to the actual SDK types, and check the corresponding native declaration.
static_assert(std::is_same<decltype(&ClientMiles::allocate_sample_handle),
    ClientMiles::HSAMPLE (*)(ClientMiles::HDIGDRIVER)>::value, "facade allocation shape");
static_assert(std::is_same<decltype(&::AIL_allocate_sample_handle),
    ::HSAMPLE (AILCALL *)(::HDIGDRIVER)>::value, "actual allocation signature");

static_assert(std::is_same<decltype(&ClientMiles::set_named_sample_file),
    S32 (*)(ClientMiles::HSAMPLE, C8 const *, void const *, U32, S32)>::value,
    "facade named-file shape with native scalar/pointer types");
static_assert(std::is_same<decltype(&::AIL_set_named_sample_file),
    S32 (AILCALL *)(::HSAMPLE, C8 const *, void const *, U32, S32)>::value,
    "actual named-file signature");

static_assert(std::is_same<decltype(&ClientMiles::sample_ms_position),
    void (*)(ClientMiles::HSAMPLE, S32 *, S32 *)>::value, "facade native output pointer types");
static_assert(std::is_same<decltype(&::AIL_sample_ms_position),
    void (AILCALL *)(::HSAMPLE, S32 *, S32 *)>::value, "actual position signature");

static_assert(std::is_same<decltype(&ClientMiles::end_sample),
    void (*)(ClientMiles::HSAMPLE)>::value, "facade end shape");
static_assert(std::is_same<decltype(&::AIL_end_sample),
    void (AILCALL *)(::HSAMPLE)>::value, "actual end signature");
static_assert(std::is_same<decltype(&ClientMiles::release_sample_handle),
    void (*)(ClientMiles::HSAMPLE)>::value, "facade release shape");
static_assert(std::is_same<decltype(&::AIL_release_sample_handle),
    void (AILCALL *)(::HSAMPLE)>::value, "actual release signature");

namespace ClientMiles
{
HSAMPLE allocate_sample_handle(HDIGDRIVER driver)
{
    return reinterpret_cast<HSAMPLE>(
        ::AIL_allocate_sample_handle(reinterpret_cast<::HDIGDRIVER>(driver)));
}

int32_t set_named_sample_file(HSAMPLE sample, const char *suffix,
                             const void *fileImage, uint32_t fileBytes, int32_t block)
{
    return ::AIL_set_named_sample_file(reinterpret_cast<::HSAMPLE>(sample),
                                       suffix, fileImage, fileBytes, block);
}

void sample_ms_position(HSAMPLE sample, int32_t *totalMilliseconds,
                        int32_t *currentMilliseconds)
{
    ::AIL_sample_ms_position(reinterpret_cast<::HSAMPLE>(sample),
                             totalMilliseconds, currentMilliseconds);
}

void end_sample(HSAMPLE sample)
{
    ::AIL_end_sample(reinterpret_cast<::HSAMPLE>(sample));
}

void release_sample_handle(HSAMPLE sample)
{
    ::AIL_release_sample_handle(reinterpret_cast<::HSAMPLE>(sample));
}
}
