#include "tree/startup-bridge23/reply.h"
#include <cstdio>
#include <cstdlib>
#include <limits>
using namespace MilesWire;
namespace {
unsigned checks=0;
void check(bool ok){++checks;if(!ok){std::fprintf(stderr,"FAIL assertion %u\n",checks);std::abort();}}
Header context(uint32_t opcode){Header h={};h.magic=Magic;h.version=Version;h.kind=Request;h.opcode=opcode;h.request=17;h.causal_request=5;h.lane=3;h.lock_lease=9;return h;}
MilesTransport::Bytes view(const std::vector<unsigned char>& v){return MilesTransport::Bytes(v.data(),v.size());}
std::vector<unsigned char> encode(Header h,const Result& r,MilesTransport::Bytes payload=MilesTransport::Bytes(),MilesTransport::Bytes text=MilesTransport::Bytes()){
 std::vector<unsigned char> v;check(MilesTransport::encodeResult(h,r,payload,text,v));return v;
}
bool same(const Result&a,const Result&b){
 if(a.transport_status!=b.transport_status||a.return_bits!=b.return_bits||a.resource.kind!=b.resource.kind||a.resource.slot!=b.resource.slot||a.resource.generation!=b.resource.generation||a.bytes.offset!=b.bytes.offset||a.bytes.length!=b.bytes.length||a.text.offset!=b.text.offset||a.text.length!=b.text.length||a.null_mask!=b.null_mask||a.callback!=b.callback)return false;
 for(unsigned i=0;i<8;++i)if(a.value[i]!=b.value[i])return false;
 return true;
}
void reject(const std::vector<unsigned char>& frame,const Header& expected,bool envelopeValid=true){
 if(envelopeValid){Header h={};Result r={};check(MilesTransport::decodeResult(view(frame),h,r));}
 StartupBridge::OwnedReply out;out.result.transport_status=77;out.result.return_bits=0xaabbccddu;out.result.resource={File,7,8};out.result.value[3]=19;out.result.callback=42;out.result.bytes={9,10};out.result.text={11,12};out.result.null_mask=23;out.text.push_back(67);out.text.push_back(0);
 const Result old=out.result;const std::vector<unsigned char> text=out.text;
 check(!StartupBridge::decodeReply(view(frame),expected,out));check(same(old,out.result));check(out.text==text);
}
const uint32_t ops[]={AIL_active_sample_count,AIL_digital_CPU_percent,AIL_digital_latency,AIL_get_timer_highest_delay,AIL_file_error};
void scalars(){
 const uint32_t values[]={0u,1u,0x7fffffffu,0x80000000u,0xffffffffu};
 const int64_t signedExpected[]={0,1,2147483647LL,-2147483647LL-1,-1};
 for(unsigned op=0;op<5;++op)for(unsigned n=0;n<5;++n){
  Header expected=context(ops[op]),h=expected;h.kind=Reply;Result r={};r.return_bits=values[n];const std::vector<unsigned char> frame=encode(h,r);const std::vector<unsigned char> saved=frame;
  StartupBridge::OwnedReply out;out.result.return_bits=9;out.text.push_back(5);
  check(StartupBridge::decodeReply(view(frame),expected,out));check(out.result.return_bits==values[n]);check(out.text.empty());check(same(out.result,r));check(frame==saved);
  if(ops[op]==AIL_get_timer_highest_delay){const uint32_t actual=out.result.return_bits;check(static_cast<uint64_t>(actual)==static_cast<uint64_t>(values[n]));}
  else {check(MilesStartup::signedValue(out.result.return_bits)==signedExpected[n]);check(static_cast<int32_t>(MilesStartup::signedValue(out.result.return_bits))==signedExpected[n]);}
 }
 std::puts("PASS scalar-bits");
}
void shapes(){
 const unsigned char payload[]={7,8};const char text[]="x";
 for(unsigned op=0;op<5;++op){Header expected=context(ops[op]),h=expected;h.kind=Reply;Result r={};
  for(unsigned kind=Driver;kind<=File;++kind){r={};r.resource={kind,1,1};reject(encode(h,r),expected);}
  for(unsigned i=0;i<8;++i){r={};r.value[i]=0xffffffffu;reject(encode(h,r),expected);}
  r={};r.callback=1;reject(encode(h,r),expected);
  r={};r.null_mask=1;reject(encode(h,r),expected);
  r={};r.null_mask=0x80000000u;reject(encode(h,r),expected);
  r={};reject(encode(h,r,MilesTransport::Bytes(payload,sizeof payload)),expected);
  reject(encode(h,r,MilesTransport::Bytes(),MilesTransport::Bytes(text,sizeof text)),expected);
  reject(encode(h,r,MilesTransport::Bytes(payload,sizeof payload),MilesTransport::Bytes(text,sizeof text)),expected);
 }
 std::puts("PASS diagnostic-shapes");
}
void contexts(){
 for(unsigned op=0;op<5;++op){Header expected=context(ops[op]);Result r={};r.return_bits=3;
  for(unsigned n=0;n<6;++n){Header h=expected;h.kind=Reply;
   switch(n){case 0:++h.request;break;case 1:++h.lane;break;case 2:++h.causal_request;break;case 3:++h.lock_lease;break;case 4:h.opcode=AIL_serve;break;default:h.kind=ReverseReply;break;}
   reject(encode(h,r),expected);
  }
  Header h=expected;h.kind=Reply;std::vector<unsigned char> frame=encode(h,r);frame.pop_back();reject(frame,expected,false);
  frame=encode(h,r);frame[0]^=1;reject(frame,expected,false);
 }
 std::puts("PASS exact-context");
}
void statuses(){
 const uint32_t statuses[]={StartupBridge::Unsupported,StartupBridge::InvalidResource,StartupBridge::InvalidFields,StartupBridge::LifecycleRefused,StartupBridge::TextTooLong,StartupBridge::InputBudgetExceeded,StartupBridge::VersionQueryFailed};
 for(unsigned op=0;op<5;++op){Header expected=context(ops[op]),h=expected;h.kind=Reply;
  for(unsigned n=0;n<sizeof statuses/sizeof statuses[0];++n){Result r={};r.transport_status=statuses[n];StartupBridge::OwnedReply out;check(StartupBridge::decodeReply(view(encode(h,r)),expected,out));check(out.result.transport_status==statuses[n]);check(out.result.return_bits==0);r.return_bits=1;reject(encode(h,r),expected);}
  Result r={};r.transport_status=0x9999;reject(encode(h,r),expected);
 }
 Header expected=context(AIL_serve),h=expected;h.kind=Reply;Result r={};r.return_bits=1;reject(encode(h,r),expected);
 std::puts("PASS refusal-and-allowlist");
}
void unchangedNeighbors(){
 Header expected=context(AIL_sample_ms_position),h=expected;h.kind=Reply;Result r={};r.value[0]=0x80000000u;r.value[1]=0xffffffffu;StartupBridge::OwnedReply out;check(StartupBridge::decodeReply(view(encode(h,r)),expected,out));check(same(r,out.result));
 expected=context(AIL_last_error);h=expected;h.kind=Reply;r={};const char empty[]="";check(StartupBridge::decodeReply(view(encode(h,r,MilesTransport::Bytes(),MilesTransport::Bytes(empty,sizeof empty))),expected,out));check(out.text.size()==1&&out.text[0]==0);check(out.result.null_mask==0);
 r.null_mask=MilesStartup::TextNull;check(StartupBridge::decodeReply(view(encode(h,r)),expected,out));check(out.text.empty());check(out.result.null_mask==MilesStartup::TextNull);
 std::puts("PASS unchanged-neighbors");
}
}
int main(){scalars();shapes();contexts();statuses();unchangedNeighbors();std::printf("PASS assertions=%u\n",checks);}
