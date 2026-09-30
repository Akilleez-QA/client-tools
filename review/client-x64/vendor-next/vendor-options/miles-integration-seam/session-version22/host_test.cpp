#include "session_version_host.h"
#include "test_support.h"
#include <Mss.h>
using namespace MilesSessionVersion;
int main(int argc,char** argv) {
    setvbuf(stdout,0,_IONBF,0);
    if(argc!=3) return 2;
    CHECK(sizeof(void*)==4);
    // Restrict the original macro oracle to a single normal matching module.
    CHECK(GetModuleHandleA(MSSDLLNAME)==0); if(failures) return 1;
    HMODULE module=LoadLibraryA(argv[1]); CHECK(module!=0); if(!module) return 1;
    char loaded[MAX_PATH]={}; const DWORD n=GetModuleFileNameA(module,loaded,MAX_PATH);
    CHECK(n && n<MAX_PATH && !_stricmp(loaded,argv[1]));
    CHECK(GetModuleHandleA(MSSDLLNAME)==module);
    std::printf("macro_oracle_dll=%s\n",loaded);
    if(failures) { FreeLibrary(module); return 1; }
    char original[Capacity]; std::memset(original,0xa5,sizeof original);
    AIL_MSS_version(original,sizeof original);
    const char* terminator=static_cast<const char*>(std::memchr(original,0,sizeof original));
    CHECK(terminator && terminator!=original);
    if(failures) { FreeLibrary(module); return 1; }
    const size_t length=static_cast<size_t>(terminator-original)+1;
    std::vector<unsigned char> q,frame; CHECK(makeQuery(request(),q));
    CHECK(queryCurrentDll(bytes(q),module,frame));
    char candidate[Capacity]; std::memset(candidate,0x69,sizeof candidate);
    CHECK(copyReply(bytes(frame),request(),candidate));
    if(failures) { FreeLibrary(module); return 1; }
    CHECK(!std::memcmp(original,candidate,length));
    if(length<Capacity) CHECK(candidate[length]==0x69);
    std::printf("macro_text=%s direct_adapter_text=%s bytes=%u compiletime_text=%s\n",
        original,candidate,static_cast<unsigned>(length),MSS_VERSION);
#ifdef VERSION_POISON_CONTROL
    CHECK(std::strcmp(original,MSS_VERSION)!=0);
    std::puts("poisoned_compiletime_substitution_rejected=yes");
#endif
    const std::vector<unsigned char> saved=frame;
    CHECK(!queryCurrentDll(bytes(q),0,frame)); CHECK(frame==saved);
    std::vector<unsigned char> invalid=q; invalid[72]=1;
    CHECK(!queryCurrentDll(bytes(invalid),module,frame)); CHECK(frame==saved);
    // Own executable is a valid live module with no string resource 1.
    HMODULE self=GetModuleHandleA(0); char missing[Capacity]={}; CHECK(self!=0);
    CHECK(LoadStringA(self,1,missing,Capacity)==0);
    CHECK(!queryCurrentDll(bytes(q),self,frame)); CHECK(frame==saved);
    std::puts("missing_resource=false_unchanged_frame");
    CHECK(FreeLibrary(module)!=0); CHECK(GetModuleHandleA(MSSDLLNAME)==0);
    if(failures) return 1;
    // Identical original DLL copies, same basename, distinct data mappings.
    // These mappings are absent from the normal basename namespace and do not
    // perform normal DLL initialization. Identity is checked by the launcher.
    const DWORD flags=LOAD_LIBRARY_AS_DATAFILE_EXCLUSIVE|LOAD_LIBRARY_AS_IMAGE_RESOURCE;
    HMODULE first=LoadLibraryExA(argv[1],0,flags);
    HMODULE second=LoadLibraryExA(argv[2],0,flags);
    CHECK(first && second && first!=second);
    CHECK(GetModuleHandleA(MSSDLLNAME)==0);
    if(failures) { if(first) FreeLibrary(first); if(second) FreeLibrary(second); return 1; }
    std::vector<unsigned char> firstFrame,secondFrame;
    CHECK(queryCurrentDll(bytes(q),first,firstFrame));
    CHECK(queryCurrentDll(bytes(q),second,secondFrame));
    CHECK(firstFrame==saved && secondFrame==saved);
    CHECK(GetModuleHandleA(MSSDLLNAME)==0);
    std::puts("same_basename_resource_handles=distinct normal_basename_module=absent both_direct_queries=matched");
    CHECK(FreeLibrary(first)!=0); CHECK(FreeLibrary(second)!=0);
    CHECK(writeFile("macro-oracle.bin",original,length));
    std::memset(original,'z',sizeof original); std::memset(candidate,0x69,sizeof candidate);
    CHECK(copyReply(bytes(secondFrame),request(),candidate)); if(failures) return 1;
    CHECK(writeFile("version-reply.bin",&secondFrame[0],secondFrame.size()));
    std::printf("owned_after_unload=%s frame_bytes=%u\n",candidate,static_cast<unsigned>(secondFrame.size()));
    std::printf("%u/%u direct resource checks; no startup/device/playback\n",checks-failures,checks);
    return failures?1:0;
}
