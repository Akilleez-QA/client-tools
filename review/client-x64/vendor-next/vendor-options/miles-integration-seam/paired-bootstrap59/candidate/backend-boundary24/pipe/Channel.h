#ifndef CLIENT_MILES_PIPE_CHANNEL_H
#define CLIENT_MILES_PIPE_CHANNEL_H

#include "../../startup-bridge23/reply.h"

namespace ClientMilesPipe {
// Private adapter seam. Production calls use the existing framed client;
// scripted implementations live only in tests. No game-facing header includes it.
class Channel {
  public:
    virtual ~Channel() {
    }
    virtual StartupBridge::OwnedReply call(uint32_t opcode, const MilesWire::Call &fields,
                                           MilesTransport::Bytes text,
                                           const std::vector<MilesWire::Handle> &verifiedResources) = 0;
    // Called only after a successful protocol close; concrete channel drains and
    // verifies child exit here. Destruction must not manufacture successful close.
    virtual void finish() = 0;
};
} // namespace ClientMilesPipe
#endif
