#include "sound-info-codec.h"
#include <stdio.h>
#include <string.h>
#include <vector>
#ifndef _WIN64
#include <windows.h>
#include <Mss.h>
#endif
using namespace MilesTransport;
static bool readFile(const char* path,std::vector<unsigned char>& out){
 FILE* f=0;if(fopen_s(&f,path,"rb")||!f)return false;
 if(fseek(f,0,SEEK_END)){fclose(f);return false;}long n=ftell(f);
 if(n<=0||n>1024*1024*16||fseek(f,0,SEEK_SET)){fclose(f);return false;}
 out.resize(static_cast<size_t>(n));bool ok=fread(&out[0],1,out.size(),f)==out.size();fclose(f);return ok;
}
static void words(const MilesWire::SoundInfo& s,unsigned* w){
 w[0]=static_cast<unsigned>(s.format);w[1]=s.data_offset;w[2]=s.data_length;w[3]=s.rate;
 w[4]=static_cast<unsigned>(s.bits);w[5]=static_cast<unsigned>(s.channels);w[6]=s.channel_mask;
 w[7]=s.samples;w[8]=s.block_size;w[9]=s.initial_offset;w[10]=s.null_mask;
}
int main(int argc,char** argv){
 if(argc!=5)return 2;std::vector<unsigned char> image,payload;
 if(!readFile(argv[1],image))return 3;
 MilesWire::SoundInfo s={};FILE* f=0;
#ifndef _WIN64
 HMODULE dll=LoadLibraryA(argv[4]);if(!dll)return 4;
 char loaded[MAX_PATH]={};DWORD loadedSize=GetModuleFileNameA(dll,loaded,MAX_PATH);
 if(!loadedSize||loadedSize>=MAX_PATH){FreeLibrary(dll);return 19;}
 printf("loaded_dll=%s\n",loaded);
 FARPROC address=GetProcAddress(dll,"_AIL_WAV_info@8");
 decltype(&AIL_WAV_info) wav=0;static_assert(sizeof(wav)==sizeof(address),"function pointer");memcpy(&wav,&address,sizeof(wav));
 if(!wav){FreeLibrary(dll);return 5;}
 std::vector<unsigned char> originalImage=image;
 AILSOUNDINFO actual={};S32 result=wav(&image[0],&actual);printf("genuine_WAV_info_result=%ld\n",result);
 if(!result){FreeLibrary(dll);return 6;}
 if(image!=originalImage){puts("FAIL vendor modified retained input");FreeLibrary(dll);return 20;}
 puts("PASS retained input unchanged");
 s.format=actual.format;s.data_length=actual.data_len;s.rate=actual.rate;s.bits=actual.bits;s.channels=actual.channels;
 s.channel_mask=actual.channel_mask;s.samples=actual.samples;s.block_size=actual.block_size;
 SoundInfoPointers pointers={actual.data_ptr,actual.initial_ptr};MilesWire::SoundInfo mapped;
 if(!mapSoundInfoPointers(s,Bytes(&image[0],image.size()),pointers,mapped)){puts("FAIL returned metadata cannot map conservatively");FreeLibrary(dll);return 7;}
 s=mapped;if(!encodeSoundInfo(s,image.size(),payload)){FreeLibrary(dll);return 8;}
 if(fopen_s(&f,argv[2],"wb")||!f){FreeLibrary(dll);return 9;}
 bool wrote=fwrite(&payload[0],1,payload.size(),f)==payload.size();fclose(f);if(!wrote){FreeLibrary(dll);return 10;}
 unsigned expected[11];words(s,expected);
 if(fopen_s(&f,argv[3],"wt")||!f){FreeLibrary(dll);return 11;}
 for(unsigned i=0;i<11;++i)fprintf(f,"%08x\n",expected[i]);fclose(f);FreeLibrary(dll);
#else
 if(!readFile(argv[2],payload)||!decodeSoundInfo(Bytes(&payload[0],payload.size()),image.size(),s))return 12;
 unsigned expected[11],observed[11];words(s,observed);
 if(fopen_s(&f,argv[3],"rt")||!f)return 13;
 for(unsigned i=0;i<11;++i){if(fscanf_s(f,"%x",&expected[i])!=1||expected[i]!=observed[i]){fclose(f);return 14;}}fclose(f);
 std::vector<unsigned char> encoded;if(!encodeSoundInfo(s,image.size(),encoded)||encoded!=payload)return 15;
#endif
 SoundInfoPointers restored={};if(!resolveSoundInfoPointers(s,Bytes(&image[0],image.size()),restored))return 16;
 MilesWire::SoundInfo mappedAgain;if(!mapSoundInfoPointers(s,Bytes(&image[0],image.size()),restored,mappedAgain))return 17;
 unsigned a[11],b[11];words(s,a);words(mappedAgain,b);for(unsigned i=0;i<11;++i)if(a[i]!=b[i])return 18;
 printf("PASS 11 scalar/offset fields; format=%d rate=%u bits=%d channels=%d data_offset=%u data_length=%u initial_offset=%u null_mask=%u\n",s.format,s.rate,s.bits,s.channels,s.data_offset,s.data_length,s.initial_offset,s.null_mask);
 return 0;
}
