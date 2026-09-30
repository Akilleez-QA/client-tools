#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <xmmintrin.h>
#include "Mss.h"
#if _MSC_VER != 1800 || !defined(_M_IX86)
#error This observation requires native v120 Win32
#endif
static void state(const char *phase) {
 unsigned short cw=0,sw=0;
 __asm fnstcw cw
 __asm fnstsw sw
 printf("STATE phase=%s tid=%lu cw=%04x sw=%04x mx=%08x\n",phase,GetCurrentThreadId(),cw,sw,_mm_getcsr());fflush(stdout);
}
int main(int argc,char **argv) {
 if(argc!=3 || (strcmp(argv[2],"inherited") && strcmp(argv[2],"pc24") && strcmp(argv[2],"pc64")))return 2;
 unsigned short original=0;
 __asm fnstcw original
 state("entry");
 unsigned short selected=original;
 if(!strcmp(argv[2],"pc24"))selected=static_cast<unsigned short>(original & ~0x0300u);
 if(!strcmp(argv[2],"pc64"))selected=static_cast<unsigned short>(original | 0x0300u);
 __asm fldcw selected
 state("before_load");
 HMODULE dll=LoadLibraryA(argv[1]);
 if(!dll)return 3;
 state("after_load");
 char path[MAX_PATH]={0};DWORD pathlen=GetModuleFileNameA(dll,path,MAX_PATH);
 if(!pathlen || pathlen>=MAX_PATH){FreeLibrary(dll);return 4;}
 printf("DLL path=%s mode=%s\n",path,argv[2]);
 auto startup=reinterpret_cast<decltype(&AIL_startup)>(GetProcAddress(dll,"_AIL_startup@0"));
 auto preference=reinterpret_cast<decltype(&AIL_get_preference)>(GetProcAddress(dll,"_AIL_get_preference@4"));
 auto shutdown=reinterpret_cast<decltype(&AIL_shutdown)>(GetProcAddress(dll,"_AIL_shutdown@0"));
 if(!startup || !preference || !shutdown){FreeLibrary(dll);return 5;}
 S32 initialized=startup();state("after_startup");
 if(!initialized){FreeLibrary(dll);return 6;}
 SINTa lock=preference(AIL_LOCK_PROTECTION),mutex=preference(AIL_MUTEX_PROTECTION);
 state("after_preferences");
 printf("PREFERENCES lock=%ld mutex=%ld header_lock=%d header_mutex=%d\n",static_cast<long>(lock),static_cast<long>(mutex),0,1);fflush(stdout);
 shutdown();state("after_shutdown");
 BOOL unloaded=FreeLibrary(dll);state("after_unload");
 __asm fldcw original
 state("restored");
 printf("SUMMARY initialized=%ld unloaded=%d defaults_match=%d no_driver_opened=1\n",static_cast<long>(initialized),unloaded,(lock==0 && mutex==1)?1:0);
 return unloaded?0:7;
}
