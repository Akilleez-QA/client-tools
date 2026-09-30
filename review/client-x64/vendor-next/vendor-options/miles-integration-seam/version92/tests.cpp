#include "tree/backend-boundary24/pipe/PipeCore.cpp"
#include <cstdio>
#include <new>
namespace C=ClientMilesPipeCore57;
using ClientMilesPipe::Session;
static bool oracleFailed=false;
static unsigned checks=0;
#define CHECK(x) do {++checks;if(!(x)){oracleFailed=true;throw std::runtime_error("oracle line " + std::to_string(__LINE__));}} while(0)
struct Supplier:ClientMilesPipe::Channel {
 unsigned calls,settled;uint32_t expectedCapacity;std::string mode;std::vector<unsigned char> prefix;
 Supplier():calls(0),settled(0),expectedCapacity(0){}
 StartupBridge::OwnedReply call(uint32_t op,const MilesWire::Call &c,MilesTransport::Bytes text,
 const std::vector<MilesWire::Handle> &resources,const Session &session) override {
  ++calls;CHECK(op==MilesWire::SessionVersion);CHECK(c.value[0]==expectedCapacity);
  for(unsigned i=1;i<8;++i)CHECK(c.value[i]==0);
  CHECK(!c.target.kind&&!c.target.slot&&!c.target.generation&&!c.resource.kind&&!c.resource.slot&&!c.resource.generation);
  CHECK(!c.output_mask&&!c.callback&&!c.reserved&&!c.bytes.offset&&!c.bytes.length&&!c.text.offset&&!c.text.length);
  CHECK(text.size==0&&resources.empty());
  MilesWire::Header h={};h.magic=MilesWire::Magic;h.version=MilesWire::Version;h.kind=MilesWire::Request;
  h.opcode=op;h.request=calls;h.lane=1;
  MilesWire::Call encodedCall=c;std::vector<unsigned char> request;
  CHECK(MilesTransport::encodeCall(h,encodedCall,MilesTransport::Bytes(),MilesTransport::Bytes(),request));
  // Independent fixed header/call byte offset: value0 begins at48+24=72.
  CHECK(request.size()==136);CHECK(request[72]==(expectedCapacity&255u));
  CHECK(request[73]==((expectedCapacity>>8)&255u));CHECK(request[74]==((expectedCapacity>>16)&255u));CHECK(request[75]==((expectedCapacity>>24)&255u));
  MilesWire::Header parsed={};uint32_t cap=0;
  CHECK(MilesSessionVersion::validateQuery(MilesTransport::Bytes(request.data(),request.size()),parsed,cap));CHECK(cap==expectedCapacity);
  MilesWire::Header reply=h;reply.kind=MilesWire::Reply;if(mode=="context")++reply.request;
  MilesWire::Result r={};if(mode=="callback")r.callback=1;
  std::vector<unsigned char> bytes=prefix,txt;
  if(mode=="oversize") {bytes.assign(expectedCapacity+1,'Q');bytes.back()=0;}
  if(mode=="nonterminated")bytes.back()='Q';
  if(mode=="missing")bytes.clear();
  if(mode=="legacy_text"){txt=bytes;bytes.clear();}
  std::vector<unsigned char> frame;
  CHECK(MilesTransport::encodeResult(reply,r,MilesTransport::Bytes(bytes.data(),bytes.size()),MilesTransport::Bytes(txt.data(),txt.size()),frame));
  StartupBridge::OwnedReply out;
  if(!StartupBridge::decodeReply(MilesTransport::Bytes(frame.data(),frame.size()),h,out))throw std::runtime_error("wire rejected");
  if(!session.validateReply(op,c,out))throw std::runtime_error("owner rejected");
  ++settled; // Scripted checkpoint only: no real Runtime join or LiveChannel.
  return out;
 }
 void finish() override {throw std::logic_error("no teardown");}
};
template<class F> static void rejects(F fn){bool caught=false;try{fn();}catch(const C::Failure&){caught=true;}CHECK(!oracleFailed);CHECK(caught);}
static void exercise(Supplier &supplier,int capacity,const std::vector<unsigned char> &prefix) {
 supplier.expectedCapacity=static_cast<uint32_t>(capacity);supplier.prefix=prefix;
 std::vector<unsigned char> buffer(static_cast<size_t>(capacity)+16,0xa5),expected=buffer;
 std::copy(prefix.begin(),prefix.end(),expected.begin()+8);
 C::MSS_version(reinterpret_cast<char *>(buffer.data()+8),capacity);
 CHECK(buffer==expected);CHECK(!oracleFailed);
}
int main(int argc,char **argv){try{
 CHECK(argc==2);const std::string mode=argv[1];Supplier supplier;MilesClientRuntime53::Runtime runtime;
 alignas(Session) static unsigned char storage[sizeof(Session)];
 Session &s=*new(storage) Session(&supplier,runtime,std::shared_ptr<void>());
 if(mode=="normal"){
  // Literal observations from own-resource84, not production capacity predicates.
  const int caps[]={1,2,4,6,7,11,256};const char *outputs[]={"","A","ABC","ABCDE","ABCDEF","ABCDEF","ABCDEF"};
  for(unsigned i=0;i<7;++i){std::vector<unsigned char> p(outputs[i],outputs[i]+std::strlen(outputs[i])+1);exercise(supplier,caps[i],p);}
  exercise(supplier,256,std::vector<unsigned char>(1,0));
  const unsigned char inner[]={'A',0,'B',0};exercise(supplier,11,std::vector<unsigned char>(inner,inner+4));
  // Independent reviewed wire budget:1MiB minus48-byte header and80-byte result.
  const int largest=1048448;std::vector<unsigned char> full(static_cast<size_t>(largest),'Z');full.back()=0;exercise(supplier,largest,full);
  unsigned calls=supplier.calls;unsigned char untouched[32];std::memset(untouched,0x67,sizeof untouched);
  rejects([&]{C::MSS_version(0,1);});rejects([&]{C::MSS_version(reinterpret_cast<char*>(untouched),0);});
  rejects([&]{C::MSS_version(reinterpret_cast<char*>(untouched),-1);});rejects([&]{C::MSS_version(reinterpret_cast<char*>(untouched),1048449);});
  CHECK(supplier.calls==calls);for(unsigned i=0;i<32;++i)CHECK(untouched[i]==0x67);
  CHECK(!s.started&&!s.uncertain());CHECK(supplier.settled==10);
  s.stopped=true;rejects([&]{C::MSS_version(reinterpret_cast<char*>(untouched),1);});CHECK(supplier.calls==calls);
 }else{
  CHECK(mode=="oversize"||mode=="nonterminated"||mode=="missing"||mode=="legacy_text"||mode=="callback"||mode=="context");
  supplier.mode=mode;supplier.expectedCapacity=2;supplier.prefix.assign(2,0);supplier.prefix[0]='A';
  unsigned char destination[18];std::memset(destination,0x67,sizeof destination);
  rejects([&]{C::MSS_version(reinterpret_cast<char*>(destination+8),2);});
  for(unsigned i=0;i<18;++i)CHECK(destination[i]==0x67);
  CHECK(supplier.calls==1&&supplier.settled==0&&s.uncertain()&&runtime.failures==1);
  rejects([&]{C::MSS_version(reinterpret_cast<char*>(destination+8),2);});CHECK(supplier.calls==1);
 }
 s.samples.reset();std::string().swap(s.lastErrorSnapshot);std::string().swap(s.redistSnapshot);
 std::printf("PASS %s checks=%u\n",mode.c_str(),checks);return 0;
 }catch(const std::exception &e){std::fprintf(stderr,"FAIL %s\n",e.what());return 1;}}
