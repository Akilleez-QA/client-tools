#ifndef CLIENT_MILES_PIPE_SESSION_H
#define CLIENT_MILES_PIPE_SESSION_H

#include "../ClientMiles.h"
#include "Channel.h"
#include <memory>

namespace ClientMilesPipe {
// Composition-root-only owner; not included by game policy. Bootstrap/Hello
// occurs in the concrete channel before selecting this sole session. Explicit
// close follows ClientMiles::shutdown and hides SessionClose from game callers.
class Session {
  public:
    explicit Session(std::unique_ptr<Channel> channel);
    ~Session();
    void close();

    // Private implementation operations, not an application backend interface.
    StartupBridge::OwnedReply request(uint32_t opcode, const MilesWire::Call &fields,
                                      MilesTransport::Bytes text = MilesTransport::Bytes());
    void requireRunning() const;
    void requireAvailable() const;
    bool started;
    bool stopped;
    std::unique_ptr<ClientMiles::DigitalDriver> driver;
    static Session &selected();

  private:
    std::unique_ptr<Channel> channel_;
    bool closed_;
    bool faulted_;
    Session(const Session &);
    Session &operator=(const Session &);
};
} // namespace ClientMilesPipe
#endif
