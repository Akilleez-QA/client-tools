#ifndef EXPERIMENTAL_SESSION_VERSION22_HOST_H
#define EXPERIMENTAL_SESSION_VERSION22_HOST_H
#include "session_version.h"
#include <windows.h>
namespace MilesSessionVersion {
// Caller holds the externally verified original module throughout this call
// and excludes concurrent unload. Resource 1 is read from this exact HMODULE;
// no basename lookup or load occurs here. A resource failure (including zero
// copied characters) returns false and leaves frame unchanged. No Miles export.
bool queryCurrentDll(MilesTransport::Bytes query, HMODULE currentDll,
                     std::vector<unsigned char>& frame);
}
#endif
