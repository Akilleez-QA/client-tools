#include "test_support.h"
using namespace MilesSessionVersion;
static void rejected(const std::vector<unsigned char>& v, const MilesWire::Header& h) {
    char target[Capacity],before[Capacity]; std::memset(target,0x69,sizeof target);
    std::memcpy(before,target,sizeof target);
    CHECK(!copyReply(bytes(v),h,target)); CHECK(!std::memcmp(before,target,sizeof target));
}
int main(int argc,char** argv) {
    setvbuf(stdout,0,_IONBF,0);
    MilesWire::Header h=request(),decoded={}; std::vector<unsigned char> q,frame;
    CHECK(makeQuery(h,q)); CHECK(q.size()==136); CHECK(validateQuery(bytes(q),decoded));
    CHECK(decoded.request==h.request && decoded.lane==h.lane);
    for(size_t n=0;n<q.size();++n) CHECK(!validateQuery(MilesTransport::Bytes(&q[0],n),decoded));
    // Every request payload byte is required to be zero.
    for(size_t i=48;i<q.size();++i) {
        std::vector<unsigned char> bad=q; bad[i]=1;
        CHECK(!validateQuery(bytes(bad),decoded));
    }
    const size_t queryHeaderOffsets[]={0,4,6,8};
    for(unsigned i=0;i<4;++i) {
        std::vector<unsigned char> bad=q; bad[queryHeaderOffsets[i]]^=0x20;
        CHECK(!validateQuery(bytes(bad),decoded));
    }
    MilesWire::Header badHeader=h; badHeader.request=0; CHECK(!makeQuery(badHeader,frame));
    badHeader=h; badHeader.lane=0; CHECK(!makeQuery(badHeader,frame));
    char text[Capacity]={},target[Capacity];
    CHECK(makeReply(h,text,frame)); CHECK(frame.size()==129);
    std::memset(target,0x69,sizeof target); CHECK(copyReply(bytes(frame),h,target));
    CHECK(!target[0] && target[1]==0x69); // Empty is distinct from no reply.
    std::memset(text,'x',sizeof text); text[Capacity-1]=0;
    CHECK(makeReply(h,text,frame)); CHECK(frame.size()==128+Capacity);
    CHECK(copyReply(bytes(frame),h,target)); CHECK(!std::memcmp(text,target,Capacity));
    text[Capacity-1]='x'; const std::vector<unsigned char> saved=frame;
    CHECK(!makeReply(h,text,frame)); CHECK(frame==saved);
    std::memset(text,0,sizeof text); std::memcpy(text,"owned bytes",12);
    const unsigned char highByte=0xe9; std::memcpy(text,&highByte,1); CHECK(makeReply(h,text,frame));
    std::memset(text,'z',sizeof text); CHECK(copyReply(bytes(frame),h,target));
    CHECK(static_cast<unsigned char>(target[0])==0xe9 && !std::strcmp(target+1,"wned bytes"));
    const std::vector<unsigned char> good=frame;
    for(size_t n=0;n<good.size();++n) {
        std::vector<unsigned char> truncated(good.begin(),good.begin()+n); rejected(truncated,h);
    }
    // Header context mismatch, noncanonical result fields and text span tampering.
    const size_t offsets[]={0,4,6,8,12,16,24,32,40,48,52,56,60,64,
        68,72,76,80,84,88,92,96,100,104,108,112,116,120,124};
    for(unsigned i=0;i<sizeof offsets/sizeof offsets[0];++i) {
        std::vector<unsigned char> bad=good; bad[offsets[i]]^=1; rejected(bad,h);
    }
    std::vector<unsigned char> bad=good; bad.back()='x'; rejected(bad,h);
    bad=good; bad[128]=0; rejected(bad,h);
    MilesWire::Result r={}; MilesWire::Header reply=h; reply.kind=MilesWire::Reply;
    CHECK(MilesTransport::encodeResult(reply,r,MilesTransport::Bytes(),MilesTransport::Bytes(),bad)); rejected(bad,h);
    char oversize[257]; std::memset(oversize,'x',sizeof oversize); oversize[256]=0;
    CHECK(MilesTransport::encodeResult(reply,r,MilesTransport::Bytes(),MilesTransport::Bytes(oversize,sizeof oversize),bad)); rejected(bad,h);
    // Retain all routing context, including a legitimate nonzero causal/lease.
    h.causal_request=7; h.lock_lease=9; text[0]='v'; text[1]=0;
    CHECK(makeQuery(h,q)); CHECK(validateQuery(bytes(q),decoded));
    CHECK(makeReply(decoded,text,frame)); CHECK(copyReply(bytes(frame),h,target));
    if(argc==3) {
        std::vector<unsigned char> actual,expected;
        CHECK(readFile(argv[1],actual)); CHECK(readFile(argv[2],expected));
        std::memset(target,0x69,sizeof target);
        CHECK(copyReply(bytes(actual),request(),target));
        CHECK(!expected.empty() && expected.size()<=Capacity);
        if(failures) return 1;
        if(!expected.empty() && expected.size()<=Capacity) CHECK(!std::memcmp(target,&expected[0],expected.size()));
        if(expected.size()<Capacity) CHECK(target[expected.size()]==0x69);
        CHECK(writeFile("consumer-copy.bin",target,expected.size()));
        std::printf("cross_process_resource_text=%s bytes=%u pointer_bits=%u\n",target,
            static_cast<unsigned>(expected.size()),static_cast<unsigned>(sizeof(void*)*8));
    } else CHECK(argc==1);
    std::printf("%u/%u version wire checks pointer_bits=%u\n",checks-failures,checks,static_cast<unsigned>(sizeof(void*)*8));
    return failures?1:0;
}
