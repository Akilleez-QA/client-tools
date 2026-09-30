#include "../candidate/callback-protocol48/file_protocol.h"
#include <algorithm>
#include <cstdio>
#include <stdexcept>
#include <vector>

namespace W = MilesWire;
namespace T = MilesTransport;
namespace P = MilesFileProtocol48;
namespace F = MilesFileChannel26;
static unsigned checks = 0;
#define CHECK(x) do { ++checks; if (!(x)) { std::printf("FAIL line %d: %s\n", __LINE__, #x); throw std::runtime_error("check"); } } while (0)
static const uint64_t RequestId = UINT64_C(0x0807060504030201);
static const uint64_t Lane = UINT64_C(0x1817161514131211);
static const uint64_t Cause = UINT64_C(0x2827262524232221);
static const uint64_t Lease = UINT64_C(0x3837363534333231);
static const uint64_t Registration = UINT64_C(0x8887868584838281);
static W::Header header(uint16_t kind, uint32_t opcode) {
    W::Header h = {};
    h.magic = W::Magic; h.version = W::Version; h.kind = kind; h.opcode = opcode;
    h.request = RequestId; h.lane = Lane;
    return h;
}
static bool sameHeader(const W::Header &a, const W::Header &b) {
    return a.magic == b.magic && a.version == b.version && a.kind == b.kind &&
        a.opcode == b.opcode && a.bytes == b.bytes && a.request == b.request &&
        a.causal_request == b.causal_request && a.lane == b.lane && a.lock_lease == b.lock_lease;
}
static bool sameHandle(const W::Handle &a, const W::Handle &b) {
    return a.kind == b.kind && a.slot == b.slot && a.generation == b.generation;
}
static T::Bytes bytes(const std::vector<unsigned char> &v) { return T::Bytes(v.data(), v.size()); }
// Test-owned wire mutation, never a native-struct copy or production encoder oracle.
static void put(std::vector<unsigned char> &v, size_t offset, uint64_t value, unsigned width) {
    CHECK(offset + width <= v.size());
    for (unsigned i = 0; i < width; ++i) { v[offset + i] = static_cast<unsigned char>(value & 255); value >>= 8; }
}
static void checkFill(const unsigned char *p, size_t n, unsigned char value) {
    for (size_t i = 0; i < n; ++i) CHECK(p[i] == value);
}
static P::InstallRequest installRequest() {
    P::InstallRequest r; r.header = header(W::Request, W::AIL_set_file_callbacks); r.registration = Registration; return r;
}
static std::vector<unsigned char> installFrame() {
    unsigned char buffer[136]; size_t written = 0;
    CHECK(P::encodeInstall(installRequest().header, Registration, buffer, sizeof buffer, written));
    CHECK(written == sizeof buffer); return std::vector<unsigned char>(buffer, buffer + written);
}
static std::vector<unsigned char> installReply(P::InstallStatus status) {
    unsigned char buffer[128]; size_t written = 0;
    CHECK(P::encodeInstallReply(installRequest(), status, buffer, sizeof buffer, written));
    CHECK(written == sizeof buffer); return std::vector<unsigned char>(buffer, buffer + written);
}
static F::Request fileRequest(uint32_t opcode, bool causal) {
    W::Header h = header(W::ReverseRequest, opcode);
    h.causal_request = causal ? Cause : 0; h.lock_lease = causal ? Lease : 0;
    W::Call c = {};
    if (opcode != W::FileOpen) { c.target.kind = W::File; c.target.slot = 7; c.target.generation = 9; }
    if (opcode == W::FileRead) c.value[0] = 3;
    if (opcode == W::FileSeek) { c.value[0] = UINT32_C(0xfffffff9); c.value[1] = 2; }
    std::vector<unsigned char> frame;
    CHECK(T::encodeCall(h, c, T::Bytes(), opcode == W::FileOpen ? T::Bytes("a", 2) : T::Bytes(), frame));
    F::Association origin = {h.request, h.causal_request, h.lane, h.lock_lease}; F::Request r;
    CHECK(F::decodeRequest(bytes(frame), origin, r) == F::Valid); return r;
}
static P::FileAckExpected expectation(uint32_t opcode = W::FileRead, bool causal = true) {
    P::FileAckExpected e; CHECK(P::expectFileAck(fileRequest(opcode, causal), Registration, e)); return e;
}
static std::vector<unsigned char> ackFrame(const P::FileAckExpected &e) {
    unsigned char buffer[136]; size_t written = 0;
    CHECK(P::encodeFileConsumptionAck(e, buffer, sizeof buffer, written));
    CHECK(written == sizeof buffer); return std::vector<unsigned char>(buffer, buffer + written);
}
static void rejectInstall(const std::vector<unsigned char> &frame, const W::Header &expected) {
    P::InstallRequest out = installRequest(); out.registration = 999; out.header.bytes = 222;
    const P::InstallRequest before = out;
    CHECK(!P::decodeInstall(bytes(frame), expected, out));
    CHECK(out.registration == before.registration && sameHeader(out.header, before.header));
}
static void rejectReply(const std::vector<unsigned char> &frame, const P::InstallRequest &expected) {
    P::InstallStatus out = P::LifecycleRefused;
    CHECK(!P::decodeInstallReply(bytes(frame), expected, out)); CHECK(out == P::LifecycleRefused);
}
static void goldenBytes() {
    // Literal wire oracle: fixed header bytes, fixed callback bytes and all remaining zeros.
    // No production constant, serializer, sizeof(native struct), or put() builds these headers.
    static const unsigned char installHeader[48] = {
        0x57,0x4d,0x53,0x31, 0x03,0x00,0x01,0x00, 0x1c,0x00,0x00,0x00, 0x88,0x00,0x00,0x00,
        1,2,3,4,5,6,7,8, 0,0,0,0,0,0,0,0, 0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18, 0,0,0,0,0,0,0,0};
    static const unsigned char replyHeader[48] = {
        0x57,0x4d,0x53,0x31, 0x03,0x00,0x02,0x00, 0x1c,0x00,0x00,0x00, 0x80,0x00,0x00,0x00,
        1,2,3,4,5,6,7,8, 0,0,0,0,0,0,0,0, 0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18, 0,0,0,0,0,0,0,0};
    static const unsigned char ackHeader[48] = {
        0x57,0x4d,0x53,0x31, 0x03,0x00,0x04,0x00, 0x0e,0x10,0x00,0x00, 0x88,0x00,0x00,0x00,
        1,2,3,4,5,6,7,8, 0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x28,
        0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18, 0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38};
    static const unsigned char reg[8] = {0x81,0x82,0x83,0x84,0x85,0x86,0x87,0x88};
    std::vector<unsigned char> expected(136, 0);
    std::copy(installHeader, installHeader + 48, expected.begin()); std::copy(reg, reg + 8, expected.begin() + 128);
    CHECK(installFrame() == expected);
    expected.assign(128, 0); std::copy(replyHeader, replyHeader + 48, expected.begin());
    std::copy(reg, reg + 8, expected.begin() + 120); CHECK(installReply(P::Installed) == expected);
    expected.assign(136, 0); std::copy(ackHeader, ackHeader + 48, expected.begin());
    expected[72] = 0x09; expected[73] = 0x10; std::copy(reg, reg + 8, expected.begin() + 128);
    CHECK(ackFrame(expectation()) == expected);
    CHECK(W::Version == 3 && W::AIL_set_file_callbacks == 28 && W::AIL_stream_sample_handle == 59);
    CHECK(W::CallbackAck == 0x100c && W::SessionClose == 0x100d && W::FileConsumptionAck == 0x100e);
    CHECK(P::InstallCallBytes == 136 && P::InstallReplyBytes == 128 && P::ConsumptionAckBytes == 136);
    CHECK(P::Installed == 0 && P::Unsupported == 1 && P::InvalidFields == 3 && P::LifecycleRefused == 0x1001);
    // Explicit historical order, independent of the enum's assigned numbers.
    const uint32_t api[] = {
        W::AIL_WAV_info, W::AIL_active_sample_count, W::AIL_allocate_sample_handle,
        W::AIL_close_stream, W::AIL_digital_CPU_percent, W::AIL_digital_latency,
        W::AIL_end_sample, W::AIL_file_error, W::AIL_file_type, W::AIL_get_preference,
        W::AIL_get_timer_highest_delay, W::AIL_last_error, W::AIL_lock,
        W::AIL_open_digital_driver, W::AIL_open_stream, W::AIL_register_EOS_callback,
        W::AIL_register_stream_callback, W::AIL_release_sample_handle, W::AIL_room_type,
        W::AIL_sample_ms_position, W::AIL_sample_playback_rate, W::AIL_sample_position,
        W::AIL_sample_reverb_levels, W::AIL_sample_status, W::AIL_sample_volume_levels,
        W::AIL_serve, W::AIL_set_3D_rolloff_factor, W::AIL_set_file_callbacks,
        W::AIL_set_listener_3D_orientation, W::AIL_set_listener_3D_position,
        W::AIL_set_listener_3D_velocity_vector, W::AIL_set_named_sample_file,
        W::AIL_set_preference, W::AIL_set_redist_directory, W::AIL_set_room_type,
        W::AIL_set_sample_3D_distances, W::AIL_set_sample_3D_position,
        W::AIL_set_sample_3D_velocity_vector, W::AIL_set_sample_file,
        W::AIL_set_sample_loop_block, W::AIL_set_sample_loop_count,
        W::AIL_set_sample_ms_position, W::AIL_set_sample_obstruction,
        W::AIL_set_sample_occlusion, W::AIL_set_sample_playback_rate,
        W::AIL_set_sample_position, W::AIL_set_sample_reverb_levels,
        W::AIL_set_sample_volume_levels, W::AIL_set_stream_loop_block,
        W::AIL_set_stream_loop_count, W::AIL_set_stream_ms_position,
        W::AIL_shutdown, W::AIL_speaker_configuration, W::AIL_start_sample,
        W::AIL_start_stream, W::AIL_startup, W::AIL_stop_sample,
        W::AIL_stream_ms_position, W::AIL_stream_sample_handle, W::AIL_stream_status,
        W::AIL_unlock};
    CHECK(sizeof api / sizeof api[0] == 61);
    for (unsigned i = 0; i < sizeof api / sizeof api[0]; ++i) CHECK(api[i] == i + 1);
}
static void boundedCall() {
    const unsigned char payloadA[] = {0x00,0x81,0xff}, payloadB[] = {0x42,0x00};
    W::Header h = header(W::Request, W::BufferChunk); W::Call c = {};
    c.target = W::Handle{W::Buffer, 3, 5}; c.resource = W::Handle{W::File, 7, 9};
    for (unsigned i = 0; i < 8; ++i) c.value[i] = UINT32_C(0x80706050) + i;
    c.output_mask = UINT32_C(0xabcdef01); c.callback = Registration;
    for (unsigned mode = 0; mode < 4; ++mode) {
        T::Bytes a = mode & 1 ? T::Bytes(payloadA, sizeof payloadA) : T::Bytes();
        T::Bytes b = mode & 2 ? T::Bytes(payloadB, sizeof payloadB) : T::Bytes();
        std::vector<unsigned char> vectorOutput; CHECK(T::encodeCall(h, c, a, b, vectorOutput));
        unsigned char guarded[160]; std::fill(guarded, guarded + sizeof guarded, 0xcd); size_t written = 999;
        CHECK(T::encodeCallInto(h, c, a, b, guarded + 4, vectorOutput.size(), written));
        CHECK(written == vectorOutput.size()); CHECK(std::equal(vectorOutput.begin(), vectorOutput.end(), guarded + 4));
        checkFill(guarded, 4, 0xcd); checkFill(guarded + 4 + written, sizeof guarded - 4 - written, 0xcd);
        // Independent offsets and payload placement, not only a shared-writer comparison.
        CHECK(vectorOutput[48] == 5 && vectorOutput[52] == 3 && vectorOutput[56] == 5);
        CHECK(vectorOutput[60] == 6 && vectorOutput[64] == 7 && vectorOutput[68] == 9);
        CHECK(vectorOutput[72] == 0x50 && vectorOutput[75] == 0x80 && vectorOutput[100] == 0x57);
        CHECK(vectorOutput[104] == (a.size ? 136 : 0) && vectorOutput[108] == a.size);
        CHECK(vectorOutput[112] == (b.size ? 136 + a.size : 0) && vectorOutput[116] == b.size);
        CHECK(vectorOutput[120] == 1 && vectorOutput[123] == 0xab && vectorOutput[124] == 0);
        CHECK(vectorOutput[128] == 0x81 && vectorOutput[135] == 0x88);
        if (a.size) CHECK(std::equal(payloadA, payloadA + sizeof payloadA, vectorOutput.begin() + 136));
        if (b.size) CHECK(std::equal(payloadB, payloadB + sizeof payloadB, vectorOutput.begin() + 136 + a.size));
    }
    for (unsigned mode = 0; mode < 12; ++mode) {
        W::Header badH = h; W::Call badC = c; T::Bytes a, b;
        unsigned char guarded[160]; std::fill(guarded, guarded + sizeof guarded, 0xcd); size_t written = 999;
        unsigned char *destination = guarded + 4; size_t capacity = 136;
        if (mode == 0) destination = 0;
        if (mode == 1) capacity = 135;
        if (mode == 2) badH.magic = 0;
        if (mode == 3) badH.kind = W::Reply;
        if (mode == 4) badH.opcode = W::EndOfSample;
        if (mode == 5) badC.reserved = 1;
        if (mode == 6) badC.target.slot = 0;
        if (mode == 7) badC.resource.generation = 0;
        if (mode == 8) a = T::Bytes(0, 1);
        if (mode == 9) a = T::Bytes(payloadA, W::MaxFrameBytes);
        if (mode == 10) { a = T::Bytes(payloadA, 3); b = T::Bytes(payloadB, W::MaxFrameBytes - 136); }
        if (mode == 11) badH.opcode = 0x100f;
        CHECK(!T::encodeCallInto(badH, badC, a, b, destination, capacity, written));
        CHECK(written == 999); checkFill(guarded, sizeof guarded, 0xcd);
    }
}
static void installValidation() {
    const std::vector<unsigned char> base = installFrame(); const W::Header expected = installRequest().header;
    P::InstallRequest decoded; CHECK(P::decodeInstall(bytes(base), expected, decoded));
    CHECK(decoded.registration == Registration && decoded.header.bytes == 136);
    // Mutate each origin field, including each high byte of all 64-bit correlations.
    const size_t offsets[] = {0,4,6,8,12,16,23,24,31,32,39,40,47};
    for (size_t i = 0; i < sizeof offsets / sizeof offsets[0]; ++i) { auto v = base; v[offsets[i]] ^= 0x40; rejectInstall(v, expected); }
    const size_t forbidden[] = {48,52,56,60,64,68,72,76,80,84,88,92,96,100,104,108,112,116,120,124};
    for (size_t i = 0; i < sizeof forbidden / sizeof forbidden[0]; ++i) { auto v = base; put(v, forbidden[i], 1, 4); rejectInstall(v, expected); }
    // Valid but forbidden handles, not merely structurally malformed handles.
    for (unsigned pos = 48; pos <= 60; pos += 12) { auto v = base; put(v,pos,W::File,4); put(v,pos+4,7,4); put(v,pos+8,9,4); rejectInstall(v,expected); }
    auto v = base; put(v,128,0,8); rejectInstall(v,expected);
    v = base; v.push_back(0); put(v,12,v.size(),4); rejectInstall(v,expected);
    v = base; v.push_back(0); put(v,12,v.size(),4); put(v,104,136,4); put(v,108,1,4); rejectInstall(v,expected);
    for (size_t n = 0; n < 136; ++n) { v.assign(base.begin(),base.begin()+n); rejectInstall(v,expected); }
    for (unsigned mode = 0; mode < 8; ++mode) {
        W::Header h = expected;
        if(mode==0)h.magic=0; if(mode==1)h.version=1; if(mode==2)h.kind=W::ReverseRequest; if(mode==3)h.opcode=W::FileOpen;
        if(mode==4)h.request=0; if(mode==5)h.lane=0; if(mode==6)h.causal_request=1; if(mode==7)h.lock_lease=1;
        rejectInstall(base,h);
    }
}
static void replyValidation() {
    const P::InstallStatus allowed[] = {P::Installed,P::Unsupported,P::InvalidFields,P::LifecycleRefused};
    const P::InstallRequest request = installRequest();
    for (unsigned i=0;i<4;++i) {
        const auto base=installReply(allowed[i]); P::InstallStatus out=P::Installed;
        CHECK(P::decodeInstallReply(bytes(base),request,out)); CHECK(out==allowed[i]);
        W::Header h={}; W::Result r={}; CHECK(T::decodeResult(bytes(base),h,r));
        CHECK(r.transport_status==static_cast<uint32_t>(allowed[i])); CHECK(r.callback==(i==0?Registration:0));
        auto v=base; put(v,120,i==0?0:Registration,8); rejectReply(v,request);
        v=base; put(v,120,Registration+1,8); rejectReply(v,request);
        const size_t forbidden[]={52,56,60,64,68,72,76,80,84,88,92,96,100,104,108,112,116};
        for(size_t j=0;j<sizeof forbidden/sizeof forbidden[0];++j){v=base;put(v,forbidden[j],1,4);rejectReply(v,request);}
        v=base;put(v,56,W::File,4);put(v,60,7,4);put(v,64,9,4);rejectReply(v,request);
    }
    const auto base=installReply(P::Installed); const uint32_t invalid[]={2,4,0x1000,0x1002,UINT32_MAX};
    for(unsigned i=0;i<5;++i){auto v=base;put(v,48,invalid[i],4);rejectReply(v,request);}
    const size_t offsets[]={0,4,6,8,12,16,23,24,31,32,39,40,47};
    for(size_t i=0;i<sizeof offsets/sizeof offsets[0];++i){auto v=base;v[offsets[i]]^=0x40;rejectReply(v,request);}
    for(size_t n=0;n<128;++n){std::vector<unsigned char> v(base.begin(),base.begin()+n);rejectReply(v,request);}
    auto v=base;v.push_back(0);put(v,12,v.size(),4);rejectReply(v,request);
    v=base;v.push_back(0);put(v,12,v.size(),4);put(v,100,128,4);put(v,104,1,4);rejectReply(v,request);
    P::InstallRequest wrong=request;wrong.registration++;rejectReply(base,wrong);
    wrong=request;wrong.registration=0;rejectReply(base,wrong);
    wrong=request;wrong.header.lane++;rejectReply(base,wrong);
}
static void ackValidation() {
    for(uint32_t op=W::FileOpen;op<=W::FileRead;++op) for(unsigned causal=0;causal<2;++causal) {
        const P::FileAckExpected e=expectation(op,causal!=0); const auto base=ackFrame(e);
        CHECK(e.original.opcode==op && e.registration==Registration);
        CHECK(P::validateFileConsumptionAck(bytes(base),e));
        // Revalidation is deliberately stateless, never a consumed-once claim.
        CHECK(P::validateFileConsumptionAck(bytes(base),e));
        W::Header h={};W::Call c={};CHECK(T::decodeCall(bytes(base),h,c));
        CHECK(h.opcode==W::FileConsumptionAck && h.kind==W::ReverseRequest && h.request==e.original.request);
        CHECK(h.causal_request==e.original.causal_request && h.lane==e.original.lane && h.lock_lease==e.original.lock_lease);
        CHECK(c.callback==Registration && c.value[0]==op);
        const size_t offsets[]={0,4,6,8,12,16,23,24,31,32,39,40,47,128,135};
        for(size_t i=0;i<sizeof offsets/sizeof offsets[0];++i){auto v=base;v[offsets[i]]^=0x40;CHECK(!P::validateFileConsumptionAck(bytes(v),e));}
        const size_t forbidden[]={48,52,56,60,64,68,76,80,84,88,92,96,100,104,108,112,116,120,124};
        for(size_t i=0;i<sizeof forbidden/sizeof forbidden[0];++i){auto v=base;put(v,forbidden[i],1,4);CHECK(!P::validateFileConsumptionAck(bytes(v),e));}
        for(unsigned pos=48;pos<=60;pos+=12){auto v=base;put(v,pos,W::File,4);put(v,pos+4,7,4);put(v,pos+8,9,4);CHECK(!P::validateFileConsumptionAck(bytes(v),e));}
        auto v=base;put(v,72,op==W::FileOpen?W::FileClose:W::FileOpen,4);CHECK(!P::validateFileConsumptionAck(bytes(v),e));
        v=base;put(v,8,W::CallbackAck,4);CHECK(!P::validateFileConsumptionAck(bytes(v),e));
        v=base;put(v,8,op,4);CHECK(!P::validateFileConsumptionAck(bytes(v),e));
        v=base;put(v,128,0,8);CHECK(!P::validateFileConsumptionAck(bytes(v),e));
        P::FileAckExpected wrong=e;wrong.registration++;CHECK(!P::validateFileConsumptionAck(bytes(base),wrong));
        wrong=e;wrong.original.request++;CHECK(!P::validateFileConsumptionAck(bytes(base),wrong));
        wrong=e;wrong.original.opcode=op==W::FileOpen?W::FileClose:W::FileOpen;CHECK(!P::validateFileConsumptionAck(bytes(base),wrong));
        // Emission must not mutate the retained original header into an ACK header.
        CHECK(e.original.opcode==op);
    }
    const auto e=expectation();const auto base=ackFrame(e);
    for(size_t n=0;n<136;++n){std::vector<unsigned char> v(base.begin(),base.begin()+n);CHECK(!P::validateFileConsumptionAck(bytes(v),e));}
    auto v=base;v.push_back(0);put(v,12,v.size(),4);CHECK(!P::validateFileConsumptionAck(bytes(v),e));
    v=base;v.push_back(0);put(v,12,v.size(),4);put(v,112,136,4);put(v,116,1,4);CHECK(!P::validateFileConsumptionAck(bytes(v),e));
    P::FileAckExpected out=e;F::Request invalid;
    CHECK(!P::expectFileAck(invalid,Registration,out));CHECK(sameHeader(out.original,e.original)&&out.registration==e.registration);
    CHECK(!P::expectFileAck(fileRequest(W::FileOpen,true),0,out));CHECK(sameHeader(out.original,e.original)&&out.registration==e.registration);
}
static void typedBounds() {
    const auto request=installRequest();const auto e=expectation();
    for(unsigned kind=0;kind<3;++kind) for(unsigned mode=0;mode<3;++mode) {
        unsigned char buffer[160];std::fill(buffer,buffer+sizeof buffer,0xad);size_t written=777;
        const size_t need=kind==1?128:136;unsigned char *p=mode==0?0:buffer+3;size_t capacity=mode==1?need-1:need;
        bool result=false;
        if(kind==0)result=P::encodeInstall(request.header,Registration,p,capacity,written);
        if(kind==1)result=P::encodeInstallReply(request,P::Installed,p,capacity,written);
        if(kind==2)result=P::encodeFileConsumptionAck(e,p,capacity,written);
        if(mode<2){CHECK(!result);CHECK(written==777);checkFill(buffer,sizeof buffer,0xad);}
        else{CHECK(result&&written==need);checkFill(buffer,3,0xad);checkFill(buffer+3+need,sizeof buffer-3-need,0xad);}
    }
    for(unsigned mode=0;mode<10;++mode) {
        unsigned char buffer[160];std::fill(buffer,buffer+sizeof buffer,0xad);size_t written=777;
        P::InstallRequest bad=request;P::FileAckExpected badAck=e;bool result=false;
        if(mode==0)result=P::encodeInstall(request.header,0,buffer,sizeof buffer,written);
        if(mode==1){bad.header.lock_lease=1;result=P::encodeInstall(bad.header,Registration,buffer,sizeof buffer,written);}
        if(mode==2){bad.registration=0;result=P::encodeInstallReply(bad,P::Installed,buffer,sizeof buffer,written);}
        if(mode==3)result=P::encodeInstallReply(bad,static_cast<P::InstallStatus>(2),buffer,sizeof buffer,written);
        if(mode==4){bad.header.causal_request=1;result=P::encodeInstallReply(bad,P::Installed,buffer,sizeof buffer,written);}
        if(mode==5){badAck.registration=0;result=P::encodeFileConsumptionAck(badAck,buffer,sizeof buffer,written);}
        if(mode==6){badAck.original.kind=W::Request;result=P::encodeFileConsumptionAck(badAck,buffer,sizeof buffer,written);}
        if(mode==7){badAck.original.opcode=W::CallbackAck;result=P::encodeFileConsumptionAck(badAck,buffer,sizeof buffer,written);}
        if(mode==8){badAck.original.request=0;result=P::encodeFileConsumptionAck(badAck,buffer,sizeof buffer,written);}
        if(mode==9){badAck.original.lane=0;result=P::encodeFileConsumptionAck(badAck,buffer,sizeof buffer,written);}
        CHECK(!result&&written==777);checkFill(buffer,sizeof buffer,0xad);
    }
}
static std::vector<unsigned char> streamReply(bool nullAlias) {
    W::Header h=header(W::Reply,W::AIL_stream_sample_handle);W::Result r={};
    r.value[0]=W::Stream;r.value[1]=11;r.value[2]=13;
    if(!nullAlias)r.resource=W::Handle{W::BorrowedSample,17,19};
    std::vector<unsigned char> out;CHECK(T::encodeResult(h,r,T::Bytes(),T::Bytes(),out));return out;
}
static void rejectStream(const std::vector<unsigned char> &v,const W::Header &expected,const W::Handle &parent) {
    W::Handle out={W::File,99,101};const W::Handle before=out;
    CHECK(!P::decodeStreamAliasSuccess(bytes(v),expected,parent,out));CHECK(sameHandle(out,before));
}
static void streamValidation() {
    const W::Header expected=header(W::Request,W::AIL_stream_sample_handle);const W::Handle parent={W::Stream,11,13};
    for(unsigned nullAlias=0;nullAlias<2;++nullAlias) {
        const auto base=streamReply(nullAlias!=0);W::Handle out={};
        CHECK(P::decodeStreamAliasSuccess(bytes(base),expected,parent,out));
        CHECK(sameHandle(out,nullAlias?W::Handle{}:W::Handle{W::BorrowedSample,17,19}));
        const size_t forbidden[]={48,52,80,84,88,92,96,100,104,108,112,116,120,124};
        for(size_t i=0;i<sizeof forbidden/sizeof forbidden[0];++i){auto v=base;put(v,forbidden[i],1,4);rejectStream(v,expected,parent);}
        const size_t correlations[]={0,4,6,8,12,16,23,24,31,32,39,40,47};
        for(size_t i=0;i<sizeof correlations/sizeof correlations[0];++i){auto v=base;v[correlations[i]]^=0x40;rejectStream(v,expected,parent);}
        for(unsigned pos=68;pos<=76;pos+=4){auto v=base;put(v,pos,0,4);rejectStream(v,expected,parent);v=base;v[pos]^=0x40;rejectStream(v,expected,parent);}
        auto v=base;put(v,56,W::OwnedSample,4);put(v,60,17,4);put(v,64,19,4);rejectStream(v,expected,parent);
        for(unsigned pos=60;pos<=64;pos+=4){v=streamReply(false);put(v,pos,0,4);rejectStream(v,expected,parent);}
        v=base;v.push_back(0);put(v,12,v.size(),4);rejectStream(v,expected,parent);
        v=base;v.push_back(0);put(v,12,v.size(),4);put(v,100,128,4);put(v,104,1,4);rejectStream(v,expected,parent);
    }
    const auto base=streamReply(false);
    for(size_t n=0;n<128;++n){std::vector<unsigned char> v(base.begin(),base.begin()+n);rejectStream(v,expected,parent);}
    W::Handle wrong=parent;wrong.kind=W::OwnedSample;rejectStream(base,expected,wrong);
    wrong=parent;wrong.slot=0;rejectStream(base,expected,wrong);wrong=parent;wrong.generation=0;rejectStream(base,expected,wrong);
    W::Header wrongH=expected;wrongH.kind=W::Reply;rejectStream(base,wrongH,parent);
    wrongH=expected;wrongH.opcode=W::AIL_open_stream;rejectStream(base,wrongH,parent);
    wrongH=expected;wrongH.request=0;rejectStream(base,wrongH,parent);
}
static void oldVersions() {
    W::Header callH=header(W::Request,W::AIL_set_file_callbacks);W::Call c={};c.callback=Registration;
    W::Header resultH=header(W::Reply,W::AIL_set_file_callbacks);W::Result r={};
    W::Header eosH=header(W::Event,W::EndOfSample);W::Eos eos={};eos.resource=W::Handle{W::OwnedSample,3,5};eos.registration=7;eos.event_sequence=9;
    std::vector<unsigned char> goodCall,goodResult,goodEos;
    CHECK(T::encodeCall(callH,c,T::Bytes(),T::Bytes(),goodCall));
    CHECK(T::encodeResult(resultH,r,T::Bytes(),T::Bytes(),goodResult));CHECK(T::encodeEos(eosH,eos,goodEos));
    W::Header decodedH={};W::Call decodedC={};W::Result decodedR={};W::Eos decodedE={};
    CHECK(T::decodeCall(bytes(goodCall),decodedH,decodedC));
    CHECK(T::decodeResult(bytes(goodResult),decodedH,decodedR));
    CHECK(T::decodeEos(bytes(goodEos),decodedH,decodedE));
    CHECK(decodedE.registration==7 && decodedE.event_sequence==9 && sameHandle(decodedE.resource,eos.resource));
    for(uint16_t version=1;version<=2;++version) {
        W::Header hc=callH,hr=resultH,he=eosH;hc.version=hr.version=he.version=version;
        std::vector<unsigned char> out(5,0xce);const auto original=out;
        CHECK(!T::encodeCall(hc,c,T::Bytes(),T::Bytes(),out));CHECK(out==original);
        CHECK(!T::encodeResult(hr,r,T::Bytes(),T::Bytes(),out));CHECK(out==original);
        CHECK(!T::encodeEos(he,eos,out));CHECK(out==original);
        unsigned char buffer[144];std::fill(buffer,buffer+sizeof buffer,0xce);size_t written=999;
        CHECK(!T::encodeCallInto(hc,c,T::Bytes(),T::Bytes(),buffer,sizeof buffer,written));CHECK(written==999);checkFill(buffer,sizeof buffer,0xce);
        CHECK(!T::encodeResultInto(hr,r,T::Bytes(),T::Bytes(),buffer,sizeof buffer,written));CHECK(written==999);checkFill(buffer,sizeof buffer,0xce);
        auto bc=goodCall,br=goodResult,be=goodEos;put(bc,4,version,2);put(br,4,version,2);put(be,4,version,2);
        W::Header oh=callH;oh.bytes=777;const W::Header savedH=oh;W::Call oc={};oc.callback=999;
        CHECK(!T::decodeCall(bytes(bc),oh,oc));CHECK(sameHeader(oh,savedH)&&oc.callback==999);
        W::Result resultOut={};resultOut.callback=999;CHECK(!T::decodeResult(bytes(br),oh,resultOut));CHECK(sameHeader(oh,savedH)&&resultOut.callback==999);
        W::Eos eosOut={};eosOut.registration=999;CHECK(!T::decodeEos(bytes(be),oh,eosOut));CHECK(sameHeader(oh,savedH)&&eosOut.registration==999);
        rejectInstall(bc,installRequest().header);
        auto reply=installReply(P::Installed);put(reply,4,version,2);rejectReply(reply,installRequest());
        auto e=expectation();auto ack=ackFrame(e);put(ack,4,version,2);CHECK(!P::validateFileConsumptionAck(bytes(ack),e));
        auto stream=streamReply(false);put(stream,4,version,2);rejectStream(stream,header(W::Request,W::AIL_stream_sample_handle),W::Handle{W::Stream,11,13});
        auto ir=installRequest();ir.header.version=version;
        CHECK(!P::encodeInstall(ir.header,ir.registration,buffer,sizeof buffer,written));CHECK(written==999);
        CHECK(!P::encodeInstallReply(ir,P::Installed,buffer,sizeof buffer,written));CHECK(written==999);
        e.original.version=version;CHECK(!P::encodeFileConsumptionAck(e,buffer,sizeof buffer,written));CHECK(written==999);checkFill(buffer,sizeof buffer,0xce);
    }
}
int main() {
    try {
        goldenBytes();std::puts("PASS independent golden install reply and ACK bytes");
        boundedCall();std::puts("PASS bounded and vector Call encoding payloads and rejection sentinels");
        installValidation();std::puts("PASS install request exact fields origin and malformed lengths");
        replyValidation();std::puts("PASS install statuses exact echo and unchanged rejected output");
        ackValidation();std::puts("PASS retained file ACK origins opcodes registration and stateless duplicate boundary");
        typedBounds();std::puts("PASS typed fixed encoders bounds and unchanged failure output");
        streamValidation();std::puts("PASS stream parent echo nullable alias and malformed success rejection");
        oldVersions();std::puts("PASS old versions rejected across all codec and typed surfaces");
        std::printf("PASS %u protocol48 checks; no SDK or endpoint execution\n",checks);return 0;
    } catch (...) {return 1;}
}
