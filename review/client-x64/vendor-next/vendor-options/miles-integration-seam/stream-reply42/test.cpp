#define main inherited_scenarios_not_run
#include "../stream-tests39/stream_test.cpp"
#undef main
struct Fault : Script {
 unsigned bad;
 explicit Fault(unsigned n):bad(n){}
 StartupBridge::OwnedReply call(uint32_t op,const Call &input,MilesTransport::Bytes text) override {
  StartupBridge::OwnedReply r=Script::call(op,input,text);
  if((bad==0 && op==AIL_open_stream) || (bad==1 && op==AIL_stream_sample_handle) || (bad>=2 && op==AIL_start_stream)) {
   if(bad==0)r.result.resource.kind=Driver;
   if(bad==1)r.result.resource.kind=OwnedSample;
   if(bad==2)r.result.return_bits=1;
   if(bad==3)r.result.value[7]=1;
   Header h={};h.magic=Magic;h.version=Version;h.kind=Request;h.opcode=op;h.request=calls;h.lane=1;
   Header reply=h;reply.kind=Reply;std::vector<unsigned char> frame;
   CHECK(MilesTransport::encodeResult(reply,r.result,MilesTransport::Bytes(),MilesTransport::Bytes(),frame));
   StartupBridge::OwnedReply out;
   if(!StartupBridge::decodeReply(MilesTransport::Bytes(&frame[0],frame.size()),h,out))throw std::runtime_error("malformed reply rejected");
   return out;
  }
  return r;
 }
};
int main(){try {
 for(unsigned m=0;m<4;++m){
  Fault *s=new Fault(m);ClientMilesPipe::Session session{std::unique_ptr<ClientMilesPipe::Channel>(s)};auto d=start();
  ClientMiles::HSTREAM stream=0;
  if(m==0){fails([&]{stream=open(*s,d);},ClientMiles::FailureReason::BackendFailed);CHECK(!stream);}
  else {
   stream=open(*s,d);
   if(m==1){s->want(AIL_stream_sample_handle,Handle{Stream,2,1});ClientMiles::HSAMPLE out=0;fails([&]{out=ClientMiles::stream_sample_handle(stream);},ClientMiles::FailureReason::BackendFailed);CHECK(!out);}
   else {s->want(AIL_start_stream,Handle{Stream,2,1});fails([&]{ClientMiles::start_stream(stream);},ClientMiles::FailureReason::BackendFailed);}
  }
  CHECK(session.uncertain());unsigned n=s->calls;fails([&]{open(*s,d);},ClientMiles::FailureReason::BackendFailed);CHECK(s->calls==n);
  std::printf("PASS malformed reply scenario %u\n",m);
 }
 return 0;
}catch(const std::exception &e){std::printf("FAIL %s\n",e.what());return 1;}}
