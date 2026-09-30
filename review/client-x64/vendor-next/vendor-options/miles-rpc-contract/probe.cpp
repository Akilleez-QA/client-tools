#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#if _MSC_VER != 1800
#error v120 required
#endif
struct Request {uint32_t version,id,op,slot,generation,reserved;};
struct Reply {uint32_t version,id,kind,result,slot,generation,eventSequence;int32_t status,total,position;};
static_assert(sizeof(Request)==24,"request layout");static_assert(sizeof(Reply)==40,"reply layout");
enum {CREATE=1,START,SERVE,STATUS,POSITION,STOP,RELEASE,QUIT};
static int64_t tick(){LARGE_INTEGER t;QueryPerformanceCounter(&t);return t.QuadPart;}
static bool transfer(HANDLE h,void *p,DWORD length,bool write){unsigned char *b=(unsigned char*)p;while(length){DWORD n=0;BOOL ok=write?WriteFile(h,b,length,&n,0):ReadFile(h,b,length,&n,0);if(!ok||!n)return false;length-=n;b+=n;}return true;}
static void printReply(const Reply &r,int64_t begin){printf("reply id=%u kind=%u result=%u slot=%u gen=%u event=%u status=%d total=%d pos=%d begin=%I64d end=%I64d tid=%lu\n",r.id,r.kind,r.result,r.slot,r.generation,r.eventSequence,r.status,r.total,r.position,begin,tick(),GetCurrentThreadId());fflush(stdout);}
#ifdef HOST
#include <xmmintrin.h>
#include "Mss.h"
#define APIs(X) X(AIL_startup,0) X(AIL_shutdown,0) X(AIL_open_digital_driver,16) X(AIL_close_digital_driver,4) X(AIL_allocate_sample_handle,4) X(AIL_release_sample_handle,4) X(AIL_set_named_sample_file,20) X(AIL_register_EOS_callback,8) X(AIL_set_sample_loop_count,8) X(AIL_start_sample,4) X(AIL_stop_sample,4) X(AIL_sample_status,4) X(AIL_sample_ms_position,12) X(AIL_open_stream,12) X(AIL_close_stream,4) X(AIL_register_stream_callback,8) X(AIL_set_stream_loop_count,8) X(AIL_start_stream,4) X(AIL_pause_stream,8) X(AIL_stream_status,4) X(AIL_stream_ms_position,12) X(AIL_serve,0)
#define DECL(f,n) static decltype(&f) p_##f;
APIs(DECL)
struct Event {uint32_t sequence,id,op,thread,eos;int64_t time;unsigned short cw,sw;unsigned mx;};
static Event events[4096];static uint32_t eventCount,eosCount,eosSequence,activeId,activeOp;static CRITICAL_SECTION gate;
static void record(bool eos=false){unsigned short cw,sw;__asm fnstcw cw
__asm fnstsw sw
unsigned mx=_mm_getcsr();EnterCriticalSection(&gate);uint32_t index=eventCount++;if(eos){++eosCount;eosSequence=index;}if(index<4096){Event &e=events[index];e.sequence=index;e.id=activeId;e.op=activeOp;e.thread=GetCurrentThreadId();e.eos=eos;e.time=tick();e.cw=cw;e.sw=sw;e.mx=mx;}LeaveCriticalSection(&gate);}
static void AILCALLBACK sampleEOS(HSAMPLE){record(true);}static void AILCALLBACK streamEOS(HSTREAM){record(true);}
static HSAMPLE sample;static HSTREAM stream;static HDIGDRIVER driver;static unsigned char data[65536];static long bytes;static bool sampleMode;static uint32_t generation=1;static const char *asset;
static Reply dispatch(const Request &r){Reply a={1,r.id,0,0,1,generation,0,-1,-1,-1};EnterCriticalSection(&gate);activeId=r.id;activeOp=r.op;LeaveCriticalSection(&gate);record();
 if(r.version!=1||r.reserved||r.op<CREATE||r.op>QUIT){a.result=2;return a;}
 if(r.op!=CREATE&&r.op!=QUIT&&(r.slot!=1||r.generation!=generation||(!sample&&!stream))){a.result=1;record();return a;}
 switch(r.op){
 case CREATE:if(sample||stream){a.result=2;break;}if(sampleMode){sample=p_AIL_allocate_sample_handle(driver);if(!sample||!p_AIL_set_named_sample_file(sample,".wav",data,bytes,0)){a.result=3;break;}p_AIL_register_EOS_callback(sample,sampleEOS);p_AIL_set_sample_loop_count(sample,1);}else{stream=p_AIL_open_stream(driver,asset,0);if(!stream){a.result=3;break;}p_AIL_register_stream_callback(stream,streamEOS);p_AIL_set_stream_loop_count(stream,1);}break;
 case START:if(sample)p_AIL_start_sample(sample);else p_AIL_start_stream(stream);break;
 case SERVE:p_AIL_serve();break;
 case STATUS:a.status=sample?(int32_t)p_AIL_sample_status(sample):p_AIL_stream_status(stream);break;
 case POSITION:{S32 total=-1,position=-1;if(sample)p_AIL_sample_ms_position(sample,&total,&position);else p_AIL_stream_ms_position(stream,&total,&position);a.total=total;a.position=position;break;}
 case STOP:if(sample)p_AIL_stop_sample(sample);else p_AIL_pause_stream(stream,1);break;
 case RELEASE:if(sample)p_AIL_release_sample_handle(sample);if(stream)p_AIL_close_stream(stream);sample=0;stream=0;++generation;a.generation=generation;break;
 case QUIT:break;
 }record();return a;}
static bool send(HANDLE pipe,const Reply &reply,bool direct,int64_t begin){if(direct){printReply(reply,begin);return true;}Reply r=reply;return transfer(pipe,&r,sizeof(r),true);}
static bool execute(const Request &r,bool direct){int64_t begin=tick();Reply reply=dispatch(r);static uint32_t sent=0;EnterCriticalSection(&gate);uint32_t pending=eosCount,seq=eosSequence;LeaveCriticalSection(&gate);if(pending>sent){Reply e={1,r.id,1,0,1,1,seq,-1,-1,-1};if(!send(GetStdHandle(STD_OUTPUT_HANDLE),e,direct,begin))return false;sent=pending;}return send(GetStdHandle(STD_OUTPUT_HANDLE),reply,direct,begin);}
int main(int argc,char **argv){if(argc!=5)return 2;sampleMode=!strcmp(argv[3],"sample");bool direct=!strcmp(argv[4],"direct");asset=argv[2];InitializeCriticalSection(&gate);FILE *f=fopen(asset,"rb");if(!f)return 3;fseek(f,0,SEEK_END);bytes=ftell(f);rewind(f);if(bytes<=0||bytes>sizeof(data)||fread(data,1,bytes,f)!=(size_t)bytes)return 3;fclose(f);HMODULE dll=LoadLibraryA(argv[1]);if(!dll)return 4;
#define BIND(f,n) p_##f=reinterpret_cast<decltype(&f)>(GetProcAddress(dll,"_" #f "@" #n));if(!p_##f)return 5;
APIs(BIND)
 char loaded[MAX_PATH]={0};GetModuleFileNameA(dll,loaded,MAX_PATH);LARGE_INTEGER freq;QueryPerformanceFrequency(&freq);fprintf(stderr,"host main=%lu frequency=%I64d loaded=%s mode=%s\n",GetCurrentThreadId(),freq.QuadPart,loaded,argv[3]);if(!p_AIL_startup())return 6;driver=p_AIL_open_digital_driver(22050,16,MSS_MC_STEREO,0);if(!driver)return 7;
 uint32_t expected=1;bool ok=true;if(direct){Request r={1,1,CREATE,1,1,0};ok=execute(r,true);r.id++;r.op=START;ok=ok&&execute(r,true);for(int i=0;i<20&&ok;++i){Sleep(50);for(uint32_t op=SERVE;op<=POSITION;++op){r.id++;r.op=op;ok=execute(r,true);}}uint32_t tail[]={STOP,RELEASE,STATUS,QUIT};for(int i=0;i<4&&ok;++i){r.id++;r.op=tail[i];ok=execute(r,true);}}else{for(unsigned n=0;n<128;++n){Request r;if(!transfer(GetStdHandle(STD_INPUT_HANDLE),&r,sizeof(r),false)){ok=false;break;}if(r.id!=expected++){ok=false;break;}if(!execute(r,false)){ok=false;break;}if(r.op==QUIT)break;}}
 if(sample)p_AIL_release_sample_handle(sample);if(stream)p_AIL_close_stream(stream);p_AIL_close_digital_driver(driver);p_AIL_shutdown();FreeLibrary(dll);
 for(uint32_t i=0;i<eventCount&&i<4096;++i){Event &e=events[i];fprintf(stderr,"event seq=%u id=%u op=%u tid=%u eos=%u qpc=%I64d cw=%04x sw=%04x mx=%08x\n",e.sequence,e.id,e.op,e.thread,e.eos,e.time,e.cw,e.sw,e.mx);}fprintf(stderr,"summary events=%u eos=%u ok=%d generation=%u\n",eventCount,eosCount,ok,generation);DeleteCriticalSection(&gate);return ok&&eventCount<4096&&eosCount==1&&generation==2?0:8;}
#else
int main(int argc,char **argv){if(argc!=5)return 2;LARGE_INTEGER clockFrequency;QueryPerformanceFrequency(&clockFrequency);printf("controller-frequency=%I64d tid=%lu\n",clockFrequency.QuadPart,GetCurrentThreadId());fflush(stdout);SECURITY_ATTRIBUTES sa={sizeof(sa),0,TRUE};HANDLE reqR,reqW,repR,repW;if(!CreatePipe(&reqR,&reqW,&sa,0)||!CreatePipe(&repR,&repW,&sa,0))return 3;SetHandleInformation(reqW,HANDLE_FLAG_INHERIT,0);SetHandleInformation(repR,HANDLE_FLAG_INHERIT,0);STARTUPINFOA si={sizeof(si)};si.dwFlags=STARTF_USESTDHANDLES;si.hStdInput=reqR;si.hStdOutput=repW;si.hStdError=GetStdHandle(STD_ERROR_HANDLE);PROCESS_INFORMATION pi;char command[2048];sprintf_s(command,"\"%s\" \"%s\" \"%s\" %s controlled",argv[1],argv[2],argv[3],argv[4]);if(!CreateProcessA(0,command,0,0,TRUE,0,0,0,&si,&pi))return 4;CloseHandle(reqR);CloseHandle(repW);bool ok=true;uint32_t id=0,events=0,replies=0;uint32_t ops[66];unsigned count=0;ops[count++]=CREATE;ops[count++]=START;for(int i=0;i<20;++i){ops[count++]=SERVE;ops[count++]=STATUS;ops[count++]=POSITION;}ops[count++]=STOP;ops[count++]=RELEASE;ops[count++]=STATUS;ops[count++]=QUIT;
 for(unsigned i=0;i<count&&ok;++i){if(i>=2&&i<62&&(i-2)%3==0)Sleep(50);Request r={1,++id,ops[i],1,1,0};int64_t begin=tick();if(!transfer(reqW,&r,sizeof(r),true)){ok=false;break;}for(unsigned j=0;j<3;++j){Reply a;if(!transfer(repR,&a,sizeof(a),false)||a.version!=1||a.id!=id){ok=false;break;}printReply(a,begin);if(a.kind==1){++events;continue;}++replies;if(a.kind!=0||a.result!=(i==64?1u:0u)){ok=false;}break;}}
 CloseHandle(reqW);CloseHandle(repR);DWORD wait=WaitForSingleObject(pi.hProcess,5000),code=99;if(wait==WAIT_OBJECT_0)GetExitCodeProcess(pi.hProcess,&code);else TerminateProcess(pi.hProcess,98);CloseHandle(pi.hThread);CloseHandle(pi.hProcess);printf("controller replies=%u events=%u host_exit=%lu ok=%d\n",replies,events,code,ok);return ok&&code==0&&events==1&&replies==66?0:9;}
#endif
