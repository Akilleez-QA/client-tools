#ifndef EXPERIMENTAL_SESSION_VERSION21_H
#define EXPERIMENTAL_SESSION_VERSION21_H
#include "../transport-candidate/codec.h"
namespace MilesSessionVersion {
enum { Capacity = 256 };
// Fixed Audio::getMilesVersion call only. Session/lane admission is external.
bool makeQuery(MilesWire::Header request, std::vector<unsigned char>& frame);
bool validateQuery(MilesTransport::Bytes frame, MilesWire::Header& request);
// Input is a readable local buffer with the exact bound used by Audio.
// Only text through its first terminator is copied; no stack tail is sent.
bool makeReply(const MilesWire::Header& request, const char (&text)[Capacity],
               std::vector<unsigned char>& frame);
// A failed decode never writes destination. Success copies text plus its NUL;
// bytes beyond that terminator retain their original values.
bool copyReply(MilesTransport::Bytes frame, const MilesWire::Header& expected,
               char (&destination)[Capacity]);
}
#endif
