#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#if _MSC_VER != 1800
#error v120 required
#endif
static int64_t tick(){LARGE_INTEGER t;QueryPerformanceCounter(&t);return t.QuadPart;}
struct Packet {uint32_t version,kind,thread,reserved;int64_t at,callbackEnd;};
static_assert(sizeof(Packet)==32,"fixed packet");
static bool transfer(HANDLE h,void *p,DWORD length,bool write){char*b=(char*)p;while(length){DWORD n=0;BOOL ok=write?WriteFile(h,b,length,&n,0):ReadFile(h,b,length,&n,0);if(!ok||!n)return false;length-=n;b+=n;}return true;}
static volatile LONG seen=0,ready=0;static int64_t startAt,frequency,publishedAt;static int phase;
struct Observation {int64_t at;LONG value;};static Observation observations[600];
static DWORD WINAPI observe(void*){while(!InterlockedCompareExchange(&ready,0,0))Sleep(1);for(int i=0;i<600;++i){int64_t target=startAt+(frequency*i)/1000+(frequency*phase)/1000000;while(tick()<target)Sleep(0);observations[i].at=tick();observations[i].value=InterlockedCompareExchange(&seen,0,0);}return 0;}
static void publish(){publishedAt=tick();InterlockedExchange(&seen,1);}
static void dump(){int first=-1;for(int i=0;i<600;++i){if(first<0&&observations[i].value)first=i;printf("observer epoch=%d qpc=%I64d seen=%ld\n",i,observations[i].at,observations[i].value);}printf("observer_summary first=%d published=%I64d start=%I64d frequency=%I64d phase_us=%d\n",first,publishedAt,startAt,frequency,phase);}
#ifdef HOST
#include "Mss.h"
#define APIs(X) X(AIL_startup,0) X(AIL_shutdown,0) X(AIL_open_digital_driver,16) X(AIL_close_digital_driver,4) X(AIL_allocate_sample_handle,4) X(AIL_release_sample_handle,4) X(AIL_set_named_sample_file,20) X(AIL_register_EOS_callback,8) X(AIL_set_sample_loop_count,8) X(AIL_start_sample,4) X(AIL_stop_sample,4) X(AIL_sample_status,4) X(AIL_sample_ms_position,12) X(AIL_open_stream,12) X(AIL_close_stream,4) X(AIL_register_stream_callback,8) X(AIL_set_stream_loop_count,8) X(AIL_start_stream,4) X(AIL_pause_stream,8) X(AIL_stream_status,4) X(AIL_stream_ms_position,12) X(AIL_serve,0)
#define DECL(f,n) static decltype(&f) p_##f;
APIs(DECL)

static Packet completion={1,2,0,0,0,0};static volatile LONG active=0,count=0,completed=0;static int arm;static HANDLE eventReady;static int64_t sentAt;static bool sendOk=true;
static void eos(){InterlockedIncrement(&active);LONG n=InterlockedIncrement(&count);if(n==1){completion.thread=GetCurrentThreadId();completion.at=tick();if(arm==0)publish();completion.callbackEnd=tick();InterlockedExchange(&completed,1);SetEvent(eventReady);}InterlockedDecrement(&active);}
static void AILCALLBACK sampleEOS(HSAMPLE){eos();}static void AILCALLBACK streamEOS(HSTREAM){eos();}
static DWORD WINAPI sender(void*){if(WaitForSingleObject(eventReady,3000)!=WAIT_OBJECT_0){sendOk=false;return 1;}while(InterlockedCompareExchange(&active,0,0))Sleep(0);sentAt=tick();sendOk=transfer(GetStdHandle(STD_OUTPUT_HANDLE),&completion,sizeof(completion),true);return 0;}
int main(int argc,char**argv){if(argc!=6)return 2;arm=atoi(argv[4]);phase=atoi(argv[5]);LARGE_INTEGER f;QueryPerformanceFrequency(&f);frequency=f.QuadPart;bool sampleMode=!strcmp(argv[3],"sample");unsigned char data[65536];FILE*file=fopen(argv[2],"rb");if(!file)return 3;size_t bytes=fread(data,1,sizeof(data),file);fclose(file);if(bytes!=9020)return 3;HMODULE dll=LoadLibraryA(argv[1]);if(!dll)return 4;
#define BIND(f,n) p_##f=reinterpret_cast<decltype(&f)>(GetProcAddress(dll,"_" #f "@" #n));if(!p_##f)return 5;
APIs(BIND)
char loaded[MAX_PATH];GetModuleFileNameA(dll,loaded,MAX_PATH);fprintf(stderr,"host loaded=%s tid=%lu frequency=%I64d arm=%d phase=%d\n",loaded,GetCurrentThreadId(),frequency,arm,phase);if(!p_AIL_startup())return 6;HDIGDRIVER driver=p_AIL_open_digital_driver(22050,16,MSS_MC_STEREO,0);if(!driver)return 7;
HSAMPLE sample=0;HSTREAM stream=0;if(sampleMode){sample=p_AIL_allocate_sample_handle(driver);if(!sample||!p_AIL_set_named_sample_file(sample,".wav",data,(S32)bytes,0))return 8;p_AIL_register_EOS_callback(sample,sampleEOS);p_AIL_set_sample_loop_count(sample,1);}else{stream=p_AIL_open_stream(driver,argv[2],0);if(!stream)return 8;p_AIL_register_stream_callback(stream,streamEOS);p_AIL_set_stream_loop_count(stream,1);}
eventReady=CreateEventA(0,FALSE,FALSE,0);HANDLE worker=CreateThread(0,0,arm==2?sender:observe,0,0,0);startAt=tick()+frequency/50;Packet begin={1,1,GetCurrentThreadId(),0,startAt,frequency};if(arm==2&&!transfer(GetStdHandle(STD_OUTPUT_HANDLE),&begin,sizeof(begin),true))return 9;InterlockedExchange(&ready,1);while(tick()<startAt)Sleep(0);int64_t before=tick();if(sample)p_AIL_start_sample(sample);else p_AIL_start_stream(stream);fprintf(stderr,"start begin=%I64d end=%I64d\n",before,tick());
for(int i=1;i<=13;++i){int64_t target=startAt+frequency*i/20;while(tick()<target)Sleep(1);int64_t b=tick();p_AIL_serve();if(arm==1&&!seen&&InterlockedCompareExchange(&completed,0,0))publish();fprintf(stderr,"serve epoch=%d begin=%I64d end=%I64d\n",i,b,tick());}
S32 total=-1,pos=-1;S32 status=sample?p_AIL_sample_status(sample):p_AIL_stream_status(stream);if(sample)p_AIL_sample_ms_position(sample,&total,&pos);else p_AIL_stream_ms_position(stream,&total,&pos);
DWORD waited=WaitForSingleObject(worker,4000);if(sample){p_AIL_stop_sample(sample);p_AIL_release_sample_handle(sample);}else{p_AIL_pause_stream(stream,1);p_AIL_close_stream(stream);}p_AIL_close_digital_driver(driver);p_AIL_shutdown();FreeLibrary(dll);fprintf(stderr,"completion count=%ld callback=%I64d callback_end=%I64d thread=%u sent=%I64d status=%d total=%d pos=%d worker=%lu send_ok=%d\n",count,completion.at,completion.callbackEnd,completion.thread,sentAt,status,total,pos,waited,sendOk);if(arm!=2)dump();CloseHandle(worker);CloseHandle(eventReady);return count==1&&waited==WAIT_OBJECT_0&&sendOk?0:10;}
#else
int main(int argc,char**argv){if(argc!=6)return 2;phase=atoi(argv[5]);LARGE_INTEGER f;QueryPerformanceFrequency(&f);frequency=f.QuadPart;SECURITY_ATTRIBUTES sa={sizeof(sa),0,TRUE};HANDLE readPipe,writePipe;if(!CreatePipe(&readPipe,&writePipe,&sa,0))return 3;SetHandleInformation(readPipe,HANDLE_FLAG_INHERIT,0);STARTUPINFOA si={sizeof(si)};si.dwFlags=STARTF_USESTDHANDLES;si.hStdInput=GetStdHandle(STD_INPUT_HANDLE);si.hStdOutput=writePipe;si.hStdError=GetStdHandle(STD_ERROR_HANDLE);PROCESS_INFORMATION pi;char cmd[2048];sprintf_s(cmd,"\"%s\" \"%s\" \"%s\" %s 2 %d",argv[1],argv[2],argv[3],argv[4],phase);if(!CreateProcessA(0,cmd,0,0,TRUE,0,0,0,&si,&pi))return 4;CloseHandle(writePipe);Packet begin;if(!transfer(readPipe,&begin,sizeof(begin),false)||begin.kind!=1||begin.callbackEnd!=frequency)return 5;startAt=begin.at;HANDLE observer=CreateThread(0,0,observe,0,0,0);InterlockedExchange(&ready,1);Packet e;if(!transfer(readPipe,&e,sizeof(e),false)||e.kind!=2||e.version!=1)return 6;int64_t received=tick();publish();printf("event callback=%I64d callback_end=%I64d received=%I64d thread=%u receiver_thread=%lu\n",e.at,e.callbackEnd,received,e.thread,GetCurrentThreadId());DWORD ow=WaitForSingleObject(observer,4000);DWORD pw=WaitForSingleObject(pi.hProcess,4000),code=99;if(pw==WAIT_OBJECT_0)GetExitCodeProcess(pi.hProcess,&code);dump();printf("controller host_exit=%lu observer_wait=%lu\n",code,ow);CloseHandle(readPipe);CloseHandle(observer);CloseHandle(pi.hThread);CloseHandle(pi.hProcess);return code==0&&ow==WAIT_OBJECT_0?0:7;}
#endif
