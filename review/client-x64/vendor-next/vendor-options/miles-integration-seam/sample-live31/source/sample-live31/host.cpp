#include "../live-bridge-candidate/admission.h"
#include "../live-bridge-candidate/common.h"
#include "../startup-bridge23/backend.h"
#include "sequence.h"
#include "oracle.h"
#ifdef _WIN64
#error host27 must compile x86
#endif
using namespace MilesWire;
inline uint64_t incarnation(const std::string &n) {
    uint64_t x = 0;
    for (unsigned i = 0; i < 16; ++i)
        x = (x << 4) | static_cast<uint64_t>(n[i] <= '9' ? n[i] - '0' : n[i] - 'a' + 10);
    return x ? x : 1;
}
inline bool zeroHandle(const Handle &h) {
    return !h.kind && !h.slot && !h.generation;
}
static int host(int argc, char **argv) {
    require(argc == 7, "host arguments");
    FILE *log = 0;
    require(!freopen_s(&log, "host.log", "w", stdout), "host log");
    setvbuf(stdout, 0, _IONBF, 0);
    HANDLE a = CreateFileA(argv[2], GENERIC_READ | GENERIC_WRITE, 0, 0, OPEN_EXISTING,
                           FILE_FLAG_OVERLAPPED, 0);
    require(a != INVALID_HANDLE_VALUE, "host command pipe");
    HANDLE b = CreateFileA(argv[3], GENERIC_READ | GENERIC_WRITE, 0, 0, OPEN_EXISTING,
                           FILE_FLAG_OVERLAPPED, 0);
    require(b != INVALID_HANDLE_VALUE, "host callback pipe");
    ULONG parent = 0;
    BOOL identified = GetNamedPipeServerProcessId(a, &parent);
    if (identified)
        require(parent == strtoul(argv[5], 0, 10), "server PID binding");
    else
        printf("LIMIT server PID query unavailable error=%lu\n", GetLastError());
    Endpoint cmd(a, 17), cb(b, 19);
    Backend backend(argv[6]);
    Oracle30 fixture(backend);
    std::string nonceText = argv[4];
    MilesCoordinator::Coordinator coordinator(incarnation(nonceText));
    uint64_t last = 0, admission = 0;
    bool hello = false, done = false;
    while (!done) {
        std::vector<unsigned char> frame = receive(cmd, &cb), unexpected;
        require(!cb.takeFrame(unexpected), "no callbacks enabled");
        Header h = {};
        Call c = {};
        require(MilesTransport::decodeCall(bytes(frame), h, c), "decode request");
        require(h.kind == Request && h.request == last + 1 && h.lane == 1 && !h.lock_lease &&
                    !h.causal_request,
                "request correlation/lane");
        last = h.request;
        StartupBridge::OwnedReply owned;
        Result &result = owned.result;
        require(h.request <= 780 && h.opcode == expected30[h.request - 1].opcode,
                "host precommitted request/opcode");
        fixture.before(h, c);
        if (!hello) {
            require(h.opcode == Hello && c.bytes.length == 32 && !c.text.length &&
                        zeroHandle(c.target) && zeroHandle(c.resource) && !c.output_mask &&
                        !c.callback && !c.reserved,
                    "hello shape");
            for (unsigned i = 0; i < 8; ++i)
                require(!c.value[i], "hello values");
            require(!memcmp(&frame[c.bytes.offset], nonceText.data(), 32), "full nonce handshake");
            hello = true;
        } else {
            bool live = true;
            std::vector<Handle> resources;
            if (!zeroHandle(c.target)) {
                void *local = 0;
                live = backend.registry.resolve(c.target, static_cast<ResourceKind>(c.target.kind),
                                                local);
                resources.push_back(c.target);
            }
            if (!zeroHandle(c.resource)) {
                void *local = 0;
                live = live && backend.registry.resolve(
                                   c.resource, static_cast<ResourceKind>(c.resource.kind), local);
                resources.push_back(c.resource);
            }
            if (!live)
                result.transport_status = StartupBridge::InvalidResource;
            else {
                MilesCoordinator::Error admitted = LiveBridge::admitNext(
                    coordinator, incarnation(nonceText), admission, h.opcode, resources);
                if (admitted != MilesCoordinator::Ok)
                    result.transport_status = StartupBridge::LifecycleRefused;
                else {
                    owned = backend.execute(h, c, frame);
                    require(LiveBridge::complete(coordinator, incarnation(nonceText), admission,
                                                 h.opcode,
                                                 result.transport_status) == MilesCoordinator::Ok,
                            "observed operation return");
                }
            }
        }
        const Expected30 &expected = expected30[h.request - 1];
        require(admission == expected.admission && result.transport_status == expected.status,
                "host precommitted admission/status");
        fixture.after(h, c, owned);
        Header reply = h;
        reply.kind = Reply;
        std::vector<unsigned char> encoded;
        require(MilesTransport::encodeResult(reply, result, MilesTransport::Bytes(),
                                             bytes(owned.text), encoded),
                "encode result");
        require(cmd.send(bytes(encoded)), "send reply");
        sent(cmd);
        printf("request=%I64u opcode=%u admission=%I64u transport=%u vendor=%u text_bytes=%u\n",
               h.request, h.opcode, admission, result.transport_status, result.return_bits,
               static_cast<unsigned>(owned.text.size()));
        done = h.opcode == SessionClose && result.transport_status == 0;
    }
    drainSession(cmd, cb, true);
    require(last == 780, "host exact780 request count");
    puts("PASS host30 ordered shutdown;257 allocations256 releases; retained directory bytes=6");
    return 0;
}
int main(int argc, char **argv) {
    try { return host(argc, argv); }
    catch (const std::exception &error) {
        printf("FAIL %s\n", error.what());
        return 1;
    }
}
