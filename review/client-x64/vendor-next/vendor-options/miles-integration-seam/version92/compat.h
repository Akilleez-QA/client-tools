#include <stdint.h>
#if defined(_WIN32) || defined(_MSC_VER) || defined(__stdcall)
#error Portable-only declaration adaptation
#endif
#define _WIN32 1
#define _MSC_VER 1800
#define __stdcall
#include "tree/backend-boundary24/ClientMiles.h"
#undef __stdcall
#undef _MSC_VER
#undef _WIN32
