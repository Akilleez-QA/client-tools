#include "live-bridge-candidate/common.h"
#include <algorithm>

struct Pair {
 HANDLE owned,peer;
 Pair():owned(INVALID_HANDLE_VALUE),peer(INVALID_HANDLE_VALUE) {
  std::string name="\\\\.\\pipe\\drain23-"+nonce();
  PSECURITY_DESCRIPTOR descriptor=userDescriptor();SECURITY_ATTRIBUTES sa={sizeof sa,descriptor,FALSE};
  ServerPipe server(name,sa);LocalFree(descriptor);
  peer=CreateFileA(name.c_str(),GENERIC_READ|GENERIC_WRITE,0,0,OPEN_EXISTING,FILE_FLAG_OVERLAPPED,0);
  require(peer!=INVALID_HANDLE_VALUE,"peer connect");server.connected();owned=server.take();
 }
 HANDLE take(){HANDLE h=owned;owned=INVALID_HANDLE_VALUE;return h;}
 void closePeer(){if(peer!=INVALID_HANDLE_VALUE){CloseHandle(peer);peer=INVALID_HANDLE_VALUE;}}
 ~Pair(){closePeer();if(owned!=INVALID_HANDLE_VALUE)CloseHandle(owned);}
};
static DWORD rawIo(HANDLE h,void *p,DWORD count,bool write) {
 OVERLAPPED ov={};ov.hEvent=CreateEventA(0,TRUE,FALSE,0);require(ov.hEvent!=0,"raw event");DWORD n=0;
 BOOL ok=write?WriteFile(h,p,count,&n,&ov):ReadFile(h,p,count,&n,&ov);
 if(!ok){require(GetLastError()==ERROR_IO_PENDING,"raw pending");
  DWORD wait=WaitForSingleObject(ov.hEvent,5000);
  if(wait!=WAIT_OBJECT_0){CancelIoEx(h,&ov);GetOverlappedResult(h,&ov,&n,TRUE);CloseHandle(ov.hEvent);throw std::runtime_error("raw watchdog");}
  require(GetOverlappedResult(h,&ov,&n,FALSE)!=FALSE,"raw result");
 }
 CloseHandle(ov.hEvent);require(n>0 && (!write || n==count),"raw progress/count");return n;
}
static std::vector<unsigned char> frame(size_t payload=0,bool reply=false) {
 MilesWire::Header h={};h.magic=MilesWire::Magic;h.version=MilesWire::Version;
 h.kind=static_cast<uint16_t>(reply?MilesWire::Reply:MilesWire::Request);h.opcode=payload?MilesWire::BufferChunk:MilesWire::AIL_file_error;h.request=17;h.lane=1;
 std::vector<unsigned char> data(payload,42),out;
 if(reply){MilesWire::Result r={};r.return_bits=0x12345678;require(MilesTransport::encodeResult(h,r,bytes(data),MilesTransport::Bytes(),out),"encode reply");}
 else {MilesWire::Call c={};if(payload){c.target.kind=MilesWire::Buffer;c.target.slot=1;c.target.generation=1;}require(MilesTransport::encodeCall(h,c,bytes(data),MilesTransport::Bytes(),out),"encode call");}
 return out;
}
struct Control {
 enum Action{Nothing,LateRead,LateError,FinishWrite};
 HANDLE target;Pair *pair;OVERLAPPED *read,*write;const void *writeBuffer;
 bool hold,armed;Action action;size_t writeSize;unsigned aborts,realErrors,incomplete,cancels;DWORD preCount,preError;
 Control():target(INVALID_HANDLE_VALUE),pair(0),read(0),write(0),writeBuffer(0),hold(false),armed(false),action(Nothing),writeSize(0),aborts(0),realErrors(0),incomplete(0),cancels(0),preCount(0),preError(0){}
} control;
struct RestoreCancellation { ~RestoreCancellation(){control.hold=false;} };
BOOL WINAPI Drain23ReadFile(HANDLE h,LPVOID p,DWORD n,LPDWORD done,LPOVERLAPPED ov){if(h==control.target)control.read=ov;return ReadFile(h,p,n,done,ov);}
BOOL WINAPI Drain23WriteFile(HANDLE h,LPCVOID p,DWORD n,LPDWORD done,LPOVERLAPPED ov){if(h==control.target){control.write=ov;control.writeBuffer=p;control.writeSize=n;}return WriteFile(h,p,n,done,ov);}
BOOL WINAPI Drain23GetOverlappedResult(HANDLE h,LPOVERLAPPED ov,LPDWORD count,BOOL wait){
 BOOL ok=GetOverlappedResult(h,ov,count,wait);DWORD e=ok?ERROR_SUCCESS:GetLastError();
 if(h==control.target && !ok){if(e==ERROR_OPERATION_ABORTED)++control.aborts;else if(e==ERROR_IO_INCOMPLETE)++control.incomplete;else ++control.realErrors;}
 SetLastError(e);return ok;
}
BOOL WINAPI Drain23CancelIoEx(HANDLE h,LPOVERLAPPED ov){
 if(h==control.target){++control.cancels;
  if(control.hold){SetLastError(ERROR_NOT_FOUND);return FALSE;} // Deliberate test-only withheld request.
  if(control.armed){control.armed=false;
   if(control.action==Control::LateRead){unsigned char payload[13]={1,2,3};rawIo(control.pair->peer,payload,sizeof payload,true);}
   if(control.action==Control::LateError)control.pair->closePeer();
   OVERLAPPED *watch=control.read;
   if(control.action==Control::FinishWrite){
    std::vector<unsigned char> got(control.writeSize);size_t used=0;
    while(used<got.size())used+=rawIo(control.pair->peer,&got[used],static_cast<DWORD>(got.size()-used),false);
    require(got==frame(524288),"peer received complete exact write");watch=control.write;
   }
   require(watch && WaitForSingleObject(watch->hEvent,5000)==WAIT_OBJECT_0,"native completion before cancellation collection");
   BOOL ok=GetOverlappedResult(h,watch,&control.preCount,FALSE);control.preError=ok?ERROR_SUCCESS:GetLastError();
   std::printf("SENSOR precancel count=%lu error=%lu pending-record-not-collected=1\n",control.preCount,control.preError);
  }
 }
 return CancelIoEx(h,ov);
}
static void target(HANDLE h,Pair &p){control=Control();control.target=h;control.pair=&p;}
static void waitRead(Endpoint &a){require(a.readPending(),"read submitted pending");require(WaitForSingleObject(a.readEvent(),5000)==WAIT_OBJECT_0,"read completion event");}
static bool session(Endpoint &a,Endpoint &b,bool ordered=false){
 try{drainSession(a,b,ordered);std::printf("SENSOR session accepted\n");return true;}
 catch(const std::exception &e){std::printf("SENSOR session rejected %s\n",e.what());return false;}
}
static void closed(Endpoint &a){require(a.state()==Endpoint::Closed && !a.pending(),"safe closed endpoint");}
static void report(Endpoint &a){
 std::printf("SENSOR failure=%d error=%lu read_pending=%d write_pending=%d send_busy=%d aborts=%u real_errors=%u\n",int(a.failure()),a.windowsError(),a.readPending(),a.writePending(),a.sendBusy(),control.aborts,control.realErrors);
#ifdef DRAIN23_CANDIDATE
 std::printf("SENSOR unread_bytes=%Iu\n",a.unreadBytes());
#endif
}
static void run(const char *name){
 if(std::strcmp(name,"exchange")==0 || std::strcmp(name,"exchange-session")==0){
  const size_t segments[]={1048576,3};
  for(unsigned i=0;i<2;++i){Pair p;Endpoint a(p.take(),segments[i]);Endpoint b(p.peer,segments[i]);p.peer=INVALID_HANDLE_VALUE;
   std::vector<unsigned char> request=frame(),response=frame(0,true),got;
   require(a.send(bytes(request)),"send request");got=receive(b,&a);require(got==request,"exact request");MilesWire::Header h={};MilesWire::Call c={};require(MilesTransport::decodeCall(bytes(got),h,c),"decode request");
   require(b.send(bytes(response)),"send response");got=receive(a,&b);require(got==response,"exact reply");MilesWire::Result r={};require(MilesTransport::decodeResult(bytes(got),h,r)&&r.return_bits==0x12345678,"decode reply");
   // Collect all output before separately cancelling both idle endpoints.
   sent(a);sent(b);
   if(std::strcmp(name,"exchange-session")==0)require(session(a,b,true),"valid exchange session accepted");
   else {a.cancel();b.cancel();require(a.drain(3000)&&b.drain(3000),"exchange cleanup");}
   require(a.failure()==Endpoint::None&&(b.failure()==Endpoint::None||b.failure()==Endpoint::PeerClosed)&&!a.sendBusy()&&!b.sendBusy(),"exchange health");
#ifdef DRAIN23_CANDIDATE
   require(a.unreadBytes()==0&&b.unreadBytes()==0,"all exchange input consumed");
#endif
  }return;
 }
 Pair p,q;HANDLE h=p.take();target(h,p);Endpoint a(h),b(q.take());RestoreCancellation restoreCancellation;
 if(std::strcmp(name,"idle")==0){a.pump();require(a.readPending(),"idle pending");require(session(a,b),"ordinary cancellation accepted");require(a.failure()==Endpoint::None&&control.aborts==1,"intentional abort benign");closed(a);closed(b);report(a);return;}
 if(std::strcmp(name,"late-read")==0||std::strcmp(name,"late-peer-error")==0){
  a.pump();require(a.readPending(),"race pending read");control.action=std::strcmp(name,"late-read")==0?Control::LateRead:Control::LateError;control.armed=true;
  bool accepted=session(a,b);closed(a);closed(b);report(a);
  if(control.action==Control::LateRead)require(control.preError==0&&control.preCount==13,"real native successful read before collect");
  else require(control.preError==ERROR_BROKEN_PIPE||control.preError==ERROR_PIPE_NOT_CONNECTED,"real native peer-close error");
  require(!accepted,"reject cancellation-time completion evidence");return;
 }
 if(std::strcmp(name,"ordered-close-input")==0){
  unsigned char data[13]={1,2,3};rawIo(p.peer,data,sizeof data,true);a.pump();require(a.readPending(),"partial input collected before close");p.closePeer();waitRead(a);
  bool accepted=session(a,b,true);closed(a);closed(b);report(a);require(a.failure()==Endpoint::PeerClosed,"ordered close fault retained");require(!accepted,"ordered peer close cannot mask input");return;
 }
 if(std::strcmp(name,"session-timeout")==0){
  a.pump();control.hold=true;bool accepted=session(a,b);control.hold=false;bool callbackClosed=b.state()==Endpoint::Closed&&!b.pending();bool commandPending=a.readPending();
  require(a.drain(3000)&&b.drain(3000),"supplement release cleanup");
  std::printf("SENSOR session_timeout rejected=%d first_retained_pending=%d second_closed_before_release=%d\n",!accepted,commandPending,callbackClosed);
  require(!accepted&&commandPending&&callbackClosed,"second channel cleanup despite first timeout");return;
 }
 if(std::strcmp(name,"buffered-input")==0||std::strcmp(name,"partial-input")==0){
  std::vector<unsigned char> v=frame();DWORD n=std::strcmp(name,"partial-input")==0?13:static_cast<DWORD>(v.size());rawIo(p.peer,&v[0],n,true);a.pump();
  bool accepted=session(a,b,true);closed(a);closed(b);report(a);require(!accepted,"reject untaken input even with ordered-close allowance");return;
 }
 if(std::strcmp(name,"queued-write")==0){std::vector<unsigned char> v=frame();require(a.send(bytes(v)),"queue write");a.cancel();require(a.drain(3000),"queued cleanup");closed(a);report(a);require(a.sendBusy()&&a.failure()==Endpoint::None,"queued unsent evidence remains distinct from cleanup");return;}
 if(std::strcmp(name,"partial-write")==0){
  // Four one-byte synchronous segments in pump leave a frame partly unissued.
  Pair r;Endpoint tiny(r.take(),1);std::vector<unsigned char> v=frame();require(tiny.send(bytes(v)),"queue segmented write");
  bool accepted=session(tiny,b);closed(tiny);closed(b);require(tiny.sendBusy(),"partly sent frame retained");require(!accepted,"reject incomplete segmented output");return;
 }
 if(std::strcmp(name,"backpressure")==0||std::strcmp(name,"completed-write")==0||std::strcmp(name,"timeout")==0||std::strcmp(name,"first-fault")==0){
  std::vector<unsigned char> v=frame(524288);require(a.send(bytes(v)),"queue large write");a.pump();require(a.readPending()&&a.writePending(),"real read and backpressured write pending");
  if(std::strcmp(name,"first-fault")==0){
   std::vector<unsigned char> bad=frame();bad[12]=47;bad[13]=bad[14]=bad[15]=0;control.hold=true;rawIo(p.peer,&bad[0],48,true);waitRead(a);a.pump();
   require(a.failure()==Endpoint::InvalidLength&&a.windowsError()==0&&a.writePending(),"first fault before write terminal result");p.closePeer();require(WaitForSingleObject(a.writeEvent(),5000)==WAIT_OBJECT_0,"late write error complete");control.hold=false;
   require(a.drain(3000),"first fault cleanup");report(a);require(control.realErrors>0&&a.failure()==Endpoint::InvalidLength&&a.windowsError()==0,"first meaningful fault unchanged");return;
  }
  if(std::strcmp(name,"timeout")==0){
   control.hold=true;OVERLAPPED *read=control.read,*write=control.write;const void *buffer=control.writeBuffer;DWORD n=0;
   require(!GetOverlappedResult(h,read,&n,FALSE)&&GetLastError()==ERROR_IO_INCOMPLETE,"OS read still incomplete");require(!GetOverlappedResult(h,write,&n,FALSE)&&GetLastError()==ERROR_IO_INCOMPLETE,"OS write still incomplete");
   require(!a.drain(0),"zero timeout while cancellation withheld");require(a.state()==Endpoint::Stopping&&a.readPending()&&a.writePending()&&a.sendBusy(),"timeout preserves ownership state");
   DWORD flags=0;require(GetHandleInformation(h,&flags)&&GetHandleInformation(a.readEvent(),&flags)&&GetHandleInformation(a.writeEvent(),&flags),"timeout handles alive");
   require(read==control.read&&write==control.write&&buffer==control.writeBuffer,"operation and borrowed buffer identities retained");
   require(!GetOverlappedResult(h,read,&n,FALSE)&&GetLastError()==ERROR_IO_INCOMPLETE,"retained read still kernel pending");require(!GetOverlappedResult(h,write,&n,FALSE)&&GetLastError()==ERROR_IO_INCOMPLETE,"retained write still kernel pending");
   std::printf("SENSOR timeout=1 real_os_pending=2 handles_alive=3 same_overlapped_and_buffer=1 adapter=withheld_cancel\n");control.hold=false;require(a.drain(3000),"release timeout cleanup");closed(a);report(a);return;
  }
  if(std::strcmp(name,"completed-write")==0){control.action=Control::FinishWrite;control.armed=true;bool accepted=session(a,b);closed(a);closed(b);report(a);require(accepted&&!a.sendBusy()&&a.failure()==Endpoint::None,"completed write accounted during stop");return;}
  bool accepted=session(a,b);closed(a);closed(b);report(a);require(a.sendBusy(),"incomplete backpressured frame retained");require(!accepted,"reject cancelled incomplete output");return;
 }
 if(std::strcmp(name,"external-abort")==0){a.pump();require(a.readPending()&&CancelIoEx(h,0),"external abort requested while Open");waitRead(a);a.pump();require(a.failure()==Endpoint::WindowsIo&&a.windowsError()==ERROR_OPERATION_ABORTED,"unrequested abort retained as real fault");require(a.drain(3000),"external abort cleanup");report(a);return;}
 throw std::runtime_error("unknown case");
}
int main(int argc,char **argv){setvbuf(stdout,0,_IONBF,0);try{require(argc==2,"case argument");run(argv[1]);std::printf("PASS %s\n",argv[1]);return 0;}catch(const std::exception &e){control.hold=false;std::printf("FAIL oracle %s\n",e.what());return 1;}}
