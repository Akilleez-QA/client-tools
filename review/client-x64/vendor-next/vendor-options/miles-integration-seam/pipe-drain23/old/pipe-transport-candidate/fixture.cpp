#include "endpoint.h"
#include <sddl.h>
#include <wincrypt.h>
#include <cstdio>
#include <string>
#include <stdexcept>
#include <cstring>
#pragma comment(lib,"advapi32.lib")
using MilesPipe::Endpoint;
static void require(bool v,const char *what) { if(!v) { std::printf("FAIL %s winerr=%lu\n",what,GetLastError());throw std::runtime_error(what); } }
static MilesTransport::Bytes bytes(const std::vector<unsigned char> &v) { return MilesTransport::Bytes(v.empty()?0:&v[0],v.size()); }
static std::vector<unsigned char> callFrame(bool reverse,size_t payload=0) {
 MilesWire::Header h={};h.magic=MilesWire::Magic;h.version=MilesWire::Version;
 h.kind=static_cast<uint16_t>(reverse?MilesWire::ReverseRequest:MilesWire::Request);
 h.opcode=payload?MilesWire::BufferChunk:MilesWire::AIL_file_error;h.request=17;h.lane=1;
 MilesWire::Call c={};if(payload) { c.target.kind=MilesWire::Buffer;c.target.slot=1;c.target.generation=1; }
 std::vector<unsigned char> data(payload);for(size_t i=0;i<data.size();++i)data[i]=static_cast<unsigned char>(i);
 std::vector<unsigned char> out;require(MilesTransport::encodeCall(h,c,bytes(data),MilesTransport::Bytes(),out),"encode call");return out;
}
static std::vector<unsigned char> replyFrame(bool reverse) {
 MilesWire::Header h={};h.magic=MilesWire::Magic;h.version=MilesWire::Version;
 h.kind=static_cast<uint16_t>(reverse?MilesWire::ReverseReply:MilesWire::Reply);h.opcode=MilesWire::AIL_file_error;h.request=17;h.lane=1;
 MilesWire::Result r={};r.return_bits=0x12345678;std::vector<unsigned char> out;
 require(MilesTransport::encodeResult(h,r,MilesTransport::Bytes(),MilesTransport::Bytes(),out),"encode reply");return out;
}
static void pauseForIo(Endpoint &a,Endpoint *b) {
 HANDLE events[4];DWORD n=0;
 if(a.readPending())events[n++]=a.readEvent();if(a.writePending())events[n++]=a.writeEvent();
 if(b) { if(b->readPending())events[n++]=b->readEvent();if(b->writePending())events[n++]=b->writeEvent(); }
 if(n)require(WaitForMultipleObjects(n,events,FALSE,2)!=WAIT_FAILED,"wait io");
 else SwitchToThread();
}
static std::vector<unsigned char> receive(Endpoint &a,Endpoint *b=0) {
 ULONGLONG begin=GetTickCount64();std::vector<unsigned char> out(4096,7);
 while(GetTickCount64()-begin<10000) {
  a.pump();if(b)b->pump();if(a.takeFrame(out)) { require(a.bodyCapacity()==0,"receive transfers storage");return out; }
  require(a.state()==Endpoint::Open,"receive channel fault");pauseForIo(a,b);
 }
 throw std::runtime_error("receive watchdog");
}
static void sent(Endpoint &a) {
 ULONGLONG begin=GetTickCount64();
 while(a.sendBusy() && GetTickCount64()-begin<10000) { a.pump();require(a.state()==Endpoint::Open,"send channel fault");pauseForIo(a,0); }
 require(!a.sendBusy(),"send watchdog");
}
static void rawWrite(HANDLE pipe,const unsigned char *data,DWORD count) {
 OVERLAPPED ov={};ov.hEvent=CreateEventA(0,TRUE,FALSE,0);require(ov.hEvent!=0,"raw event");DWORD done=0;
 BOOL ok=WriteFile(pipe,data,count,&done,&ov);
 if(!ok) {
  DWORD e=GetLastError();require(e==ERROR_IO_PENDING,"raw write");
  DWORD wait=WaitForSingleObject(ov.hEvent,10000);
  if(wait!=WAIT_OBJECT_0) { CancelIoEx(pipe,&ov);GetOverlappedResult(pipe,&ov,&done,TRUE);CloseHandle(ov.hEvent);throw std::runtime_error("raw write watchdog"); }
  require(GetOverlappedResult(pipe,&ov,&done,FALSE)!=0,"raw result");
 }
 CloseHandle(ov.hEvent);require(done==count,"raw short write");
}
static int child(const char *mode,const char *commandName,const char *callbackName) {
 FILE *childLog=0;std::string log="child-"+std::string(mode)+".log";
 require(freopen_s(&childLog,log.c_str(),"w",stdout)==0,"child log");setvbuf(stdout,0,_IONBF,0);
 HANDLE command=CreateFileA(commandName,GENERIC_READ|GENERIC_WRITE,0,0,OPEN_EXISTING,FILE_FLAG_OVERLAPPED,0);
 require(command!=INVALID_HANDLE_VALUE,"child command open");
 HANDLE callback=CreateFileA(callbackName,GENERIC_READ|GENERIC_WRITE,0,0,OPEN_EXISTING,FILE_FLAG_OVERLAPPED,0);
 require(callback!=INVALID_HANDLE_VALUE,"child callback open");
 Endpoint cb(callback,7);
 if(std::strcmp(mode,"backpressure")==0) {
  std::vector<unsigned char> got=receive(cb);require(got==callFrame(true),"reverse exact call");
  require(cb.send(bytes(replyFrame(true))),"reverse send");sent(cb);
  // Keep command unread/open until controller proves write cancellation completed.
  got=receive(cb);require(got==callFrame(true),"release command");
  CloseHandle(command);require(cb.drain(3000),"child callback drain");
  std::printf("PASS child backpressure command-read-count=0\n");return 0;
 }
 Endpoint cmd(command,std::strcmp(mode,"fragmented")==0?3:1048576);
 if(std::strcmp(mode,"exchange")==0 || std::strcmp(mode,"fragmented")==0) {
  std::vector<unsigned char> got=receive(cmd,&cb);require(got==callFrame(false),"call exact bytes");
  MilesWire::Header h={};MilesWire::Call c={};require(MilesTransport::decodeCall(bytes(got),h,c),"decode call");
  require(cmd.send(bytes(replyFrame(false))),"reply send");sent(cmd);
  std::printf("PASS child exchange read-completions=%u\n",cmd.readCompletions());
 } else {
  ULONGLONG begin=GetTickCount64();while(cmd.state()==Endpoint::Open && GetTickCount64()-begin<10000) { cmd.pump();pauseForIo(cmd,0); }
  if(std::strcmp(mode,"bad-small")==0 || std::strcmp(mode,"bad-large")==0) {
   require(cmd.failure()==Endpoint::InvalidLength && cmd.bodyCapacity()==0,"invalid size no allocation");
   std::printf("PASS child invalid-size body-capacity=%Iu\n",cmd.bodyCapacity());
  } else { require(cmd.failure()==Endpoint::PeerClosed,"partial peer close");std::vector<unsigned char> out;require(!cmd.takeFrame(out),"partial undelivered");std::printf("PASS child partial frame rejected\n"); }
 }
 require(cmd.drain(3000),"child command drain");require(cb.drain(3000),"child callback drain");return 0;
}
struct ServerPipe {
 HANDLE pipe,event;OVERLAPPED ov;bool pending;
 ServerPipe(const std::string &name,SECURITY_ATTRIBUTES &sa):pipe(INVALID_HANDLE_VALUE),event(0),pending(false) {
  std::memset(&ov,0,sizeof ov);
  pipe=CreateNamedPipeA(name.c_str(),PIPE_ACCESS_DUPLEX|FILE_FLAG_OVERLAPPED|FILE_FLAG_FIRST_PIPE_INSTANCE,
    PIPE_TYPE_BYTE|PIPE_READMODE_BYTE|PIPE_WAIT|PIPE_REJECT_REMOTE_CLIENTS,1,4096,4096,0,&sa);
  require(pipe!=INVALID_HANDLE_VALUE,"CreateNamedPipe");event=CreateEventA(0,TRUE,FALSE,0);if(!event) { CloseHandle(pipe);pipe=INVALID_HANDLE_VALUE;throw std::runtime_error("connect event"); }ov.hEvent=event;
  if(!ConnectNamedPipe(pipe,&ov)) { DWORD e=GetLastError();require(e==ERROR_IO_PENDING || e==ERROR_PIPE_CONNECTED,"ConnectNamedPipe");pending=e==ERROR_IO_PENDING; }
 }
 void connected() { if(pending) { require(WaitForSingleObject(event,10000)==WAIT_OBJECT_0,"connect timeout");DWORD n=0;require(GetOverlappedResult(pipe,&ov,&n,FALSE)!=0,"connect result");pending=false; } }
 HANDLE take() { HANDLE h=pipe;pipe=INVALID_HANDLE_VALUE;return h; }
 ~ServerPipe() { if(pending) { CancelIoEx(pipe,&ov);DWORD n;GetOverlappedResult(pipe,&ov,&n,TRUE); }if(pipe!=INVALID_HANDLE_VALUE)CloseHandle(pipe);if(event)CloseHandle(event); }
};
static std::string nonce() {
 HCRYPTPROV provider=0;require(CryptAcquireContextA(&provider,0,0,PROV_RSA_FULL,CRYPT_VERIFYCONTEXT)!=0,"random provider");
 unsigned char random[16];BOOL ok=CryptGenRandom(provider,sizeof random,random);CryptReleaseContext(provider,0);require(ok!=0,"random bytes");
 char text[33];const char hex[]="0123456789abcdef";for(unsigned i=0;i<16;++i) { text[i*2]=hex[random[i]>>4];text[i*2+1]=hex[random[i]&15]; }text[32]=0;return text;
}
static PSECURITY_DESCRIPTOR userDescriptor() {
 HANDLE token=0;require(OpenProcessToken(GetCurrentProcess(),TOKEN_QUERY,&token)!=0,"token");DWORD needed=0;
 GetTokenInformation(token,TokenUser,0,0,&needed);std::vector<unsigned char> storage(needed);
 require(GetTokenInformation(token,TokenUser,&storage[0],needed,&needed)!=0,"token user");CloseHandle(token);
 LPSTR sid=0;require(ConvertSidToStringSidA(reinterpret_cast<TOKEN_USER *>(&storage[0])->User.Sid,&sid)!=0,"sid text");
 std::string sddl="D:P(A;;GA;;;";sddl+=sid;sddl+=")";LocalFree(sid);PSECURITY_DESCRIPTOR descriptor=0;
 require(ConvertStringSecurityDescriptorToSecurityDescriptorA(sddl.c_str(),SDDL_REVISION_1,&descriptor,0)!=0,"private acl");return descriptor;
}
static void runCase(const char *childExe,const char *mode) {
 std::string base="\\\\.\\pipe\\swg-media-private-"+nonce(),commandName=base+"-command",callbackName=base+"-callback";
 PSECURITY_DESCRIPTOR descriptor=userDescriptor();SECURITY_ATTRIBUTES sa={sizeof sa,descriptor,FALSE};
 ServerPipe command(commandName,sa),callback(callbackName,sa);LocalFree(descriptor);
 std::string args="\""+std::string(childExe)+"\" --child "+mode+" "+commandName+" "+callbackName;
 std::vector<char> line(args.begin(),args.end());line.push_back(0);STARTUPINFOA si={};si.cb=sizeof si;PROCESS_INFORMATION process={};
 HANDLE job=CreateJobObjectA(0,0);require(job!=0,"watchdog job");
 JOBOBJECT_EXTENDED_LIMIT_INFORMATION jobInfo={};jobInfo.BasicLimitInformation.LimitFlags=JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE;
 if(!SetInformationJobObject(job,JobObjectExtendedLimitInformation,&jobInfo,sizeof jobInfo)) { CloseHandle(job);throw std::runtime_error("job policy"); }
 if(!CreateProcessA(childExe,&line[0],0,0,FALSE,CREATE_SUSPENDED,0,0,&si,&process)) { CloseHandle(job);throw std::runtime_error("CreateProcess exact child"); }
 if(!AssignProcessToJobObject(job,process.hProcess)) { TerminateProcess(process.hProcess,91);WaitForSingleObject(process.hProcess,5000);CloseHandle(process.hThread);CloseHandle(process.hProcess);CloseHandle(job);throw std::runtime_error("job assignment"); }
 if(ResumeThread(process.hThread)==static_cast<DWORD>(-1)) { TerminateProcess(process.hProcess,92);WaitForSingleObject(process.hProcess,5000);CloseHandle(process.hThread);CloseHandle(process.hProcess);CloseHandle(job);throw std::runtime_error("resume child"); }CloseHandle(process.hThread);
 try {
  command.connected();callback.connected();Endpoint cb(callback.take(),5);
  if(std::strcmp(mode,"exchange")==0 || std::strcmp(mode,"fragmented")==0) {
   Endpoint cmd(command.take(),std::strcmp(mode,"fragmented")==0?7:1048576);
   require(cmd.send(bytes(callFrame(false))),"call send");std::vector<unsigned char> got=receive(cmd,&cb);
   require(got==replyFrame(false),"reply exact bytes");MilesWire::Header h={};MilesWire::Result r={};require(MilesTransport::decodeResult(bytes(got),h,r) && r.return_bits==0x12345678,"decode reply");
   std::printf("PASS %s reads=%u writes=%u\n",mode,cmd.readCompletions(),cmd.writeCompletions());require(cmd.drain(3000),"controller drain");
  } else if(std::strcmp(mode,"backpressure")==0) {
   Endpoint cmd(command.take());require(cmd.send(bytes(callFrame(false,524288))),"large command send");cmd.pump();require(cmd.writePending(),"command backpressure pending");
   require(cb.send(bytes(callFrame(true))),"reverse request send");std::vector<unsigned char> got=receive(cb,&cmd);require(got==replyFrame(true),"reverse reply exact");
   require(cmd.writePending(),"command still blocked after reverse progress");require(cmd.drain(3000),"cancel pending read and write");
   require(!cmd.pending() && cmd.state()==Endpoint::Closed,"cancel drained");
   require(cb.send(bytes(callFrame(true))),"child release send");sent(cb);
   std::printf("PASS backpressure reverse-progress-while-command-pending=1 cancellation-drained=1\n");
  } else {
   HANDLE raw=command.take();std::vector<unsigned char> data=callFrame(false);
   DWORD count=std::strcmp(mode,"close-header")==0?13:60;
   if(std::strcmp(mode,"bad-small")==0 || std::strcmp(mode,"bad-large")==0) {
    uint32_t n=std::strcmp(mode,"bad-small")==0?47:1048577;for(unsigned i=0;i<4;++i)data[12+i]=static_cast<unsigned char>(n>>(8*i));count=48;
   }
   rawWrite(raw,&data[0],count);CloseHandle(raw);std::printf("PASS %s sent-bytes=%lu\n",mode,count);
  }
  require(cb.drain(3000),"controller callback drain");
  if(WaitForSingleObject(process.hProcess,15000)!=WAIT_OBJECT_0)throw std::runtime_error("child watchdog");
  DWORD code=99;require(GetExitCodeProcess(process.hProcess,&code)!=0 && code==0,"child exit");
  std::printf("CASE %s child_exit=0\n",mode);
  CloseHandle(process.hProcess);CloseHandle(job);
 } catch(...) { TerminateProcess(process.hProcess,90);WaitForSingleObject(process.hProcess,5000);CloseHandle(process.hProcess);CloseHandle(job);throw; }
}
int main(int argc,char **argv) {
 setvbuf(stdout,0,_IONBF,0);
 try {
  if(argc==5 && std::strcmp(argv[1],"--child")==0)return child(argv[2],argv[3],argv[4]);
  require(argc==2,"child executable argument");
  const char *cases[]={"exchange","fragmented","bad-small","bad-large","close-header","close-body","backpressure"};
  for(unsigned i=0;i<7;++i)runCase(argv[1],cases[i]);
  std::printf("PASS 7 private cross-process transport cases\n");return 0;
 } catch(const std::exception &e) { std::printf("FAIL exception %s\n",e.what());return 1; }
}
