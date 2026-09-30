#include "session_lifecycle.h"
#include <windows.h>
#include <cstdio>
static unsigned checks;
static bool check(bool value,int line) { ++checks;if(!value)std::printf("FAIL %d\n",line);return value; }
#define CHECK(x) if(!check((x),__LINE__))return 1
static DWORD WINAPI foreign(void *p) {
    MilesHost::SessionLifecycle &s=*static_cast<MilesHost::SessionLifecycle *>(p);
    int32_t value=99;
    if(s.startup(value)!=MilesHost::SessionLifecycle::WrongThread || value!=0)return 1;
    MilesWire::Handle h={MilesWire::Driver,88,99};
    if(s.openDriver(44100,16,2,0,h)!=MilesHost::SessionLifecycle::WrongThread || h.kind || h.slot || h.generation)return 2;
    if(s.shutdown(true)!=MilesHost::SessionLifecycle::WrongThread)return 3;
    return 0;
}
int main() {
    typedef MilesHost::SessionLifecycle S;
    CHECK(!GetModuleHandleA("mss32.dll"));
    S s(2);
    MilesWire::Handle out={MilesWire::Driver,88,99}, invalid={MilesWire::Driver,1,1};
    CHECK(s.openDriver(44100,16,2,0,out)==S::NotStarted);
    CHECK(!out.kind && !out.slot && !out.generation);
    out=invalid;
    CHECK(s.allocateSample(invalid,out)==S::NotStarted);
    CHECK(!out.kind && !out.slot && !out.generation);
    CHECK(s.releaseSample(invalid,false)==S::NotStarted);
    CHECK(s.shutdown(false)==S::NotStarted);
    CHECK(s.shutdown(true)==S::NotStarted);
    void *ptr=reinterpret_cast<void *>(1);
    CHECK(!s.resources().resolve(invalid,MilesWire::Driver,ptr) && !ptr);
    HANDLE thread=CreateThread(0,0,foreign,&s,0,0);
    CHECK(thread!=0);
    CHECK(WaitForSingleObject(thread,10000)==WAIT_OBJECT_0);
    DWORD exitCode=99;CHECK(GetExitCodeThread(thread,&exitCode)!=0 && exitCode==0);
    CHECK(CloseHandle(thread)!=0);
    CHECK(!GetModuleHandleA("mss32.dll"));
    std::printf("PASS %u lifecycle preflight checks; original vendor DLL not loaded\n",checks);
    return 0;
}
