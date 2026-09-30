#include "../host-candidate/retained_buffers.h"
#include <new>
#include <cstdlib>
#include <cstdio>
#include <vector>
static bool observing=false;
static unsigned payloadAllocations=0;
void* operator new(size_t n) { if(observing && n==9020)++payloadAllocations;void* p=std::malloc(n?n:1);if(!p)throw std::bad_alloc();return p; }
void operator delete(void* p) { std::free(p); }
int main() {
 std::vector<unsigned char> input(9020,11);MilesHost::RetainedBuffers retained(32768,1);
 MilesHost::RetainedBuffers::Token token=77;observing=true;
 bool ok=retained.stage(MilesHost::RetainedBuffers::Binary,&input[0],input.size(),0,input.size(),token);observing=false;
 MilesHost::RetainedBuffers::View view={};
 bool viewed=retained.view(token,view);
 bool pass=ok && payloadAllocations==1 && retained.bytes()==9020 && viewed && view.size==9020 && view.data[9019]==11;
 printf("%s ordinary payload-sized allocations=%u; live logical staged bytes=%u; RSS/capacity not measured\n",pass?"PASS":"FAIL",payloadAllocations,view.size);
 return pass?0:1;
}
