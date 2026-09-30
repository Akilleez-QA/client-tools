#include "session_file_owner.h"
#include <cstdio>
#include <cstdlib>
#include <new>
#include <cstring>
#include "test_allocators.h"
namespace Script36 {extern unsigned opens,closes,reads,seeks;extern int submitFailure;extern bool throwOpen,throwClose,dispatchUncertain,openFails;void pump();void pumpFirst();}
namespace MilesFileOwner36 {
// Test-only trusted authority, not production host routing or wire authority.
class HostAssociationMapper {
public:static TrustedAssociation test(uint64_t s,uint64_t i,uint64_t admission=0){
    MilesFileChannel26::Association w={i,admission?100u:0u,8,0};
    return TrustedAssociation(s,i,admission,w,admission?MilesCoordinator::CausalReverseIo:MilesCoordinator::Unsolicited);
}
};
}
using namespace MilesFileOwner36;
using namespace MilesFileChannel26;
using MilesFileExecutor30::EngineFileWorker;
static unsigned checks=0;
#define CHECK(x) do{++checks;if(!(x)){std::printf("FAIL line %d: %s\n",__LINE__,#x);return 1;}}while(0)
static std::vector<unsigned char> frame(uint32_t opcode,uint64_t id,MilesWire::Handle file=MilesWire::Handle(),bool causal=false,uint32_t n=0){
    MilesWire::Header h={};h.magic=MilesWire::Magic;h.version=MilesWire::Version;h.kind=MilesWire::ReverseRequest;h.opcode=opcode;h.request=id;h.causal_request=causal?100:0;h.lane=8;
    MilesWire::Call c={};c.target=file;if(opcode==MilesWire::FileRead)c.value[0]=n;
    std::vector<unsigned char> result;
    MilesTransport::encodeCall(h,c,MilesTransport::Bytes(),opcode==MilesWire::FileOpen?MilesTransport::Bytes("a",2):MilesTransport::Bytes(),result);return result;
}
static MilesTransport::Bytes bytes(const std::vector<unsigned char> &v){return MilesTransport::Bytes(v.data(),v.size());}
static MilesWire::Handle opened(SessionFileOwner &o,uint64_t i){
    MilesWire::Header h={};MilesWire::Result r={};MilesTransport::decodeResult(o.reply(i),h,r);return r.resource;
}
int main(){
    EngineFileWorker *worker=EngineFileWorker::create();
    std::shared_ptr<void> engine(new int(3));
    auto context=std::make_shared<FileSessionContext>(*worker,engine);
    std::weak_ptr<void> engineWatch=engine;engine.reset();
    {
        MilesCoordinator::Coordinator coordinator(77);SessionFileOwner owner(coordinator,77,1,context,2,8);
        std::vector<MilesWire::Handle> empty;
        CHECK(coordinator.admitGame(77,1,8,0,MilesCoordinator::Ordinary,empty)==MilesCoordinator::Ok);
        auto f=frame(MilesWire::FileOpen,1,MilesWire::Handle(),true);
        CHECK(owner.receive(HostAssociationMapper::test(76,1,1),bytes(f))==SessionFileOwner::Rejected);
        CHECK(owner.receive(HostAssociationMapper::test(77,1,1),bytes(f))==SessionFileOwner::Queued);
        CHECK(Script36::opens==0 && owner.retainedOperations()==1);
        CHECK(owner.receive(HostAssociationMapper::test(77,1,1),bytes(f))==SessionFileOwner::Rejected);
        MilesWire::Handle reserved={MilesWire::File,1,1};SessionFileOwner::FileState state;
        CHECK(owner.fileState(reserved,state) && state==SessionFileOwner::Reserved);
        CHECK(owner.reply(1).size==0);
        Script36::pump();CHECK(Script36::opens==1);
        denyAllocation=true;owner.poll();denyAllocation=false;
        CHECK(owner.reply(1).size==128);
        MilesWire::Handle handle=opened(owner,1);CHECK(handle.slot==1 && handle.generation==1);
        CHECK(owner.fileState(handle,state) && state==SessionFileOwner::Published);
        MilesCoordinator::Readiness ready={};CHECK(coordinator.readiness(77,1,ready)==MilesCoordinator::Ok && ready.callbackPins==1);
        CHECK(coordinator.completeAdmission(77,1)==MilesCoordinator::PendingCallback);
        CHECK(!owner.acknowledge(76,1));CHECK(owner.acknowledge(77,1));CHECK(!owner.acknowledge(77,1));
        CHECK(coordinator.completeAdmission(77,1)==MilesCoordinator::Ok);
        auto r=frame(MilesWire::FileRead,2,handle,false,19);
        CHECK(owner.receive(HostAssociationMapper::test(77,2),bytes(r))==SessionFileOwner::Queued);
        Script36::pump();denyAllocation=true;owner.poll();denyAllocation=false;
        CHECK(owner.reply(2).size==147 && owner.reply(2).data[146]==18);
        CHECK(owner.acknowledge(77,2));
        auto seek=frame(MilesWire::FileSeek,3,handle);
        CHECK(owner.receive(HostAssociationMapper::test(77,3),bytes(seek))==SessionFileOwner::Queued);
        Script36::pump();denyAllocation=true;owner.poll();denyAllocation=false;
        MilesWire::Header h={};MilesWire::Result result={};CHECK(MilesTransport::decodeResult(owner.reply(3),h,result));CHECK(result.return_bits==static_cast<uint32_t>(-17));CHECK(owner.acknowledge(77,3));
        CHECK(coordinator.beginDrain(77)==MilesCoordinator::Ok);CHECK(coordinator.beginClose(77,1)==MilesCoordinator::Ok);
        auto close=frame(MilesWire::FileClose,4,handle);
        CHECK(owner.receive(HostAssociationMapper::test(77,4),bytes(close))==SessionFileOwner::Queued);
        CHECK(owner.fileState(handle,state) && state==SessionFileOwner::ClosePending);
        auto duplicate=frame(MilesWire::FileClose,5,handle);
        CHECK(owner.receive(HostAssociationMapper::test(77,5),bytes(duplicate))==SessionFileOwner::Rejected);
        Script36::pump();denyAllocation=true;owner.poll();denyAllocation=false;
        CHECK(Script36::closes==1 && owner.fileState(handle,state) && state==SessionFileOwner::ClosedAwaitingAck);
        owner.poll();CHECK(Script36::closes==1);CHECK(owner.acknowledge(77,4));CHECK(!owner.fileState(handle,state));
        CHECK(coordinator.readiness(77,1,ready)==MilesCoordinator::Ok && ready.callbackPins==0 && ready.vendorTerminationUnproven);
    }
    // Prequeue allocation/submit refusal performs no open; unanswered callback retained.
    for(int failure=1;failure<=2;++failure){
        MilesCoordinator::Coordinator c(80+failure);SessionFileOwner o(c,80+failure,1,context,1,2);
        unsigned before=Script36::opens;Script36::submitFailure=failure;auto f=frame(MilesWire::FileOpen,1);
        CHECK(o.receive(HostAssociationMapper::test(80+failure,1),bytes(f))==SessionFileOwner::FailedUnanswered);
        CHECK(c.state()==MilesCoordinator::Failed && Script36::opens==before && o.retainedOperations()==1 && o.reply(1).size==0);
        MilesCoordinator::Readiness r={};CHECK(c.readiness(80+failure,1,r)==MilesCoordinator::Ok && r.callbackPins==1);
        Script36::submitFailure=0;
        auto late=frame(MilesWire::FileOpen,2);CHECK(o.receive(HostAssociationMapper::test(80+failure,2),bytes(late))==SessionFileOwner::FailedUnanswered);
        CHECK(Script36::opens==before && o.retainedOperations()==2 && o.reply(2).size==0);
    }
    // Fail exactly the next allocation after registry reservation but before op publication.
    {
        MilesCoordinator::Coordinator c(89);SessionFileOwner o(c,89,1,context,1,2);auto f=frame(MilesWire::FileOpen,1);
        unsigned before=Script36::opens;failAfterReservationOwner=&o;
        auto outcome=o.receive(HostAssociationMapper::test(89,1),bytes(f));failAfterReservationOwner=0;
        SessionFileOwner::FileState state;
        CHECK(reservationFailureTriggered && outcome==SessionFileOwner::FailedUnanswered);
        CHECK(c.state()==MilesCoordinator::Failed && Script36::opens==before && !o.retainedOperations());
        CHECK(!o.fileState(MilesWire::Handle{MilesWire::File,1,1},state));
        MilesCoordinator::Readiness r={};CHECK(c.readiness(89,1,r)==MilesCoordinator::Ok && r.callbackPins==0);
    }
    // Uncertain open retains the pre-reserved identity, and never retries/auto-closes.
    {
        MilesCoordinator::Coordinator c(90);SessionFileOwner o(c,90,1,context,1,2);auto f=frame(MilesWire::FileOpen,1);
        Script36::throwOpen=true;CHECK(o.receive(HostAssociationMapper::test(90,1),bytes(f))==SessionFileOwner::Queued);
        Script36::pump();Script36::throwOpen=false;o.poll();SessionFileOwner::FileState s;
        CHECK(c.state()==MilesCoordinator::Failed && o.fileState(MilesWire::Handle{MilesWire::File,1,1},s) && s==SessionFileOwner::Uncertain);
        unsigned before=Script36::opens;o.poll();CHECK(Script36::opens==before && !o.reply(1).size && !o.acknowledge(90,1));
    }
    // Close uncertainty preserves binding/generation; no repeat close or fabricated reply.
    {
        MilesCoordinator::Coordinator c(91);SessionFileOwner o(c,91,1,context,1,2);auto f=frame(MilesWire::FileOpen,1);
        CHECK(o.receive(HostAssociationMapper::test(91,1),bytes(f))==SessionFileOwner::Queued);Script36::pump();o.poll();auto h=opened(o,1);CHECK(o.acknowledge(91,1));
        auto close=frame(MilesWire::FileClose,2,h);Script36::throwClose=true;CHECK(o.receive(HostAssociationMapper::test(91,2),bytes(close))==SessionFileOwner::Queued);Script36::pump();Script36::throwClose=false;o.poll();
        SessionFileOwner::FileState s;CHECK(c.state()==MilesCoordinator::Failed && o.fileState(h,s) && s==SessionFileOwner::Uncertain);
        unsigned before=Script36::closes;o.poll();CHECK(before==Script36::closes && !o.reply(2).size && !o.acknowledge(91,2));
    }
    // Earlier dispatch uncertainty stays sticky across later known close and its ACK.
    {
        MilesCoordinator::Coordinator c(93);SessionFileOwner o(c,93,1,context,1,5);auto f=frame(MilesWire::FileOpen,1);
        CHECK(o.receive(HostAssociationMapper::test(93,1),bytes(f))==SessionFileOwner::Queued);Script36::pump();o.poll();auto h=opened(o,1);CHECK(o.acknowledge(93,1));
        auto read=frame(MilesWire::FileRead,2,h,false,1);Script36::dispatchUncertain=true;
        CHECK(o.receive(HostAssociationMapper::test(93,2),bytes(read))==SessionFileOwner::Queued);Script36::dispatchUncertain=false;
        auto close=frame(MilesWire::FileClose,3,h);CHECK(o.receive(HostAssociationMapper::test(93,3),bytes(close))==SessionFileOwner::Queued);
        Script36::pump();o.poll();SessionFileOwner::FileState state;
        CHECK(o.fileState(h,state) && state==SessionFileOwner::Uncertain && !o.reply(2).size && o.reply(3).size==128);
        CHECK(o.acknowledge(93,3));CHECK(o.fileState(h,state) && state==SessionFileOwner::Uncertain);
        CHECK(o.retainedOperations()==1 && c.state()==MilesCoordinator::Failed && !o.acknowledge(93,2));
    }
    // Healthy close ACK cannot retire a file before an earlier read ACK.
    {
        MilesCoordinator::Coordinator c(95);SessionFileOwner o(c,95,1,context,1,5);auto f=frame(MilesWire::FileOpen,1);
        CHECK(o.receive(HostAssociationMapper::test(95,1),bytes(f))==SessionFileOwner::Queued);Script36::pump();o.poll();auto h=opened(o,1);CHECK(o.acknowledge(95,1));
        auto read=frame(MilesWire::FileRead,2,h,false,1);auto close=frame(MilesWire::FileClose,3,h);
        CHECK(o.receive(HostAssociationMapper::test(95,2),bytes(read))==SessionFileOwner::Queued);CHECK(o.receive(HostAssociationMapper::test(95,3),bytes(close))==SessionFileOwner::Queued);
        Script36::pump();o.poll();SessionFileOwner::FileState state;CHECK(o.acknowledge(95,3));CHECK(o.fileState(h,state));CHECK(o.acknowledge(95,2));CHECK(!o.fileState(h,state));
    }
    // Reused operation slot makes later close poll before earlier uncertain seek.
    {
        MilesCoordinator::Coordinator c(96);SessionFileOwner o(c,96,1,context,1,5);auto f=frame(MilesWire::FileOpen,1);
        CHECK(o.receive(HostAssociationMapper::test(96,1),bytes(f))==SessionFileOwner::Queued);Script36::pump();o.poll();auto h=opened(o,1);CHECK(o.acknowledge(96,1));
        auto read=frame(MilesWire::FileRead,2,h,false,1);auto seek=frame(MilesWire::FileSeek,3,h);
        CHECK(o.receive(HostAssociationMapper::test(96,2),bytes(read))==SessionFileOwner::Queued);Script36::dispatchUncertain=true;CHECK(o.receive(HostAssociationMapper::test(96,3),bytes(seek))==SessionFileOwner::Queued);Script36::dispatchUncertain=false;
        Script36::pumpFirst();o.poll();CHECK(o.acknowledge(96,2));auto close=frame(MilesWire::FileClose,4,h);CHECK(o.receive(HostAssociationMapper::test(96,4),bytes(close))==SessionFileOwner::Queued);
        Script36::pump();o.poll();CHECK(o.acknowledge(96,4));SessionFileOwner::FileState state;CHECK(o.fileState(h,state) && state==SessionFileOwner::Uncertain && o.retainedOperations()==1);
    }
    // Observed native open failure is a genuine reply, not transport failure.
    {
        MilesCoordinator::Coordinator c(94);SessionFileOwner o(c,94,1,context,1,2);auto f=frame(MilesWire::FileOpen,1);
        Script36::openFails=true;CHECK(o.receive(HostAssociationMapper::test(94,1),bytes(f))==SessionFileOwner::Queued);Script36::pump();Script36::openFails=false;
        denyAllocation=true;o.poll();denyAllocation=false;
        CHECK(o.reply(1).size==128 && !opened(o,1).slot && c.state()==MilesCoordinator::Active);CHECK(o.acknowledge(94,1));
    }
    // File capacity is exhausted before an additional open is submitted.
    {
        MilesCoordinator::Coordinator c(92);SessionFileOwner o(c,92,1,context,1,3);auto f=frame(MilesWire::FileOpen,1);
        CHECK(o.receive(HostAssociationMapper::test(92,1),bytes(f))==SessionFileOwner::Queued);auto g=frame(MilesWire::FileOpen,2);
        CHECK(o.receive(HostAssociationMapper::test(92,2),bytes(g))==SessionFileOwner::FailedUnanswered);Script36::pump();o.poll();
    }
    // Allocation-free codec parity and rejected-output preservation, including payload.
    for(unsigned n=0;n<17;++n){
        MilesWire::Header h={};h.magic=MilesWire::Magic;h.version=MilesWire::Version;h.kind=MilesWire::ReverseReply;h.opcode=MilesWire::FileRead;h.request=44;h.lane=8;
        MilesWire::Result r={};r.return_bits=0xffffffffu;r.resource=MilesWire::Handle{MilesWire::File,3,4};
        unsigned char payload[17]={};for(unsigned i=0;i<n;++i)payload[i]=static_cast<unsigned char>(i);
        std::vector<unsigned char> expected;CHECK(MilesTransport::encodeResult(h,r,MilesTransport::Bytes(payload,n),MilesTransport::Bytes(),expected));
        unsigned char output[145]={};size_t written=999;
        denyAllocation=true;bool good=MilesTransport::encodeResultInto(h,r,MilesTransport::Bytes(payload,n),MilesTransport::Bytes(),output,sizeof output,written);denyAllocation=false;
        CHECK(good && written==expected.size() && std::memcmp(output,expected.data(),written)==0);
        written=999;output[0]=42;CHECK(!MilesTransport::encodeResultInto(h,r,MilesTransport::Bytes(payload,n),MilesTransport::Bytes(),output,127,written));CHECK(written==999 && output[0]==42);
        h.magic=0;CHECK(!MilesTransport::encodeResultInto(h,r,MilesTransport::Bytes(),MilesTransport::Bytes(),output,sizeof output,written));CHECK(written==999 && output[0]==42);
    }
    CHECK(!engineWatch.expired());context.reset();CHECK(engineWatch.expired());EngineFileWorker::destroy(worker);
    std::printf("PASS %u portable owner/encoding checks; scripted platform only\n",checks);return 0;
}
