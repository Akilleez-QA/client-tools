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
// Dispatch-thread owned. Quiescence, borrowed-parent ownership and session binding
// are required from the caller. No vendor memory is freed by this container.
class ResourceRegistry {
    struct Entry {
        uint32_t kind, generation, state;
        void *local;
        Entry() : kind(0), generation(1), state(0), local(0) {}
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

  public:
    explicit ResourceRegistry(uint32_t maxSlots = 65536, uint32_t maxGeneration = UINT32_MAX)
        : capacity(maxSlots), generationLimit(maxGeneration) {
        if (!capacity || !generationLimit)
            throw std::invalid_argument("zero registry bound");
    }
    bool insert(MilesWire::ResourceKind kind, void *local, MilesWire::Handle &out) {
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
    bool resolve(const MilesWire::Handle &h, MilesWire::ResourceKind expected, void *&out) const {
        out = 0;
        if (!knownResource(expected) || h.kind != static_cast<uint32_t>(expected) || !h.slot ||
            h.slot > entries.size())
            return false;
        const Entry &e = entries[h.slot - 1];
        if (e.state != 1 || e.kind != h.kind || e.generation != h.generation || !e.local)
            return false;
        out = e.local;
        return true;
    }
    bool beginClose(const MilesWire::Handle &h) {
        Entry *e = entry(h);
        if (!e || e->state != 1)
            return false;
        e->state = 2;
        return true;
    }
    bool retire(const MilesWire::Handle &h) {
        Entry *e = entry(h);
        if (!e)
            return false;
        e->local = 0;
        e->kind = 0;
        if (e->generation == generationLimit)
            e->state = 3;
        else {
            ++e->generation;
            e->state = 0;
        }
        return true;
    }
};
} // namespace MilesTransport
#endif
