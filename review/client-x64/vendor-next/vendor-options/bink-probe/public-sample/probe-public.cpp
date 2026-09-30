#include <windows.h>
#include <stdio.h>
#include <vector>
#include <io.h>
#include <fcntl.h>
#include "bink.h"
#define BIND(name,decor) decltype(&name) p##name=(decltype(&name))GetProcAddress(dll,decor); if(!p##name){printf("{\"error\":\"missing export\",\"export\":\"%s\",\"winerror\":%lu}\n",decor,GetLastError());return 3;}
int main(int argc,char**argv){
 _setmode(_fileno(stdout),_O_BINARY);
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
 // This bounded public sample has zero tracks; audio extraction is not exercised.
 if(b->NumTracks!=0){puts("{\"error\":\"unexpected_audio_track_not_tested\"}");pBinkClose(b);return 11;}
 for(unsigned f=1;f<=32&&f<=b->Frames;++f){
  S32 status=pBinkDoFrame(b);printf("{\"frame\":%u,\"decode_status\":%ld,\"read_error\":%lu}\n",f,status,b->ReadError);
  if(b->ReadError)return 6;
  if(f==1||f==8||f==16||f==32){memset(pixels.data(),0,pixels.size());S32 copy=pBinkCopyToBuffer(b,pixels.data(),b->Width*4,b->Height,0,0,BINKSURFACE32A|BINKCOPYALL);printf("{\"kind\":\"pixels\",\"frame\":%u,\"copy_status\":%ld,\"length\":%u}\n",f,copy,unsigned(pixels.size()));if(fwrite(pixels.data(),1,pixels.size(),stdout)!=pixels.size())return 8;putchar('\n');}

  if(f<32&&f<b->Frames)pBinkNextFrame(b);
 }
 pBinkClose(b);FreeLibrary(dll);return 0;
}
