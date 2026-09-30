#include <windows.h>
#include <stdio.h>
#include <vector>
#include "bink.h"
#define BIND(name,decor) decltype(&name) p##name=(decltype(&name))GetProcAddress(dll,decor); if(!p##name){printf("{\"error\":\"missing export\",\"export\":\"%s\",\"winerror\":%lu}\n",decor,GetLastError());return 3;}
int main(int argc,char**argv){
 SetErrorMode(SEM_FAILCRITICALERRORS|SEM_NOGPFAULTERRORBOX);
 HMODULE dll=LoadLibraryA("C:\\vendor-bink-probe\\binkw32.dll");
 if(!dll){printf("{\"error\":\"LoadLibrary\",\"winerror\":%lu}\n",GetLastError());return 2;}
 BIND(BinkOpen,"_BinkOpen@8"); BIND(BinkClose,"_BinkClose@4");
 BIND(BinkDoFrame,"_BinkDoFrame@4"); BIND(BinkNextFrame,"_BinkNextFrame@4");
 BIND(BinkCopyToBuffer,"_BinkCopyToBuffer@28"); BIND(BinkGetError,"_BinkGetError@0");
 BIND(BinkSetSoundTrack,"_BinkSetSoundTrack@8");
 BIND(BinkOpenTrack,"_BinkOpenTrack@8"); BIND(BinkCloseTrack,"_BinkCloseTrack@4"); BIND(BinkGetTrackData,"_BinkGetTrackData@8");
 printf("{\"event\":\"runtime_loaded_exports_resolved\",\"pointer_bytes\":%u,\"header\":\"%s\"}\n",unsigned(sizeof(void*)),BINKVERSION);
 if(argc<2){puts("{\"event\":\"no_asset_decode_not_run\"}");FreeLibrary(dll);return 0;}
 pBinkSetSoundTrack(0,0);
 HBINK b=pBinkOpen(argv[1],BINKSNDTRACK|BINKNOTHREADEDIO|BINKNOSKIP|BINKALPHA);
 if(!b){printf("BinkOpen failed: %s\n",pBinkGetError());return 4;}
 if(!b->Width||!b->Height||b->Width>1920||b->Height>1080){pBinkClose(b);return 5;}
 printf("{\"width\":%lu,\"height\":%lu,\"frames\":%lu,\"rate\":%lu,\"rate_div\":%lu,\"tracks\":%ld}\n",b->Width,b->Height,b->Frames,b->FrameRate,b->FrameRateDiv,b->NumTracks);
 std::vector<unsigned char> pixels(b->Width*b->Height*4);
 HBINKTRACK t=b->NumTracks>0?pBinkOpenTrack(b,0):0;
 std::vector<unsigned char> pcm;
 if(t){if(t->MaxSize>4*1024*1024||!t->MaxSize){pBinkCloseTrack(t);t=0;}else{pcm.resize(t->MaxSize);printf("{\"track_frequency\":%lu,\"bits\":%lu,\"channels\":%lu,\"max_size\":%lu}\n",t->Frequency,t->Bits,t->Channels,t->MaxSize);}}
 for(unsigned f=1;f<=32&&f<=b->Frames;++f){
  S32 status=pBinkDoFrame(b);printf("{\"frame\":%u,\"decode_status\":%ld,\"read_error\":%lu}\n",f,status,b->ReadError);
  if(b->ReadError)return 6;
  if(t){U32 n=pBinkGetTrackData(t,pcm.data());if(n>pcm.size())return 7;char path[100];sprintf_s(path,"C:\\vendor-bink-probe\\track-%02u.pcm",f);FILE*o=0;fopen_s(&o,path,"wb");if(!o)return 8;fwrite(pcm.data(),1,n,o);fclose(o);}
  if(f==1||f==8||f==16||f==32){memset(pixels.data(),0,pixels.size());S32 copy=pBinkCopyToBuffer(b,pixels.data(),b->Width*4,b->Height,0,0,BINKSURFACE32A|BINKCOPYALL);char path[100];sprintf_s(path,"C:\\vendor-bink-probe\\frame-%02u.bgra",f);FILE*o=0;fopen_s(&o,path,"wb");if(!o)return 8;fwrite(pixels.data(),1,pixels.size(),o);fclose(o);printf("{\"frame\":%u,\"copy_status\":%ld}\n",f,copy);}
  if(f<32&&f<b->Frames)pBinkNextFrame(b);
 }
 if(t)pBinkCloseTrack(t);pBinkClose(b);FreeLibrary(dll);return 0;
}
