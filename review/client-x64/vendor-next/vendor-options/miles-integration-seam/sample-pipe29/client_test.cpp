#include "../backend-boundary24/pipe/Session.h"
#include "../native-sample27/ClientMilesSample.h"
#include "prepared_input.h"
#include <cstdio>
#include <stdexcept>
#include <cstring>
#include <cstdlib>
#include <new>

static bool failAllocation=false;
static int allocationsUntilFailure=-1;
void *operator new(std::size_t size) {
    if (allocationsUntilFailure==0) { allocationsUntilFailure=-1; throw std::bad_alloc(); }
    if (allocationsUntilFailure>0) --allocationsUntilFailure;
    if (failAllocation) { failAllocation=false; throw std::bad_alloc(); }
    void *p=std::malloc(size?size:1); if (!p) throw std::bad_alloc(); return p;
}
void operator delete(void *p) noexcept { std::free(p); }
void *operator new[](std::size_t size) { return ::operator new(size); }
void operator delete[](void *p) noexcept { ::operator delete(p); }

static unsigned checks=0;
#define CHECK(x) do { if (!(x)) throw std::runtime_error(#x); ++checks; } while(0)
using namespace MilesWire;
struct Script : ClientMilesPipe::Channel {
    unsigned calls, allocations, releases, mask;
    uint32_t nextKind;
    bool nullAllocation, throwsNext, extraOutput, extraField;
    uint32_t refused;
    Script() : calls(0), allocations(0), releases(0), mask(0), nextKind(OwnedSample),
        nullAllocation(false), throwsNext(false), extraOutput(false), extraField(false), refused(0) {}
    StartupBridge::OwnedReply call(uint32_t op,const Call &fields,MilesTransport::Bytes) override {
        ++calls;
        if (throwsNext) { throwsNext=false; throw std::runtime_error("uncertain exchange"); }
        Result result={}; result.transport_status=refused; refused=0;
        if (!result.transport_status) {
            if (op==AIL_startup) result.return_bits=1;
            if (op==AIL_open_digital_driver) result.resource=Handle{Driver,1,1};
            if (op==AIL_allocate_sample_handle) {
                CHECK(fields.target.kind==Driver); ++allocations;
                if (!nullAllocation) result.resource=Handle{nextKind,2,allocations};
            }
            if (op==AIL_sample_ms_position) {
                CHECK(fields.target.kind==OwnedSample);
                mask=fields.output_mask;
                result.value[0]=(mask&1)?static_cast<uint32_t>(-37):0;
                result.value[1]=(mask&2)?static_cast<uint32_t>(-123):0;
                if (extraOutput) result.value[1]=42;
                if (extraField) result.value[3]=42;
            }
            if (op==AIL_release_sample_handle) { CHECK(fields.target.kind==OwnedSample); ++releases; }
        }
        Header expected={}; expected.magic=Magic; expected.version=Version;
        expected.kind=Request; expected.opcode=op; expected.request=calls; expected.lane=1;
        Header response=expected; response.kind=Reply;
        std::vector<unsigned char> frame;
        CHECK(MilesTransport::encodeResult(response,result,MilesTransport::Bytes(),MilesTransport::Bytes(),frame));
        StartupBridge::OwnedReply out;
        if (!StartupBridge::decodeReply(MilesTransport::Bytes(&frame[0],frame.size()),expected,out))
            throw std::runtime_error("typed reply rejected");
        return out;
    }
    void finish() override {}
};
template<class F> void failure(F fn,ClientMiles::FailureReason reason) {
    bool caught=false; try { fn(); } catch(const ClientMiles::Failure &e) { caught=e.reason()==reason; }
    CHECK(caught);
}
static ClientMiles::HDIGDRIVER start() {
    CHECK(ClientMiles::startup()==1);
    return ClientMiles::open_digital_driver(22050,16,2,0);
}
static void basic() {
    Script *script=new Script;
    ClientMilesPipe::Session session{std::unique_ptr<ClientMilesPipe::Channel>(script)};
    ClientMiles::HDIGDRIVER driver=start();
    unsigned beforeAllocation=script->calls;
    failAllocation=true;
    bool allocationCaught=false;
    try { ClientMiles::allocate_sample_handle(driver); } catch(const std::bad_alloc &) { allocationCaught=true; }
    CHECK(allocationCaught && !failAllocation && script->calls==beforeAllocation);
    script->nullAllocation=true;
    CHECK(ClientMiles::allocate_sample_handle(driver)==0);
    script->nullAllocation=false;
    ClientMiles::HSAMPLE sample=ClientMiles::allocate_sample_handle(driver);
    CHECK(sample!=0);
    CHECK(session.sampleProxyCount()==1);
    for(unsigned mask=0;mask<4;++mask) {
        int32_t total=77,current=88;
        ClientMiles::sample_ms_position(sample,(mask&1)?&total:0,(mask&2)?&current:0);
        CHECK(script->mask==mask); CHECK(total==((mask&1)?-37:77)); CHECK(current==((mask&2)?-123:88));
    }
    script->refused=StartupBridge::InvalidResource;
    int32_t total=55,current=66;
    failure([&]{ClientMiles::sample_ms_position(sample,&total,&current);},ClientMiles::FailureReason::InvalidDriver);
    CHECK(total==55 && current==66);
    ClientMiles::end_sample(sample);
    ClientMiles::release_sample_handle(sample);
    CHECK(session.sampleProxyCount()==0); // released raw pointer is now invalid; never reuse it
    ClientMiles::HSAMPLE newer=ClientMiles::allocate_sample_handle(driver);
    CHECK(newer!=0 && session.sampleProxyCount()==1);
    ClientMiles::release_sample_handle(newer);
    ClientMiles::shutdown(); session.close();
}
static void faults(unsigned scenario) {
    Script *script=new Script;
    ClientMilesPipe::Session session{std::unique_ptr<ClientMilesPipe::Channel>(script)};
    ClientMiles::HDIGDRIVER driver=start();
    ClientMiles::HSAMPLE sample=0;
    if (scenario>1) sample=ClientMiles::allocate_sample_handle(driver);
    int32_t total=51,current=61;
    if(scenario==0) { script->throwsNext=true; failure([&]{ClientMiles::allocate_sample_handle(driver);},ClientMiles::FailureReason::BackendFailed); }
    if(scenario==1) { script->nextKind=BorrowedSample; failure([&]{ClientMiles::allocate_sample_handle(driver);},ClientMiles::FailureReason::BackendFailed); }
    if(scenario==2) { script->throwsNext=true; failure([&]{ClientMiles::release_sample_handle(sample);},ClientMiles::FailureReason::BackendFailed); }
    if(scenario==3) { script->throwsNext=true; failure([&]{ClientMiles::sample_ms_position(sample,&total,&current);},ClientMiles::FailureReason::BackendFailed); }
    if(scenario==4) { script->extraOutput=true; failure([&]{ClientMiles::sample_ms_position(sample,&total,0);},ClientMiles::FailureReason::BackendFailed); }
    if(scenario==5) { script->extraField=true; failure([&]{ClientMiles::sample_ms_position(sample,&total,&current);},ClientMiles::FailureReason::BackendFailed); }
    CHECK(total==51 && current==61);
    unsigned before=script->calls;
    failure([&]{ClientMiles::allocate_sample_handle(driver);},ClientMiles::FailureReason::BackendFailed);
    failure([]{ClientMiles::shutdown();},ClientMiles::FailureReason::BackendFailed);
    CHECK(script->calls==before); // Session abandonment is not observed remote release.
}
static void repeated() {
    Script *script=new Script;
    ClientMilesPipe::Session session{std::unique_ptr<ClientMilesPipe::Channel>(script)};
    ClientMiles::HDIGDRIVER driver=start();
    for(unsigned i=0;i<256;++i) {
        auto sample=ClientMiles::allocate_sample_handle(driver);
        CHECK(sample && session.sampleProxyCount()==1);
        ClientMiles::release_sample_handle(sample);
        CHECK(session.sampleProxyCount()==0);
    }
    CHECK(script->allocations==256 && script->releases==256);
    script->refused=StartupBridge::LifecycleRefused;
    failure([&]{ClientMiles::allocate_sample_handle(driver);},ClientMiles::FailureReason::WrongState);
    CHECK(session.sampleProxyCount()==0 && !session.uncertain());
    script->nullAllocation=true;
    CHECK(!ClientMiles::allocate_sample_handle(driver) && session.sampleProxyCount()==0);
    script->nullAllocation=false;
    const unsigned before=script->calls;
    allocationsUntilFailure=1; // proxy allocation succeeds; list publication fails
    bool caught=false;
    try { ClientMiles::allocate_sample_handle(driver); } catch(const std::bad_alloc &) { caught=true; }
    CHECK(caught && allocationsUntilFailure==-1 && script->calls==before && session.sampleProxyCount()==0);
    auto sample=ClientMiles::allocate_sample_handle(driver);
    script->refused=StartupBridge::LifecycleRefused;
    failure([&]{ClientMiles::release_sample_handle(sample);},ClientMiles::FailureReason::WrongState);
    CHECK(session.sampleProxyCount()==1 && !session.uncertain());
    ClientMiles::release_sample_handle(sample);
    CHECK(session.sampleProxyCount()==0);
    ClientMiles::shutdown();session.close();
}
static void shutdownLive(unsigned scenario) {
    Script *script=new Script;
    ClientMilesPipe::Session session{std::unique_ptr<ClientMilesPipe::Channel>(script)};
    auto sample=ClientMiles::allocate_sample_handle(start());
    const unsigned before=script->calls;
    if(scenario==1) {
        script->refused=StartupBridge::LifecycleRefused;
        failure([]{ClientMiles::shutdown();},ClientMiles::FailureReason::WrongState);
        CHECK(script->calls==before+1 && session.sampleProxyCount()==1 && !session.uncertain());
        ClientMiles::end_sample(sample); // refusal preserves usable ownership
    }
    if(scenario==2) {
        script->throwsNext=true;
        failure([]{ClientMiles::shutdown();},ClientMiles::FailureReason::BackendFailed);
        CHECK(script->calls==before+1 && session.sampleProxyCount()==1 && session.uncertain());
        failure([&]{ClientMiles::end_sample(sample);},ClientMiles::FailureReason::BackendFailed);
        failure([]{ClientMiles::shutdown();},ClientMiles::FailureReason::BackendFailed);
        CHECK(script->calls==before+1 && session.sampleProxyCount()==1);
        return; // local abandonment is not vendor cleanup
    }
    ClientMiles::shutdown();
    CHECK(session.sampleProxyCount()==0 && !session.started && session.stopped);
    session.close();
}
static void retained() {
    const unsigned char original[]={1,2,3,4}; char suffix[]=".wav";
    MilesHost::BufferUpload upload(4,4);
    CHECK(upload.append(0,original,4));
    bool caught=false;
    try { SamplePipe28::PreparedInput invalid(upload,suffix,9); } catch(const std::invalid_argument &) { caught=true; }
    CHECK(caught); CHECK(upload.seal());
    SamplePipe28::PreparedInput prepared(upload,suffix,9); suffix[1]='x';
    CHECK(prepared.image().size==4 && prepared.image().data[2]==3);
    CHECK(std::strcmp(reinterpret_cast<const char *>(prepared.suffix().data),".wav")==0);
    caught=false;
    try { SamplePipe28::PreparedInput invalid(upload,suffix,8); } catch(const std::length_error &) { caught=true; }
    CHECK(caught);
}
int main() {
    try { basic(); for(unsigned i=0;i<6;++i) faults(i); repeated(); for(unsigned i=0;i<3;++i) shutdownLive(i); retained();
        std::printf("PASS %u scripted assertions; no vendor/engine/runtime\n",checks); return 0; }
    catch(const std::exception &e) { std::fprintf(stderr,"FAIL %s\n",e.what()); return 1; }
}
