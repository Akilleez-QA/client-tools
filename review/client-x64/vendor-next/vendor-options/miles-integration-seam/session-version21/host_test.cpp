#include "session_version_host.h"
#include "test_support.h"
#include <Mss.h>
using namespace MilesSessionVersion;
int main(int argc,char** argv) {
    setvbuf(stdout,0,_IONBF,0);
    if(argc!=2) return 2;
    CHECK(sizeof(void*)==4);
    // The Python launcher verifies path and exact DLL hash immediately before
    // launching. The probe binds the actual mapped module to that same path.
    CHECK(GetModuleHandleA(MSSDLLNAME)==0);
    if(failures) return 1;
    HMODULE module=LoadLibraryA(argv[1]); CHECK(module!=0); if(!module) return 1;
    char loaded[MAX_PATH]={}; DWORD n=GetModuleFileNameA(module,loaded,MAX_PATH);
    CHECK(n && n<MAX_PATH && !_stricmp(loaded,argv[1]));
    CHECK(GetModuleHandleA(MSSDLLNAME)==module);
    std::printf("loaded_dll=%s\n",loaded);
    if(failures) { FreeLibrary(module); return 1; }
    char direct[Capacity]; std::memset(direct,0xa5,sizeof direct);
    int count=LoadStringA(module,1,direct,Capacity);
    CHECK(count>0 && count<Capacity); if(count<=0 || count>=Capacity) { FreeLibrary(module); return 1; }
    CHECK(direct[count]==0);
    std::vector<unsigned char> q,frame; CHECK(makeQuery(request(),q));
    CHECK(queryCurrentDll(bytes(q),module,frame));
    if(failures) { FreeLibrary(module); return 1; }
    char candidate[Capacity]; std::memset(candidate,0x69,sizeof candidate);
    CHECK(copyReply(bytes(frame),request(),candidate));
    if(failures) { FreeLibrary(module); return 1; }
    CHECK(!std::memcmp(direct,candidate,static_cast<size_t>(count)+1));
    if(count+1<Capacity) CHECK(candidate[count+1]==0x69);
    std::printf("resource_text=%s resource_bytes=%d compiletime_text=%s\n",direct,count+1,MSS_VERSION);
#ifdef VERSION_POISON_CONTROL
    CHECK(std::strcmp(direct,MSS_VERSION)!=0);
    std::puts("poisoned_compiletime_substitution_rejected=yes");
#endif
    const std::vector<unsigned char> saved=frame;
    CHECK(!queryCurrentDll(bytes(q),0,frame)); CHECK(frame==saved);
    std::vector<unsigned char> invalid=q; invalid[72]=1;
    CHECK(!queryCurrentDll(bytes(invalid),module,frame)); CHECK(frame==saved);
    CHECK(GetModuleHandleA(MSSDLLNAME)==module); // Macro released only its own ref.
    CHECK(FreeLibrary(module)!=0); CHECK(GetModuleHandleA(MSSDLLNAME)==0);
    // Releasing DLL and replacing local buffers must not invalidate wire bytes.
    CHECK(writeFile("resource-direct.bin",direct,static_cast<size_t>(count)+1));
    std::memset(direct,'z',sizeof direct); std::memset(candidate,0x69,sizeof candidate);
    CHECK(copyReply(bytes(frame),request(),candidate));
    if(failures) return 1;
    CHECK(writeFile("version-reply.bin",&frame[0],frame.size()));
    std::printf("owned_after_unload=%s frame_bytes=%u\n",candidate,static_cast<unsigned>(frame.size()));
    std::printf("%u/%u genuine resource checks; no startup/device/playback\n",checks-failures,checks);
    return failures?1:0;
}
