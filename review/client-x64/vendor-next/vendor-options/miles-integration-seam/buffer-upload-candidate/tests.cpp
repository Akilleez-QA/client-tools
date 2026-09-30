#include "buffer_upload.h"
#include "../protocol-candidate/miles_wire.h"
#include <cstdio>
#include <limits>
#include <stdexcept>
static bool check(bool ok,unsigned &count,int line){++count;if(!ok)std::printf("FAIL line%d\n",line);return ok;}
#define CHECK(x) if(!check((x),count,__LINE__))return 1
int main(){
 using MilesHost::BufferUpload;
 unsigned count=0; unsigned char input[7]={1,2,3,4,5,6,7};
 std::vector<unsigned char> out(1,99);
 BufferUpload a(7,7);
 CHECK(!a.copySealed(out) && out.size()==1 && out[0]==99);
 CHECK(!a.seal() && !a.sealed());
 CHECK(!a.append(1,input,1) && a.received()==0);
 CHECK(!a.append(0,0,1) && a.received()==0);
 CHECK(!a.append(0,input,0) && a.received()==0);
 CHECK(!a.append(0,input,8) && a.received()==0);
 CHECK(!a.append(0,input,(std::numeric_limits<size_t>::max)()) && a.received()==0);
 CHECK(a.append(0,input,3) && a.received()==3);
 CHECK(!a.append(0,input,3) && a.received()==3);
 CHECK(!a.append(2,input,1) && a.received()==3);
 CHECK(!a.append(4,input,1) && a.received()==3);
 CHECK(!a.seal() && !a.sealed());
 CHECK(a.append(3,input+3,4) && a.received()==7);
 input[0]=42;
 CHECK(a.seal() && a.sealed());
 CHECK(a.seal());
 CHECK(!a.append(7,input,1));
 CHECK(!a.append(0,input,7));
 CHECK(a.copySealed(out) && out.size()==7 && out[0]==1 && out[6]==7);
 out[0]=88;
 CHECK(a.copySealed(out) && out[0]==1);
 bool rejected=false;try{BufferUpload tooLarge(8,7);}catch(const std::out_of_range &){rejected=true;}
 CHECK(rejected);
 BufferUpload empty(0,0);
 CHECK(empty.seal() && empty.size()==0);
 CHECK(empty.copySealed(out) && out.empty());
 CHECK(!empty.append(0,input,1));
 {
  BufferUpload temporary(7,7);CHECK(temporary.append(0,input,7) && temporary.seal() && temporary.copySealed(out));
 }
 CHECK(out.size()==7 && out[0]==42 && out[6]==7);
 // Asset larger than transport frame: assembly permits multiple bounded chunks.
 const uint32_t total=MilesWire::MaxFrameBytes+17;
 std::vector<unsigned char> big(total);for(size_t i=0;i<big.size();++i)big[i]=static_cast<unsigned char>(i%251);
 BufferUpload large(total,total);
 CHECK(large.append(0,&big[0],MilesWire::MaxFrameBytes-136));
 CHECK(!large.seal());
 const uint32_t prefix=large.received();
 CHECK(large.append(prefix,&big[prefix],big.size()-prefix) && large.seal());
 CHECK(large.copySealed(out) && out==big);
 std::printf("PASS %u upload mechanism checks; no vendor calls\n",count);return 0;
}
