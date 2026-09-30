#include "host_association_mapper.h"
#include "../callback-composition46/selected_fixture.h"
#include <cstdio>
#include <stdexcept>
namespace Script36 {
extern unsigned opens, closes;
extern bool dispatchUncertain, throwOpen, openFails;
void pump();
}
using namespace MilesFileOwner36;
using MilesFileExecutor30::EngineFileWorker;
static unsigned checks = 0;
#define CHECK(x) do { ++checks; if (!(x)) { std::printf("FAIL line %d: %s\n", __LINE__, #x); throw std::runtime_error("check"); } } while (0)
static const uint64_t Session = 77, Background = 999;
struct Fixture {
    std::unique_ptr<EngineFileWorker, void (*)(EngineFileWorker *)> worker;
    std::shared_ptr<FileSessionContext> context;
    const uint64_t session;
    MilesCoordinator::Coordinator coordinator;
    SessionFileOwner owner;
    HostAssociationMapper mapper;
    explicit Fixture(size_t capacity = 8, uint64_t sessionId = Session, bool alternate = false,
        std::shared_ptr<void> callbackLifetime = std::shared_ptr<void>(new int(2)), size_t fileCapacity = 8)
        : worker(EngineFileWorker::create(), &EngineFileWorker::destroy),
          context(new FileSessionContext(*worker, std::shared_ptr<void>(new int(1)),
              Script46::selected(alternate, callbackLifetime))), session(sessionId),
          coordinator(session), owner(coordinator, session, 1, context, fileCapacity, 8),
          mapper(session, Background, coordinator, owner, capacity) {}
    void begin(uint64_t wire = 100, uint64_t admission = 1, uint64_t lease = 0,
               MilesCoordinator::Action action = MilesCoordinator::Ordinary) {
        CHECK(mapper.publishCommand(wire, admission, 8, lease, action,
            std::vector<MilesWire::Handle>()) == MilesCoordinator::Ok);
    }
    MilesCoordinator::Readiness pins() const {
        MilesCoordinator::Readiness result = {};
        CHECK(coordinator.readiness(session, 1, result) == MilesCoordinator::Ok);
        return result;
    }
};
static std::vector<unsigned char> request(uint64_t reverse, uint64_t cause = 100,
    uint64_t lane = 8, uint64_t lease = 0, uint32_t opcode = MilesWire::FileOpen,
    MilesWire::Handle target = MilesWire::Handle(), uint32_t value = 0) {
    MilesWire::Header header = {};
    header.magic = MilesWire::Magic; header.version = MilesWire::Version;
    header.kind = MilesWire::ReverseRequest; header.opcode = opcode;
    header.request = reverse; header.causal_request = cause;
    header.lane = lane; header.lock_lease = lease;
    MilesWire::Call call = {}; call.target = target; call.value[0] = value;
    std::vector<unsigned char> frame;
    CHECK(MilesTransport::encodeCall(header, call, MilesTransport::Bytes(),
        opcode == MilesWire::FileOpen ? MilesTransport::Bytes("a", 2) : MilesTransport::Bytes(), frame));
    return frame;
}
static MilesTransport::Bytes bytes(const std::vector<unsigned char> &v) {
    return MilesTransport::Bytes(v.data(), v.size());
}
static void ready(Fixture &f) { Script36::pump(); f.mapper.poll(); }
static void acknowledge(Fixture &f, uint64_t wire) {
    CHECK(f.mapper.markReplyQueued(wire));
    CHECK(f.mapper.acknowledgeConsumed(f.session, wire));
}
int main() {
    try {
        // Forward return first: the command stays pinned until its real ACK.
        {
            Fixture f; f.begin(); auto frame = request(501);
            unsigned before = Script36::opens;
            CHECK(f.mapper.receiveReverse(Session, bytes(frame)) == SessionFileOwner::Queued);
            CHECK(Script36::opens == before && f.mapper.retainedReverse() == 1);
            CHECK(f.mapper.reply(1).size == 0); // Local intake is NOT reverse identity.
            ready(f); CHECK(Script36::opens == before + 1 && f.mapper.reply(501).size == 128);
            CHECK(f.mapper.observeForwardReturn(Session, 100));
            CHECK(f.mapper.commandState() == HostAssociationMapper::ReturnedWaiting);
            CHECK(f.pins().requestPins == 1 && f.pins().callbackPins == 1);
            CHECK(!f.mapper.consumeCommand(100));
            CHECK(f.mapper.publishCommand(200, 2, 8, 0, MilesCoordinator::Ordinary,
                std::vector<MilesWire::Handle>()) == MilesCoordinator::Busy);
            acknowledge(f, 501);
            CHECK(f.mapper.commandState() == HostAssociationMapper::Settled);
            CHECK(f.pins().requestPins == 0 && f.pins().callbackPins == 0);
            CHECK(!f.mapper.consumeCommand(99)); CHECK(f.mapper.consumeCommand(100));
            CHECK(!f.mapper.consumeCommand(100)); f.begin(200, 2);
            CHECK(f.mapper.currentWireRequest() == 200);
        }
        std::puts("PASS forward-before-ACK join and distinct wire/local IDs");
        // ACK first: callback settlement is not a forward completion observation.
        {
            Fixture f; f.begin(); auto frame = request(91);
            CHECK(f.mapper.receiveReverse(Session, bytes(frame)) == SessionFileOwner::Queued);
            ready(f); acknowledge(f, 91);
            CHECK(f.mapper.commandState() == HostAssociationMapper::Executing);
            CHECK(f.pins().requestPins == 1 && f.pins().callbackPins == 0);
            CHECK(f.mapper.observeForwardReturn(Session, 100));
            CHECK(f.mapper.commandState() == HostAssociationMapper::Settled);
            CHECK(f.mapper.consumeCommand(100));
        }
        std::puts("PASS ACK-before-forward join");
        // Background work does not borrow an active command's identity or lease.
        {
            Fixture f; f.begin(); auto frame = request(71, 0, Background);
            CHECK(f.mapper.receiveReverse(Session, bytes(frame)) == SessionFileOwner::Queued);
            ready(f); CHECK(f.mapper.observeForwardReturn(Session, 100));
            CHECK(f.mapper.commandState() == HostAssociationMapper::Settled);
            CHECK(f.pins().requestPins == 0 && f.pins().callbackPins == 1);
            CHECK(f.mapper.consumeCommand(100)); f.begin(200, 2);
            acknowledge(f, 71);
            CHECK(f.mapper.commandState() == HostAssociationMapper::Executing);
        }
        std::puts("PASS unsolicited callback during unrelated command");
        {
            Fixture f; auto open = request(9, 0, Background);
            CHECK(f.mapper.receiveReverse(Session, bytes(open)) == SessionFileOwner::Queued);
            ready(f); MilesWire::Header h = {}; MilesWire::Result result = {};
            CHECK(MilesTransport::decodeResult(f.mapper.reply(9), h, result));
            acknowledge(f, 9);
            auto close = request(10, 0, Background, 0, MilesWire::FileClose, result.resource);
            CHECK(f.mapper.receiveReverse(Session, bytes(close)) == SessionFileOwner::Queued);
            ready(f); acknowledge(f, 10);
            SessionFileOwner::FileState state;
            CHECK(!f.owner.fileState(result.resource, state));
            CHECK(f.mapper.commandState() == HostAssociationMapper::Empty && !f.mapper.retainedReverse());
        }
        std::puts("PASS idle callback open-close lifetime");
        // Verify each causal field and the reserved background convention.
        for (unsigned mode = 0; mode != 6; ++mode) {
            Fixture f; f.begin();
            auto frame = request(1, mode == 0 ? 999 : mode >= 3 ? 0 : 100,
                mode == 1 ? 9 : mode == 3 ? Background : mode == 4 ? 8 : mode >= 3 ? Background : 8,
                mode == 2 || mode == 3 ? 1 : 0);
            unsigned before = Script36::opens;
            CHECK(f.mapper.receiveReverse(mode == 5 ? 78 : Session, bytes(frame)) == SessionFileOwner::Rejected);
            CHECK(f.coordinator.state() == MilesCoordinator::Failed);
            CHECK(Script36::opens == before && !f.owner.retainedOperations());
        }
        std::puts("PASS causal/session/lane/lease validation");
        {
            Fixture f;
            CHECK(f.mapper.publishCommand(100, 1, 8, 0, MilesCoordinator::AcquireLock,
                std::vector<MilesWire::Handle>()) == MilesCoordinator::InvalidIdentity);
            CHECK(f.mapper.publishCommand(100, 1, 8, 0, MilesCoordinator::ReleaseLock,
                std::vector<MilesWire::Handle>()) == MilesCoordinator::InvalidIdentity);
            CHECK(f.mapper.commandState() == HostAssociationMapper::Empty);
            CHECK(f.coordinator.activeAdmission() == 0 && f.coordinator.leaseDepth() == 0);
            f.begin();
        }
        std::puts("PASS unsupported lock actions rejected before admission");
        // Replay while pending and after retirement never repeats a file call.
        for (unsigned after = 0; after != 2; ++after) {
            Fixture f; f.begin(); auto frame = request(80);
            CHECK(f.mapper.receiveReverse(Session, bytes(frame)) == SessionFileOwner::Queued);
            ready(f); if (after) acknowledge(f, 80);
            unsigned before = Script36::opens;
            CHECK(f.mapper.receiveReverse(Session, bytes(frame)) == SessionFileOwner::Rejected);
            ready(f); CHECK(Script36::opens == before && f.coordinator.state() == MilesCoordinator::Failed);
        }
        std::puts("PASS reverse replay before and after ACK");
        // ACK has to identify a transmitted reverse result, not an intake ordinal.
        for (unsigned mode = 0; mode != 4; ++mode) {
            Fixture f; f.begin(); auto frame = request(501);
            CHECK(f.mapper.receiveReverse(Session, bytes(frame)) == SessionFileOwner::Queued);
            ready(f);
            if (mode) CHECK(f.mapper.markReplyQueued(501));
            if (mode == 3) CHECK(f.mapper.acknowledgeConsumed(Session, 501));
            CHECK(!f.mapper.acknowledgeConsumed(mode == 2 ? 78 : Session, mode == 1 ? 1 : 501));
            CHECK(f.coordinator.state() == MilesCoordinator::Failed);
            CHECK(f.owner.retainedOperations() == (mode == 3 ? 0u : 1u));
        }
        std::puts("PASS early/stale/duplicate/peer-intake ACK rejection");
        {
            Fixture f; f.begin(); auto frame = request(1);
            Script36::dispatchUncertain = true;
            CHECK(f.mapper.receiveReverse(Session, bytes(frame)) == SessionFileOwner::Queued);
            Script36::dispatchUncertain = false; ready(f);
            CHECK(f.mapper.observeForwardReturn(Session, 100));
            CHECK(f.mapper.commandState() == HostAssociationMapper::ReturnedWaiting);
            CHECK(f.coordinator.state() == MilesCoordinator::Failed);
            CHECK(!f.mapper.reply(1).size && f.mapper.retainedReverse() == 1);
            CHECK(f.pins().requestPins == 1 && f.pins().callbackPins == 1);
        }
        std::puts("PASS uncertain file execution retains forward and callback pins");
        {
            Fixture f(1); f.begin(); auto frame = request(1);
            CHECK(f.mapper.receiveReverse(Session, bytes(frame)) == SessionFileOwner::Queued);
            frame = request(2);
            CHECK(f.mapper.receiveReverse(Session, bytes(frame)) == SessionFileOwner::FailedUnanswered);
            CHECK(f.owner.retainedOperations() == 1 && f.mapper.retainedReverse() == 1);
            ready(f); // Only previously admitted work may run.
        }
        std::puts("PASS reverse storage capacity fails before second file admission");
        {
            Fixture f; f.begin(); auto frame = request(1); frame.resize(8);
            CHECK(f.mapper.receiveReverse(Session, bytes(frame)) == SessionFileOwner::Rejected);
            CHECK(!f.owner.retainedOperations());
        }
        std::puts("PASS malformed frame rejected");
        // Two complete independent sessions use real retained tables through every layer.
        {
            CHECK(sizeof(ClientMiles::FileHandle)>sizeof(uint32_t));
            std::shared_ptr<void> lifeA(new int(11)),lifeB(new int(22));
            std::weak_ptr<void> watchA=lifeA,watchB=lifeB;
            {
                Fixture a(8,177,false,lifeA),b(8,178,true,lifeB);
                lifeA.reset();lifeB.reset();a.context.reset();b.context.reset();
                a.begin();b.begin();auto open=request(501);
                const unsigned beforeA=Script36::opens,beforeB=Script46::opensB;
                CHECK(a.mapper.receiveReverse(a.session,bytes(open))==SessionFileOwner::Queued);
                CHECK(b.mapper.receiveReverse(b.session,bytes(open))==SessionFileOwner::Queued);
                CHECK(Script36::opens==beforeA && Script46::opensB==beforeB);
                ready(b);a.mapper.poll();
                CHECK(Script36::opens==beforeA+1 && Script46::opensB==beforeB+1);
                MilesWire::Header h={};MilesWire::Result ar={},br={};
                CHECK(MilesTransport::decodeResult(a.mapper.reply(501),h,ar));
                CHECK(MilesTransport::decodeResult(b.mapper.reply(501),h,br));
                CHECK(ar.return_bits==7 && br.return_bits==UINT32_C(0x80000001));
                CHECK(!watchA.expired() && !watchB.expired());
                CHECK(a.mapper.observeForwardReturn(a.session,100));
                CHECK(b.mapper.observeForwardReturn(b.session,100));
                acknowledge(b,501);CHECK(a.mapper.commandState()==HostAssociationMapper::ReturnedWaiting);
                acknowledge(a,501);CHECK(a.mapper.consumeCommand(100));CHECK(b.mapper.consumeCommand(100));
                CHECK(!watchA.expired() && !watchB.expired());
                // Same reverse IDs across sessions remain separate; local B handle stays >32 bits.
                auto readA=request(502,0,Background,0,MilesWire::FileRead,ar.resource,3);
                auto readB=request(502,0,Background,0,MilesWire::FileRead,br.resource,3);
                CHECK(a.mapper.receiveReverse(a.session,bytes(readA))==SessionFileOwner::Queued);
                CHECK(b.mapper.receiveReverse(b.session,bytes(readB))==SessionFileOwner::Queued);
                ready(a);b.mapper.poll();
                CHECK(a.mapper.reply(502).size==131 && b.mapper.reply(502).size==131);
                CHECK(a.mapper.reply(502).data[128]==0 && b.mapper.reply(502).data[128]==0xa0);
                CHECK(Script46::readsB==1);acknowledge(a,502);acknowledge(b,502);
                auto seekA=request(503,0,Background,0,MilesWire::FileSeek,ar.resource);
                auto seekB=request(503,0,Background,0,MilesWire::FileSeek,br.resource);
                CHECK(a.mapper.receiveReverse(a.session,bytes(seekA))==SessionFileOwner::Queued);
                CHECK(b.mapper.receiveReverse(b.session,bytes(seekB))==SessionFileOwner::Queued);
                ready(b);a.mapper.poll();MilesWire::Result sr={};
                CHECK(MilesTransport::decodeResult(a.mapper.reply(503),h,sr));CHECK(sr.return_bits==static_cast<uint32_t>(-17));
                CHECK(MilesTransport::decodeResult(b.mapper.reply(503),h,sr));CHECK(sr.return_bits==UINT32_C(0x80000000));
                CHECK(Script46::seeksB==1);acknowledge(a,503);acknowledge(b,503);
                auto closeA=request(504,0,Background,0,MilesWire::FileClose,ar.resource);
                auto closeB=request(504,0,Background,0,MilesWire::FileClose,br.resource);
                CHECK(a.mapper.receiveReverse(a.session,bytes(closeA))==SessionFileOwner::Queued);
                CHECK(b.mapper.receiveReverse(b.session,bytes(closeB))==SessionFileOwner::Queued);
                ready(a);b.mapper.poll();CHECK(Script46::closesB==1);
                acknowledge(a,504);acknowledge(b,504);
                CHECK(!a.owner.retainedOperations() && !b.owner.retainedOperations());
                CHECK(!watchA.expired() && !watchB.expired()); // Session remains callback owner.
            }
            CHECK(watchA.expired() && watchB.expired());
        }
        std::puts("PASS two sessions select distinct retained tables through mapper-owner-job-invocation");
        {
            std::shared_ptr<void> life(new int(33));std::weak_ptr<void> watch=life;
            {
                Fixture f(8,Session,false,life);life.reset();f.context.reset();f.begin();
                auto open=request(501);Script36::throwOpen=true;
                CHECK(f.mapper.receiveReverse(Session,bytes(open))==SessionFileOwner::Queued);
                ready(f);Script36::throwOpen=false;
                CHECK(f.coordinator.state()==MilesCoordinator::Failed);
                CHECK(f.owner.retainedOperations()==1 && f.mapper.retainedReverse()==1);
                CHECK(!f.mapper.reply(501).size && !watch.expired());
                CHECK(f.mapper.observeForwardReturn(Session,100));
                CHECK(f.mapper.commandState()==HostAssociationMapper::ReturnedWaiting);
                CHECK(!f.mapper.consumeCommand(100));CHECK(!watch.expired());
                // Rejected ACK cannot release uncertain ownership.
                CHECK(!f.mapper.acknowledgeConsumed(Session,501));CHECK(!watch.expired());
            }
            CHECK(watch.expired()); // Test-only fake-file teardown, NOT production cleanup proof.
        }
        std::puts("PASS selected callback exception retains table through uncertain path");
        {
            Fixture f;f.begin();auto first=request(501),second=request(502);
            CHECK(f.mapper.receiveReverse(Session,bytes(first))==SessionFileOwner::Queued);
            CHECK(f.mapper.receiveReverse(Session,bytes(second))==SessionFileOwner::Queued);
            ready(f);CHECK(f.mapper.observeForwardReturn(Session,100));
            acknowledge(f,502);
            CHECK(f.mapper.commandState()==HostAssociationMapper::ReturnedWaiting);
            CHECK(f.pins().callbackPins==1 && f.pins().requestPins==1);
            acknowledge(f,501);CHECK(f.mapper.commandState()==HostAssociationMapper::Settled);
            CHECK(!f.pins().callbackPins && !f.pins().requestPins);
        }
        std::puts("PASS multiple causal callbacks ACK out of order");
        {
            Fixture f;f.begin();auto first=request(501),second=request(502);
            CHECK(f.mapper.receiveReverse(Session,bytes(first))==SessionFileOwner::Queued);
            ready(f);CHECK(f.mapper.observeForwardReturn(Session,100));
            CHECK(f.mapper.commandState()==HostAssociationMapper::ReturnedWaiting);
            CHECK(f.mapper.receiveReverse(Session,bytes(second))==SessionFileOwner::Queued);
            ready(f);acknowledge(f,501);
            CHECK(f.mapper.commandState()==HostAssociationMapper::ReturnedWaiting);
            CHECK(f.pins().callbackPins==1);acknowledge(f,502);
            CHECK(f.mapper.commandState()==HostAssociationMapper::Settled);
        }
        std::puts("PASS second causal callback arrives while returned waiting");
        for(unsigned mode=0;mode<3;++mode) {
            Fixture f;f.begin();auto open=request(501);
            CHECK(f.mapper.receiveReverse(Session,bytes(open))==SessionFileOwner::Queued);
            ready(f);if(mode==2)CHECK(f.mapper.observeForwardReturn(Session,100));
            CHECK(!f.mapper.observeForwardReturn(mode==0?78:Session,mode==1?101:100));
            CHECK(f.coordinator.state()==MilesCoordinator::Failed);
            CHECK(f.pins().requestPins==1 && f.pins().callbackPins==1);
            CHECK(f.mapper.retainedReverse()==1 && !f.mapper.consumeCommand(100));
        }
        std::puts("PASS stale wrong and duplicate forward return cannot release pins");
        for(unsigned mode=0;mode<2;++mode) {
            Fixture f;f.begin();MilesWire::Handle unknown={MilesWire::File,7,99};
            auto invalid=mode==0?request(501,100,8,0,MilesWire::FileClose,unknown)
                                :request(501,100,8,0,MilesWire::FileOpen,MilesWire::Handle(),1);
            const unsigned before=Script36::opens;
            CHECK(f.mapper.receiveReverse(Session,bytes(invalid))==SessionFileOwner::Rejected);
            CHECK(f.coordinator.state()==MilesCoordinator::Failed);
            CHECK(!f.owner.retainedOperations() && f.mapper.retainedReverse()==1);
            CHECK(!f.mapper.reply(501).size && Script36::opens==before);
            CHECK(f.pins().requestPins==1 && !f.pins().callbackPins);
            auto later=request(502);
            CHECK(f.mapper.receiveReverse(Session,bytes(later))==SessionFileOwner::Rejected);
            ready(f);CHECK(Script36::opens==before);
            CHECK(f.mapper.retainedReverse()==2 && !f.owner.retainedOperations());
        }
        std::puts("PASS valid envelope owner target and open-field rejection");
        {
            Fixture f;f.begin();CHECK(f.mapper.observeForwardReturn(Session,100));
            CHECK(f.mapper.commandState()==HostAssociationMapper::Settled);
            CHECK(!f.pins().requestPins && !f.pins().callbackPins);
            CHECK(f.mapper.consumeCommand(100));
        }
        std::puts("PASS zero callback forward return settles");
        {
            Fixture f;f.begin();auto open=request(501);
            CHECK(f.mapper.receiveReverse(Session,bytes(open))==SessionFileOwner::Queued);ready(f);
            CHECK(f.mapper.markReplyQueued(501));CHECK(!f.mapper.markReplyQueued(501));
            CHECK(f.coordinator.state()==MilesCoordinator::Failed);
            CHECK(f.owner.retainedOperations()==1 && f.mapper.retainedReverse()==1);
        }
        std::puts("PASS duplicate reply queue observation fails with ownership retained");
        {
            Fixture f;f.begin();CHECK(f.mapper.observeForwardReturn(Session,100));
            const unsigned before=Script36::opens;auto late=request(501);
            CHECK(f.mapper.receiveReverse(Session,bytes(late))==SessionFileOwner::Rejected);
            CHECK(f.coordinator.state()==MilesCoordinator::Failed && Script36::opens==before);
            CHECK(!f.owner.retainedOperations() && !f.mapper.retainedReverse());
        }
        std::puts("PASS causal callback after settled is refused before file admission");
        // One file slot: two failed opens must not consume or publish it.
        {
            Fixture f(8,Session,false,std::shared_ptr<void>(new int(49)),1);
            Script36::openFails=true;
            for (uint64_t id=601; id!=603; ++id) {
                auto frame=request(id,0,Background);
                CHECK(f.mapper.receiveReverse(Session,bytes(frame))==SessionFileOwner::Queued);
                ready(f); MilesWire::Header h={}; MilesWire::Result result={};
                CHECK(MilesTransport::decodeResult(f.mapper.reply(id),h,result));
                CHECK(result.return_bits==0 && !result.resource.kind && !result.resource.slot && !result.resource.generation);
                CHECK(f.coordinator.state()!=MilesCoordinator::Failed);
                acknowledge(f,id); CHECK(!f.owner.retainedOperations());
            }
            Script36::openFails=false;
            auto frame=request(603,0,Background);
            CHECK(f.mapper.receiveReverse(Session,bytes(frame))==SessionFileOwner::Queued);
            ready(f); MilesWire::Header h={}; MilesWire::Result result={};
            CHECK(MilesTransport::decodeResult(f.mapper.reply(603),h,result));
            CHECK(result.return_bits==7 && result.resource.kind==MilesWire::File && result.resource.slot);
            acknowledge(f,603);
            auto close=request(604,0,Background,0,MilesWire::FileClose,result.resource);
            CHECK(f.mapper.receiveReverse(Session,bytes(close))==SessionFileOwner::Queued);
            ready(f); acknowledge(f,604);
            SessionFileOwner::FileState state;
            CHECK(!f.owner.fileState(result.resource,state));
        }
        std::puts("PASS failed open with nonzero local output publishes no resource and reuses one slot");
        {
            Fixture f; f.begin(); auto frame=request(701);
            const unsigned before=Script36::opens;
            CHECK(f.mapper.receiveReverse(Session,bytes(frame))==SessionFileOwner::Queued);
            CHECK(Script36::opens==before && !f.mapper.reply(701).size);
            CHECK(f.mapper.observeForwardReturn(Session,100));
            CHECK(f.mapper.commandState()==HostAssociationMapper::ReturnedWaiting);
            CHECK(Script36::opens==before && !f.mapper.reply(701).size);
            CHECK(f.pins().requestPins==1 && f.pins().callbackPins==1);
            CHECK(!f.mapper.consumeCommand(100));
            ready(f); CHECK(Script36::opens==before+1 && f.mapper.reply(701).size==128);
            CHECK(f.mapper.commandState()==HostAssociationMapper::ReturnedWaiting);
            CHECK(f.pins().requestPins==1 && f.pins().callbackPins==1);
            acknowledge(f,701);
            CHECK(f.mapper.commandState()==HostAssociationMapper::Settled);
            CHECK(!f.pins().requestPins && !f.pins().callbackPins);
            CHECK(f.mapper.consumeCommand(100));
        }
        std::puts("PASS forward return while actual portable job Pending then completion and ACK");
        // No Fixture/SessionFileOwner exists here: isolate Invocation's ownership.
        {
            using namespace MilesFileChannel26;
            std::shared_ptr<void> life(new int(49)), context(new int(50));
            std::weak_ptr<void> weakLife=life, weakContext=context;
            FileServices services=Script46::selected(false,life);
            std::weak_ptr<const void> weakTable=services.owner;
            auto frame=request(801,0,Background); Request decoded;
            Association association={801,0,Background,0};
            CHECK(decodeRequest(bytes(frame),association,decoded)==Valid);
            std::unique_ptr<Invocation> invocation(new Invocation(decoded,services,
                std::shared_ptr<const Binding>(),context));
            services=FileServices(); life.reset(); context.reset();
            CHECK(!weakLife.expired() && !weakTable.expired() && !weakContext.expired());
            const unsigned before=Script36::opens;
            CHECK(invocation->invokeOnAdmittedExecutor());
            CHECK(Script36::opens==before+1 && invocation->completion().state==Returned);
            CHECK(invocation->completion().opened.callbackResult==7 && invocation->completion().opened.handle.value==0);
            CHECK(!weakLife.expired() && !weakTable.expired() && !weakContext.expired());
            invocation.reset();
            CHECK(weakLife.expired() && weakTable.expired() && weakContext.expired());
        }
        std::puts("PASS isolated Invocation retains selected table and context without session owner");
        std::printf("PASS %u composed selected-service/control-owner checks; scripted worker/job only\n", checks);
        return 0;
    } catch (...) { return 1; }
}
