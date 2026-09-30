#include "../backend-boundary24/pipe/Session.h"
#include "../native-stream28/ClientMilesStream.h"
#include "../native-playback28/ClientMilesPlayback.h"
#include <cstdio>
#include <cstring>
#include <climits>
#include <stdexcept>
using namespace MilesWire;
static unsigned checks=0;
#define CHECK(x) do{++checks;if(!(x))throw std::runtime_error(#x);}while(0)
struct Script:ClientMilesPipe::Channel {
 unsigned calls,expected,mask;uint32_t values[8],status,returned,pair[2],generation,aliasGeneration;
 bool wrongParent,throws,nullResult;Handle target;
 Script():calls(0),expected(0),mask(0),status(0),returned(0),generation(1),aliasGeneration(1),wrongParent(false),throws(false),nullResult(false),target(){std::memset(values,0,sizeof values);pair[0]=pair[1]=0;}
 void want(unsigned op,Handle h,unsigned m=0){expected=op;target=h;mask=m;std::memset(values,0,sizeof values);}
 StartupBridge::OwnedReply call(uint32_t op,const Call &input,MilesTransport::Bytes text) override {
  ++calls;Header h={};h.magic=Magic;h.version=Version;h.kind=Request;h.opcode=op;h.request=calls;h.lane=1;
  std::vector<unsigned char> frame;CHECK(MilesTransport::encodeCall(h,input,MilesTransport::Bytes(),text,frame));
  Header checked={};Call c={};CHECK(MilesTransport::decodeCall(MilesTransport::Bytes(&frame[0],frame.size()),checked,c));
  Result r={};
  if(op==AIL_startup)r.return_bits=1;
  else if(op==AIL_open_digital_driver)r.resource=Handle{Driver,1,1};
  else if(op!=AIL_shutdown&&op!=SessionClose){
   CHECK(op==expected&&c.target.kind==target.kind&&c.target.slot==target.slot&&c.target.generation==target.generation);
   CHECK(c.output_mask==mask&&!c.reserved&&!c.callback&&!c.resource.kind&&!c.resource.slot&&!c.resource.generation&&!c.bytes.length);
   for(unsigned i=0;i<8;++i)CHECK(c.value[i]==values[i]);
   if(op==AIL_open_stream){CHECK(c.text.length==8);CHECK(!std::memcmp(&frame[c.text.offset],"fixture",8));}else CHECK(!c.text.length);
   if(throws)throw std::runtime_error("unknown outcome");
   r.transport_status=status;
   if(!status){
    r.return_bits=returned;
    if(op==AIL_open_stream&&!nullResult)r.resource=Handle{Stream,2,generation};
    if(op==AIL_stream_sample_handle){if(!nullResult)r.resource=Handle{BorrowedSample,3,aliasGeneration};r.value[0]=Stream;r.value[1]=wrongParent?99u:2u;r.value[2]=generation;}
    if(op==AIL_stream_ms_position||op==AIL_sample_volume_levels){if(mask&1)r.value[0]=pair[0];if(mask&2)r.value[1]=pair[1];}
   }
  }
  Header reply=h;reply.kind=Reply;CHECK(MilesTransport::encodeResult(reply,r,MilesTransport::Bytes(),MilesTransport::Bytes(),frame));
  StartupBridge::OwnedReply out;if(!StartupBridge::decodeReply(MilesTransport::Bytes(&frame[0],frame.size()),h,out))throw std::runtime_error("invalid reply");return out;
 }
 void finish() override{}
};
template<class F>static void fails(F f,ClientMiles::FailureReason reason){bool caught=false;try{f();}catch(const ClientMiles::Failure &e){caught=true;CHECK(e.reason()==reason);}CHECK(caught);}
static ClientMiles::HDIGDRIVER start(){CHECK(ClientMiles::startup()!=0);return ClientMiles::open_digital_driver(22050,16,2,0);}
static ClientMiles::HSTREAM open(Script &s,ClientMiles::HDIGDRIVER d){s.want(AIL_open_stream,Handle{Driver,1,1});s.values[0]=0x80000000u;return ClientMiles::open_stream(d,"fixture",INT_MIN);}
static void happy(){
 Script *s=new Script;ClientMilesPipe::Session session{std::unique_ptr<ClientMilesPipe::Channel>(s)};ClientMiles::HDIGDRIVER d=start();
 s->nullResult=true;CHECK(!open(*s,d));s->nullResult=false;
 ClientMiles::HSTREAM stream=open(*s,d);CHECK(stream!=0);Handle sh={Stream,2,1};Handle bh={BorrowedSample,3,1};
 s->want(AIL_stream_sample_handle,sh);s->nullResult=true;CHECK(!ClientMiles::stream_sample_handle(stream));s->nullResult=false;
 ClientMiles::HSAMPLE sample=ClientMiles::stream_sample_handle(stream);CHECK(sample&&ClientMiles::stream_sample_handle(stream)==sample);
 unsigned n=s->calls;fails([&]{ClientMiles::release_sample_handle(sample);},ClientMiles::FailureReason::InvalidArgument);CHECK(n==s->calls);
 fails([&]{ClientMiles::start_sample(sample);},ClientMiles::FailureReason::InvalidArgument);CHECK(n==s->calls);
 s->want(AIL_set_sample_volume_levels,bh);s->values[0]=0x80000000u;s->values[1]=0x3f800000u;ClientMiles::set_sample_volume_levels(sample,-0.f,1.f);
 s->want(AIL_set_sample_reverb_levels,bh);s->values[0]=0x3f800000u;ClientMiles::set_sample_reverb_levels(sample,1.f,0.f);
 s->want(AIL_set_sample_playback_rate,bh);s->values[0]=0xffffffffu;ClientMiles::set_sample_playback_rate(sample,-1);
 s->want(AIL_sample_playback_rate,bh);s->returned=0x80000000u;CHECK(ClientMiles::sample_playback_rate(sample)==INT_MIN);s->returned=0;
 s->want(AIL_sample_volume_levels,bh,7);s->pair[0]=s->pair[1]=0x3f800000u;float f=0;ClientMiles::sample_volume_levels(sample,&f,&f);CHECK(f==1.f);
 s->want(AIL_start_stream,sh);ClientMiles::start_stream(stream);
 s->want(AIL_set_stream_loop_count,sh);s->values[0]=0xffffffffu;ClientMiles::set_stream_loop_count(stream,-1);
 s->want(AIL_set_stream_loop_block,sh);s->values[0]=0x80000000u;s->values[1]=0xffffffffu;ClientMiles::set_stream_loop_block(stream,INT_MIN,-1);
 s->want(AIL_set_stream_ms_position,sh);s->values[0]=0x80000000u;ClientMiles::set_stream_ms_position(stream,INT_MIN);
 s->want(AIL_stream_status,sh);s->returned=0xffffffffu;CHECK(ClientMiles::stream_status(stream)==-1);s->returned=0;
 for(unsigned mask=0;mask<4;++mask){s->want(AIL_stream_ms_position,sh,mask);s->pair[0]=0x80000000u;s->pair[1]=0xffffffffu;int32_t a=7,b=8;ClientMiles::stream_ms_position(stream,(mask&1)?&a:0,(mask&2)?&b:0);CHECK(a==((mask&1)?INT_MIN:7)&&b==((mask&2)?-1:8));}
 s->want(AIL_stream_ms_position,sh,7);s->pair[0]=s->pair[1]=0xffffffffu;int32_t t=0;ClientMiles::stream_ms_position(stream,&t,&t);CHECK(t==-1);
 s->want(AIL_close_stream,sh);s->status=StartupBridge::LifecycleRefused;fails([&]{ClientMiles::close_stream(stream);},ClientMiles::FailureReason::WrongState);CHECK(!session.uncertain());
 s->status=0;s->want(AIL_stream_sample_handle,sh);CHECK(ClientMiles::stream_sample_handle(stream)==sample);
 s->want(AIL_close_stream,sh);ClientMiles::close_stream(stream);
 for(unsigned i=0;i<256;++i){++s->generation;stream=open(*s,d);s->want(AIL_close_stream,Handle{Stream,2,s->generation});ClientMiles::close_stream(stream);}
 stream=open(*s,d);s->want(AIL_stream_sample_handle,Handle{Stream,2,s->generation});CHECK(ClientMiles::stream_sample_handle(stream)!=0);
 ClientMiles::shutdown();session.close();
}
static void broken(unsigned mode){
 Script *s=new Script;ClientMilesPipe::Session session{std::unique_ptr<ClientMilesPipe::Channel>(s)};auto d=start();auto stream=open(*s,d);Handle sh={Stream,2,1};
 s->want(AIL_stream_sample_handle,sh);CHECK(ClientMiles::stream_sample_handle(stream)!=0);
 if(mode==0){s->want(AIL_close_stream,sh);s->throws=true;fails([&]{ClientMiles::close_stream(stream);},ClientMiles::FailureReason::BackendFailed);}
 else if(mode==3){s->want(AIL_stream_ms_position,sh,7);s->pair[0]=0;s->pair[1]=1;int32_t out=17;fails([&]{ClientMiles::stream_ms_position(stream,&out,&out);},ClientMiles::FailureReason::BackendFailed);CHECK(out==17);}
 else {s->wrongParent=mode==1;s->aliasGeneration=mode==2?2:1;s->nullResult=mode==4;fails([&]{ClientMiles::stream_sample_handle(stream);},ClientMiles::FailureReason::BackendFailed);}
 CHECK(session.uncertain());unsigned before=s->calls;fails([&]{ClientMiles::start_stream(stream);},ClientMiles::FailureReason::BackendFailed);CHECK(s->calls==before);
}
int main(){try{happy();for(unsigned m=0;m<5;++m)broken(m);std::printf("PASS %u stream scripted checks; no host/file/runtime evidence\n",checks);return 0;}catch(const std::exception &e){std::printf("FAIL %s\n",e.what());return 1;}}
