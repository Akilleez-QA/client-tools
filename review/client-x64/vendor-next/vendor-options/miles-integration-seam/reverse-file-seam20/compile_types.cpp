// Syntax-only checks. No vendor/engine includes, callbacks, allocation, or main.
#include "ClientAudioFileCallbacks.h"
#include <limits>
#include <type_traits>

namespace FileCallbacks = ClientAudioFileCallbacks;

static_assert(sizeof(uint32_t) == 4, "unsigned callback scalars are 32 bits");
static_assert(sizeof(int32_t) == 4, "signed callback scalars are 32 bits");
static_assert(sizeof(FileCallbacks::LocalFileHandle) == sizeof(uintptr_t),
              "local key follows client pointer width");
static_assert(sizeof(uintptr_t) == sizeof(void *), "local key width");
static_assert(std::numeric_limits<int32_t>::is_signed, "seek signedness");
static_assert(!std::is_convertible<FileCallbacks::LocalFileHandle, bool>::value,
              "open success must not be inferred from the native key");
static_assert(!std::is_convertible<FileCallbacks::LocalFileHandle, void *>::value,
              "native keys are not registry pointers");

typedef FileCallbacks::OpenResult (*OpenSignature)(char const *);
typedef void (*CloseSignature)(FileCallbacks::LocalFileHandle);
typedef int32_t (*SeekSignature)(FileCallbacks::LocalFileHandle, int32_t, uint32_t);
typedef uint32_t (*ReadSignature)(FileCallbacks::LocalFileHandle, void *, uint32_t);

static_assert(std::is_same<decltype(&FileCallbacks::open), OpenSignature>::value,
              "open signature");
static_assert(std::is_same<decltype(&FileCallbacks::close), CloseSignature>::value,
              "close signature");
static_assert(std::is_same<decltype(&FileCallbacks::seek), SeekSignature>::value,
              "seek signature");
static_assert(std::is_same<decltype(&FileCallbacks::read), ReadSignature>::value,
              "read signature");

constexpr FileCallbacks::OpenResult zeroHandleSuccess = {1u, {0u}};
static_assert(zeroHandleSuccess.callbackResult != 0 &&
                  zeroHandleSuccess.handle.value == 0,
              "success and zero local handle coexist");
static_assert(FileCallbacks::SeekBegin == 0 && FileCallbacks::SeekCurrent == 1 &&
                  FileCallbacks::SeekEnd == 2,
              "reviewed Miles seek origin values");
