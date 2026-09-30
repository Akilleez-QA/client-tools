#include <windows.h>
#include <mmsystem.h>
#include <tlhelp32.h>
#include <xmmintrin.h>
#include <cstdio>
#include <cstring>
#include <vector>
#include "Mss.h"
volatile LONG sampleDone=0,streamDone=0;
void trace(char const *stage) { unsigned short cw=0; __asm fnstcw cw
 std::printf("event=%s tick=%lu thread=%lu cw=%04x mxcsr=%08x\n",stage,GetTickCount(),GetCurrentThreadId(),cw,_mm_getcsr()); }
void AILCALLBACK eos(HSAMPLE) { InterlockedIncrement(&sampleDone);trace("sample-eos"); }
void AILCALLBACK eosStream(HSTREAM) { InterlockedIncrement(&streamDone);trace("stream-eos"); }
void modules() { HANDLE snap=CreateToolhelp32Snapshot(TH32CS_SNAPMODULE,GetCurrentProcessId());MODULEENTRY32 m={sizeof(m)};if(Module32First(snap,&m)) do {std::printf("module=%s\n",m.szExePath);}while(Module32Next(snap,&m));CloseHandle(snap); }
#define BIND(f,bytes) decltype(&f) p_##f=reinterpret_cast<decltype(&f)>(GetProcAddress(dll,"_" #f "@" #bytes));if(!p_##f){std::printf("missing=%s\n",#f);return 4;}
int main(int argc,char **argv) {
 std::setvbuf(stdout,0,_IONBF,0);if(argc!=5)return 2;bool const sampleMode=std::strcmp(argv[4],"sample")==0;bool const streamMode=std::strcmp(argv[4],"stream")==0;if(!sampleMode&&!streamMode)return 2;trace("entry");
 HMODULE dll=LoadLibraryA(argv[1]);if(!dll){std::printf("load-error=%lu\n",GetLastError());return 3;}char ver[128]={0};LoadStringA(dll,1,ver,sizeof(ver));std::printf("runtime-resource-version=%s wave-devices=%u\n",ver,waveOutGetNumDevs());
 BIND(AIL_startup,0);BIND(AIL_shutdown,0);BIND(AIL_last_error,0);BIND(AIL_open_digital_driver,16);BIND(AIL_close_digital_driver,4);BIND(AIL_allocate_sample_handle,4);BIND(AIL_release_sample_handle,4);BIND(AIL_set_named_sample_file,20);BIND(AIL_set_sample_loop_count,8);BIND(AIL_register_EOS_callback,8);BIND(AIL_start_sample,4);BIND(AIL_sample_status,4);BIND(AIL_sample_ms_position,12);BIND(AIL_serve,0);BIND(AIL_open_stream,12);BIND(AIL_register_stream_callback,8);BIND(AIL_set_stream_loop_count,8);BIND(AIL_start_stream,4);BIND(AIL_stream_status,4);BIND(AIL_close_stream,4);
 BIND(AIL_set_redist_directory,4);BIND(AIL_decompress_ASI,24);BIND(AIL_mem_free_lock,4);p_AIL_set_redist_directory("C:/vendor-miles-probe/miles");
 S32 started=p_AIL_startup();std::printf("startup=%ld error=%s\n",started,p_AIL_last_error());trace("startup");if(!started)return 5;
 FILE *mp3=std::fopen(argv[3],"rb");if(!mp3)return 20;std::fseek(mp3,0,SEEK_END);long mpsz=std::ftell(mp3);std::rewind(mp3);std::vector<unsigned char> compressed(mpsz);if(std::fread(&compressed[0],1,mpsz,mp3)!=mpsz)return 21;std::fclose(mp3);void *decoded=0;U32 decodedSize=0;trace("decode-start");S32 decodedOkay=p_AIL_decompress_ASI(&compressed[0],mpsz,".mp3",&decoded,&decodedSize,0);std::printf("decode-okay=%ld bytes=%lu error=%s\n",decodedOkay,decodedSize,p_AIL_last_error());trace("decode-end");if(decodedOkay&&decoded){FILE *o=std::fopen("decoded-original.wav","wb");if(o){std::fwrite(decoded,1,decodedSize,o);std::fclose(o);}p_AIL_mem_free_lock(decoded);}modules();
 HDIGDRIVER driver=p_AIL_open_digital_driver(22050,16,MSS_MC_STEREO,0);std::printf("driver=%p error=%s\n",driver,p_AIL_last_error());modules();if(!driver){p_AIL_shutdown();std::puts("BLOCKED no original Miles output driver; no playback verdict");return 6;}
 FILE *f=std::fopen(argv[2],"rb");if(!f)return 7;std::fseek(f,0,SEEK_END);long size=std::ftell(f);std::rewind(f);std::vector<unsigned char> data(size<8192?8192:size);if(std::fread(&data[0],1,size,f)!=size)return 8;std::fclose(f);
 DWORD begin=0; if(sampleMode){ HSAMPLE s=p_AIL_allocate_sample_handle(driver);if(!s)return 9;S32 accepted=p_AIL_set_named_sample_file(s,".wav",&data[0],size,0);std::printf("sample-accepted=%ld\n",accepted);if(!accepted)return 10;p_AIL_set_sample_loop_count(s,1);p_AIL_register_EOS_callback(s,eos);trace("sample-start");p_AIL_start_sample(s);
 begin=GetTickCount();while(GetTickCount()-begin<3000&&!sampleDone){p_AIL_serve();S32 total=0,current=0;p_AIL_sample_ms_position(s,&total,&current);std::printf("sample tick=%lu status=%lu position=%ld total=%ld\n",GetTickCount(),p_AIL_sample_status(s),current,total);Sleep(10);}trace("sample-drain-start");begin=GetTickCount();while(GetTickCount()-begin<500){p_AIL_serve();Sleep(5);}trace("sample-drain-end");p_AIL_release_sample_handle(s); }
 if(streamMode){ HSTREAM stream=p_AIL_open_stream(driver,argv[2],0);std::printf("stream=%p error=%s\n",stream,p_AIL_last_error());if(!stream)return 11;p_AIL_register_stream_callback(stream,eosStream);p_AIL_set_stream_loop_count(stream,1);trace("stream-start");p_AIL_start_stream(stream);begin=GetTickCount();while(GetTickCount()-begin<3000&&!streamDone){p_AIL_serve();std::printf("stream tick=%lu status=%ld\n",GetTickCount(),p_AIL_stream_status(stream));Sleep(10);}trace("stream-drain-start");begin=GetTickCount();while(GetTickCount()-begin<500){p_AIL_serve();Sleep(5);}trace("stream-drain-end");p_AIL_close_stream(stream); } modules();p_AIL_close_digital_driver(driver);p_AIL_shutdown();trace("shutdown");std::printf("sample-eos=%ld stream-eos=%ld\n",sampleDone,streamDone);FreeLibrary(dll);return sampleDone==(sampleMode?1:0)&&streamDone==(streamMode?1:0)?0:12;
}
