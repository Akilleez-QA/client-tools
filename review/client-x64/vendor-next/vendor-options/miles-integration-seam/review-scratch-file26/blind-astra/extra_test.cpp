#define main baseline_main
#include "../../file-channel26/channel_test.cpp"
#undef main
#include <limits>

Local::OpenResult unusedOpen(const char*) { Local::OpenResult r = {}; return r; }
void throwingClose(Local::LocalFileHandle) { ++calls; throw 1; }
int32_t throwingSeek(Local::LocalFileHandle, int32_t, uint32_t) { ++calls; throw 1; }
uint32_t throwingRead(Local::LocalFileHandle, void*, uint32_t) { ++calls; throw 1; }

int main() {
 if (baseline_main()) return 1;
 Request saved = request(MilesWire::FileOpen,0,0,"sentinel");
 // Every unused scalar and envelope field for each operation.
 for (uint32_t op=MilesWire::FileOpen; op<=MilesWire::FileRead; ++op) {
   const auto good=frame(op,0,0,op==MilesWire::FileOpen?"a":"");
   unsigned used=op==MilesWire::FileSeek?2:op==MilesWire::FileRead?1:0;
   for(unsigned i=used;i<8;++i) { auto bad=good; put32(bad,72+4*i,1); CHECK(decodeRequest(bytes(bad),expected,saved)!=Valid); CHECK(saved.name()=="sentinel"); }
   const size_t offsets[]={60,104,120,124,128,132};
   for(size_t off:offsets) { auto bad=good; put32(bad,off,1); CHECK(decodeRequest(bytes(bad),expected,saved)!=Valid); }
   for(size_t n=0;n<good.size();++n) { CHECK(decodeRequest(MilesTransport::Bytes(good.data(),n),expected,saved)!=Valid); }
 }
 for(int32_t value: {std::numeric_limits<int32_t>::min(),int32_t(-1),int32_t(0),std::numeric_limits<int32_t>::max()}) {
   for(uint32_t origin=0;origin<=2;++origin) {
     auto req=request(MilesWire::FileSeek,static_cast<uint32_t>(value),origin); seekResult=value;
     Invocation work(req,services,binding(0),lifetime()); invoke(work);
     CHECK(seekOffset==value && seekOrigin==origin && work.completion().returnBits==static_cast<uint32_t>(value));
   }
 }
 // Valid largest read and immutable request after input buffer destruction.
 const uint32_t maximum=MilesWire::MaxFrameBytes-128;
 auto req=request(MilesWire::FileRead,maximum); readResult=maximum;
 Invocation work(req,services,binding(0),lifetime()); invoke(work);
 std::vector<unsigned char> reply;
 CHECK(encodeCompletion(work,noFile,reply)==Valid && reply.size()==MilesWire::MaxFrameBytes);
 OwnedReply decoded; CHECK(decodeReply(bytes(reply),req,decoded)==Valid && decoded.bytes.size()==maximum);
 auto before=decoded.bytes;
 failNextAllocation=true; bool caught=false;
 try { decodeReply(bytes(reply),req,decoded); } catch(const std::bad_alloc&) { caught=true; }
 CHECK(caught && !failNextAllocation && decoded.bytes==before && decoded.returnBits==maximum);
 // No post-call retry when any non-open service throws.
 FileServices throwing={unusedOpen,throwingClose,throwingSeek,throwingRead};
 for(uint32_t op=MilesWire::FileClose;op<=MilesWire::FileRead;++op) {
   Invocation failing(request(op),throwing,binding(0),lifetime()); unsigned prior=calls;
   CHECK(failing.invokeOnAdmittedExecutor()); CHECK(failing.finished() && failing.completion().state==CallThrew);
   CHECK(!failing.invokeOnAdmittedExecutor() && calls==prior+1);
   CHECK(encodeCompletion(failing,noFile,reply)==InvalidResult);
 }
 // Reply forbidden fields and truncations, untouched output.
 req=request(MilesWire::FileRead,4); readResult=2;
 Invocation read(req,services,binding(0),lifetime()); invoke(read); CHECK(encodeCompletion(read,noFile,reply)==Valid);
 const size_t replyOffsets[]={48,56,68,72,76,80,84,88,92,96,108,116,120,124};
 for(size_t off:replyOffsets) { auto bad=reply; put32(bad,off,1); CHECK(decodeReply(bytes(bad),req,decoded)!=Valid); CHECK(decoded.bytes==before); }
 for(size_t n=0;n<reply.size();++n) CHECK(decodeReply(MilesTransport::Bytes(reply.data(),n),req,decoded)!=Valid);
 std::printf("PASS independent boundary checks; %u total assertions\n",checks);
}
