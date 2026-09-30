#include <stdint.h>
#if defined(_WIN32) || defined(_MSC_VER) || defined(__stdcall)
#error Portable-only declaration shim
#endif
#define _WIN32 1
#define _MSC_VER 1800
#define __stdcall
#include "tree/native-file-callbacks35/ClientMilesFileCallbacks.h"
#undef __stdcall
#undef _MSC_VER
#undef _WIN32
