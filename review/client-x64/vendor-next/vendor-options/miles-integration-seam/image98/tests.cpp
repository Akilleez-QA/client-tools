// Actual93 Core/Session. Runtime and Channel are explicit suppliers; no Backend/SDK.
#include "tree/backend-boundary24/pipe/PipeCore.cpp"
#include "tree/buffer-upload-candidate/buffer_upload.h"
#include "tree/transport-candidate/resource_registry.h"
#include <cstdio>
#include <new>
namespace C=ClientMilesPipeCore57;
using ClientMilesPipe::Session;
static unsigned checks=0;
static bool anyCheckFailed=false;
#define CHECK(x) do { ++checks; if(!(x)) { anyCheckFailed=true; std::fprintf(stderr,"FAIL line=%d %s\n",__LINE__,#x); throw std::runtime_error("check failed"); } } while(0)
static bool same(const MilesWire::Handle &a,const MilesWire::Handle &b) {
    return a.kind==b.kind && a.slot==b.slot && a.generation==b.generation;
}
static MilesTransport::Bytes bytes(const std::vector<unsigned char> &v) {
    return MilesTransport::Bytes(v.data(),v.size());
}
enum Fault { None, BadBegin, RefusedRelease, BadRelease };
// Literal wire sequence and split boundaries. Never derived from production policy.
static const uint32_t smallOps[]={4097,4098,4099,9,4100};
static const uint32_t largeOps[]={4097,4098,4098,4099,9,4100};
static const uint32_t largeSizes[]={1048440,19};
struct Supplier:ClientMilesPipe::Channel {
    MilesTransport::ResourceRegistry registry;
    std::unique_ptr<MilesHost::BufferUpload> upload;
    std::vector<unsigned char> sealed,expected;
    MilesWire::Handle id;
    const uint32_t *ops;
    size_t opCount,step,chunkIndex;
    uint32_t budget,resultBits;
    uint64_t charged,peak;
    unsigned calls,classifications,releases;
    Fault fault;
    bool large;
    explicit Supplier(uint32_t b):registry(1),id(),ops(0),opCount(0),step(0),chunkIndex(0),
        budget(b),resultBits(0),charged(0),peak(0),calls(0),classifications(0),releases(0),fault(None),large(false){}
    void expect(const std::vector<unsigned char> &input,uint32_t bits,bool big,Fault f=None) {
        CHECK(!upload && !charged);expected=input;resultBits=bits;large=big;fault=f;
        ops=big?largeOps:smallOps;opCount=big?6u:5u;step=0;chunkIndex=0;
    }
    StartupBridge::OwnedReply call(uint32_t op,const MilesWire::Call &fields,
        MilesTransport::Bytes payload,MilesTransport::Bytes text,
        const std::vector<MilesWire::Handle> &resources,const Session &session) override {
        ++calls;CHECK(step<opCount);CHECK(op==ops[step]);++step;
        CHECK(!text.size);CHECK(!fields.bytes.offset && !fields.bytes.length);
        CHECK(!fields.text.offset && !fields.text.length);
        CHECK(!fields.callback && !fields.reserved && !fields.output_mask);
        MilesWire::Header h={};h.magic=MilesWire::Magic;h.version=MilesWire::Version;
        h.kind=MilesWire::Request;h.opcode=op;h.request=calls;h.lane=1;
        std::vector<unsigned char> frame;
        CHECK(MilesTransport::encodeCall(h,fields,payload,text,frame));
        CHECK(frame.size()<=1048576u);
        MilesWire::Header decoded={};MilesWire::Call c={};
        CHECK(MilesTransport::decodeCall(bytes(frame),decoded,c));
        CHECK(decoded.request==calls && decoded.opcode==op && decoded.lane==1);
        CHECK(!c.text.offset && !c.text.length);
        MilesWire::Result result={};
        if(op==4097u) {
            CHECK(resources.empty());CHECK(StartupBridge::nullHandle(c.target));CHECK(StartupBridge::nullHandle(c.resource));
            CHECK(c.value[0]==expected.size());CHECK(!c.bytes.length);
            CHECK(!upload && !charged);charged=2u*static_cast<uint64_t>(expected.size());CHECK(charged<=budget);
            if(charged>peak)peak=charged;
            MilesTransport::ResourceRegistry::Reservation reservation;
            CHECK(registry.reserve(MilesWire::Buffer,MilesWire::Handle(),reservation));
            upload.reset(new MilesHost::BufferUpload(static_cast<uint32_t>(expected.size()),budget/2));
            CHECK(registry.publish(reservation,upload.get(),id));result.resource=id;
            if(fault==BadBegin)result.resource.kind=MilesWire::Driver;
        } else {
            CHECK(resources.size()==1 && same(resources[0],id));
            void *local=0;CHECK(registry.resolve(id,MilesWire::Buffer,local));CHECK(local==upload.get());
            if(op==9u) {CHECK(StartupBridge::nullHandle(c.target));CHECK(same(c.resource,id));}
            else {CHECK(same(c.target,id));CHECK(StartupBridge::nullHandle(c.resource));}
            if(op==4098u) {
                CHECK(chunkIndex<(large?2u:1u));
                const uint32_t expectedSize=large?largeSizes[chunkIndex]:static_cast<uint32_t>(expected.size());
                const uint32_t expectedOffset=chunkIndex?1048440u:0u;
                CHECK(c.value[0]==expectedOffset);CHECK(c.bytes.length==expectedSize);
                CHECK(c.bytes.offset==136u);CHECK(frame.size()==136u+expectedSize);
                CHECK(std::memcmp(frame.data()+c.bytes.offset,expected.data()+expectedOffset,expectedSize)==0);
                CHECK(upload->append(c.value[0],frame.data()+c.bytes.offset,c.bytes.length));++chunkIndex;
            } else if(op==4099u) {
                CHECK(chunkIndex==(large?2u:1u));CHECK(!c.bytes.length);CHECK(c.value[0]==0);
                CHECK(upload->received()==expected.size());CHECK(upload->seal());CHECK(upload->copySealed(sealed));
                CHECK(sealed==expected);
            } else if(op==9u) {
                CHECK(!c.bytes.length);CHECK(c.value[0]==expected.size());CHECK(upload->sealed());CHECK(sealed==expected);
                ++classifications;result.return_bits=resultBits; // literal injected return, no SDK invoked
            } else {
                CHECK(op==4100u);CHECK(!c.bytes.length);CHECK(c.value[0]==0);CHECK(sealed==expected);
                if(fault==RefusedRelease)result.transport_status=StartupBridge::Unsupported;
                else if(fault==BadRelease)result.return_bits=1;
                else {
                    CHECK(registry.beginClose(id));CHECK(registry.retire(id));
                    upload.reset();std::vector<unsigned char>().swap(sealed);charged=0;++releases;
                    local=0;CHECK(!registry.resolve(id,MilesWire::Buffer,local));
                }
            }
        }
        for(unsigned n=(op==4097u || op==4098u || op==9u)?1u:0u;n<8;++n)CHECK(c.value[n]==0);
        MilesWire::Header reply=h;reply.kind=MilesWire::Reply;
        CHECK(MilesTransport::encodeResult(reply,result,MilesTransport::Bytes(),MilesTransport::Bytes(),frame));
        MilesWire::Header genericHeader={};MilesWire::Result generic={};
        CHECK(MilesTransport::decodeResult(bytes(frame),genericHeader,generic));
        StartupBridge::OwnedReply out;out.result.return_bits=0x12345678u;
        const bool accepted=StartupBridge::decodeReply(bytes(frame),h,out);
        if((fault==BadBegin && op==4097u) || (fault==BadRelease && op==4100u)) {
            CHECK(!accepted);CHECK(out.result.return_bits==0x12345678u);
            throw std::runtime_error("actual typed decoder rejected scripted malformed reply");
        }
        CHECK(accepted);CHECK(session.validateReply(op,fields,out));
        if(op!=4097u && result.transport_status==StartupBridge::Success) {
            MilesWire::Call wrongPhase={};wrongPhase.target=id;
            const uint32_t other=op==4100u?4099u:4100u;
            CHECK(!session.validateReply(other,wrongPhase,StartupBridge::OwnedReply()));
        }
        // No Runtime publish/returned or Endpoint is executed by this supplier.
        return out;
    }
    void finish() override {throw std::logic_error("no teardown");}
};
template<class F> static void rejects(F f) {
    bool caught=false;
    try {f();} catch(...) {caught=true;}
    CHECK(!anyCheckFailed);CHECK(caught);
}
static void terminal(Session &s,Supplier &supplier,MilesClientRuntime53::Runtime &runtime,
                     const std::vector<unsigned char> &input) {
    CHECK(s.uncertain());CHECK(runtime.failures>0);
    const unsigned calls=supplier.calls;
    rejects([&]{(void)C::file_type(input.data(),static_cast<uint32_t>(input.size()));});
    CHECK(supplier.calls==calls);CHECK(!anyCheckFailed);
}
int main(int argc,char **argv) {
    try {
        CHECK(argc==2);const std::string mode=argv[1];
        const bool budgetMode=mode=="budget";
        Supplier supplier(budgetMode?14u:2096918u);MilesClientRuntime53::Runtime runtime;
        // Synthetic placement storage avoids calling intentionally terminal Session destructor.
        // Manual release below covers test-owned C++ members only; no teardown claim.
        alignas(Session) static unsigned char storage[sizeof(Session)];
        Session &s=*new(storage) Session(&supplier,runtime,std::shared_ptr<void>(),supplier.budget);
        s.started=true;
        const unsigned char literals[]={0x52,0x00,0xff,0x7f,0x80,0x23,0x19};
        const std::vector<unsigned char> small(literals,literals+7);
        if(mode=="success") {
            const uint32_t bits[]={0u,0xffffffffu,0x80000000u,37u};
            const int32_t values[]={0,-1,INT32_MIN,37};
            for(unsigned i=0;i<4;++i) {
                std::vector<unsigned char> input=small;
                supplier.expect(small,bits[i],false);
                CHECK(C::file_type(input.data(),7)==values[i]);CHECK(input==small);
                CHECK(supplier.step==5 && supplier.charged==0 && !supplier.upload);
            }
            CHECK(supplier.classifications==4 && supplier.releases==4);
            std::puts("PASS literal-signed-results-sequential-retirement");
            std::vector<unsigned char> input(1048459u);
            for(size_t i=0;i<input.size();++i)input[i]=static_cast<unsigned char>(i&255u);
            input[1048439]=0xe1;input[1048440]=0x5a;input[1048458]=0xc3;
            const std::vector<unsigned char> original=input;
            supplier.expect(original,123u,true);
            CHECK(C::file_type(input.data(),1048459u)==123);CHECK(input==original);
            CHECK(supplier.step==6 && supplier.chunkIndex==2 && supplier.peak==2096918u);
            CHECK(supplier.classifications==5 && supplier.releases==5 && !supplier.charged);
            CHECK(!s.uncertain() && !runtime.failures);
            std::puts("PASS literal-cross-frame-reconstruction");
        } else if(budgetMode) {
            std::vector<unsigned char> over(8,0xab);const std::vector<unsigned char> original=over;
            rejects([&]{(void)C::file_type(over.data(),8);});CHECK(over==original);
            rejects([&]{(void)C::file_type(0,7);});rejects([&]{(void)C::file_type(small.data(),0);});
            CHECK(supplier.calls==0 && !s.uncertain() && !runtime.failures);
            for(unsigned i=0;i<2;++i) {
                supplier.expect(small,7u,false);CHECK(C::file_type(small.data(),7)==7);
                CHECK(supplier.charged==0 && supplier.peak==14 && supplier.step==5);
            }
            CHECK(supplier.calls==10 && supplier.releases==2);
            std::puts("PASS explicit-two-N-budget-restoration");
        } else {
            Fault fault=None;
            if(mode=="malformed-begin")fault=BadBegin;
            else if(mode=="refused-release")fault=RefusedRelease;
            else if(mode=="malformed-release")fault=BadRelease;
            else CHECK(false);
            std::vector<unsigned char> input=small;
            supplier.expect(small,37u,false,fault);
            bool returned=false;int32_t output=777;
            rejects([&]{output=C::file_type(input.data(),7);returned=true;});
            CHECK(!returned && output==777 && input==small);
            CHECK(supplier.calls==(fault==BadBegin?1u:5u));
            CHECK(supplier.classifications==(fault==BadBegin?0u:1u));
            CHECK(supplier.releases==0 && supplier.upload && supplier.charged==14);
            terminal(s,supplier,runtime,input);CHECK(input==small);
            std::printf("PASS %s-terminal-no-classification-return\n",mode.c_str());
        }
        CHECK(!anyCheckFailed);
        // Only synthetic fixture members are released; production teardown remains unavailable.
        s.samples.reset();std::string().swap(s.lastErrorSnapshot);std::string().swap(s.redistSnapshot);
        std::printf("PASS assertions=%u\n",checks);return 0;
    } catch(const std::exception &e) {std::fprintf(stderr,"FAIL %s\n",e.what());return 1;}
      catch(...) {std::fprintf(stderr,"FAIL unknown exception\n");return 1;}
}
