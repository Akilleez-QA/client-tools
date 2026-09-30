#include "../startup-metadata-v4/metadata.h"
#include <cstdio>
#include <cstring>
static unsigned checks,failures;
static void check(bool value,int line){++checks;if(!value){++failures;printf("FAIL line %d\n",line);}}
#define CHECK(x) check(!!(x),__LINE__)
int main(){
 using namespace MilesStartup;
 SessionInputs owner;CHECK(owner.retainedBytes()==0);
 char first[]="one",second[]="two";
 const char* a=owner.retain(MilesTransport::Bytes(first,sizeof first));CHECK(a!=0);
 const char* b=owner.retain(MilesTransport::Bytes(second,sizeof second));CHECK(b!=0);
 first[0]='X';second[0]='Y';
 CHECK(a&&!std::strcmp(a,"one"));CHECK(b&&!std::strcmp(b,"two"));
 std::vector<unsigned char> large(RequestTextLimit,'L');large.back()=0;
 const char* c=owner.retain(MilesTransport::Bytes(&large[0],large.size()));CHECK(c!=0);
 const size_t remaining=MilesWire::MaxFrameBytes-owner.retainedBytes();
 CHECK(remaining>0&&remaining<=RequestTextLimit);
 std::vector<unsigned char> tail(remaining,'T');tail.back()=0;
 const char* d=owner.retain(MilesTransport::Bytes(&tail[0],tail.size()));CHECK(d!=0);
 CHECK(owner.retainedBytes()==MilesWire::MaxFrameBytes);
 CHECK(a&&!std::strcmp(a,"one")&&b&&!std::strcmp(b,"two"));
 CHECK(c&&!std::memcmp(c,&large[0],large.size())&&d&&!std::memcmp(d,&tail[0],tail.size()));
 const char zero=0;CHECK(owner.retain(MilesTransport::Bytes(&zero,1))==0);
 CHECK(owner.retainedBytes()==MilesWire::MaxFrameBytes);
 CHECK(a&&!std::strcmp(a,"one")&&b&&!std::strcmp(b,"two"));
 CHECK(c&&!std::memcmp(c,&large[0],large.size())&&d&&!std::memcmp(d,&tail[0],tail.size()));
 printf("%u/%u supplemental retention checks\n",checks-failures,checks);
 return failures||checks!=15?1:0;
}
