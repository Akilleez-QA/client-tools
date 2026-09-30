// Actual81 implementation; only Runtime dependency and Channel transport are substituted.
#include "tree/backend-boundary24/pipe/PipeCore.cpp"
#include <cstdio>
#include <new>
namespace C=ClientMilesPipeCore57;
using ClientMilesPipe::Session;
unsigned checks=0; bool anyCheckFailed=false;
#define CHECK(x) do { ++checks; if(!(x)) {anyCheckFailed=true;std::printf("FAIL line=%d %s\n",__LINE__,#x);throw std::runtime_error("check failed");} } while(0)
struct Supplier:ClientMilesPipe::Channel {
 unsigned calls; uint32_t expectedOp; bool isNull,refuse,malformed;std::string value,input; Session *owner;
 Supplier():calls(0),expectedOp(0),isNull(false),refuse(false),malformed(false),owner(0){}
 StartupBridge::OwnedReply call(uint32_t op,const MilesWire::Call &fields,MilesTransport::Bytes text,
   const std::vector<MilesWire::Handle> &,const Session &session) override {
  ++calls;CHECK(op==expectedOp);
  CHECK(!fields.target.kind&&!fields.target.slot&&!fields.target.generation);
  CHECK(!fields.resource.kind&&!fields.resource.slot&&!fields.resource.generation);
  CHECK(!fields.bytes.offset&&!fields.bytes.length&&!fields.text.offset&&!fields.text.length);
  CHECK(!fields.output_mask&&!fields.callback&&!fields.reserved);
  for(unsigned i=0;i<8;++i)CHECK(fields.value[i]==0);
  if(expectedOp==MilesWire::AIL_last_error)CHECK(text.size==0);
  else {CHECK(text.size>0&&text.data);CHECK(text.data[text.size-1]==0);CHECK(!std::memchr(text.data,0,text.size-1));}
  input=text.size?std::string(reinterpret_cast<const char*>(text.data),text.size):std::string();
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
template<class F> void rejects(F f){bool failed=false;try{f();}catch(const C::Failure&){failed=true;}CHECK(!anyCheckFailed);CHECK(failed);}
const char *invokeLast(Supplier &s){s.expectedOp=MilesWire::AIL_last_error;return C::last_error();}
const char *invokeRedist(Supplier &s,const char *p){s.expectedOp=MilesWire::AIL_set_redist_directory;return C::set_redist_directory(p);}
int main(){try{
 Supplier supplier;MilesClientRuntime53::Runtime runtime;
 alignas(Session) static unsigned char storage[sizeof(Session)];
 Session &s=*new(storage) Session(&supplier,runtime,std::shared_ptr<void>());
 supplier.value="prestart";CHECK(std::string(invokeRedist(supplier,""))=="prestart");CHECK(supplier.input==std::string(1,'\0'));
 unsigned calls=supplier.calls;rejects([&]{invokeLast(supplier);});CHECK(supplier.calls==calls);
 s.started=true;
 for(unsigned mode=0;mode<3;++mode){supplier.isNull=mode==0;supplier.value=mode==2?std::string(200,'x'):"";
  const char *p=invokeLast(supplier);CHECK((p==0)==supplier.isNull);if(p)CHECK(std::string(p)==supplier.value);
  const char *q=invokeRedist(supplier,"directory");CHECK((q==0)==supplier.isNull);if(q)CHECK(std::string(q)==supplier.value);
  if(p)CHECK(std::string(p)==supplier.value);
 }
 std::puts("PASS native-shaped-null-empty-text");
 supplier.isNull=false;supplier.value="redist-owned";const char *redist=invokeRedist(supplier,"original");
 supplier.value=std::string(170,'e');const char *error=invokeLast(supplier);CHECK(std::string(redist)=="redist-owned");
 supplier.value="replacement";CHECK(std::string(invokeRedist(supplier,redist))=="replacement");CHECK(supplier.input==std::string("redist-owned\0",13));CHECK(std::string(error)==std::string(170,'e'));
 redist=s.redistSnapshot.c_str();supplier.value="new error";invokeLast(supplier);CHECK(redist==s.redistSnapshot.c_str()&&std::string(redist)=="replacement");
 std::puts("PASS independent-snapshot-lifetimes");
 const std::string good(MilesStartup::RequestTextLimit-1,'p');
 std::unique_ptr<char[]> bad(new char[MilesStartup::RequestTextLimit]);std::memset(bad.get(),'q',MilesStartup::RequestTextLimit);
 supplier.value="at-limit";invokeRedist(supplier,good.c_str());CHECK(supplier.input.size()==MilesStartup::RequestTextLimit);CHECK(supplier.input==good+std::string(1,'\0'));
 calls=supplier.calls;std::string beforeError=s.lastErrorSnapshot,beforeRedist=s.redistSnapshot;
 rejects([&]{invokeRedist(supplier,bad.get());});rejects([&]{invokeRedist(supplier,0);});CHECK(supplier.calls==calls);CHECK(s.lastErrorSnapshot==beforeError&&s.redistSnapshot==beforeRedist);
 std::puts("PASS bounded-directory-before-send");
 supplier.refuse=true;rejects([&]{invokeLast(supplier);});rejects([&]{invokeRedist(supplier,"valid");});CHECK(!s.uncertain());CHECK(s.lastErrorSnapshot==beforeError&&s.redistSnapshot==beforeRedist);supplier.refuse=false;
 calls=supplier.calls;{MilesCallbackGuard47::Scope guard;bool denied=false;try{invokeLast(supplier);}catch(const MilesCallbackGuard47::ReentryDenied&){denied=true;}CHECK(denied&&guard.violated());}CHECK(supplier.calls==calls);
 s.stopped=true;rejects([&]{invokeLast(supplier);});rejects([&]{invokeRedist(supplier,"valid");});CHECK(supplier.calls==calls);s.stopped=false;
 CHECK(s.lastErrorSnapshot==beforeError&&s.redistSnapshot==beforeRedist);
 std::puts("PASS refused-and-forbidden-calls-preserve-snapshots");
 supplier.malformed=true;rejects([&]{invokeLast(supplier);});CHECK(s.uncertain()&&runtime.failures==1);CHECK(s.lastErrorSnapshot==beforeError&&s.redistSnapshot==beforeRedist);
 calls=supplier.calls;rejects([&]{invokeLast(supplier);});rejects([&]{invokeRedist(supplier,"valid");});CHECK(supplier.calls==calls);
 std::puts("PASS malformed-reply-retains-snapshots");
 // Synthetic owner storage only; no real Session destructor or engine/vendor teardown.
 s.samples.reset();std::string().swap(s.lastErrorSnapshot);std::string().swap(s.redistSnapshot);
 std::printf("PASS assertions=%u\n",checks);return 0;
 }catch(const std::exception &e){std::fprintf(stderr,"FAIL %s\n",e.what());return 1;}}
