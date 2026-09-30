#ifndef EXPERIMENTAL_SESSION_VERSION21_HOST_H
#define EXPERIMENTAL_SESSION_VERSION21_HOST_H
#include "session_version.h"
#include <windows.h>
namespace MilesSessionVersion {
// Caller holds the verified original x86 module throughout this operation and
// excludes concurrent unload. Failure leaves frame unchanged. No Miles export.
bool queryCurrentDll(MilesTransport::Bytes query, HMODULE currentDll,
                     std::vector<unsigned char>& frame);
}
#endif
