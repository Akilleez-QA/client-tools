#include "ClientMilesSample.h"
#include <type_traits>

namespace
{
using namespace ClientMiles;
static_assert(!std::is_convertible<HSAMPLE, HDIGDRIVER>::value, "distinct opaque identities");
static_assert(!std::is_convertible<HDIGDRIVER, HSAMPLE>::value, "driver is not an owned sample");
static_assert(std::is_same<decltype(&allocate_sample_handle),
    HSAMPLE (*)(HDIGDRIVER)>::value, "allocation declaration");
static_assert(std::is_same<decltype(&set_named_sample_file),
    int32_t (*)(HSAMPLE, const char *, const void *, uint32_t, int32_t)>::value,
    "pointer-plus-extent named-file declaration");
static_assert(std::is_same<decltype(&sample_ms_position),
    void (*)(HSAMPLE, int32_t *, int32_t *)>::value, "nullable signed outputs");
static_assert(std::is_same<decltype(&end_sample), void (*)(HSAMPLE)>::value, "end declaration");
static_assert(std::is_same<decltype(&release_sample_handle), void (*)(HSAMPLE)>::value,
    "release declaration");
}

// Compile-only call shapes. This function is never linked or executed.
void compileNullableOutputs(ClientMiles::HSAMPLE sample, int32_t *output)
{
    ClientMiles::sample_ms_position(sample, output, 0);
    ClientMiles::sample_ms_position(sample, 0, output);
    ClientMiles::sample_ms_position(sample, 0, 0);
}
