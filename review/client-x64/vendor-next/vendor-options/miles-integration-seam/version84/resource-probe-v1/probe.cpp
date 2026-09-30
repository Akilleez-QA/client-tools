#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <cstdio>
#include <cstring>
#if _MSC_VER != 1800 || !defined(_M_IX86)
#error Selected probe requires actual v120 x86
#endif
static void dump(const char *label,const unsigned char *p,unsigned n) {
    std::printf("%s=",label);
    for(unsigned i=0;i<n;++i)std::printf("%02X",static_cast<unsigned>(p[i]));
    std::printf("\n");
}
int main() {
    HMODULE self=GetModuleHandleA(0);
    if(!self)return 2;
    CPINFO info={};const UINT acp=GetACP();
    const BOOL cpOk=GetCPInfo(acp,&info);
    std::printf("ACP=%u CPINFO_OK=%d MAX_CHAR_SIZE=%u THREAD_LOCALE=%lu\n",
        acp,static_cast<int>(cpOk),info.MaxCharSize,GetThreadLocale());
    const UINT ids[]={1,2,3,33};
    const char *names[]={"nonempty","explicit_empty","missing_same_bundle","missing_bundle"};
    const int capacities[]={1,2,4,6,7,11};
    unsigned cases=0;bool safe=true;
    for(unsigned row=0;row<4;++row)for(unsigned col=0;col<6;++col) {
        unsigned char memory[32];unsigned char before[32];
        std::memset(memory,0xA5,sizeof memory);
        const int capacity=capacities[col];
        std::memset(memory,0xC3,8);
        std::memset(memory+8+capacity,0xD7,sizeof memory-8-static_cast<unsigned>(capacity));
        std::memcpy(before,memory,sizeof memory);
        std::printf("CASE=%u KIND=%s ID=%u CAPACITY=%d OFFSET=8\n",++cases,names[row],ids[row],capacity);
        dump("BEFORE",before,sizeof before);
        SetLastError(0x12345678);
        const int count=LoadStringA(self,ids[row],reinterpret_cast<char *>(memory+8),capacity);
        const DWORD error=GetLastError();
        dump("AFTER",memory,sizeof memory);
        const bool guards=std::memcmp(memory,before,8)==0 &&
            std::memcmp(memory+8+capacity,before+8+capacity,sizeof memory-8-static_cast<unsigned>(capacity))==0;
        std::printf("COUNT=%d LAST_ERROR=%lu GUARDS=%d\n",count,error,guards?1:0);
        safe=safe&&guards;
    }
    std::printf("CASES=%u GUARDS_ALL=%d\n",cases,safe?1:0);
    return safe?0:3;
}
