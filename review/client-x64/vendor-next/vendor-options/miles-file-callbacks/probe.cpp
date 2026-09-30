#include <windows.h>
#include <cstdio>
#include <cstring>
#include "Mss.h"
struct Event { LONG seq; DWORD tick,tid; LONG phase,depth,active; const char *op; UINTa h; long a,b,result; };
static Event events[4096]; static volatile LONG count=0,active=0,phase=0,done=0,errors=0;
static __declspec(thread) LONG depth=0;
static CRITICAL_SECTION lock; static FILE *file=0; static UINTa chosen=0; static const char *path=0;
static long size=0; static DWORD origin;
static void log(const char *op,UINTa h,long a,long b,long result) {
 LONG n=InterlockedIncrement(&count)-1;if(n>=4096)return;
 Event &e=events[n];e.seq=n;e.tick=GetTickCount()-origin;e.tid=GetCurrentThreadId();e.phase=phase;e.depth=depth;e.active=active;e.op=op;e.h=h;e.a=a;e.b=b;e.result=result;
}
struct Scope { const char *op;UINTa h;bool ok; Scope(const char *s,UINTa v):op(s),h(v) {++depth;InterlockedIncrement(&active);ok=depth<=8;log(op,h,0,0,-999);if(!ok)InterlockedIncrement(&errors);} ~Scope(){InterlockedDecrement(&active);--depth;} };
static U32 AILCALLBACK openCb(MSS_FILE const *name,UINTa *h) {
 Scope s("open-enter",0);*h=0;U32 result=0;long kind=!strcmp(name,"owned-reference.wav")?1:!strcmp(name,"missing-reference.wav")?2:3;
 if(s.ok){EnterCriticalSection(&lock);if(kind==1&&!file){file=fopen(path,"rb");if(file){*h=chosen;result=1;}}LeaveCriticalSection(&lock);}
 log("open-exit",*h,kind,0,result);return result;
}
static void AILCALLBACK closeCb(UINTa h) {
 Scope s("close-enter",h);long result=-1;if(s.ok){EnterCriticalSection(&lock);if(file&&h==chosen){result=fclose(file);file=0;}else InterlockedIncrement(&errors);LeaveCriticalSection(&lock);}log("close-exit",h,0,0,result);
}
static S32 AILCALLBACK seekCb(UINTa h,S32 off,U32 type) {
 Scope s("seek-enter",h);long result=-1;if(s.ok){EnterCriticalSection(&lock);if(file&&h==chosen&&type<=2){long base=type==0?0:type==1?ftell(file):size;__int64 pos=(__int64)base+off;if(pos>=0&&pos<=size&&fseek(file,(long)pos,SEEK_SET)==0)result=ftell(file);}if(result<0)InterlockedIncrement(&errors);LeaveCriticalSection(&lock);}log("seek-exit",h,off,type,result);return result;
}
static U32 AILCALLBACK readCb(UINTa h,void *buffer,U32 bytes) {
 Scope s("read-enter",h);U32 result=0;long pos=-1;if(s.ok){EnterCriticalSection(&lock);if(file&&h==chosen){pos=ftell(file);if(pos>=0&&pos<=size){U32 remain=(U32)(size-pos);result=(U32)fread(buffer,1,bytes<remain?bytes:remain,file);}else InterlockedIncrement(&errors);}else InterlockedIncrement(&errors);LeaveCriticalSection(&lock);}log("read-exit",h,bytes,pos,result);return result;
}
static void AILCALLBACK eos(HSTREAM){Scope s("eos-enter",chosen);InterlockedIncrement(&done);log("eos-exit",chosen,0,0,done);}
#define BIND(f,n) decltype(&f) p_##f=reinterpret_cast<decltype(&f)>(GetProcAddress(dll,"_" #f "@" #n));if(!p_##f){printf("missing %s\n",#f);FreeLibrary(dll);return 4;}
int main(int argc,char **argv){
 if(argc!=4||(strcmp(argv[3],"0")&&strcmp(argv[3],"1")))return 2;
 setvbuf(stdout,0,_IONBF,0);origin=GetTickCount();chosen=argv[3][0]-'0';path=argv[2];InitializeCriticalSection(&lock);
 FILE *check=fopen(path,"rb");if(!check)return 3;fseek(check,0,SEEK_END);size=ftell(check);fclose(check);if(size<=0||size>65536)return 3;
 printf("main=%lu handle=%lu file_bytes=%ld names=1:owned-reference.wav,2:missing-reference.wav,3:unexpected\n",GetCurrentThreadId(),(unsigned long)chosen,size);
 HMODULE dll=LoadLibraryA(argv[1]);if(!dll)return 4;
 BIND(AIL_startup,0);BIND(AIL_shutdown,0);BIND(AIL_open_digital_driver,16);BIND(AIL_close_digital_driver,4);BIND(AIL_last_error,0);BIND(AIL_set_file_callbacks,16);BIND(AIL_open_stream,12);BIND(AIL_close_stream,4);BIND(AIL_register_stream_callback,8);BIND(AIL_set_stream_loop_count,8);BIND(AIL_start_stream,4);BIND(AIL_serve,0);
 int rc=0;if(!p_AIL_startup()){FreeLibrary(dll);return 5;}
 HDIGDRIVER driver=p_AIL_open_digital_driver(22050,16,MSS_MC_STEREO,0);
 if(!driver){printf("driver failed: %s\n",p_AIL_last_error());p_AIL_shutdown();FreeLibrary(dll);return 6;}
 p_AIL_set_file_callbacks(openCb,closeCb,seekCb,readCb);
 phase=1;HSTREAM missing=p_AIL_open_stream(driver,"missing-reference.wav",0);printf("missing_stream=%p error=%s\n",missing,p_AIL_last_error());if(missing){p_AIL_close_stream(missing);rc=7;}
 phase=2;HSTREAM stream=p_AIL_open_stream(driver,"owned-reference.wav",0);printf("valid_stream=%p error=%s\n",stream,p_AIL_last_error());
 if(stream){p_AIL_register_stream_callback(stream,eos);p_AIL_set_stream_loop_count(stream,1);phase=3;log("no-serve-start",chosen,0,0,0);DWORD begin=GetTickCount();p_AIL_start_stream(stream);Sleep(200);log("no-serve-end",chosen,0,0,0);phase=4;while(GetTickCount()-begin<2000&&!done){p_AIL_serve();Sleep(5);}if(!done)rc=8;phase=5;begin=GetTickCount();while(GetTickCount()-begin<500){p_AIL_serve();Sleep(5);}phase=6;p_AIL_close_stream(stream);}else rc=9;
 phase=7;p_AIL_close_digital_driver(driver);p_AIL_shutdown();FreeLibrary(dll);
 if(file){printf("adapter_cleanup_unclosed_file=1\n");fclose(file);file=0;rc=10;}
 LONG total=count;for(LONG i=0;i<total&&i<4096;++i){Event &e=events[i];printf("seq=%ld ms=%lu tid=%lu phase=%ld depth=%ld active=%ld op=%s h=%lu a=%ld b=%ld result=%ld\n",e.seq,e.tick,e.tid,e.phase,e.depth,e.active,e.op,(unsigned long)e.h,e.a,e.b,e.result);}
 printf("summary events=%ld overflow=%d errors=%ld eos=%ld rc=%d\n",total,total>4096,errors,done,rc);DeleteCriticalSection(&lock);return rc?rc:(total>4096||errors||done!=1)?11:0;
}
