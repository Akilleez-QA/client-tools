#ifndef STARTUP_BRIDGE23_REPLY_H
#define STARTUP_BRIDGE23_REPLY_H
#include "../session-version22/session_version.h"
#include "../startup-metadata-v4/metadata.h"
#include <cstring>
#include <stdexcept>
namespace StartupBridge {
enum Status {
    Success = 0,
    Unsupported = 1,
    InvalidResource = 2,
    InvalidFields = 3,
    LifecycleRefused = 0x1001,
    TextTooLong = 0x1002,
    InputBudgetExceeded = 0x1003,
    VersionQueryFailed = 0x1004
};
inline Status mapMetadata(MilesStartup::Status s) {
    switch (s) {
    case MilesStartup::Complete:
        return Success;
    case MilesStartup::Unsupported:
        return Unsupported;
    case MilesStartup::InvalidResource:
        return InvalidResource;
    case MilesStartup::InvalidFields:
        return InvalidFields;
    case MilesStartup::TextTooLong:
        return TextTooLong;
    case MilesStartup::InputBudgetExceeded:
        return InputBudgetExceeded;
    }
    throw std::runtime_error("unmapped metadata status");
}
inline bool knownStatus(uint32_t s) {
    return s <= InvalidFields || (s >= LifecycleRefused && s <= VersionQueryFailed);
}
inline bool metadata(uint32_t op) {
    return op == MilesWire::AIL_set_redist_directory || op == MilesWire::AIL_get_preference ||
           op == MilesWire::AIL_set_preference || op == MilesWire::AIL_last_error ||
           op == MilesWire::AIL_speaker_configuration;
}
// Scalar result fields plus owned text. Span offsets are cleared after decode;
// callers never need a hidden retained frame or a borrowed text pointer.
struct OwnedReply {
    MilesWire::Result result;
    std::vector<unsigned char> text;
    OwnedReply() {
        std::memset(&result, 0, sizeof result);
    }
};
inline bool nullHandle(const MilesWire::Handle &h) {
    return !h.kind && !h.slot && !h.generation;
}
inline bool decodeReply(MilesTransport::Bytes frame, const MilesWire::Header &expected,
                        OwnedReply &out) {
    MilesWire::Header h = {};
    OwnedReply candidate;
    if (!MilesTransport::decodeResult(frame, h, candidate.result))
        return false;
    MilesWire::Result &r = candidate.result;
    if (h.kind != MilesWire::Reply || h.opcode != expected.opcode ||
        h.request != expected.request || h.lane != expected.lane ||
        h.causal_request != expected.causal_request || h.lock_lease != expected.lock_lease ||
        !knownStatus(r.transport_status) || r.bytes.length || r.callback)
        return false;
    const bool ok = r.transport_status == Success;
    const bool textOp = ok && (h.opcode == MilesWire::AIL_set_redist_directory ||
                               h.opcode == MilesWire::AIL_last_error);
    const bool versionOp = ok && h.opcode == MilesWire::SessionVersion;
    const bool valueOp = ok && h.opcode == MilesWire::AIL_speaker_configuration;
    const bool returnOp =
        ok && (h.opcode == MilesWire::AIL_startup || h.opcode == MilesWire::AIL_get_preference ||
               h.opcode == MilesWire::AIL_set_preference);
    const bool resourceOp = ok && h.opcode == MilesWire::AIL_open_digital_driver;
    if ((!returnOp && r.return_bits) || (!resourceOp && !nullHandle(r.resource)))
        return false;
    if (resourceOp && !nullHandle(r.resource) && r.resource.kind != MilesWire::Driver)
        return false;
    for (unsigned i = 0; i < 8; ++i)
        if (!(valueOp && i == 3) && r.value[i])
            return false;
    if (versionOp) {
        char text[MilesSessionVersion::Capacity];
        if (!MilesSessionVersion::copyReply(frame, expected, text))
            return false;
        candidate.text.assign(reinterpret_cast<unsigned char *>(text),
                              reinterpret_cast<unsigned char *>(text) + r.text.length);
    } else if (textOp) {
        if (r.null_mask & ~MilesStartup::TextNull)
            return false;
        if (r.null_mask == MilesStartup::TextNull) {
            if (r.text.length)
                return false;
        } else {
            if (!r.text.length || r.text.length > MilesStartup::ReplyTextLimit)
                return false;
            const unsigned char *text = frame.data + r.text.offset;
            if (text[r.text.length - 1] || std::memchr(text, 0, r.text.length - 1))
                return false;
            candidate.text.assign(text, text + r.text.length);
        }
    } else if (r.text.length || r.null_mask)
        return false;
    r.text = MilesWire::Span();
    r.bytes = MilesWire::Span();
    out.text.swap(candidate.text);
    out.result = r;
    return true;
}
} // namespace StartupBridge
#endif
