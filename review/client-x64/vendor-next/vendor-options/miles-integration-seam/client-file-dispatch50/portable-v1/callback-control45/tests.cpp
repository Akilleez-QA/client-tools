#include "host_association_mapper.h"
#include "../callback-composition46/selected_fixture.h"
#include <cstdio>
#include <stdexcept>
namespace Script36 {
extern unsigned opens, closes;
extern bool dispatchUncertain, throwOpen, openFails;
void pump();
void pumpFirst();
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
static std::vector<unsigned char> ack(const std::vector<unsigned char> &frame) {
    MilesWire::Header h={};MilesWire::Call c={};
    CHECK(MilesTransport::decodeCall(bytes(frame),h,c));
    MilesFileChannel26::Association a={h.request,h.causal_request,h.lane,h.lock_lease};
    MilesFileChannel26::Request r;MilesFileProtocol48::FileAckExpected e;
    CHECK(MilesFileChannel26::decodeRequest(bytes(frame),a,r)==MilesFileChannel26::Valid);
    CHECK(MilesFileProtocol48::expectFileAck(r,1,e));
    std::vector<unsigned char> result(MilesFileProtocol48::ConsumptionAckBytes);size_t written=0;
    CHECK(MilesFileProtocol48::encodeFileConsumptionAck(e,result.data(),result.size(),written));
    CHECK(written==result.size());return result;
}
static void consume(Fixture &f,const std::vector<unsigned char> &frame) {
    MilesWire::Header h={};MilesWire::Call c={};CHECK(MilesTransport::decodeCall(bytes(frame),h,c));
    CHECK(f.mapper.markReplyQueued(h.request));auto a=ack(frame);
    CHECK(f.mapper.receiveControl(f.session,bytes(a))==HostAssociationMapper::AckConsumed);
}
static MilesWire::Handle opened(Fixture &f,const std::vector<unsigned char> &frame) {
    CHECK(f.mapper.receiveControl(f.session,bytes(frame))==HostAssociationMapper::FileQueued);
    ready(f);MilesWire::Header h={};MilesWire::Result r={};
    CHECK(MilesTransport::decodeResult(f.mapper.reply(501),h,r));
    CHECK(r.return_bits==7 && r.resource.kind==MilesWire::File);consume(f,frame);return r.resource;
}
int main() {
 try {
    { Fixture f;MilesCoordinator::Coordinator other(Session);bool threw=false;
      try {HostAssociationMapper wrong(Session,Background,other,f.owner,8);}catch(const std::invalid_argument &){threw=true;}
      CHECK(threw);CHECK(!f.mapper.retainedReverse() && !f.owner.retainedOperations()); }
    std::puts("PASS distinct coordinator same session refused");
    { Fixture f;f.begin();auto first=request(501),second=request(502);
      const unsigned before=Script36::opens;
      CHECK(f.mapper.receiveControl(Session,bytes(first))==HostAssociationMapper::FileQueued);
      CHECK(f.mapper.receiveControl(Session,bytes(second))==HostAssociationMapper::FileQueued);
      CHECK(f.mapper.observeForwardReturn(Session,100));
      CHECK(f.mapper.commandState()==HostAssociationMapper::ReturnedWaiting);
      CHECK(Script36::opens==before && !f.mapper.reply(501).size);
      CHECK(f.pins().requestPins==1 && f.pins().callbackPins==2);
      ready(f);CHECK(Script36::opens==before+2);
      consume(f,second);CHECK(f.mapper.commandState()==HostAssociationMapper::ReturnedWaiting);
      CHECK(f.pins().callbackPins==1);consume(f,first);
      CHECK(f.mapper.commandState()==HostAssociationMapper::Settled);
      CHECK(!f.pins().callbackPins && !f.pins().requestPins && !f.mapper.retainedReverse()); }
    std::puts("PASS Pending forward join and older original ACK after newer intake");
    { Fixture f;f.begin();auto frame=request(501);
      CHECK(f.mapper.receiveControl(Session,bytes(frame))==HostAssociationMapper::FileQueued);
      ready(f);consume(f,frame);CHECK(f.mapper.commandState()==HostAssociationMapper::Executing);
      CHECK(f.mapper.observeForwardReturn(Session,100));CHECK(f.mapper.commandState()==HostAssociationMapper::Settled); }
    std::puts("PASS ACK before forward return does not settle prematurely");
    for(unsigned mode=0;mode!=5;++mode) {
      Fixture f;f.begin();auto frame=request(501);auto a=ack(frame);
      CHECK(f.mapper.receiveControl(Session,bytes(frame))==HostAssociationMapper::FileQueued);
      if(mode!=0)ready(f); // early while Pending versus ready but unsent
      if(mode>=2)CHECK(f.mapper.markReplyQueued(501));
      if(mode==4)CHECK(f.mapper.receiveControl(Session,bytes(a))==HostAssociationMapper::AckConsumed);
      if(mode==3){MilesWire::Header h={};MilesWire::Call c={};CHECK(MilesTransport::decodeCall(bytes(a),h,c));h.request=1;
        CHECK(MilesTransport::encodeCall(h,c,MilesTransport::Bytes(),MilesTransport::Bytes(),a));}
      CHECK(f.mapper.receiveControl(mode==2?Session+1:Session,bytes(a))==HostAssociationMapper::ControlRejected);
      CHECK(f.coordinator.state()==MilesCoordinator::Failed);
      CHECK(f.mapper.retainedReverse()==(mode==4?0u:1u));
      CHECK(f.owner.retainedOperations()==(mode==4?0u:1u));
      ready(f);
    }
    std::puts("PASS pending early unsent wrong-session unknown and duplicate ACK refused");
    for(unsigned mode=0;mode!=12;++mode) {
      Fixture f;f.begin();auto frame=request(501);
      CHECK(f.mapper.receiveControl(Session,bytes(frame))==HostAssociationMapper::FileQueued);
      ready(f);CHECK(f.mapper.markReplyQueued(501));auto a=ack(frame);
      MilesWire::Header h={};MilesWire::Call c={};CHECK(MilesTransport::decodeCall(bytes(a),h,c));
      switch(mode){case 0:++h.causal_request;break;case 1:++h.lane;break;case 2:++h.lock_lease;break;
        case 3:++c.callback;break;case 4:c.value[0]=MilesWire::FileClose;break;case 5:c.value[1]=1;break;
        case 6:h.kind=MilesWire::Request;break;case 7:c.target.kind=MilesWire::File;c.target.slot=1;c.target.generation=1;break;
        case 8:c.resource.kind=MilesWire::File;c.resource.slot=1;c.resource.generation=1;break;case 9:c.output_mask=1;break;
        case 10:h.opcode=MilesWire::CallbackAck;break;default:break;}
      CHECK(MilesTransport::encodeCall(h,c,MilesTransport::Bytes(),MilesTransport::Bytes(),a));
      if(mode==11)a.resize(8);
      CHECK(f.mapper.receiveControl(Session,bytes(a))==HostAssociationMapper::ControlRejected);
      CHECK(f.coordinator.state()==MilesCoordinator::Failed);
      CHECK(f.mapper.retainedReverse()==1 && f.owner.retainedOperations()==1);
      CHECK(f.pins().callbackPins==1 && f.pins().requestPins==1);
    }
    std::puts("PASS exact retained ACK context opcode registration and unused fields");
    { Fixture f;f.begin();auto bad=request(501,100,8,0,MilesWire::FileOpen,MilesWire::Handle(),1);
      const unsigned before=Script36::opens;
      CHECK(f.mapper.receiveControl(Session,bytes(bad))==HostAssociationMapper::ControlRejected);
      CHECK(!f.mapper.retainedReverse() && !f.owner.retainedOperations());ready(f);
      CHECK(Script36::opens==before && f.coordinator.state()==MilesCoordinator::Failed); }
    std::puts("PASS malformed file fields rejected before correlation publication");
    for(unsigned reversed=0;reversed!=2;++reversed) {
      Fixture f;auto open=request(501,0,Background);auto file=opened(f,open);
      auto filler=request(502,0,Background,0,MilesWire::FileRead,file,1);
      if(reversed)CHECK(f.mapper.receiveControl(Session,bytes(filler))==HostAssociationMapper::FileQueued);
      auto read=request(503,0,Background,0,MilesWire::FileRead,file,1);
      Script36::dispatchUncertain=true;
      CHECK(f.mapper.receiveControl(Session,bytes(read))==HostAssociationMapper::FileQueued);
      Script36::dispatchUncertain=false;
      if(reversed){Script36::pumpFirst();f.mapper.poll();consume(f,filler);}
      auto close=request(504,0,Background,0,MilesWire::FileClose,file);
      CHECK(f.mapper.receiveControl(Session,bytes(close))==HostAssociationMapper::FileQueued);
      ready(f);CHECK(f.coordinator.state()==MilesCoordinator::Failed);
      CHECK(!f.mapper.reply(503).size && f.mapper.reply(504).size==128);consume(f,close);
      SessionFileOwner::FileState state;
      CHECK(f.owner.fileState(file,state) && state==SessionFileOwner::Uncertain);
      CHECK(f.mapper.retainedReverse()==1 && f.owner.retainedOperations()==1);
      auto a=ack(read);CHECK(f.mapper.receiveControl(Session,bytes(a))==HostAssociationMapper::ControlRejected);
      CHECK(f.owner.fileState(file,state) && state==SessionFileOwner::Uncertain);
    }
    std::puts("PASS sibling uncertainty retained across both slot poll orders and close ACK");
    std::printf("PASS %u dispatch50 checks; scripted job only\n",checks);return 0;
 }catch(...){return 1;}
}
