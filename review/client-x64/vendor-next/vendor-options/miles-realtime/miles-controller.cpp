#include <windows.h>
#include <cstdio>
#include <cstring>
int main(int argc,char**argv){
 if(argc!=2||(std::strcmp(argv[1],"sample")&&std::strcmp(argv[1],"stream")))return 2;
 std::setvbuf(stdout,0,_IONBF,0);std::printf("controller-start tick=%lu thread=%lu pointer=%u\n",GetTickCount(),GetCurrentThreadId(),unsigned(sizeof(void*)));
 SECURITY_ATTRIBUTES sa={sizeof(sa),0,TRUE};HANDLE read=0,write=0;if(!CreatePipe(&read,&write,&sa,0))return 3;if(!SetHandleInformation(write,HANDLE_FLAG_INHERIT,0))return 4;
 STARTUPINFOA si={sizeof(si)};si.dwFlags=STARTF_USESTDHANDLES;si.hStdInput=read;si.hStdOutput=GetStdHandle(STD_OUTPUT_HANDLE);si.hStdError=GetStdHandle(STD_ERROR_HANDLE);PROCESS_INFORMATION pi={0};
 char cmd[]="C:\\vendor-miles-probe\\miles-command-host.exe C:\\vendor-miles-probe\\Mss32.dll C:\\vendor-miles-probe\\sample.wav C:\\vendor-miles-probe\\sample.mp3 command";
 if(!CreateProcessA(0,cmd,0,0,TRUE,0,0,0,&si,&pi)){CloseHandle(read);CloseHandle(write);return 5;}CloseHandle(read);CloseHandle(pi.hThread);
 char command[16];std::sprintf(command,"%s\n",argv[1]);DWORD written=0;bool okay=WriteFile(write,command,DWORD(std::strlen(command)),&written,0)!=0&&written==std::strlen(command);CloseHandle(write);
 DWORD wait=WaitForSingleObject(pi.hProcess,10000);if(wait!=WAIT_OBJECT_0){TerminateProcess(pi.hProcess,99);WaitForSingleObject(pi.hProcess,2000);CloseHandle(pi.hProcess);return 6;}DWORD code=0;GetExitCodeProcess(pi.hProcess,&code);CloseHandle(pi.hProcess);std::printf("controller-end tick=%lu child=%lu command-written=%u\n",GetTickCount(),code,okay?1:0);return okay?int(code):7;
}
