// Actual81 implementation; only Runtime dependency and Channel transport are substituted.
#include "tree/backend-boundary24/pipe/PipeCore.cpp"
#include <cstdio>
#include <new>
namespace C=ClientMilesPipeCore57;
using ClientMilesPipe::Session;
unsigned checks=0;
#define CHECK(x) do { ++checks; if(!(x)) {std::printf("FAIL line=%d %s\n",__LINE__,#x);throw std::runtime_error("check failed");} } while(0)
struct Supplier:ClientMilesPipe::Channel {
 unsigned calls; bool isNull,refuse,malformed;std::string value,input; Session *owner;
 Supplier():calls(0),isNull(false),refuse(false),malformed(false),owner(0){}
 StartupBridge::OwnedReply call(uint32_t op,const MilesWire::Call &fields,MilesTransport::Bytes text,
   const std::vector<MilesWire::Handle> &,const Session &session) override {
  ++calls;input=text.size?std::string(reinterpret_cast<const char*>(text.data),text.size):std::string();
  MilesWire::Header request={};request.magic=MilesWire::Magic;request.version=MilesWire::Version;
  request.kind=MilesWire::Request;request.opcode=op;request.request=calls;request.lane=1;
  MilesWire::Header h=request;h.kind=MilesWire::Reply;MilesWire::Result result={};
  if(refuse)result.transport_status=StartupBridge::Unsupported;
  else if(isNull)result.null_mask=MilesStartup::TextNull;
  std::vector<unsigned char> body;
  if(!refuse&&!isNull){body.assign(value.begin(),value.end());body.push_back(0);}
  if(malformed)result.callback=1;
  std::vector<unsigned char> frame;
  CHECK(MilesTransport::encodeResult(h,result,MilesTransport::Bytes(),MilesTransport::Bytes(body.data(),body.size()),frame));
  StartupBridge::OwnedReply out;
  if(!StartupBridge::decodeReply(MilesTransport::Bytes(frame.data(),frame.size()),request,out))throw std::runtime_error("actual decoder rejected reply");
  CHECK(session.validateReply(op,fields,out));
  // Completion is scripted, not LiveChannel/Runtime ACK or worker behavior.
  return out;
 }
 void finish() override {throw std::logic_error("no teardown");}
};
template<class F> void rejects(F f){bool failed=false;try{f();}catch(const C::Failure&){failed=true;}CHECK(failed);}
int main(){try{
 Supplier supplier;MilesClientRuntime53::Runtime runtime;
 alignas(Session) static unsigned char storage[sizeof(Session)];
 Session &s=*new(storage) Session(&supplier,runtime,std::shared_ptr<void>());
 supplier.value="prestart";CHECK(std::string(C::set_redist_directory(""))=="prestart");CHECK(supplier.input==std::string(1,'\0'));
 unsigned calls=supplier.calls;rejects([]{C::last_error();});CHECK(supplier.calls==calls);
 s.started=true;
 for(unsigned mode=0;mode<3;++mode){supplier.isNull=mode==0;supplier.value=mode==2?std::string(200,'x'):"";
  const char *p=C::last_error();CHECK((p==0)==supplier.isNull);if(p)CHECK(std::string(p)==supplier.value);
  const char *q=C::set_redist_directory("directory");CHECK((q==0)==supplier.isNull);if(q)CHECK(std::string(q)==supplier.value);
  if(p)CHECK(std::string(p)==supplier.value);
 }
 std::puts("PASS native-shaped-null-empty-text");
 supplier.isNull=false;supplier.value="redist-owned";const char *redist=C::set_redist_directory("original");
 supplier.value=std::string(170,'e');const char *error=C::last_error();CHECK(std::string(redist)=="redist-owned");
 supplier.value="replacement";CHECK(std::string(C::set_redist_directory(redist))=="replacement");CHECK(supplier.input==std::string("redist-owned\0",13));CHECK(std::string(error)==std::string(170,'e'));
 redist=s.redistSnapshot.c_str();supplier.value="new error";C::last_error();CHECK(redist==s.redistSnapshot.c_str()&&std::string(redist)=="replacement");
 std::puts("PASS independent-snapshot-lifetimes");
 const std::string good(MilesStartup::RequestTextLimit-1,'p'),bad(MilesStartup::RequestTextLimit,'q');
 supplier.value="at-limit";C::set_redist_directory(good.c_str());CHECK(supplier.input.size()==MilesStartup::RequestTextLimit);CHECK(supplier.input==good+std::string(1,'\0'));
 calls=supplier.calls;std::string beforeError=s.lastErrorSnapshot,beforeRedist=s.redistSnapshot;
 rejects([&]{C::set_redist_directory(bad.data());});rejects([]{C::set_redist_directory(0);});CHECK(supplier.calls==calls);CHECK(s.lastErrorSnapshot==beforeError&&s.redistSnapshot==beforeRedist);
 std::puts("PASS bounded-directory-before-send");
 supplier.refuse=true;rejects([]{C::last_error();});rejects([]{C::set_redist_directory("valid");});CHECK(!s.uncertain());CHECK(s.lastErrorSnapshot==beforeError&&s.redistSnapshot==beforeRedist);supplier.refuse=false;
 calls=supplier.calls;{MilesCallbackGuard47::Scope guard;bool denied=false;try{C::last_error();}catch(const MilesCallbackGuard47::ReentryDenied&){denied=true;}CHECK(denied&&guard.violated());}CHECK(supplier.calls==calls);
 s.stopped=true;rejects([]{C::last_error();});rejects([]{C::set_redist_directory("valid");});CHECK(supplier.calls==calls);s.stopped=false;
 CHECK(s.lastErrorSnapshot==beforeError&&s.redistSnapshot==beforeRedist);
 std::puts("PASS refused-and-forbidden-calls-preserve-snapshots");
 supplier.malformed=true;rejects([]{C::last_error();});CHECK(s.uncertain()&&runtime.failures==1);CHECK(s.lastErrorSnapshot==beforeError&&s.redistSnapshot==beforeRedist);
 calls=supplier.calls;rejects([]{C::last_error();});rejects([]{C::set_redist_directory("valid");});CHECK(supplier.calls==calls);
 std::puts("PASS malformed-reply-retains-snapshots");
 // Synthetic owner storage only; no real Session destructor or engine/vendor teardown.
 s.samples.reset();std::string().swap(s.lastErrorSnapshot);std::string().swap(s.redistSnapshot);
 std::printf("PASS assertions=%u\n",checks);return 0;
 }catch(const std::exception &e){std::fprintf(stderr,"FAIL %s\n",e.what());return 1;}}
