#include "session_version_host.h"
#if !defined(_WIN32) || defined(_WIN64)
#error This adapter belongs to the original x86 Windows host.
#endif
#include <cstring>
namespace MilesSessionVersion {
bool queryCurrentDll(MilesTransport::Bytes query, HMODULE currentDll,
                     std::vector<unsigned char>& frame) {
    MilesWire::Header request={};
    if (!validateQuery(query,request) || !currentDll) return false;
    char text[Capacity]; std::memset(text,0xa5,sizeof text);
    const int count=LoadStringA(currentDll,1,text,Capacity);
    if(count<=0 || count>=Capacity || text[count]!=0) return false;
    return makeReply(request,text,frame);
}
}
