#include "AutoByteStream.h"
#include <cstdio>
#include <cstring>
#include <limits>
#define CHECK(x) do {++checks;if(!(x)){std::printf("FAIL %d\n",__LINE__);return 1;}}while(0)
int main(){unsigned checks=0;for(unsigned count=0;count<=3;++count){Archive::AutoArray<unsigned char> a;Archive::AutoList<unsigned char> l;for(unsigned i=0;i<count;++i){a.get().push_back(static_cast<unsigned char>(0x31+i));l.get().push_back(static_cast<unsigned char>(0x31+i));}unsigned char expected[]={0x7e,0,0,0,0,0x31,0x32,0x33};expected[1]=static_cast<unsigned char>(count);Archive::ByteStream ab,lb;ab.put(expected,1);lb.put(expected,1);a.pack(ab);l.pack(lb);CHECK(ab.getSize()==5+count);CHECK(lb.getSize()==5+count);CHECK(!std::memcmp(ab.getBuffer(),expected,5+count));CHECK(!std::memcmp(lb.getBuffer(),expected,5+count));Archive::ReadIterator ar=ab.begin(),lr=lb.begin();ar.advance(1);lr.advance(1);Archive::AutoArray<unsigned char> aa;Archive::AutoList<unsigned char> ll;aa.unpack(ar);ll.unpack(lr);CHECK(aa.get()==a.get());CHECK(ll.get()==l.get());CHECK(ar.getSize()==0&&lr.getSize()==0);}
CHECK(ArchiveCount::fromSize<unsigned int>((std::numeric_limits<unsigned int>::max)())==(std::numeric_limits<unsigned int>::max)());
if(sizeof(size_t)>4){bool rejected=false;try{ArchiveCount::fromSize<unsigned int>(static_cast<size_t>((std::numeric_limits<unsigned int>::max)())+1);}catch(std::out_of_range const&){rejected=true;}CHECK(rejected);}else std::puts("SKIP helper out-of-range not representable in size_t");
std::printf("checks=%u failures=0\n",checks);return checks==(sizeof(size_t)>4?30u:29u)?0:2;}
