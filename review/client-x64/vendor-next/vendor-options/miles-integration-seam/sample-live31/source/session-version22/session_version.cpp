#include "session_version.h"
#include <cstring>
namespace MilesSessionVersion {
namespace {
bool nullHandle(const MilesWire::Handle& h) { return !h.kind && !h.slot && !h.generation; }
bool requestHeader(const MilesWire::Header& h) {
    return h.magic==MilesWire::Magic && h.version==MilesWire::Version &&
        h.kind==MilesWire::Request && h.opcode==MilesWire::SessionVersion &&
        h.request && h.lane;
}
bool sameContext(const MilesWire::Header& a, const MilesWire::Header& b) {
    return a.request==b.request && a.causal_request==b.causal_request &&
        a.lane==b.lane && a.lock_lease==b.lock_lease;
}
}
bool makeQuery(MilesWire::Header request, std::vector<unsigned char>& frame) {
    if (!requestHeader(request)) return false;
    MilesWire::Call call={};
    return MilesTransport::encodeCall(request,call,MilesTransport::Bytes(),MilesTransport::Bytes(),frame);
}
bool validateQuery(MilesTransport::Bytes frame, MilesWire::Header& request) {
    MilesWire::Header h={}; MilesWire::Call c={};
    if (!MilesTransport::decodeCall(frame,h,c) || !requestHeader(h) ||
        !nullHandle(c.target) || !nullHandle(c.resource) || c.bytes.length ||
        c.text.length || c.output_mask || c.callback) return false;
    for (unsigned i=0;i<8;++i) if(c.value[i]) return false;
    request=h; return true;
}
bool makeReply(const MilesWire::Header& request, const char (&text)[Capacity],
               std::vector<unsigned char>& frame) {
    if (!requestHeader(request)) return false;
    size_t length=0;
    while(length<Capacity && text[length]) ++length;
    if (length==Capacity) return false;
    MilesWire::Header h=request; h.kind=MilesWire::Reply;
    MilesWire::Result r={};
    return MilesTransport::encodeResult(h,r,MilesTransport::Bytes(),
        MilesTransport::Bytes(text,length+1),frame);
}
bool copyReply(MilesTransport::Bytes frame, const MilesWire::Header& expected,
               char (&destination)[Capacity]) {
    MilesWire::Header h={}; MilesWire::Result r={};
    if (!requestHeader(expected) || !MilesTransport::decodeResult(frame,h,r) ||
        h.kind!=MilesWire::Reply || h.opcode!=MilesWire::SessionVersion ||
        !sameContext(h,expected) || r.transport_status || r.return_bits ||
        !nullHandle(r.resource) || r.bytes.length || r.null_mask || r.callback ||
        !r.text.length || r.text.length>Capacity) return false;
    for (unsigned i=0;i<8;++i) if(r.value[i]) return false;
    const unsigned char* text=frame.data+r.text.offset;
    if(text[r.text.length-1]) return false;
    for(uint32_t i=0;i+1<r.text.length;++i) if(!text[i]) return false;
    std::memmove(destination,text,r.text.length);
    return true;
}
}
