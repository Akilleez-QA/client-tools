#ifndef CLIENT_MILES_PIPE_SESSION_H
#define CLIENT_MILES_PIPE_SESSION_H

#include "PipeCore.h"
#include "Channel.h"
#include <memory>
#include "../../client-runtime53/client_file_runtime.h"

namespace ClientMilesPipe {
struct SampleState;
// Composition-root-only owner; not included by game policy. Bootstrap/Hello
// occurs in the concrete channel before selecting this sole session. Explicit
// normal close remains unavailable pending paired shutdown proof; no public protocol API.
class Session {
  public:
    Session(Channel *channel, MilesClientRuntime53::Runtime &,
            std::shared_ptr<void> callbackCodeLifetime);
    ~Session();
    void close();

    // Private implementation operations, not an application backend interface.
    StartupBridge::OwnedReply request(uint32_t opcode, const MilesWire::Call &fields,
                                      MilesTransport::Bytes text = MilesTransport::Bytes());
    bool uncertain() const { return faulted_; }
    size_t sampleProxyCount() const; // private composition/test observation
    void rejectResult(); // terminal uncertainty; no retry after an invalid sample result
    void requireRunning() const;
    void requireAvailable() const;
    // Pure owner/request checks after wire decoding, before admission settlement.
    bool validateReply(uint32_t opcode,const MilesWire::Call &,
        const StartupBridge::OwnedReply &) const;
    void installFiles(ClientMiles::FileOpenCallback, ClientMiles::FileCloseCallback,
        ClientMiles::FileSeekCallback, ClientMiles::FileReadCallback);
    bool started;
    bool stopped;
    std::unique_ptr<ClientMiles::DigitalDriver> driver;
    std::unique_ptr<SampleState> samples;
    static Session &selected();

  private:
    Channel *channel_; // retained private root; no automatic teardown in59
    bool closed_;
    bool faulted_;
    MilesClientRuntime53::Runtime &runtime_; // retained by private root, never deleted here
    std::shared_ptr<void> callbackCodeLifetime_;
    bool filesPrepared_, filesInstalled_;
    std::vector<MilesWire::Handle> verifiedResources(const MilesWire::Call &) const;
    Session(const Session &);
    Session &operator=(const Session &);
};
} // namespace ClientMilesPipe
#endif
