#include "retained_buffers.h"
#include <cstring>
#include <limits>
#include <atomic>
namespace MilesHost {
namespace {
std::atomic<uint64_t> nextToken(1);
uint64_t reserveToken() {
    uint64_t value=nextToken.load();
    while(value) {
        if(nextToken.compare_exchange_weak(value,value+1))return value;
    }
    return 0; // Never reuse tokens, including after exhaustion.
}
}
RetainedBuffers::RetainedBuffers(size_t bytes, size_t count)
    : limit(bytes), maxEntries(count), used(0), activeToken(0) {}
bool RetainedBuffers::stage(Kind kind, const void *frame, size_t frameSize,
                           size_t offset, size_t length, Token &out) {
    if (kind != Binary && kind != Text && kind != NullText) return false;
    if (offset > frameSize || length > frameSize - offset) return false;
    if (length > (std::numeric_limits<uint32_t>::max)()) return false;
    if (entries.size() >= maxEntries || length > limit - used) return false;
    if (kind == NullText) {
        if (offset || length) return false;
    } else if (!frame || !length) return false;
    const unsigned char *source = 0;
    if (length) source = static_cast<const unsigned char *>(frame) + offset;
    if (kind == Text && (source[length-1] != 0 || std::memchr(source, 0, length-1))) return false;
    Entry candidate;
    candidate.kind = kind;
    if (length) candidate.bytes.assign(source, source + length);
    // Any allocation exception leaves published tokens, active copy and accounting unchanged.
    const Token token = reserveToken();
    if (!token) return false;
    entries.insert(std::make_pair(token, candidate));
    out = token;
    used += length;
    return true;
}
bool RetainedBuffers::view(Token token, View &out) const {
    Entries::const_iterator i = entries.find(token);
    if (i == entries.end()) return false;
    out.kind = i->second.kind;
    out.size = static_cast<uint32_t>(i->second.bytes.size());
    out.data = out.size ? &i->second.bytes[0] : 0;
    return true;
}
bool RetainedBuffers::commit(Token token) {
    if (entries.find(token) == entries.end()) return false;
    if (activeToken) entries.erase(activeToken);
    activeToken = token;
    return true;
}
bool RetainedBuffers::retire(Token token) {
    Entries::iterator i = entries.find(token);
    if (token == activeToken || i == entries.end()) return false;
    used -= i->second.bytes.size();
    entries.erase(i);
    return true;
}
void RetainedBuffers::deactivate() { activeToken = 0; }
}
