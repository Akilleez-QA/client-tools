#include "backend-boundary24/pipe/Session.h"
#include "native-sample27/ClientMilesSample.h"
#include <cassert>
#include <cstdio>
#include <stdexcept>
struct CheckedChannel : ClientMilesPipe::Channel {
    unsigned calls=0, allocated=0, released=0, lastMask=99;
    unsigned refusal=0;
    bool nullNext=false, throwNext=false;
    StartupBridge::OwnedReply call(uint32_t op, const MilesWire::Call &c, MilesTransport::Bytes) override {
        ++calls;
        if(throwNext) { throwNext=false; throw std::runtime_error("lost reply"); }
        MilesWire::Result r={}; r.transport_status=refusal; refusal=0;
        if(!r.transport_status) {
            if(op==MilesWire::AIL_startup) r.return_bits=1;
            if(op==MilesWire::AIL_open_digital_driver) r.resource=MilesWire::Handle{MilesWire::Driver,1,1};
            if(op==MilesWire::AIL_allocate_sample_handle) {
                ++allocated;
                assert(c.target.kind==MilesWire::Driver);
                if(!nullNext) r.resource=MilesWire::Handle{MilesWire::OwnedSample,2,allocated};
                nullNext=false;
            }
            if(op==MilesWire::AIL_sample_ms_position) {
                lastMask=c.output_mask;
                if(c.output_mask&1) r.value[0]=0x80000000u;
                if(c.output_mask&2) r.value[1]=0xffffffffu;
            }
            if(op==MilesWire::AIL_release_sample_handle) ++released;
        }
        MilesWire::Header h={}; h.magic=MilesWire::Magic; h.version=MilesWire::Version;
        h.kind=MilesWire::Reply; h.opcode=op; h.request=calls; h.lane=1;
        std::vector<unsigned char> frame;
        assert(MilesTransport::encodeResult(h,r,{}, {},frame));
        StartupBridge::OwnedReply reply; h.kind=MilesWire::Request;
        assert(StartupBridge::decodeReply(MilesTransport::Bytes(frame.data(),frame.size()),h,reply));
        return reply;
    }
    void finish() override {}
};
template<class F> void fails(F f, ClientMiles::FailureReason reason) {
    bool caught=false;
    try { f(); } catch(const ClientMiles::Failure &e) { caught=e.reason()==reason; }
    assert(caught);
}
int main() {
    CheckedChannel *channel=new CheckedChannel;
    ClientMilesPipe::Session session{std::unique_ptr<ClientMilesPipe::Channel>(channel)};
    assert(ClientMiles::startup()==1);
    auto driver=ClientMiles::open_digital_driver(22050,16,2,0);
    channel->nullNext=true;
    assert(ClientMiles::allocate_sample_handle(driver)==0 && session.sampleProxyCount()==0);
    for(unsigned n=0;n<64;++n) {
        auto sample=ClientMiles::allocate_sample_handle(driver);
        for(unsigned mask=0;mask<4;++mask) {
            int32_t a=11,b=22;
            ClientMiles::sample_ms_position(sample,(mask&1)?&a:0,(mask&2)?&b:0);
            assert(channel->lastMask==mask);
            assert(a==((mask&1)?INT32_MIN:11) && b==((mask&2)?-1:22));
        }
        ClientMiles::end_sample(sample); // end preserves allocation and queryability
        int32_t a=11,b=22;
        ClientMiles::sample_ms_position(sample,&a,&b);
        channel->refusal=StartupBridge::LifecycleRefused;
        fails([&]{ClientMiles::release_sample_handle(sample);},ClientMiles::FailureReason::WrongState);
        assert(session.sampleProxyCount()==1 && !session.uncertain());
        ClientMiles::release_sample_handle(sample);
        assert(session.sampleProxyCount()==0);
    }
    assert(channel->released==64);
    auto sample=ClientMiles::allocate_sample_handle(driver);
    int32_t a=11,b=22;
    channel->refusal=StartupBridge::LifecycleRefused;
    fails([&]{ClientMiles::sample_ms_position(sample,&a,&b);},ClientMiles::FailureReason::WrongState);
    assert(a==11 && b==22 && !session.uncertain());
    channel->throwNext=true;
    fails([&]{ClientMiles::sample_ms_position(sample,&a,&b);},ClientMiles::FailureReason::BackendFailed);
    assert(a==11 && b==22 && session.uncertain());
    const unsigned calls=channel->calls;
    fails([&]{ClientMiles::shutdown();},ClientMiles::FailureReason::BackendFailed);
    assert(channel->calls==calls);
    puts("PASS bounded source-only client/codec check; no native or host execution");
}
