#include "session_version_host.h"
#if !defined(_WIN32) || defined(_WIN64) || defined(UNICODE)
#error This adapter requires the original x86 ANSI Windows SDK branch.
#endif
#include <Mss.h>
#include <cstring>
namespace MilesSessionVersion {
bool queryCurrentDll(MilesTransport::Bytes query, HMODULE currentDll,
                     std::vector<unsigned char>& frame) {
    MilesWire::Header request={};
    if (!validateQuery(query,request) || !currentDll ||
        GetModuleHandleA(MSSDLLNAME)!=currentDll) return false;
    char text[Capacity];
    // Detect an unexpected macro path that leaves an unterminated buffer.
    // Do not silently fabricate an empty version on transport/identity failure.
    std::memset(text,0xa5,sizeof text);
    AIL_MSS_version(text,sizeof text);
    return makeReply(request,text,frame);
}
}
