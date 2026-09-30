#include "host_association_mapper.h"
#include <cstdio>
#include <stdexcept>
namespace Script36 {
extern unsigned opens, closes;
extern bool dispatchUncertain;
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
    MilesCoordinator::Coordinator coordinator;
    SessionFileOwner owner;
    HostAssociationMapper mapper;
    explicit Fixture(size_t capacity = 8)
        : worker(EngineFileWorker::create(), &EngineFileWorker::destroy),
          context(new FileSessionContext(*worker, std::shared_ptr<void>(new int(1)))),
          coordinator(Session), owner(coordinator, Session, 1, context, 8, 8),
          mapper(Session, Background, coordinator, owner, capacity) {}
    void begin(uint64_t wire = 100, uint64_t admission = 1, uint64_t lease = 0,
               MilesCoordinator::Action action = MilesCoordinator::Ordinary) {
        CHECK(mapper.publishCommand(wire, admission, 8, lease, action,
            std::vector<MilesWire::Handle>()) == MilesCoordinator::Ok);
    }
    MilesCoordinator::Readiness pins() const {
        MilesCoordinator::Readiness result = {};
        CHECK(coordinator.readiness(Session, 1, result) == MilesCoordinator::Ok);
        return result;
    }
};
static std::vector<unsigned char> request(uint64_t reverse, uint64_t cause = 100,
    uint64_t lane = 8, uint64_t lease = 0, uint32_t opcode = MilesWire::FileOpen,
    MilesWire::Handle target = MilesWire::Handle()) {
    MilesWire::Header header = {};
    header.magic = MilesWire::Magic; header.version = MilesWire::Version;
    header.kind = MilesWire::ReverseRequest; header.opcode = opcode;
    header.request = reverse; header.causal_request = cause;
    header.lane = lane; header.lock_lease = lease;
    MilesWire::Call call = {}; call.target = target;
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
    CHECK(f.mapper.acknowledgeConsumed(Session, wire));
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
        std::printf("PASS %u control-owner checks; scripted executor only\n", checks);
        return 0;
    } catch (...) { return 1; }
}
