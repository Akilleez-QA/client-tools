// Include unchanged actual implementation: exposes actual private proxy types,
// not copied type definitions or a rewritten validator.
#include "tree/backend-boundary24/pipe/ClientMilesPipe.cpp"
#include "tree/session-file-admission34/coordinator.h"
#include <cstdio>
#include <sstream>
#include <new>
using namespace ClientMilesPipe;
static unsigned checks=0;
#define CHECK(x) do{++checks;if(!(x)){std::printf("FAIL %d: %s\n",__LINE__,#x);throw std::runtime_error("check");}}while(0)
static MilesWire::Handle handle(uint32_t kind,uint32_t slot){MilesWire::Handle h={kind,slot,1};return h;}
static std::string snapshot(const Session &s,bool flags=true){
 std::ostringstream out;if(flags)out<<s.started<<s.stopped<<s.uncertain();out<<s.driver.get()<<s.samples.get();
 if(s.driver)out<<s.driver->wire.kind<<','<<s.driver->wire.slot<<','<<s.driver->wire.generation<<s.driver->owner;
 for(auto i=s.samples->proxies.begin();i!=s.samples->proxies.end();++i)out<<i->get()<<(*i)->live<<(*i)->wire.kind<<','<<(*i)->wire.slot<<','<<(*i)->wire.generation;
 for(auto i=s.samples->streams.begin();i!=s.samples->streams.end();++i)out<<i->get()<<(*i)->live<<(*i)->wire.kind<<','<<(*i)->wire.slot<<','<<(*i)->wire.generation<<(*i)->borrowed.live<<(*i)->borrowed.wire.kind<<','<<(*i)->borrowed.wire.slot<<','<<(*i)->borrowed.wire.generation;
 return out.str();
}
static void checkPure(Session &s,uint32_t op,const MilesWire::Call &c,const StartupBridge::OwnedReply &r,bool expected){
 const std::string before=snapshot(s);const MilesWire::Call original=c;const MilesWire::Result originalResult=r.result;const auto text=r.text;
 CHECK(s.validateReply(op,c,r)==expected);CHECK(snapshot(s)==before);
 CHECK(!std::memcmp(&original,&c,sizeof c));CHECK(!std::memcmp(&originalResult,&r.result,sizeof originalResult));CHECK(text==r.text);
}
struct Supplier:Channel {
 unsigned returnedObservations,completed;unsigned mode;
 MilesCoordinator::Coordinator coordinator;
 Supplier():returnedObservations(0),completed(0),mode(0),coordinator(77){CHECK(coordinator.registerSessionFiles(77,1)==MilesCoordinator::Ok);}
 StartupBridge::OwnedReply call(uint32_t opcode,const MilesWire::Call &fields,MilesTransport::Bytes,
     const std::vector<MilesWire::Handle> &resources,const Session &owner) override {
  // SCRIPTED PHASE ORDER, not actual LiveChannel execution. Real codec, owner
  // validator and coordinator are used; no real Runtime::returned is substituted.
  CHECK(coordinator.admitGame(77,completed+1,1,0,MilesCoordinator::Ordinary,resources)==MilesCoordinator::Ok);
  MilesCoordinator::CallbackId cb={};CHECK(coordinator.admitCallback(77,1,MilesCoordinator::CausalReverseIo,completed+1,cb)==MilesCoordinator::Ok);
  MilesWire::Header h={};h.magic=MilesWire::Magic;h.version=MilesWire::Version;h.kind=MilesWire::Request;h.opcode=opcode;h.request=completed+10;h.lane=1;
  MilesWire::Header rh=h;rh.kind=MilesWire::Reply;MilesWire::Result r={};
  if(mode==1)r.transport_status=StartupBridge::Unsupported;
  else {r.value[0]=mode==2?99:0;r.value[1]=42;}
  std::vector<unsigned char> bytes;CHECK(MilesTransport::encodeResult(rh,r,MilesTransport::Bytes(),MilesTransport::Bytes(),bytes));
  StartupBridge::OwnedReply reply;CHECK(StartupBridge::decodeReply(MilesTransport::Bytes(bytes.data(),bytes.size()),h,reply));
  if(!owner.validateReply(opcode,fields,reply)){coordinator.fail(77);throw std::runtime_error("rejected before observation");}
  ++returnedObservations;
  CHECK(coordinator.completeAdmission(77,completed+1)==MilesCoordinator::PendingCallback);
  MilesCoordinator::Readiness pins={};CHECK(coordinator.readiness(77,1,pins)==MilesCoordinator::Ok);
  CHECK(pins.requestPins==1 && pins.callbackPins==1);
  CHECK(coordinator.acknowledge(77,cb)==MilesCoordinator::Ok);
  CHECK(coordinator.completeAdmission(77,completed+1)==MilesCoordinator::Ok);++completed;
  return reply;
 }
 void finish() override {throw std::logic_error("no teardown workload");}
};
int main(){try{
 Supplier supplier;MilesClientRuntime53::Runtime unavailable;
 // One actual Session constructor; no terminal destructor executed. Its only
 // private shared_ptr receives an empty pin. Public proxy allocations are freed
 // explicitly at end, not claimed as production lifecycle/Session destruction.
 alignas(Session) static unsigned char storage[sizeof(Session)];
 Session &s=*new(storage) Session(&supplier,unavailable,std::shared_ptr<void>());s.started=true;
 s.driver.reset(new ClientMiles::DigitalDriver);s.driver->wire=handle(MilesWire::Driver,1);s.driver->owner=&s;
 std::unique_ptr<ClientMiles::Sample> sample(new ClientMiles::Sample);sample->wire=handle(MilesWire::OwnedSample,2);sample->live=true;
 ClientMiles::Sample *owned=sample.get();s.samples->proxies.push_back(std::move(sample));
 for(unsigned i=0;i<2;++i){std::unique_ptr<ClientMiles::OwnedStream> stream(new ClientMiles::OwnedStream);stream->wire=handle(MilesWire::Stream,3+i);stream->live=true;s.samples->streams.push_back(std::move(stream));}
 const uint32_t ops[]={MilesWire::AIL_sample_ms_position,MilesWire::AIL_stream_ms_position,MilesWire::AIL_sample_volume_levels,MilesWire::AIL_sample_reverb_levels};
 for(unsigned op:ops)for(uint32_t mask=0;mask<9;++mask){
  MilesWire::Call c={};c.output_mask=mask;StartupBridge::OwnedReply r;
  const bool expectedMask=(mask==0 || mask==1 || mask==2 || mask==3 || mask==7);
  checkPure(s,op,c,r,expectedMask);
  if(!expectedMask)continue;
  r.result.value[0]=(mask&1)?0x80000000u:0;r.result.value[1]=(mask&2)?((mask&4)?0x80000000u:17):0;checkPure(s,op,c,r,true);
  if(!(mask&1)){r.result.value[0]=1;checkPure(s,op,c,r,false);r.result.value[0]=0;}
  if(!(mask&2)){r.result.value[1]=1;checkPure(s,op,c,r,false);}
  if(mask&4){r.result.value[1]=18;checkPure(s,op,c,r,false);}
 }
 std::puts("PASS real validator pair topology and bit preservation");
 auto first=s.samples->streams.begin();ClientMiles::OwnedStream &parent=**first;ClientMiles::OwnedStream &other=**(++first);
 MilesWire::Call c={};c.target=parent.wire;StartupBridge::OwnedReply r;r.result.value[0]=c.target.kind;r.result.value[1]=c.target.slot;r.result.value[2]=c.target.generation;
 checkPure(s,MilesWire::AIL_stream_sample_handle,c,r,true);r.result.resource=handle(MilesWire::BorrowedSample,5);checkPure(s,MilesWire::AIL_stream_sample_handle,c,r,true);
 ++r.result.value[2];checkPure(s,MilesWire::AIL_stream_sample_handle,c,r,false);--r.result.value[2];
 parent.live=false;checkPure(s,MilesWire::AIL_stream_sample_handle,c,r,false);parent.live=true;
 parent.borrowed.live=true;parent.borrowed.wire=r.result.resource;checkPure(s,MilesWire::AIL_stream_sample_handle,c,r,true);
 ++r.result.resource.slot;checkPure(s,MilesWire::AIL_stream_sample_handle,c,r,false);--r.result.resource.slot;
 r.result.resource=MilesWire::Handle();checkPure(s,MilesWire::AIL_stream_sample_handle,c,r,false);
 parent.borrowed.live=false;r.result.resource=handle(MilesWire::BorrowedSample,5);other.borrowed.live=true;other.borrowed.wire=r.result.resource;checkPure(s,MilesWire::AIL_stream_sample_handle,c,r,false);other.borrowed.live=false;
 std::puts("PASS actual proxy alias echo stability uniqueness and null transitions");
 for(unsigned kind=0;kind<2;++kind){StartupBridge::OwnedReply allocation;MilesWire::Call input={};uint32_t op=kind?MilesWire::AIL_open_stream:MilesWire::AIL_allocate_sample_handle;
  checkPure(s,op,input,allocation,true);allocation.result.resource=kind?parent.wire:owned->wire;checkPure(s,op,input,allocation,false);
  if(kind)parent.live=false;else owned->live=false;
  checkPure(s,op,input,allocation,true); // Existing unpublished reservation is not a live duplicate.
  if(kind)parent.live=true;else owned->live=true;
  allocation.result.resource.slot=20;checkPure(s,op,input,allocation,true);}
 StartupBridge::OwnedReply driver;driver.result.resource=s.driver->wire;MilesWire::Call input={};checkPure(s,MilesWire::AIL_open_digital_driver,input,driver,false);
 std::puts("PASS duplicate allocation identities refused without publication");
 int32_t output=-9;
 ClientMiles::sample_ms_position(owned,0,&output);CHECK(output==42 && supplier.returnedObservations==1 && supplier.completed==1);
 output=-10;supplier.mode=1;bool refused=false;try{ClientMiles::sample_ms_position(owned,0,&output);}catch(const ClientMiles::Failure &){refused=true;}
 CHECK(refused && output==-10 && supplier.returnedObservations==2 && supplier.completed==2 && !s.uncertain());
 std::puts("PASS actual facade writes after scripted coordinator ACK join and refusal observation");
 const std::string before=snapshot(s,false);const MilesWire::Handle oldWire=owned->wire;output=-11;supplier.mode=2;bool rejected=false;
 try{ClientMiles::sample_ms_position(owned,0,&output);}catch(const ClientMiles::Failure &){rejected=true;}
 CHECK(rejected && output==-11 && supplier.returnedObservations==2 && supplier.completed==2);
 CHECK(s.uncertain() && unavailable.failures==1 && owned->wire.slot==oldWire.slot && owned->live);
 MilesCoordinator::Readiness pins={};CHECK(supplier.coordinator.readiness(77,1,pins)==MilesCoordinator::Ok);
 CHECK(pins.requestPins==1 && pins.callbackPins==1 && supplier.coordinator.activeAdmission()==3 && supplier.coordinator.state()==MilesCoordinator::Failed);
 CHECK(snapshot(s,false)==before); // Fault flag alone changed; all proxy state retained.
 std::puts("PASS malformed pair retains actual coordinator admission and callback pins");
 s.driver.reset();s.samples.reset();
 std::printf("PASS %u checks; portable validator and scripted phase only\n",checks);return 0;
}catch(...){return 1;}}
