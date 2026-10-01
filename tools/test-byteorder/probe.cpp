#if !defined(_MSC_VER) || _MSC_VER < 1800
#error This test requires MSVC 2013 or newer
#endif
#include <stdio.h>
#include "sharedFoundation/FirstSharedFoundation.h"
#include "sharedFoundation/ByteOrder.h"
static_assert(sizeof(ulong)==4, "32-bit long contract");
static_assert(sizeof(ushort)==2, "16-bit short contract");
static unsigned long checks=0;
static bool checkLong(ulong x)
{
    // Independent byte oracle, not the intrinsic or a round-trip-only test.
    unsigned char const *bytes=reinterpret_cast<unsigned char const *>(&x);
    ulong expected=0;
    for(int i=0;i<4;++i) expected=expected*256+bytes[i];
    ++checks;
    if(htonl(x)!=expected || ntohl(x)!=expected) { printf("FAIL long %08lx\n",x);return false; }
    return true;
}
int main()
{
    for(unsigned int n=0;n<65536;++n) {
        ushort x=static_cast<ushort>(n);
        ushort expected=static_cast<ushort>((n%256)*256+n/256);
        ++checks;
        if(htons(x)!=expected || ntohs(x)!=expected) { puts("FAIL short");return 1; }
    }
    ulong const edges[]={0,0xffffffffUL,0x80000000UL,0x7fffffffUL,0xaaaaaaaaUL,0x55555555UL,0x01020304UL};
    for(unsigned int i=0;i<sizeof(edges)/sizeof(edges[0]);++i) if(!checkLong(edges[i])) return 1;
    for(unsigned int i=0;i<32;++i) if(!checkLong(1UL<<i)||!checkLong(~(1UL<<i)))return 1;
    for(unsigned int pos=0;pos<4;++pos) for(ulong b=0;b<256;++b) if(!checkLong(b<<(pos*8)))return 1;
    ulong x=0x12345678UL;
    for(unsigned int i=0;i<100000;++i){x=x*1664525UL+1013904223UL;if(!checkLong(x))return 1;}
    printf("PASS %lu input cases (both directions)\n",checks);
    return checks==166631UL?0:2;
}
