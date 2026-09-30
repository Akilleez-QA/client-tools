#ifndef TEST_SELECTED44_NATIVE35_COMPAT_H
#define TEST_SELECTED44_NATIVE35_COMPAT_H
// Test only: no ABI evidence. System integer declarations precede macro scope.
#include <stdint.h>
#if defined(_WIN32) || defined(_MSC_VER) || defined(__stdcall)
#error This wrapper is only for the explicitly portable Linux value test.
#endif
#define _WIN32 1
#define _MSC_VER 1800
#define __stdcall
#include "native-file-callbacks35/ClientMilesFileCallbacks.h"
#undef __stdcall
#undef _MSC_VER
#undef _WIN32
#endif
