#include <windows.h>
#include <xmmintrin.h>
#include <cstdio>
#include <cstring>
#include "Mss.h"
struct Event { long seq; __int64 qpc; DWORD tid; const char *op; long status,total,pos,flag; unsigned short cw,sw; unsigned mxcsr; };
static Event events[4096]; static long count=0,done=0,statusCache=-1,totalCache=-1,posCache=-1;
static CRITICAL_SECTION gate; static LARGE_INTEGER origin,freq; static unsigned char data[65536];
static __int64 now(){LARGE_INTEGER t;QueryPerformanceCounter(&t);return t.QuadPart;}
// No Miles call while gate is held. Every shared observation is protected by gate.
static long record(const char *op,int update=0,long status=-1,long total=-1,long pos=-1){
 unsigned short cw,sw;__asm fnstcw cw
 __asm fnstsw sw
 unsigned mx=_mm_getcsr();DWORD tid=GetCurrentThreadId();EnterCriticalSection(&gate);
 if(update==1)statusCache=status;if(update==2){totalCache=total;posCache=pos;}if(update==3)++done;
 long n=count++;if(n<4096){Event &e=events[n];e.seq=n;e.qpc=now()-origin.QuadPart;e.tid=tid;e.op=op;e.status=statusCache;e.total=totalCache;e.pos=posCache;e.flag=done;e.cw=cw;e.sw=sw;e.mxcsr=mx;}
 long flag=done;LeaveCriticalSection(&gate);return flag;
}
static void AILCALLBACK sampleEOS(HSAMPLE){record("eos",3);}
static void AILCALLBACK streamEOS(HSTREAM){record("eos",3);}
#define BIND(f,n) decltype(&f) p_##f=reinterpret_cast<decltype(&f)>(GetProcAddress(dll,"_" #f "@" #n));if(!p_##f){printf("missing=%s\n",#f);FreeLibrary(dll);return 4;}
int main(int argc,char **argv){
 if(argc!=4||(strcmp(argv[3],"sample")&&strcmp(argv[3],"stream")))return 2;
 bool sample=!strcmp(argv[3],"sample");InitializeCriticalSection(&gate);QueryPerformanceFrequency(&freq);QueryPerformanceCounter(&origin);record("entry");
 FILE *f=fopen(argv[2],"rb");if(!f)return 3;fseek(f,0,SEEK_END);long size=ftell(f);rewind(f);if(size<=0||size>sizeof(data)){fclose(f);return 3;}size_t got=fread(data,1,size,f);fclose(f);if(got!=(size_t)size)return 3;
 HMODULE dll=LoadLibraryA(argv[1]);if(!dll)return 4;char loaded[MAX_PATH]={0};GetModuleFileNameA(dll,loaded,sizeof(loaded));
 BIND(AIL_startup,0);BIND(AIL_shutdown,0);BIND(AIL_open_digital_driver,16);BIND(AIL_close_digital_driver,4);BIND(AIL_allocate_sample_handle,4);BIND(AIL_release_sample_handle,4);BIND(AIL_set_named_sample_file,20);BIND(AIL_register_EOS_callback,8);BIND(AIL_set_sample_loop_count,8);BIND(AIL_start_sample,4);BIND(AIL_sample_status,4);BIND(AIL_sample_ms_position,12);BIND(AIL_open_stream,12);BIND(AIL_close_stream,4);BIND(AIL_register_stream_callback,8);BIND(AIL_set_stream_loop_count,8);BIND(AIL_start_stream,4);BIND(AIL_stream_status,4);BIND(AIL_stream_ms_position,12);BIND(AIL_serve,0);
 int rc=0;HSAMPLE s=0;HSTREAM st=0;HDIGDRIVER driver=0;bool started=p_AIL_startup()!=0;
 if(!started)rc=5;
 if(!rc){driver=p_AIL_open_digital_driver(22050,16,MSS_MC_STEREO,0);if(!driver)rc=6;}
 if(!rc&&sample){s=p_AIL_allocate_sample_handle(driver);if(!s)rc=7;else if(!p_AIL_set_named_sample_file(s,".wav",data,size,0))rc=8;else {p_AIL_register_EOS_callback(s,sampleEOS);p_AIL_set_sample_loop_count(s,1);}}
 if(!rc&&!sample){st=p_AIL_open_stream(driver,argv[2],0);if(!st)rc=9;else {p_AIL_register_stream_callback(st,streamEOS);p_AIL_set_stream_loop_count(st,1);}}
 if(!rc){record("start-enter");if(sample)p_AIL_start_sample(s);else p_AIL_start_stream(st);record("start-return");
 __int64 begin=now(),last=begin,hold=0;bool sawDone=false;
 for(;;){__int64 t=now();if(hold&&t-hold>=freq.QuadPart/2)break;if(!hold&&t-begin>=freq.QuadPart*3){rc=10;break;}
 if(t-last<(freq.QuadPart+19)/20){Sleep(1);continue;}last=t;
 record("serve-enter");p_AIL_serve();record("status-enter");long status=sample?(long)p_AIL_sample_status(s):p_AIL_stream_status(st);record("status-return",1,status);
 S32 total=-1,pos=-1;if(sample)p_AIL_sample_ms_position(s,&total,&pos);else p_AIL_stream_ms_position(st,&total,&pos);
 long flag=record("position-return",2,-1,total,pos);if(status==SMP_DONE)sawDone=true;if(flag&&!hold){hold=now();record("hold-start");}
 }
 if(!sawDone&&!rc)rc=11;
 }
 record("release-enter");if(s)p_AIL_release_sample_handle(s);if(st)p_AIL_close_stream(st);record("release-return");if(driver)p_AIL_close_digital_driver(driver);if(started)p_AIL_shutdown();record("shutdown-return");FreeLibrary(dll);
 printf("mode=%s main=%lu frequency=%I64d loaded=%s bytes=%ld SMP_DONE=%d\n",argv[3],events[0].tid,freq.QuadPart,loaded,size,SMP_DONE);
 for(long i=0;i<count&&i<4096;++i){Event &e=events[i];printf("seq=%ld qpc=%I64d tid=%lu op=%s status=%ld total=%ld pos=%ld flag=%ld cw=%04x sw=%04x mxcsr=%08x\n",e.seq,e.qpc,e.tid,e.op,e.status,e.total,e.pos,e.flag,e.cw,e.sw,e.mxcsr);}
 printf("summary events=%ld overflow=%d eos=%ld rc=%d\n",count,count>4096,done,rc);DeleteCriticalSection(&gate);return rc?rc:(count>4096||done!=1)?12:0;
}
