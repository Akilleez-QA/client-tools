#ifndef MILES_HOST_ASSOCIATION_MAPPER45_H
#define MILES_HOST_ASSOCIATION_MAPPER45_H
#include "../file-owner36/session_file_owner.h"

namespace MilesFileOwner36 {
// Private single-control-thread composition. The pipe owner authenticates peers
// and posts events here; no other thread may mutate coordinator/owner directly.
class HostAssociationMapper {
public:
    enum CommandState { Empty, Executing, ReturnedWaiting, Settled };
    HostAssociationMapper(uint64_t session, uint64_t backgroundLane,
        MilesCoordinator::Coordinator &, SessionFileOwner &, size_t maxReverse);
    // This slice accepts Ordinary actions only. Lock/unlock need a dispatcher
    // outcome contract before they may change lease state at completion.
    // Must succeed before the command is sent. Resources have already passed
    // the session's genuine registry checks. Wire and local IDs are distinct.
    MilesCoordinator::Error publishCommand(uint64_t wireRequest, uint64_t admission,
        uint64_t lane, uint64_t lease, MilesCoordinator::Action,
        const std::vector<MilesWire::Handle> &resources, bool cleanup = false);
    // Forward reply has passed full opcode/envelope/value validation elsewhere.
    // true records it, even if causal ACKs still prevent settlement. Never waits.
    bool observeForwardReturn(uint64_t authenticatedSession, uint64_t wireRequest);
    // Outer command result owner explicitly consumes a Settled result once.
    bool consumeCommand(uint64_t wireRequest);
    SessionFileOwner::Intake receiveReverse(uint64_t authenticatedSession,
                                           MilesTransport::Bytes frame);
    void poll();
    MilesTransport::Bytes reply(uint64_t reverseRequest) const;
    // Only after Endpoint.send accepted the complete reply for this request.
    // Queueing is not consumption and does not release the operation.
    bool markReplyQueued(uint64_t reverseRequest);
    // Called only for a fully validated ACK on the authenticated reverse pipe.
    // ACK carries reverse identity, NEVER a peer-selected local intake ordinal.
    bool acknowledgeConsumed(uint64_t authenticatedSession, uint64_t reverseRequest);
    void fail(); // Unknown outcomes remain pinned. Supplies no file cleanup.
    CommandState commandState() const { return command.state; }
    uint64_t currentWireRequest() const { return command.wire; }
    size_t retainedReverse() const;
private:
    struct Reverse {
        uint64_t wire, intake;
        bool queued;
        Reverse() : wire(0), intake(0), queued(false) {}
    };
    struct Command {
        uint64_t wire, admission, lane, lease;
        CommandState state;
        Command() : wire(0), admission(0), lane(0), lease(0), state(Empty) {}
    };
    uint64_t session, backgroundLane, lastWire, lastReverse, lastIntake;
    MilesCoordinator::Coordinator &coordinator;
    SessionFileOwner &owner;
    Command command;
    std::vector<Reverse> reverse;
    Reverse *find(uint64_t);
    const Reverse *find(uint64_t) const;
    void settle();
    HostAssociationMapper(const HostAssociationMapper &);
    HostAssociationMapper &operator=(const HostAssociationMapper &);
};
}
#endif
