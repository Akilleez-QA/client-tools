#include <windows.h>
#include <stdio.h>
#include <string>
#include <io.h>
#include <fcntl.h>
int main(){
 _setmode(_fileno(stdout),_O_BINARY);
 SECURITY_ATTRIBUTES sa={sizeof(sa),0,TRUE};HANDLE r,w;
 if(!CreatePipe(&r,&w,&sa,0))return 1;SetHandleInformation(r,HANDLE_FLAG_INHERIT,0);
 STARTUPINFOA si={sizeof(si)};si.dwFlags=STARTF_USESTDHANDLES;si.hStdOutput=w;si.hStdError=w;si.hStdInput=GetStdHandle(STD_INPUT_HANDLE);
 PROCESS_INFORMATION pi={0};char cmd[]="C:\\vendor-bink-probe\\probe32.exe";
 if(!CreateProcessA(0,cmd,0,0,TRUE,CREATE_NO_WINDOW,0,"C:\\vendor-bink-probe",&si,&pi))return 2;
 CloseHandle(w);DWORD start=GetTickCount();std::string data;
 for(;;){DWORD available=0,n=0;if(!PeekNamedPipe(r,0,0,0,&available,0))break;
  if(available){char buf[4096];if(!ReadFile(r,buf,available>4096?4096:available,&n,0))break;data.append(buf,n);if(data.size()>65536){TerminateProcess(pi.hProcess,9);return 3;}}
  else if(WaitForSingleObject(pi.hProcess,10)==WAIT_OBJECT_0){DWORD remaining=0;if(!PeekNamedPipe(r,0,0,0,&remaining,0)||!remaining)break;}
  if(GetTickCount()-start>60000){TerminateProcess(pi.hProcess,10);return 4;}
 }
 WaitForSingleObject(pi.hProcess,1000);DWORD code=0;GetExitCodeProcess(pi.hProcess,&code);
 // FNV-1a-64 is transport checksum, not a cryptographic or fidelity claim.
 unsigned __int64 hash=14695981039346656037ULL;for(size_t i=0;i<data.size();++i){hash^=(unsigned char)data[i];hash*=1099511628211ULL;}
 printf("BINKPROBE/1 pointer_bytes=%u length=%u child_exit=%lu fnv1a64=%016I64x\n",unsigned(sizeof(void*)),unsigned(data.size()),code,hash);fwrite(data.data(),1,data.size(),stdout);
 CloseHandle(r);CloseHandle(pi.hThread);CloseHandle(pi.hProcess);return code;
}
