#ifndef MILES_TRANSPORT_SOUND_INFO_CODEC_H
#define MILES_TRANSPORT_SOUND_INFO_CODEC_H
#include "codec.h"
namespace MilesTransport {
enum SoundInfoNullBits { DataIsNull = 1, InitialIsNull = 2 };
struct SoundInfoPointers {
    const void *data;
    const void *initial;
};
// Conservative candidate bounds, not a WAV parser or proof of vendor semantics.
bool validateSoundInfo(const MilesWire::SoundInfo &, size_t retainedSize);
bool encodeSoundInfo(const MilesWire::SoundInfo &, size_t retainedSize,
                     std::vector<unsigned char> &);
bool decodeSoundInfo(Bytes, size_t retainedSize, MilesWire::SoundInfo &);
// Caller owns the actual immutable retained allocation for the entire operation.
// Pointer values remain local. Scalar fields are copied; offsets/mask are derived.
bool mapSoundInfoPointers(const MilesWire::SoundInfo &scalars, Bytes retained, SoundInfoPointers,
                          MilesWire::SoundInfo &);
bool resolveSoundInfoPointers(const MilesWire::SoundInfo &, Bytes retained, SoundInfoPointers &);
} // namespace MilesTransport
#endif
