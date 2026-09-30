#include "sharedDebug/FirstSharedDebug.h"
#include "sharedDebug/DebugHelp.h"
#include <intrin.h>
#include <stdint.h>
#include <stdio.h>
#pragma intrinsic(_ReturnAddress)
static uint64 observed[3];
static volatile int barrier=0;
__declspec(noinline) static void leaf(int tail) {
 observed[0]=static_cast<uint64>(reinterpret_cast<uintptr_t>(_ReturnAddress()));
 uint64 frames[16];DebugHelp::getCallStack(frames,16);
 printf("CASE tail=%d\n",tail);
 for(int i=0;i<3;++i)printf("return[%d]=%016I64x\n",i,observed[i]);
 for(int i=0;i<16;++i)printf("frame[%d]=%016I64x\n",i,frames[i]);
 for(int j=0;j<3;++j){int found=-1;for(int i=0;i<16;++i)if(frames[i]==observed[j]){found=i;break;}printf("match[%d]=%d\n",j,found);}
 ++barrier;
}
__declspec(noinline) static void retainedMiddle(){observed[1]=static_cast<uint64>(reinterpret_cast<uintptr_t>(_ReturnAddress()));leaf(0);++barrier;}
__declspec(noinline) static void tailMiddle(){observed[1]=static_cast<uint64>(reinterpret_cast<uintptr_t>(_ReturnAddress()));leaf(1);}
__declspec(noinline) static void outer(int tail){observed[2]=static_cast<uint64>(reinterpret_cast<uintptr_t>(_ReturnAddress()));if(tail)tailMiddle();else retainedMiddle();++barrier;}
int main(){outer(0);outer(1);return 0;}
