#ifndef MILES_TRANSPORT_REGISTRY_H
#define MILES_TRANSPORT_REGISTRY_H
#include "../protocol-candidate/miles_wire.h"
#include <stdexcept>
#include <vector>
namespace MilesTransport {
inline bool knownResource(uint32_t k) { return k >= MilesWire::Driver && k <= MilesWire::File; }
inline bool validHandle(const MilesWire::Handle &h) {
    return (h.kind == 0 && h.slot == 0 && h.generation == 0) ||
           (knownResource(h.kind) && h.slot && h.generation);
}
// Dispatch-thread owned. Vendor quiescence and session binding
// are required from the caller. No vendor memory is freed by this container.
class ResourceRegistry {
    struct Entry {
        uint32_t kind, generation, state;
        void *local;
        MilesWire::Handle parent;
        Entry() : kind(0), generation(1), state(0), local(0) {
            parent.kind = parent.slot = parent.generation = 0;
        }
    };
    std::vector<Entry> entries;
    uint32_t capacity, generationLimit;
    Entry *entry(const MilesWire::Handle &h) {
        if (!knownResource(h.kind) || !h.slot || h.slot > entries.size())
            return 0;
        Entry &e = entries[h.slot - 1];
        return e.kind == h.kind && e.generation == h.generation && (e.state == 1 || e.state == 2)
                   ? &e
                   : 0;
    }

    bool insertEntry(MilesWire::ResourceKind kind, void *local, MilesWire::Handle &out) {
        if (!knownResource(kind) || !local)
            return false;
        size_t i = 0;
        for (; i < entries.size(); ++i)
            if (entries[i].state == 0)
                break;
        if (i == entries.size()) {
            if (i >= capacity)
                return false;
            entries.push_back(Entry());
        }
        Entry &e = entries[i];
        e.kind = kind;
        e.local = local;
        e.state = 1;
        MilesWire::Handle h = {static_cast<uint32_t>(kind), static_cast<uint32_t>(i + 1),
                               e.generation};
        out = h;
        return true;
    }
    static bool same(const MilesWire::Handle &a, const MilesWire::Handle &b) {
        return a.kind == b.kind && a.slot == b.slot && a.generation == b.generation;
    }
    void retireEntry(Entry &e) {
        e.local = 0;
        e.kind = 0;
        e.parent.kind = e.parent.slot = e.parent.generation = 0;
        if (e.generation == generationLimit)
            e.state = 3;
        else {
            ++e.generation;
            e.state = 0;
        }
    }

  public:
    explicit ResourceRegistry(uint32_t maxSlots = 65536, uint32_t maxGeneration = UINT32_MAX)
        : capacity(maxSlots), generationLimit(maxGeneration) {
        if (!capacity || !generationLimit)
            throw std::invalid_argument("zero registry bound");
    }
    bool insert(MilesWire::ResourceKind kind, void *local, MilesWire::Handle &out) {
        if (kind == MilesWire::BorrowedSample)
            return false;
        return insertEntry(kind, local, out);
    }
    bool insertBorrowed(const MilesWire::Handle &parent, void *local, MilesWire::Handle &out) {
        void *stream = 0;
        if (!local || !resolve(parent, MilesWire::Stream, stream))
            return false;
        for (size_t i = 0; i < entries.size(); ++i) {
            const Entry &e = entries[i];
            if (e.state == 1 && e.kind == MilesWire::BorrowedSample && same(e.parent, parent)) {
                if (e.local != local)
                    return false; // never silently retarget an existing alias
                MilesWire::Handle h = {MilesWire::BorrowedSample, static_cast<uint32_t>(i + 1),
                                       e.generation};
                out = h;
                return true;
            }
        }
        MilesWire::Handle h;
        if (!insertEntry(MilesWire::BorrowedSample, local, h))
            return false;
        entries[h.slot - 1].parent = parent;
        out = h;
        return true;
    }
    bool resolve(const MilesWire::Handle &h, MilesWire::ResourceKind expected, void *&out) const {
        out = 0;
        if (!knownResource(expected) || h.kind != static_cast<uint32_t>(expected) || !h.slot ||
            h.slot > entries.size())
            return false;
        const Entry &e = entries[h.slot - 1];
        if (e.state != 1 || e.kind != h.kind || e.generation != h.generation || !e.local)
            return false;
        if (e.kind == MilesWire::BorrowedSample) {
            void *stream = 0;
            if (!resolve(e.parent, MilesWire::Stream, stream))
                return false;
        }
        out = e.local;
        return true;
    }
    bool beginClose(const MilesWire::Handle &h) {
        Entry *e = entry(h);
        if (!e || e->state != 1 || e->kind == MilesWire::BorrowedSample)
            return false;
        e->state = 2;
        return true;
    }
    bool retire(const MilesWire::Handle &h) {
        Entry *e = entry(h);
        if (!e || e->kind == MilesWire::BorrowedSample)
            return false;
        if (e->kind == MilesWire::Stream) {
            for (size_t i = 0; i < entries.size(); ++i) {
                Entry &alias = entries[i];
                if (alias.state == 1 && alias.kind == MilesWire::BorrowedSample &&
                    same(alias.parent, h))
                    retireEntry(alias);
            }
        }
        retireEntry(*e);
        return true;
    }
};
} // namespace MilesTransport
#endif
