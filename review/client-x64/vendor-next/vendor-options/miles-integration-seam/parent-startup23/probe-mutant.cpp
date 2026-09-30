#include "reply-mutant.h"
#include <cstdio>
#include <cstdlib>
using namespace MilesWire;
using namespace StartupBridge;
static unsigned checks=0;
static void check(bool ok,const char* what){++checks;if(!ok){std::fprintf(stderr,"FAIL %s\n",what);std::exit(1);}}
static MilesTransport::Bytes view(const std::vector<unsigned char>& v){return MilesTransport::Bytes(v.empty()?0:&v[0],v.size());}
static std::vector<unsigned char> encoded(Header h,Result r,const char* p,size_t n){std::vector<unsigned char> v;h.kind=Reply;if(!MilesTransport::encodeResult(h,r,MilesTransport::Bytes(),MilesTransport::Bytes(p,n),v))std::abort();return v;}
static void rejects(const std::vector<unsigned char>& frame,const Header& expected,const char* label){OwnedReply out;out.result.return_bits=999;out.text.assign(4,'z');check(!decodeReply(view(frame),expected,out),label);check(out.result.return_bits==999&&out.text==std::vector<unsigned char>(4,'z'),"rejection preserves destination");}
int main(){
 Header expected={};expected.magic=Magic;expected.version=Version;expected.kind=Request;expected.opcode=AIL_last_error;expected.request=7;expected.lane=1;
 Result r={};OwnedReply out;std::vector<unsigned char> frame=encoded(expected,r,"abc",4);
 check(decodeReply(view(frame),expected,out),"valid text accepted");
 frame.assign(frame.size(),0x55);check(out.text.size()==4&&!std::memcmp(&out.text[0],"abc",4),"text owns bytes independently");
 check(out.result.text.length==0&&out.result.text.offset==0,"no dangling frame span");
 r.null_mask=MilesStartup::TextNull;frame=encoded(expected,r,0,0);check(decodeReply(view(frame),expected,out)&&out.text.empty()&&out.result.null_mask==1,"valid null preserved");
 r=Result();frame=encoded(expected,r,"",1);check(decodeReply(view(frame),expected,out)&&out.text.size()==1&&out.result.null_mask==0,"empty differs from null");
 Header wrong=expected;++wrong.request;rejects(frame,wrong,"wrong pending request rejected");
 wrong=expected;++wrong.lane;rejects(frame,wrong,"wrong lane rejected");
 r.transport_status=4;rejects(encoded(expected,r,0,0),expected,"unknown ambiguous status rejected");
 r=Result();const char embedded[]={'a',0,'b',0};rejects(encoded(expected,r,embedded,sizeof embedded),expected,"embedded NUL rejected");
 rejects(encoded(expected,r,"abc",3),expected,"missing final NUL rejected");
 r.value[0]=1;rejects(encoded(expected,r,"abc",4),expected,"unexpected scalar rejected");
 r=Result();r.resource.kind=Driver;r.resource.slot=1;r.resource.generation=1;rejects(encoded(expected,r,"abc",4),expected,"unexpected resource rejected");
 r=Result();r.transport_status=InvalidFields;rejects(encoded(expected,r,"abc",4),expected,"error with text rejected");
 r=Result();r.null_mask=2;rejects(encoded(expected,r,0,0),expected,"unknown null mask rejected");
 check(checks==23,"exact test count before final count check");
 std::printf("%u/%u pure reply-boundary checks\n",checks,24u);return checks==24?0:2;
}
