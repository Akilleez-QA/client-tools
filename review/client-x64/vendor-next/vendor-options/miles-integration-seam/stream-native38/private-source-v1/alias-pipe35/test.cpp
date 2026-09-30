#include "../protocol-candidate/pair_outputs.h"
#include "../backend-boundary24/pipe/Session.h"
#include "../native-playback28/ClientMilesPlayback.h"
#include <cstdio>
#include <cstring>
#include <stdexcept>
#include <climits>
static unsigned checks=0;
#define CHECK(x) do {++checks;if(!(x))throw std::runtime_error(#x);}while(0)
using namespace MilesWire;
static uint32_t bits(float f){uint32_t u;std::memcpy(&u,&f,4);return u;}
static float floating(uint32_t u){float f;std::memcpy(&f,&u,4);return f;}
struct Script:ClientMilesPipe::Channel {
 unsigned calls,expected,mask;uint32_t values[8],answer,pair[2],refused;bool extra,unrequested,throws;uint32_t allocationKind;
 Script():calls(0),expected(0),mask(0),answer(0),refused(0),extra(false),unrequested(false),throws(false),allocationKind(OwnedSample){std::memset(values,0,sizeof values);pair[0]=pair[1]=0;}
 void want(unsigned op,unsigned output=0){expected=op;mask=output;std::memset(values,0,sizeof values);}
 StartupBridge::OwnedReply call(uint32_t op,const Call &fields,MilesTransport::Bytes text) override {
  ++calls;CHECK(!text.size);
  Header h={};h.magic=Magic;h.version=Version;h.kind=Request;h.opcode=op;h.request=calls;h.lane=1;
  std::vector<unsigned char> encoded;CHECK(MilesTransport::encodeCall(h,fields,MilesTransport::Bytes(),text,encoded));
  Header decoded={};Call c={};CHECK(MilesTransport::decodeCall(MilesTransport::Bytes(&encoded[0],encoded.size()),decoded,c));
  CHECK(decoded.opcode==op&&decoded.request==calls);
  Result r={};
  if(op==AIL_startup)r.return_bits=1;
  else if(op==AIL_open_digital_driver)r.resource=Handle{Driver,1,1};
  else if(op==AIL_allocate_sample_handle)r.resource=Handle{allocationKind,2,1};
  else if(op!=AIL_shutdown&&op!=SessionClose&&op!=AIL_release_sample_handle){
   CHECK(op==expected&&c.target.kind==OwnedSample&&c.target.slot==2&&c.target.generation==1);
   CHECK(c.output_mask==mask&&!c.callback&&!c.reserved&&!c.resource.kind&&!c.resource.slot&&!c.resource.generation&&!c.bytes.length&&!c.text.length);
   for(unsigned i=0;i<8;++i)CHECK(c.value[i]==values[i]);
   if(throws)throw std::runtime_error("uncertain scripted channel");
   r.transport_status=refused;
   if(!refused){r.return_bits=answer;if(mask&1)r.value[0]=pair[0];if(mask&2)r.value[1]=pair[1];if(extra)r.value[3]=1;if(unrequested)r.value[1]=1;}
  }
  Header reply=h;reply.kind=Reply;CHECK(MilesTransport::encodeResult(reply,r,MilesTransport::Bytes(),MilesTransport::Bytes(),encoded));
  StartupBridge::OwnedReply out;
  if(!StartupBridge::decodeReply(MilesTransport::Bytes(&encoded[0],encoded.size()),h,out))throw std::runtime_error("malformed scripted reply");
  return out;
 }
 void finish() override {}
};
template<class F>static void fails(F f,ClientMiles::FailureReason expected){bool caught=false;try{f();}catch(const ClientMiles::Failure &e){caught=true;CHECK(e.reason()==expected);}CHECK(caught);}
static ClientMiles::HSAMPLE start(Script *script){(void)script;CHECK(ClientMiles::startup()!=0);return ClientMiles::allocate_sample_handle(ClientMiles::open_digital_driver(22050,16,2,0));}
static void happy(){
 Script *script=new Script;ClientMilesPipe::Session session{std::unique_ptr<ClientMilesPipe::Channel>(script)};
 ClientMiles::HSAMPLE sample=start(script);CHECK(sample!=0);
 script->want(AIL_start_sample);
 ClientMiles::start_sample(sample);
 script->want(AIL_stop_sample);
 ClientMiles::stop_sample(sample);
 script->want(AIL_sample_status);
 script->answer=0xffffffffu;CHECK(ClientMiles::sample_status(sample)==0xffffffffu);script->answer=0;
 script->want(AIL_set_sample_loop_count);
 script->values[0]=0x80000000u;
 ClientMiles::set_sample_loop_count(sample, INT_MIN);
 script->want(AIL_set_sample_loop_block);
 script->values[0]=0x80000000u;
 script->values[1]=0xffffffffu;
 ClientMiles::set_sample_loop_block(sample, INT_MIN, -1);
 script->want(AIL_set_sample_ms_position);
 script->values[0]=0x80000000u;
 ClientMiles::set_sample_ms_position(sample, INT_MIN);
 script->want(AIL_set_sample_position);
 script->values[0]=0xffffffffu;
 ClientMiles::set_sample_position(sample, 0xffffffffu);
 script->want(AIL_sample_position);
 script->answer=0xffffffffu;CHECK(ClientMiles::sample_position(sample)==0xffffffffu);script->answer=0;
 script->want(AIL_set_sample_playback_rate);
 script->values[0]=0x80000000u;
 ClientMiles::set_sample_playback_rate(sample, INT_MIN);
 script->want(AIL_sample_playback_rate);
 script->answer=0xffffffffu;CHECK(ClientMiles::sample_playback_rate(sample)==-1);script->answer=0;
 script->want(AIL_set_sample_volume_levels);
 script->values[0]=0x80000000u;
 script->values[1]=0x7fc01234u;
 ClientMiles::set_sample_volume_levels(sample, floating(0x80000000u), floating(0x7fc01234u));
 script->want(AIL_set_sample_reverb_levels);
 script->values[0]=0x80000000u;
 script->values[1]=0x7fc01234u;
 ClientMiles::set_sample_reverb_levels(sample, floating(0x80000000u), floating(0x7fc01234u));
 script->want(AIL_set_sample_3D_position);
 script->values[0]=0x80000000u;
 script->values[1]=0x7fc01234u;
 script->values[2]=0x00000001u;
 ClientMiles::set_sample_3D_position(sample, floating(0x80000000u), floating(0x7fc01234u), floating(0x00000001u));
 script->want(AIL_set_sample_3D_velocity_vector);
 script->values[0]=0x80000000u;
 script->values[1]=0x7fc01234u;
 script->values[2]=0x00000001u;
 ClientMiles::set_sample_3D_velocity_vector(sample, floating(0x80000000u), floating(0x7fc01234u), floating(0x00000001u));
 script->want(AIL_set_sample_3D_distances);
 script->values[0]=0x80000000u;
 script->values[1]=0x7fc01234u;
 script->values[2]=0x80000000u;
 ClientMiles::set_sample_3D_distances(sample, floating(0x80000000u), floating(0x7fc01234u), INT_MIN);
 script->want(AIL_set_sample_occlusion);
 script->values[0]=0x80000000u;
 ClientMiles::set_sample_occlusion(sample, floating(0x80000000u));
 script->want(AIL_set_sample_obstruction);
 script->values[0]=0x80000000u;
 ClientMiles::set_sample_obstruction(sample, floating(0x80000000u));
 const uint32_t patterns[]={0u,0x80000000u,0x7f800000u,0xff800000u,0x7fc01234u,1u,0xbf800000u};
 for(unsigned i=0;i<sizeof(patterns)/sizeof(patterns[0]);++i){
  script->want(AIL_set_sample_obstruction);script->values[0]=patterns[i];ClientMiles::set_sample_obstruction(sample,floating(patterns[i]));
  script->want(AIL_set_sample_loop_count);script->values[0]=0;ClientMiles::set_sample_loop_count(sample,0);
  script->want(AIL_sample_playback_rate);script->answer=0x80000000u;CHECK(ClientMiles::sample_playback_rate(sample)==INT_MIN);script->answer=0;
 }
 for(unsigned mask=0;mask<4;++mask){
  for(unsigned op=0;op<2;++op){
   script->want(op?AIL_sample_reverb_levels:AIL_sample_volume_levels,mask);script->pair[0]=0x80000000u;script->pair[1]=0x7fc01234u;
   float a=3.f,b=4.f;
   if(op)ClientMiles::sample_reverb_levels(sample,(mask&1)?&a:0,(mask&2)?&b:0);
   else ClientMiles::sample_volume_levels(sample,(mask&1)?&a:0,(mask&2)?&b:0);
   CHECK(bits(a)==((mask&1)?script->pair[0]:bits(3.f)));CHECK(bits(b)==((mask&2)?script->pair[1]:bits(4.f)));
  }
 }
 script->want(AIL_sample_volume_levels,7);script->pair[0]=script->pair[1]=0x7f800000u;
 float alias=1.f;ClientMiles::sample_volume_levels(sample,&alias,&alias);CHECK(bits(alias)==0x7f800000u);
 const unsigned before=script->calls;
 fails([&]{ClientMiles::start_sample(reinterpret_cast<ClientMiles::HSAMPLE>(1));},ClientMiles::FailureReason::InvalidArgument);CHECK(script->calls==before);
 script->want(AIL_sample_volume_levels,3);script->refused=StartupBridge::InvalidFields;
 float a=7.f,b=8.f;fails([&]{ClientMiles::sample_volume_levels(sample,&a,&b);},ClientMiles::FailureReason::InvalidArgument);
 CHECK(a==7.f&&b==8.f&&!session.uncertain());script->refused=0;
 ClientMiles::sample_volume_levels(sample,&a,&b);CHECK(bits(a)==0x7f800000u&&bits(b)==0x7f800000u);
 ClientMiles::release_sample_handle(sample);ClientMiles::shutdown();session.close();
}
static void broken(unsigned mode){
 Script *script=new Script;ClientMilesPipe::Session session{std::unique_ptr<ClientMilesPipe::Channel>(script)};
 ClientMiles::HSAMPLE sample=start(script);float a=7.f,b=8.f;
 script->want(AIL_sample_volume_levels,mode==0?1:3);script->pair[0]=0x3f000000;script->pair[1]=0x3f800000;
 script->unrequested=mode==0;script->extra=mode==1;script->throws=mode==2;
 fails([&]{ClientMiles::sample_volume_levels(sample,&a,mode==0?0:&b);},ClientMiles::FailureReason::BackendFailed);
 CHECK(a==7.f&&b==8.f&&session.uncertain());unsigned before=script->calls;
 fails([&]{ClientMiles::stop_sample(sample);},ClientMiles::FailureReason::BackendFailed);CHECK(script->calls==before);
}
static void borrowed(){
 Script *script=new Script;script->allocationKind=BorrowedSample;
 ClientMilesPipe::Session session{std::unique_ptr<ClientMilesPipe::Channel>(script)};
 fails([&]{start(script);},ClientMiles::FailureReason::BackendFailed);CHECK(session.uncertain());
}
static void topology(){
 Header h={};h.magic=Magic;h.version=Version;h.kind=Request;h.opcode=AIL_sample_ms_position;h.request=1;h.lane=1;
 Call c={};std::vector<unsigned char> frame;
 CHECK(Version==2);CHECK(MilesTransport::encodeCall(h,c,MilesTransport::Bytes(),MilesTransport::Bytes(),frame));
 frame[4]=1;frame[5]=0;Header decoded={};Call fields={};
 CHECK(!MilesTransport::decodeCall(MilesTransport::Bytes(&frame[0],frame.size()),decoded,fields));

 for(unsigned mask=0;mask<16;++mask){
  bool valid=mask==0||mask==1||mask==2||mask==3||mask==7;
  CHECK(MilesWire::validPairMask(mask)==valid);
  if(!valid)continue;
  MilesWire::PairOutputs<int32_t> p(mask);
  CHECK((p.first()!=0)==bool(mask&1));CHECK((p.second()!=0)==bool(mask&2));
  CHECK(MilesWire::pairMask(p.first(),p.second())==mask);
  if(mask==7){*p.second()=-123;*p.first()=456;CHECK(*p.second()==456);}
 }
 CHECK(!MilesWire::validPairMask(0x80000007u));
}
static void aliases(unsigned op,bool mismatch){
 Script *script=new Script;ClientMilesPipe::Session session{std::unique_ptr<ClientMilesPipe::Channel>(script)};
 ClientMiles::HSAMPLE sample=start(script);
 script->want(op==0?AIL_sample_ms_position:op==1?AIL_sample_volume_levels:AIL_sample_reverb_levels,7);
 script->pair[0]=0x80000000u;script->pair[1]=mismatch?0u:script->pair[0];
 int32_t time=17;float value=17.f;
 const auto invoke=[&]{if(op==0)ClientMiles::sample_ms_position(sample,&time,&time);
  else if(op==1)ClientMiles::sample_volume_levels(sample,&value,&value);
  else ClientMiles::sample_reverb_levels(sample,&value,&value);};
 if(mismatch){fails(invoke,ClientMiles::FailureReason::BackendFailed);CHECK(time==17&&value==17.f&&session.uncertain());}
 else {invoke();CHECK(op==0?time==INT_MIN:bits(value)==0x80000000u);ClientMiles::release_sample_handle(sample);ClientMiles::shutdown();session.close();}
}
int main(){try{topology();for(unsigned op=0;op<3;++op){aliases(op,false);aliases(op,true);}happy();for(unsigned i=0;i<3;++i)broken(i);borrowed();std::printf("PASS %u scripted checks; no SDK/runtime evidence\n",checks);return 0;}catch(const std::exception &e){std::printf("FAIL %s\n",e.what());return 1;}}
