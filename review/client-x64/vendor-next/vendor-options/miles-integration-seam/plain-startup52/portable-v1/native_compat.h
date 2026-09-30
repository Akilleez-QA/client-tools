// Portable value/ownership test only: this does not test the Windows ABI.
#include <stdint.h>
#if defined(_WIN32) || defined(_MSC_VER) || defined(__stdcall)
#error This shim is for a non-Windows portable compiler only
#endif
#define _WIN32 1
#define _MSC_VER 1800
#define __stdcall
#include "../candidate/ClientMiles.h"
#undef __stdcall
#undef _MSC_VER
#undef _WIN32
