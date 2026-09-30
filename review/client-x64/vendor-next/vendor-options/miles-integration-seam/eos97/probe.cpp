// Original-DLL diagnostic only. No engine or public pipe EOS implementation.
#include <windows.h>
#include <stdint.h>
#include <cstdio>
#include <cstring>
#include "Mss.h"
#if _MSC_VER != 1800 || !defined(_M_IX86)
#error Original diagnostic requires v120 x86
#endif
#define API(X) X(AIL_startup,0) X(AIL_shutdown,0) X(AIL_open_digital_driver,16) X(AIL_close_digital_driver,4) X(AIL_allocate_sample_handle,4) X(AIL_release_sample_handle,4) X(AIL_set_named_sample_file,20) X(AIL_register_EOS_callback,8) X(AIL_set_sample_loop_count,8) X(AIL_start_sample,4) X(AIL_open_stream,12) X(AIL_close_stream,4) X(AIL_register_stream_callback,8) X(AIL_set_stream_loop_count,8) X(AIL_start_stream,4)
#define DECL(n,b) static decltype(&n) p_##n;
API(DECL)
// Events:1 registration begin,2 registration return,3 start begin,4 start return,
// 5 callback entry,6 observer last work,7 hold release,8 cleanup begin,9 cleanup end.
struct Record {volatile LONG ready;LONG sequence;int type,arg,prior;DWORD thread;LONGLONG clock;uintptr_t resource;};
static Record records[256];static volatile LONG used=0,callbacks=0;
static HANDLE entered,releaseHold,done,finished;
static HSAMPLE sample=0;static HSTREAM stream=0;static bool sampleMode=false;
static int mode=0; //0 idle,1 immediate replacement,2 active null
static LONGLONG ticks(){LARGE_INTEGER x;QueryPerformanceCounter(&x);return x.QuadPart;}
static void dump(){const LONG n=InterlockedCompareExchange(&used,0,0);for(LONG i=0;i<n&&i<256;++i){Record &r=records[i];if(InterlockedCompareExchange(&r.ready,0,0))std::printf("R %ld %d %d %d %lu %I64d %Iu\n",r.sequence,r.type,r.arg,r.prior,r.thread,r.clock,r.resource);}std::fflush(stdout);}
static void stop(unsigned code){dump();TerminateProcess(GetCurrentProcess(),code);}
static void record(int type,int arg=0,int prior=0,uintptr_t resource=0){LONG i=InterlockedIncrement(&used)-1;if(i>=256){stop(90);return;}Record &r=records[i];r.sequence=i+1;r.type=type;r.arg=arg;r.prior=prior;r.thread=GetCurrentThreadId();r.clock=ticks();r.resource=resource;InterlockedExchange(&r.ready,1);}
static void observed(int which,uintptr_t resource){InterlockedIncrement(&callbacks);record(5,which,0,resource);SetEvent(entered);if(mode==2&&which==1&&WaitForSingleObject(releaseHold,2000)!=WAIT_OBJECT_0){stop(91);return;}record(6,which,0,resource);SetEvent(done);}
static void AILCALLBACK sampleA(HSAMPLE h){observed(1,reinterpret_cast<uintptr_t>(h));}
static void AILCALLBACK sampleB(HSAMPLE h){observed(2,reinterpret_cast<uintptr_t>(h));}
static void AILCALLBACK streamA(HSTREAM h){observed(1,reinterpret_cast<uintptr_t>(h));}
static void AILCALLBACK streamB(HSTREAM h){observed(2,reinterpret_cast<uintptr_t>(h));}
static void registration(int which){record(1,which);int old=3;if(sampleMode){AILSAMPLECB cb=which==1?sampleA:which==2?sampleB:0;AILSAMPLECB prior=p_AIL_register_EOS_callback(sample,cb);old=!prior?0:prior==sampleA?1:prior==sampleB?2:3;}else{AILSTREAMCB cb=which==1?streamA:which==2?streamB:0;AILSTREAMCB prior=p_AIL_register_stream_callback(stream,cb);old=!prior?0:prior==streamA?1:prior==streamB?2:3;}record(2,which,old);}
static DWORD WINAPI watchdog(void*){if(WaitForSingleObject(finished,15000)!=WAIT_OBJECT_0)stop(92);return 0;}
static DWORD WINAPI remover(void*){if(WaitForSingleObject(entered,5000)!=WAIT_OBJECT_0){stop(93);return 0;}registration(0);return 0;}
static DWORD WINAPI releaser(void*){if(WaitForSingleObject(entered,5000)!=WAIT_OBJECT_0){stop(94);return 0;}Sleep(100);record(7);SetEvent(releaseHold);return 0;}
int main(int argc,char **argv){
 if(argc!=5)return 2;sampleMode=std::strcmp(argv[3],"sample")==0;
 if(!sampleMode&&std::strcmp(argv[3],"stream"))return 2;
 mode=!std::strcmp(argv[4],"idle")?0:!std::strcmp(argv[4],"replace")?1:!std::strcmp(argv[4],"active_null")?2:-1;if(mode<0)return 2;
 entered=CreateEventA(0,TRUE,FALSE,0);releaseHold=CreateEventA(0,TRUE,FALSE,0);done=CreateEventA(0,TRUE,FALSE,0);finished=CreateEventA(0,TRUE,FALSE,0);
 if(!entered||!releaseHold||!done||!finished)return 3;
 HANDLE watch=CreateThread(0,0,watchdog,0,0,0);if(!watch)return 3;
 LARGE_INTEGER frequency;QueryPerformanceFrequency(&frequency);std::printf("META type=%s mode=%s freq=%I64d hold=100 watchdog=15000\n",argv[3],argv[4],frequency.QuadPart);std::fflush(stdout);
 HMODULE dll=LoadLibraryA(argv[1]);if(!dll){stop(4);return 4;}
#define BIND(n,b) p_##n=reinterpret_cast<decltype(&n)>(GetProcAddress(dll,"_" #n "@" #b));if(!p_##n){stop(5);return 5;}
 API(BIND)
 static unsigned char data[1048576];FILE *file=0;if(fopen_s(&file,argv[2],"rb")||!file){stop(6);return 6;}
 const size_t count=std::fread(data,1,sizeof data,file);const bool extra=std::fgetc(file)!=EOF;std::fclose(file);if(!count||extra){stop(6);return 6;}
 if(!p_AIL_startup()){stop(7);return 7;}HDIGDRIVER driver=p_AIL_open_digital_driver(22050,16,MSS_MC_STEREO,0);if(!driver){stop(8);return 8;}
 if(sampleMode){sample=p_AIL_allocate_sample_handle(driver);if(!sample||!p_AIL_set_named_sample_file(sample,".wav",data,static_cast<S32>(count),0)){stop(9);return 9;}p_AIL_set_sample_loop_count(sample,1);}else{stream=p_AIL_open_stream(driver,argv[2],0);if(!stream){stop(9);return 9;}p_AIL_set_stream_loop_count(stream,1);}
 std::printf("RESOURCE %Iu\n",sampleMode?reinterpret_cast<uintptr_t>(sample):reinterpret_cast<uintptr_t>(stream));std::fflush(stdout);
 if(mode==0){registration(0);registration(1);registration(2);registration(0);registration(0);registration(2);}else registration(1);
 HANDLE removeThread=0,releaseThread=0;
 if(mode==2){removeThread=CreateThread(0,0,remover,0,0,0);releaseThread=CreateThread(0,0,releaser,0,0,0);if(!removeThread||!releaseThread){stop(10);return 10;}}
 record(3);if(sampleMode)p_AIL_start_sample(sample);else p_AIL_start_stream(stream);record(4);
 if(mode==1)registration(2);
 if(WaitForSingleObject(done,5000)!=WAIT_OBJECT_0){stop(11);return 11;}
 if(mode==2){if(WaitForSingleObject(removeThread,2000)!=WAIT_OBJECT_0||WaitForSingleObject(releaseThread,2000)!=WAIT_OBJECT_0){stop(12);return 12;}CloseHandle(removeThread);CloseHandle(releaseThread);}
 else registration(0);
 // Observer-last-work is not vendor-stack unwind or producer termination.
 record(8);if(sampleMode)p_AIL_release_sample_handle(sample);else p_AIL_close_stream(stream);
 p_AIL_close_digital_driver(driver);p_AIL_shutdown();FreeLibrary(dll);record(9);
 dump();std::printf("SUMMARY callbacks=%ld\n",InterlockedCompareExchange(&callbacks,0,0));std::fflush(stdout);
 SetEvent(finished);WaitForSingleObject(watch,2000);CloseHandle(watch);
 // Events and bounded records remain process-owned until exit; no callback-state free.
 return 0;
}
