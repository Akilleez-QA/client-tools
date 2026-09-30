#ifndef LIVE_BRIDGE_ADMISSION_H
#define LIVE_BRIDGE_ADMISSION_H
#include "../coordinator-candidate/coordinator.h"
namespace LiveBridge {
inline MilesCoordinator::Error admit(MilesCoordinator::Coordinator& owner,
    uint64_t session, uint64_t ordinal, uint32_t opcode,
    const std::vector<MilesWire::Handle>& resources) {
    if (owner.state() == MilesCoordinator::Draining) {
        if (opcode != MilesWire::SessionClose) return MilesCoordinator::WrongState;
        return owner.admitCleanup(session, ordinal, 1, 0, MilesCoordinator::Ordinary, resources);
    }
    return owner.admitGame(session, ordinal, 1, 0, MilesCoordinator::Ordinary, resources);
}
inline MilesCoordinator::Error admitNext(MilesCoordinator::Coordinator& owner,
    uint64_t session, uint64_t& lastAdmitted, uint32_t opcode,
    const std::vector<MilesWire::Handle>& resources) {
    if (lastAdmitted == UINT64_MAX) return MilesCoordinator::Capacity;
    MilesCoordinator::Error result = admit(owner, session, lastAdmitted + 1, opcode, resources);
    if (result == MilesCoordinator::Ok) ++lastAdmitted;
    return result;
}
inline MilesCoordinator::Error complete(MilesCoordinator::Coordinator& owner,
    uint64_t session, uint64_t ordinal, uint32_t opcode, uint32_t transportStatus) {
    MilesCoordinator::Error result = owner.completeAdmission(session, ordinal);
    if (result != MilesCoordinator::Ok) return result;
    // Backend validates fields and prerequisites and returns only after real shutdown.
    if (opcode == MilesWire::AIL_shutdown && transportStatus == 0)
        return owner.beginDrain(session);
    return MilesCoordinator::Ok;
}
}
#endif
