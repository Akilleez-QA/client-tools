#include "ByteStream.h"
#include <climits>
#include <cstdio>
#include <cstring>
#define REQUIRE(x) do { ++checks; if (!(x)) {std::printf("FAIL %d\n",__LINE__); return 1;} } while(0)
int main() {
 unsigned checks=0; unsigned char seed[]={1,2,3,4,5,6,7,8};
 // Alias a strict subsection of initialized bytes, with existing spare capacity.
 Archive::ByteStream a(seed,8); a.setAllocatedSizeLimit(64); a.put(a.getBuffer()+2,4);
 unsigned char expected[]={1,2,3,4,5,6,7,8,3,4,5,6};
 REQUIRE(a.getSize()==12); REQUIRE(!std::memcmp(a.getBuffer(),expected,12));
 // Both old aliases stay valid while shared storage is detached.
 Archive::ByteStream b=a; b.put(a.getBuffer()+8,4); REQUIRE(a.getSize()==12); REQUIRE(b.getSize()==16); REQUIRE(!std::memcmp(b.getBuffer()+12,expected+8,4));
 a.setAllocatedSizeLimit(128); REQUIRE(!std::memcmp(a.getBuffer(),expected,12)); REQUIRE(b.getSize()==16);
 unsigned char untouched=77; Archive::ReadIterator r=a.begin(); r.advance(11); bool caught=false;
 try {r.get(&untouched,ULONG_MAX);} catch(Archive::ReadException const&) {caught=true;}
 REQUIRE(caught); REQUIRE(untouched==77); REQUIRE(r.getReadPosition()==11); REQUIRE(r.getSize()==1);
 r.get(&untouched,1); REQUIRE(untouched==6); REQUIRE(r.getSize()==0);
 // Distinct streams shared only through Data; mutating one does not invalidate the other's reader.
 Archive::ReadIterator br=b.begin(); a.clear(); REQUIRE(br.getSize()==16); br.get(&untouched,1); REQUIRE(untouched==1);
 // Clear a shared stream and reuse retained capacity.
 Archive::ByteStream c=b; c.clear(); c.put(seed,3); REQUIRE(c.getSize()==3); REQUIRE(b.getSize()==16); REQUIRE(!std::memcmp(b.getBuffer(),expected,12));
 std::printf("checks=%u failures=0\n",checks); return checks==18?0:2;
}
