#include "../ClientMiles.h"
#include <Mss.h>
#include <cstring>
#include <list>
#include <type_traits>
#include <windows.h>

#if !defined(_WIN64) || _MSC_VER != 1800
#error This source check requires native v120 x64 with the possessed private header.
#endif

// These assertions inspect the actual private header; no SDK declarations are
// duplicated in the public facade and no import-library replacement is supplied.
static_assert(sizeof(SINTa) == 8 && sizeof(intptr_t) == sizeof(SINTa),
              "facade preference width matches this WIN64 header");
static_assert(std::is_same<intptr_t, SINTa>::value, "exact signed native preference type");
static_assert(sizeof(U32) == sizeof(uint32_t) && sizeof(S32) == sizeof(int32_t),
              "fixed scalar widths match this SDK");
static_assert(std::is_same<U32, uint32_t>::value && std::is_same<S32, int32_t>::value,
              "fixed scalar types exactly match this SDK");
static_assert(std::is_same<decltype(&ClientMiles::startup), decltype(&::AIL_startup)>::value,
              "facade startup signature matches SDK");
static_assert(std::is_same<decltype(&ClientMiles::shutdown), decltype(&::AIL_shutdown)>::value,
              "facade shutdown signature matches SDK");
static_assert(
    std::is_same<decltype(&ClientMiles::get_preference), decltype(&::AIL_get_preference)>::value,
    "facade get preference signature matches SDK");
static_assert(
    std::is_same<decltype(&ClientMiles::set_preference), decltype(&::AIL_set_preference)>::value,
    "facade set preference signature matches SDK");
static_assert(DIG_MIXER_CHANNELS == 1 && DIG_DS_MIX_FRAGMENT_CNT == 42,
              "observed preference identifiers");
static_assert(MSS_MC_STEREO == 2, "observed speaker specification");
static_assert(std::is_same<decltype(&::AIL_get_preference), SINTa(AILCALL *)(U32)>::value,
              "actual get preference declaration");
static_assert(std::is_same<decltype(&::AIL_set_preference), SINTa(AILCALL *)(U32, SINTa)>::value,
              "actual set preference declaration");

namespace {
std::list<std::string> retainedDirectories;

ClientMiles::OwnedText copyText(const char *text) {
    ClientMiles::OwnedText out;
    out.isNull = text == 0;
    if (text)
        out.value = text;
    return out;
}
} // namespace

// Compile-only candidate. Every operation delegates to the actual SDK symbol;
// none of this code has been linked with or executed against an x64 Miles DLL.
namespace ClientMiles {
int32_t startup() {
    return ::AIL_startup();
}

void shutdown() {
    ::AIL_shutdown();
    retainedDirectories.clear();
}

intptr_t get_preference(uint32_t number) {
    return ::AIL_get_preference(number);
}

intptr_t set_preference(uint32_t number, intptr_t value) {
    return ::AIL_set_preference(number, value);
}

OwnedText last_errorOwned() {
    return copyText(::AIL_last_error());
}

OwnedText set_redist_directoryOwned(const char *directory) {
    if (!directory)
        throw Failure(FailureReason::InvalidArgument, "null redistribution directory");
    retainedDirectories.push_back(directory);
    return copyText(::AIL_set_redist_directory(retainedDirectories.back().c_str()));
}

OwnedText MSS_versionOwned() {
    char text[256];
    std::memset(text, 0xa5, sizeof text);
    AIL_MSS_version(text, sizeof text);
    if (!std::memchr(text, 0, sizeof text) || !text[0])
        throw Failure(FailureReason::QueryFailed, "native Miles version resource unavailable");
    return copyText(text);
}

HDIGDRIVER open_digital_driver(uint32_t frequency, int32_t bits, int32_t channels, uint32_t flags) {
    return reinterpret_cast<HDIGDRIVER>(
        ::AIL_open_digital_driver(frequency, bits, channels, flags));
}

int32_t speaker_configuration_spec(HDIGDRIVER driver) {
    MSS_MC_SPEC spec = MSS_MC_INVALID;
    ::AIL_speaker_configuration(reinterpret_cast<::HDIGDRIVER>(driver), 0, 0, 0, &spec);
    return static_cast<int32_t>(spec);
}
} // namespace ClientMiles
