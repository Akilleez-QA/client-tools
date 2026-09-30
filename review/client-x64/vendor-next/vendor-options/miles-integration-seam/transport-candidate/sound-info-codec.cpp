#include "sound-info-codec.h"
#include <string.h>
namespace MilesTransport {
namespace {
void put(std::vector<unsigned char> &b, uint32_t x) {
    for (unsigned i = 0; i < 4; ++i) {
        b.push_back(static_cast<unsigned char>(x & 255));
        x >>= 8;
    }
}
uint32_t get(const unsigned char *&p) {
    uint32_t x = 0;
    for (unsigned i = 0; i < 4; ++i)
        x |= static_cast<uint32_t>(*p++) << (8 * i);
    return x;
}
int32_t signedBits(uint32_t bits) {
    int32_t result;
    memcpy(&result, &bits, 4);
    return result;
}
bool retainedValid(Bytes b) {
    if (b.size > UINT32_MAX || (b.size && !b.data))
        return false;
    uintptr_t base = reinterpret_cast<uintptr_t>(b.data);
    return b.size <= UINTPTR_MAX - base;
}
bool offset(Bytes b, const void *p, uint32_t &out) {
    const uintptr_t base = reinterpret_cast<uintptr_t>(b.data),
                    value = reinterpret_cast<uintptr_t>(p);
    if (value < base || value - base > b.size)
        return false;
    out = static_cast<uint32_t>(value - base);
    return true;
}
} // namespace
bool validateSoundInfo(const MilesWire::SoundInfo &s, size_t retainedSize) {
    if (retainedSize > UINT32_MAX || (s.null_mask & ~3u))
        return false;
    if (s.null_mask & DataIsNull) {
        if (s.data_offset || s.data_length)
            return false;
    } else if (s.data_offset > retainedSize || s.data_length > retainedSize - s.data_offset)
        return false;
    if (s.null_mask & InitialIsNull) {
        if (s.initial_offset)
            return false;
    } else if (s.initial_offset >= retainedSize)
        return false;
    return true;
}
bool encodeSoundInfo(const MilesWire::SoundInfo &s, size_t retainedSize,
                     std::vector<unsigned char> &out) {
    if (!validateSoundInfo(s, retainedSize))
        return false;
    std::vector<unsigned char> b;
    b.reserve(44);
    put(b, static_cast<uint32_t>(s.format));
    put(b, s.data_offset);
    put(b, s.data_length);
    put(b, s.rate);
    put(b, static_cast<uint32_t>(s.bits));
    put(b, static_cast<uint32_t>(s.channels));
    put(b, s.channel_mask);
    put(b, s.samples);
    put(b, s.block_size);
    put(b, s.initial_offset);
    put(b, s.null_mask);
    out.swap(b);
    return true;
}
bool decodeSoundInfo(Bytes b, size_t retainedSize, MilesWire::SoundInfo &out) {
    if (!b.data || b.size != 44)
        return false;
    const unsigned char *p = b.data;
    MilesWire::SoundInfo s;
    s.format = signedBits(get(p));
    s.data_offset = get(p);
    s.data_length = get(p);
    s.rate = get(p);
    s.bits = signedBits(get(p));
    s.channels = signedBits(get(p));
    s.channel_mask = get(p);
    s.samples = get(p);
    s.block_size = get(p);
    s.initial_offset = get(p);
    s.null_mask = get(p);
    if (!validateSoundInfo(s, retainedSize))
        return false;
    out = s;
    return true;
}
bool mapSoundInfoPointers(const MilesWire::SoundInfo &scalars, Bytes retained,
                          SoundInfoPointers pointers, MilesWire::SoundInfo &out) {
    if (!retainedValid(retained))
        return false;
    MilesWire::SoundInfo s = scalars;
    s.data_offset = s.initial_offset = s.null_mask = 0;
    if (!pointers.data)
        s.null_mask |= DataIsNull;
    else if (!offset(retained, pointers.data, s.data_offset))
        return false;
    if (!pointers.initial)
        s.null_mask |= InitialIsNull;
    else if (!offset(retained, pointers.initial, s.initial_offset))
        return false;
    if (!validateSoundInfo(s, retained.size))
        return false;
    out = s;
    return true;
}
bool resolveSoundInfoPointers(const MilesWire::SoundInfo &s, Bytes retained,
                              SoundInfoPointers &out) {
    if (!retainedValid(retained) || !validateSoundInfo(s, retained.size))
        return false;
    if (!retained.data && (s.null_mask != 3))
        return false;
    SoundInfoPointers pointers;
    pointers.data = (s.null_mask & DataIsNull) ? 0 : retained.data + s.data_offset;
    pointers.initial = (s.null_mask & InitialIsNull) ? 0 : retained.data + s.initial_offset;
    out = pointers;
    return true;
}
} // namespace MilesTransport
