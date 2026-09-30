#include "common.h"
#include "admission.h"
static unsigned checks;
static void check(bool value,const char* name) { ++checks;require(value,name); }
struct Pair {
 HANDLE peer;Endpoint* server;
 Pair():peer(INVALID_HANDLE_VALUE),server(0) {
  std::string name="\\\\.\\pipe\\repair-"+nonce();
  SECURITY_ATTRIBUTES sa={sizeof sa,0,FALSE};ServerPipe pipe(name,sa);
  peer=CreateFileA(name.c_str(),GENERIC_READ|GENERIC_WRITE,0,0,OPEN_EXISTING,0,0);
  require(peer!=INVALID_HANDLE_VALUE,"test peer");pipe.connected();server=new Endpoint(pipe.take());
 }
 ~Pair(){if(peer!=INVALID_HANDLE_VALUE)CloseHandle(peer);delete server;}
 void closePeer(){CloseHandle(peer);peer=INVALID_HANDLE_VALUE;}
 void write(const std::vector<unsigned char>& data){DWORD n=0;require(WriteFile(peer,&data[0],static_cast<DWORD>(data.size()),&n,0)&&n==data.size(),"test write");}
private:Pair(const Pair&);Pair& operator=(const Pair&);
};
static std::vector<unsigned char> response() {
 MilesWire::Header h={};h.magic=MilesWire::Magic;h.version=MilesWire::Version;h.kind=MilesWire::Reply;h.opcode=MilesWire::SessionClose;h.request=1;h.lane=1;
 MilesWire::Result r={};std::vector<unsigned char> out;
 require(MilesTransport::encodeResult(h,r,MilesTransport::Bytes(),MilesTransport::Bytes(),out),"test response");return out;
}
int main(int argc,char**) {
 if(argc>1)return 7; // Benign child must remain suspended in the failure control.
 try {
  using namespace MilesCoordinator;std::vector<MilesWire::Handle> none;Coordinator owner(1);uint64_t ordinal=0;
  check(LiveBridge::admitNext(owner,1,ordinal,MilesWire::AIL_shutdown,none)==Ok,"early shutdown admitted for validation");
  check(LiveBridge::complete(owner,1,1,MilesWire::AIL_shutdown,4)==Ok && owner.state()==Active,"rejected shutdown stays active");
  check(LiveBridge::admitNext(owner,1,ordinal,MilesWire::AIL_startup,none)==Ok,"startup still ordinary admission");
  check(LiveBridge::complete(owner,1,2,MilesWire::AIL_startup,0)==Ok && owner.state()==Active,"startup does not drain");
  check(LiveBridge::admitNext(owner,1,ordinal,MilesWire::AIL_shutdown,none)==Ok,"shutdown validation admission");
  check(LiveBridge::complete(owner,1,3,MilesWire::AIL_shutdown,3)==Ok && owner.state()==Active,"bad fields cannot drain");
  check(LiveBridge::admitNext(owner,1,ordinal,MilesWire::AIL_shutdown,none)==Ok,"ready shutdown admission");
  check(LiveBridge::complete(owner,1,4,MilesWire::AIL_shutdown,0)==Ok && owner.state()==Draining,"only success drains model");
  check(LiveBridge::admitNext(owner,1,ordinal,MilesWire::AIL_startup,none)==WrongState && ordinal==4,"no cleanup escalation or ordinal consumption");
  check(LiveBridge::admitNext(owner,1,ordinal,MilesWire::SessionClose,none)==Ok,"explicit session close cleanup");
  check(LiveBridge::complete(owner,1,5,MilesWire::SessionClose,0)==Ok,"complete close model");
  for(unsigned kind=0;kind<2;++kind) {
   Pair command,callback;command.write(response());
   if(!kind)callback.closePeer();else callback.write(std::vector<unsigned char>(48,0));
   bool failed=false;try{receive(*command.server,callback.server);}catch(const std::runtime_error&){failed=true;}
   check(failed,"callback fault wins over command ready");
   check(callback.server->failure()==(!kind?Endpoint::PeerClosed:Endpoint::InvalidLength),"actual callback fault classified");
   failed=false;try{drainSession(*command.server,*callback.server,false);}catch(const std::runtime_error&){failed=true;}
   check(failed,"drain does not erase prior fault");
  }
  {
   Pair command,callback;command.write(response());callback.closePeer();
   std::vector<unsigned char> frame=receive(*command.server,callback.server,true);
   MilesWire::Header h={};MilesWire::Result r={};
   check(MilesTransport::decodeResult(bytes(frame),h,r)&&h.opcode==MilesWire::SessionClose&&!r.transport_status,"ordered final reply still validated");
   command.closePeer();drainSession(*command.server,*callback.server,true);
   check(command.server->state()==Endpoint::Closed&&callback.server->state()==Endpoint::Closed,"ordered peer close accepted");
  }
  {
   Pair command,callback;command.write(response());callback.write(std::vector<unsigned char>(48,0));
   bool failed=false;try{receive(*command.server,callback.server,true);}catch(const std::runtime_error&){failed=true;}
   check(failed&&callback.server->failure()==Endpoint::InvalidLength,"ordered boundary cannot mask corruption");
  }
  HANDLE observed=0,process=0,thread=0,job=0;bool rejected=false;
  {
   ChildProcess child;char path[MAX_PATH];require(GetModuleFileNameA(0,path,MAX_PATH)!=0,"self path");
   std::string args="\""+std::string(path)+"\" --child";std::vector<char> line(args.begin(),args.end());line.push_back(0);child.create(path,&line[0]);
   process=child.info.hProcess;thread=child.info.hThread;job=child.job;
   require(DuplicateHandle(GetCurrentProcess(),process,GetCurrentProcess(),&observed,SYNCHRONIZE|PROCESS_QUERY_INFORMATION,FALSE,0)!=0,"observe child");
   try{child.assignAndResume(0);}catch(const std::runtime_error&){rejected=true;}
  }
  DWORD exitCode=0,flags=0;
  check(rejected,"actual invalid job rejected");
  check(WaitForSingleObject(observed,0)==WAIT_OBJECT_0&&GetExitCodeProcess(observed,&exitCode)&&exitCode==90,"suspended child terminated before execution");
  check(!GetHandleInformation(process,&flags)&&GetLastError()==ERROR_INVALID_HANDLE,"process owner handle closed");
  check(!GetHandleInformation(thread,&flags)&&GetLastError()==ERROR_INVALID_HANDLE,"thread owner handle closed");
  check(!GetHandleInformation(job,&flags)&&GetLastError()==ERROR_INVALID_HANDLE,"job owner handle closed");CloseHandle(observed);
  printf("PASS %u repair checks; synthetic policy, real pipes and benign process only\n",checks);return checks==25?0:2;
 }catch(const std::exception& e){printf("FAILED %s\n",e.what());return 1;}
}
