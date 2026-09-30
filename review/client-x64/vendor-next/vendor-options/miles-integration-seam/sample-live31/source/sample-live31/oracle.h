#ifndef SAMPLE_LIVE30_ORACLE_H
#define SAMPLE_LIVE30_ORACLE_H
// Registry/lifetime observations only. No query of an unbound/freed vendor sample.
struct Oracle30 {
    Backend &backend;
    void *beforeNative;
    MilesWire::Handle live;
    unsigned allocations, ends, releases;
    explicit Oracle30(Backend &owner) : backend(owner), beforeNative(0), live(),
                                        allocations(0), ends(0), releases(0) {}
    void before(const MilesWire::Header &h, const MilesWire::Call &c) {
        beforeNative = 0;
        if (h.opcode == MilesWire::AIL_end_sample || h.opcode == MilesWire::AIL_release_sample_handle) {
            const bool resolved = backend.registry.resolve(c.target, MilesWire::OwnedSample, beforeNative);
            require(resolved == (h.request != 10 && h.request != 778), "pre-call expected sample liveness");
        }
    }
    void after(const MilesWire::Header &h, const MilesWire::Call &c,
               const StartupBridge::OwnedReply &reply) {
        void *native = 0;
        if (h.opcode == MilesWire::AIL_allocate_sample_handle) {
            ++allocations;
            live = reply.result.resource;
            require(live.kind == MilesWire::OwnedSample && live.slot == 2 &&
                    live.generation == allocations, "actual allocated sample generation");
            require(backend.registry.resolve(live, MilesWire::OwnedSample, native) && native,
                    "actual allocated native sample tracked");
            void *driver = 0;
            require(backend.registry.resolve(backend.driverId, MilesWire::Driver, driver) &&
                    driver == backend.driver, "live actual parent driver");
            printf("owned allocation=%u slot=%u generation=%u tracked=1\n", allocations,live.slot,live.generation);
        } else if (h.opcode == MilesWire::AIL_end_sample && reply.result.transport_status == 0) {
            ++ends;
            require(backend.registry.resolve(c.target, MilesWire::OwnedSample, native) &&
                    native == beforeNative, "end preserves actual native identity");
        } else if (h.opcode == MilesWire::AIL_release_sample_handle) {
            ++releases;
            require(beforeNative && !backend.registry.resolve(c.target, MilesWire::OwnedSample, native),
                    "confirmed release retires identity");
        } else if (h.opcode == MilesWire::AIL_shutdown || h.opcode == MilesWire::SessionClose) {
            require(backend.shutdown && !backend.started && !backend.driver &&
                    !backend.registry.resolve(live, MilesWire::OwnedSample, native),
                    "shutdown invalidates final sample without vendor dereference");
            require(allocations == 257 && ends == 256 && releases == 256,
                    "exact successful original-DLL lifecycle call counts");
            require(backend.metadataInputs.retainedBytes() == 6, "retained redist input");
            printf("lifetime_totals request=%I64u allocations=%u ends=%u releases=%u live=0\n",
                   h.request,allocations,ends,releases);
        }
    }
  private:
    Oracle30(const Oracle30 &);
    Oracle30 &operator=(const Oracle30 &);
};
#endif
