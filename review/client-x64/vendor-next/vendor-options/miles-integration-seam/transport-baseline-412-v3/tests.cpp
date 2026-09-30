#include "codec.h"
#include <stdio.h>
#include <string.h>
using namespace MilesWire;
using namespace MilesTransport;
static int count = 0, failed = 0;
static void check(bool ok, int line, const char* expression) {
    ++count;
    if (!ok) { ++failed; printf("FAIL %d line %d: %s\n", count, line, expression); }
}
#define CHECK(x) check(!!(x), __LINE__, #x)
static Header head(uint16_t kind, uint32_t op) {
    Header h = {Magic, Version, kind, op, 0, 0x0807060504030201ULL, 0, 0, 0};
    return h;
}
int main() {
    Call c = {};
    c.target.kind = OwnedSample;
    c.target.slot = 3;
    c.target.generation = 2;
    c.value[0] = 0x80000001;
    c.callback = 0x8877665544332211ULL;
    unsigned char payload[] = {0xde, 0xad};
    unsigned char text[] = {0x78, 0};
    std::vector<unsigned char> b;
    CHECK(encodeCall(head(Request, AIL_sample_status), c, Bytes(payload, 2), Bytes(text, 2), b));
    // Independent literal expected offsets and little-endian bytes, not codec-generated.
    unsigned char golden[140] = {0x57, 0x4d, 0x53, 0x31, 1, 0, 1, 0, 24, 0, 0, 0,
                                 140,  0,    0,    0,    1, 2, 3, 4, 5,  6, 7, 8};
    golden[48] = 2;
    golden[52] = 3;
    golden[56] = 2;
    golden[72] = 1;
    golden[75] = 128;
    golden[104] = 136;
    golden[108] = 2;
    golden[112] = 138;
    golden[116] = 2;
    const unsigned char cb[] = {0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88};
    memcpy(golden + 128, cb, 8);
    golden[136] = 0xde;
    golden[137] = 0xad;
    golden[138] = 0x78;
    CHECK(b.size() == sizeof(golden) && memcmp(&b[0], golden, sizeof(golden)) == 0);
    Header h = {};
    Call d = {};
    CHECK(decodeCall(Bytes(golden, sizeof(golden)), h, d));
    CHECK(d.value[0] == 0x80000001 && d.callback == c.callback &&
          h.request == 0x0807060504030201ULL);
    for (size_t n = 0; n < b.size(); ++n) {
        h.magic = 42;
        CHECK(!decodeCall(Bytes(&b[0], n), h, d) && h.magic == 42);
    }
    const size_t offsets[] = {0, 4, 6, 8, 12, 48, 52, 56, 104, 108, 112, 116, 124};
    for (size_t i = 0; i < sizeof(offsets) / sizeof(offsets[0]); ++i) {
        std::vector<unsigned char> x = b;
        x[offsets[i]] = (offsets[i] == 52 || offsets[i] == 56) ? 0 : 255;
        CHECK(!decodeCall(Bytes(&x[0], x.size()), h, d));
    }
    std::vector<unsigned char> x = b;
    x[104] = 138;
    x[112] = 136;
    CHECK(!decodeCall(Bytes(&x[0], x.size()), h, d));
    x = b;
    x.push_back(0);
    x[12] = 141;
    CHECK(!decodeCall(Bytes(&x[0], x.size()), h, d));
    CHECK(!encodeCall(head(Request, 1), c, Bytes(payload, SIZE_MAX), Bytes(), x));
    CHECK(!encodeCall(head(Request, 1), c, Bytes(0, 1), Bytes(), x));
    Result result = {};
    result.return_bits = 0x87654321;
    result.callback = c.callback;
    CHECK(encodeResult(head(Reply, 24), result, Bytes(), Bytes(), x));
    unsigned char gr[128] = {0x57, 0x4d, 0x53, 0x31, 1, 0, 2, 0, 24, 0, 0, 0,
                             128,  0,    0,    0,    1, 2, 3, 4, 5,  6, 7, 8};
    gr[52] = 0x21;
    gr[53] = 0x43;
    gr[54] = 0x65;
    gr[55] = 0x87;
    memcpy(gr + 120, cb, 8);
    CHECK(x.size() == 128 && memcmp(&x[0], gr, 128) == 0);
    Result rd = {};
    CHECK(decodeResult(Bytes(gr, 128), h, rd) && rd.return_bits == result.return_bits);
    for (size_t n = 0; n < 128; ++n)
        CHECK(!decodeResult(Bytes(gr, n), h, rd));
    Eos e = {};
    e.resource = c.target;
    e.registration = 7;
    e.event_sequence = 8;
    CHECK(encodeEos(head(Event, EndOfSample), e, x));
    unsigned char ge[80] = {0x57, 0x4d, 0x53, 0x31, 1, 0, 3, 0, 10, 16, 0, 0,
                            80,   0,    0,    0,    1, 2, 3, 4, 5,  6,  7, 8};
    ge[48] = 2;
    ge[52] = 3;
    ge[56] = 2;
    ge[64] = 7;
    ge[72] = 8;
    CHECK(x.size() == 80 && memcmp(&x[0], ge, 80) == 0);
    Eos ed = {};
    CHECK(decodeEos(Bytes(ge, 80), h, ed) && ed.event_sequence == 8);
    for (size_t n = 0; n < 80; ++n)
        CHECK(!decodeEos(Bytes(ge, n), h, ed));
    ge[60] = 1;
    CHECK(!decodeEos(Bytes(ge, 80), h, ed));
    // Exact maximum, one-byte excess, canonical empty spans and overlapping payloads.
    std::vector<unsigned char> maximum(MaxFrameBytes - 136, 0x5a);
    CHECK(encodeCall(head(Request, 1), c, Bytes(&maximum[0], maximum.size()), Bytes(), x));
    CHECK(x.size() == MaxFrameBytes && decodeCall(Bytes(&x[0], x.size()), h, d));
    CHECK(!encodeCall(head(Request, 1), c, Bytes(&maximum[0], maximum.size()), Bytes(text, 1), x));
    CHECK(encodeCall(head(ReverseRequest, FileRead), c, Bytes(), Bytes(), x));
    CHECK(decodeCall(Bytes(&x[0], x.size()), h, d));
    x[104] = 136;
    CHECK(!decodeCall(Bytes(&x[0], x.size()), h, d));
    x = b;
    x[112] = 137;
    CHECK(!decodeCall(Bytes(&x[0], x.size()), h, d));
    x = b;
    x[112] = 139;
    CHECK(!decodeCall(Bytes(&x[0], x.size()), h, d));
    x = b;
    memset(&x[108], 255, 4);
    CHECK(!decodeCall(Bytes(&x[0], x.size()), h, d));
    CHECK(!encodeCall(head(Request, EndOfSample), c, Bytes(), Bytes(), x));
    CHECK(!encodeResult(head(Reply, EndOfStream), result, Bytes(), Bytes(), x));
    CHECK(encodeResult(head(ReverseReply, FileRead), result, Bytes(payload, 2), Bytes(text, 2), x));
    CHECK(decodeResult(Bytes(&x[0], x.size()), h, rd) && rd.bytes.offset == 128 &&
          rd.text.offset == 130);
    x[100] = 1;
    CHECK(!decodeResult(Bytes(&x[0], x.size()), h, rd));
    Header sentinel = {};
    sentinel.magic = 77;
    Call unchanged = {};
    unchanged.callback = 99;
    CHECK(!decodeCall(Bytes(), sentinel, unchanged) && sentinel.magic == 77 &&
          unchanged.callback == 99);
    std::vector<unsigned char> unchangedBytes(1, 42);
    Call invalid = c;
    invalid.reserved = 1;
    CHECK(!encodeCall(head(Request, 1), invalid, Bytes(), Bytes(), unchangedBytes) &&
          unchangedBytes.size() == 1 && unchangedBytes[0] == 42);
    int a = 1, z = 2;
    void *p = 0;
    ResourceRegistry registry(1, 2);
    Handle one = {}, two = {};
    CHECK(!registry.insert(Driver, 0, one));
    CHECK(registry.insert(OwnedSample, &a, one));
    CHECK(registry.resolve(one, OwnedSample, p) && p == &a);
    CHECK(!registry.resolve(one, Driver, p) && p == 0);
    CHECK(!registry.insert(Stream, &z, two));
    CHECK(registry.beginClose(one));
    CHECK(!registry.resolve(one, OwnedSample, p));
    CHECK(!registry.beginClose(one));
    CHECK(registry.retire(one));
    CHECK(!registry.retire(one));
    CHECK(registry.insert(OwnedSample, &z, two));
    CHECK(two.slot == one.slot && two.generation == one.generation + 1);
    CHECK(!registry.resolve(one, OwnedSample, p));
    CHECK(registry.resolve(two, OwnedSample, p) && p == &z);
    CHECK(registry.retire(two));
    CHECK(!registry.insert(OwnedSample, &a, one));
    CHECK(!registry.resolve(two, OwnedSample, p));
    Handle nullHandle = {};
    CHECK(!registry.resolve(nullHandle, Null, p));
    ResourceRegistry files;
    int originalFileZero = 0;
    CHECK(files.insert(File, &originalFileZero, one));
    CHECK(files.resolve(one, File, p) && *static_cast<int *>(p) == 0);
    printf("%d/%d checks passed\n", count - failed, count);
    return failed ? 1 : 0;
}
