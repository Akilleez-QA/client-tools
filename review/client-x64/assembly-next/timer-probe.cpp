#if _MSC_VER != 1800
#error v120 required
#endif
#include <intrin.h>
#include <stdio.h>
// Runner prepends the actual ProfilerTimer.cpp include, retaining its real headers.
int main()
{
 DWORD_PTR processMask=0, systemMask=0;
 if(!GetProcessAffinityMask(GetCurrentProcess(),&processMask,&systemMask)||!processMask)return 2;
 DWORD_PTR pin=processMask&(~processMask+1);
 DWORD_PTR previous=SetThreadAffinityMask(GetCurrentThread(),pin);if(!previous)return 3;
 unsigned count=0;
 for(unsigned i=0;i<10000;++i){
  _mm_lfence();unsigned __int64 before=__rdtsc();_mm_lfence();
  unsigned __int64 value=static_cast<unsigned __int64>(readTimeStampCounter());
  _mm_lfence();unsigned __int64 after=__rdtsc();_mm_lfence();
  if(value==0 || value<before || value>after){printf("FAIL timestamp sample %u\n",i);return 1;}
  ++count;
 }
 if(!SetThreadAffinityMask(GetCurrentThread(),previous))return 4;
 printf("PASS %u bracketed TSC samples\n",count);return count==10000?0:5;
}
