#ifndef MILES_HOST_SESSION_LIFECYCLE_H
#define MILES_HOST_SESSION_LIFECYCLE_H
#include "../transport-candidate/resource_registry.h"
#include <vector>
namespace MilesHost {
// Internal candidate, not an exported AIL facade. Exactly one session may own the
// process-global Miles runtime. All operations are confined to the constructing
// control-dispatch thread; coordinator must establish lane/lease admission.
class SessionLifecycle {
public:
    enum Status { Ok, WrongThread, NotStarted, AlreadyStarted, QuiescenceRequired,
                  UnknownResource, CapacityFailure, StorageFailure };
    explicit SessionLifecycle(uint32_t resourceLimit=65536);
    // Caller must explicitly shutdown before destruction. Destructor never calls
    // the vendor on an arbitrary thread; it does NOT establish quiescence.
    ~SessionLifecycle();
    Status startup(int32_t &vendorResult);
    Status openDriver(uint32_t frequency,int32_t bits,int32_t channels,uint32_t flags,
                      MilesWire::Handle &out);
    Status allocateSample(const MilesWire::Handle &driver,MilesWire::Handle &out);
    Status releaseSample(const MilesWire::Handle &sample,bool callbacksQuiesced);
    Status shutdown(bool callbacksQuiesced);
    const MilesTransport::ResourceRegistry &resources() const { return registry; }
private:
    struct Record { MilesWire::Handle handle,parent; void *native; bool sample; };
    MilesTransport::ResourceRegistry registry;
    std::vector<Record> records;
    unsigned long thread;
    bool started;
    bool onThread() const;
    bool reserveRecord();
    SessionLifecycle(const SessionLifecycle &);
    SessionLifecycle &operator=(const SessionLifecycle &);
};
}
#endif
