#include "../live-bridge-candidate/admission.h"
#include "../live-bridge-candidate/common.h"
#include "reply.h"
#ifndef _WIN64
#include "backend.h"
#include "fixture.h"
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
static void pureControls() {
    const uint32_t mapped[] = {StartupBridge::mapMetadata(MilesStartup::Complete),
                               StartupBridge::mapMetadata(MilesStartup::Unsupported),
                               StartupBridge::mapMetadata(MilesStartup::InvalidResource),
                               StartupBridge::mapMetadata(MilesStartup::InvalidFields),
                               StartupBridge::mapMetadata(MilesStartup::TextTooLong),
                               StartupBridge::mapMetadata(MilesStartup::InputBudgetExceeded),
                               StartupBridge::LifecycleRefused,
                               StartupBridge::VersionQueryFailed};
    for (unsigned i = 0; i < 8; ++i)
        for (unsigned j = i + 1; j < 8; ++j)
            require(mapped[i] != mapped[j], "disjoint shared status meanings");
    require(mapped[4] == 0x1002 && mapped[5] == 0x1003 && !StartupBridge::knownStatus(4) &&
                !StartupBridge::knownStatus(5),
            "metadata status4/5 mapped once");
    require(MilesStartup::signedValue(0xffffffffu) == -1 &&
                MilesStartup::signedValue(0x80000000u) == -2147483647LL - 1,
            "pure negative signed-bit controls");
    Header expected = {};
    expected.magic = Magic;
    expected.version = Version;
    expected.kind = Request;
    expected.opcode = MilesWire::AIL_last_error;
    expected.request = 1;
    expected.lane = 1;
    Header response = expected;
    response.kind = Reply;
    Result fields = {};
    std::vector<unsigned char> encoded;
    const char text[] = "owned";
    require(MilesTransport::encodeResult(response, fields, MilesTransport::Bytes(),
                                         MilesTransport::Bytes(text, sizeof text), encoded),
            "pure text encode");
    StartupBridge::OwnedReply owned;
    require(StartupBridge::decodeReply(bytes(encoded), expected, owned), "pure text decode");
    const std::vector<unsigned char> saved = owned.text;
    encoded.back() = 'x';
    require(!StartupBridge::decodeReply(bytes(encoded), expected, owned) && owned.text == saved,
            "malformed reply preserves owned destination");
    fields.transport_status = 4;
    require(MilesTransport::encodeResult(response, fields, MilesTransport::Bytes(),
                                         MilesTransport::Bytes(), encoded),
            "ambiguous status encode");
    require(!StartupBridge::decodeReply(bytes(encoded), expected, owned) && owned.text == saved,
            "old status4 rejected by composed decoder");
    fields.transport_status = StartupBridge::LifecycleRefused;
    require(MilesTransport::encodeResult(response, fields, MilesTransport::Bytes(),
                                         MilesTransport::Bytes(), encoded) &&
                StartupBridge::decodeReply(bytes(encoded), expected, owned) && owned.text.empty(),
            "named lifecycle error decode");
}
#ifndef _WIN64
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
    FixtureOracle fixture(backend);
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
        if (hello && h.opcode != Hello)
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
    require(last == 23, "host exact request count");
    puts("PASS host ordered shutdown; retained directory bytes=8; no callback registrations");
    return 0;
}
#else
static std::string frameDigest(const std::vector<unsigned char> &frame) {
    HCRYPTPROV provider = 0;
    HCRYPTHASH hash = 0;
    require(CryptAcquireContextA(&provider, 0, 0, PROV_RSA_AES, CRYPT_VERIFYCONTEXT) != 0,
            "reply hash provider");
    require(CryptCreateHash(provider, CALG_SHA_256, 0, 0, &hash) != 0, "reply hash");
    require(CryptHashData(hash, &frame[0], static_cast<DWORD>(frame.size()), 0) != 0,
            "reply hash bytes");
    unsigned char digest[32];
    DWORD size = 32;
    require(CryptGetHashParam(hash, HP_HASHVAL, digest, &size, 0) != 0 && size == 32,
            "reply digest");
    CryptDestroyHash(hash);
    CryptReleaseContext(provider, 0);
    std::string text;
    const char hex[] = "0123456789abcdef";
    for (unsigned i = 0; i < 32; ++i) {
        text += hex[digest[i] >> 4];
        text += hex[digest[i] & 15];
    }
    return text;
}
struct Client {
    Endpoint &cmd;
    Endpoint &cb;
    uint64_t next;
    unsigned checks;
    Client(Endpoint &a, Endpoint &b) : cmd(a), cb(b), next(0), checks(0) {
    }
    StartupBridge::OwnedReply call(uint32_t op, const Call &c = Call(),
                                   MilesTransport::Bytes payload = MilesTransport::Bytes(),
                                   MilesTransport::Bytes text = MilesTransport::Bytes(),
                                   uint32_t expected = StartupBridge::Success) {
        Header h = {};
        h.magic = Magic;
        h.version = Version;
        h.kind = Request;
        h.opcode = op;
        h.request = ++next;
        h.lane = 1;
        std::vector<unsigned char> frame;
        require(MilesTransport::encodeCall(h, c, payload, text, frame), "encode call");
        require(cmd.send(bytes(frame)), "send call");
        frame = receive(cmd, &cb, op == SessionClose);
        std::vector<unsigned char> unexpected;
        require(!cb.takeFrame(unexpected), "no callback traffic");
        StartupBridge::OwnedReply owned;
        require(StartupBridge::decodeReply(bytes(frame), h, owned), "typed owned reply/context");
        const Result &r = owned.result;
        printf("reply request=%I64u opcode=%u status=%u bytes=%u sha256=%s return_bits=%u "
               "value3=%u null_mask=%u text_hex=",
               next, op, r.transport_status, static_cast<unsigned>(frame.size()),
               frameDigest(frame).c_str(), r.return_bits, r.value[3], r.null_mask);
        if (owned.text.empty())
            printf("-");
        else
            for (size_t i = 0; i < owned.text.size(); ++i)
                printf("%02x", static_cast<unsigned>(owned.text[i]));
        puts("");
        require(r.transport_status == expected, "transport result");
        ++checks;
        std::vector<unsigned char>().swap(frame);
        return owned;
    }

  private:
    Client(const Client &);
    Client &operator=(const Client &);
};
static int controller(int argc, char **argv) {
    require(argc == 3, "controller arguments");
    std::string random = nonce(), base = "\\\\.\\pipe\\swg-startup23-" + random,
                commandName = base + "-cmd", callbackName = base + "-cb";
    PSECURITY_DESCRIPTOR sd = userDescriptor();
    SECURITY_ATTRIBUTES sa = {sizeof sa, sd, FALSE};
    ServerPipe a(commandName, sa), b(callbackName, sa);
    LocalFree(sd);
    char pid[32];
    sprintf_s(pid, "%lu", GetCurrentProcessId());
    std::string args = "\"" + std::string(argv[1]) + "\" --host " + commandName + " " +
                       callbackName + " " + random + " " + pid + " \"" + argv[2] + "\"";
    std::vector<char> line(args.begin(), args.end());
    line.push_back(0);
    ChildProcess child;
    child.create(argv[1], &line[0]);
    child.assignAndResume(child.job);
    a.connected();
    b.connected();
    ULONG actual = 0;
    require(GetNamedPipeClientProcessId(a.pipe, &actual) && actual == child.info.dwProcessId,
            "child command PID binding");
    require(GetNamedPipeClientProcessId(b.pipe, &actual) && actual == child.info.dwProcessId,
            "child callback PID binding");
    Endpoint cmd(a.take(), 23), cb(b.take(), 29);
    Client client(cmd, cb);
    using StartupBridge::OwnedReply;
    client.call(Hello, Call(), MilesTransport::Bytes(random.data(), random.size()));
    OwnedReply version = client.call(SessionVersion);
    require(version.text.size() == 5, "actual original bounded version");
    const std::vector<unsigned char> versionSaved = version.text;
    OwnedReply dot = client.call(MilesWire::AIL_set_redist_directory, Call(),
                                 MilesTransport::Bytes(), MilesTransport::Bytes(".", 2));
    OwnedReply directory = client.call(MilesWire::AIL_set_redist_directory, Call(),
                                       MilesTransport::Bytes(), MilesTransport::Bytes("miles", 6));
    require(dot.text != directory.text || dot.result.null_mask != directory.result.null_mask,
            "distinct framed directories");
    const std::vector<unsigned char> directorySaved = directory.text;
    const char malformed[] = {'m', 'i', 'l', 'e', 's', 0, 'x', 0};
    client.call(MilesWire::AIL_set_redist_directory, Call(), MilesTransport::Bytes(),
                MilesTransport::Bytes(malformed, sizeof malformed), StartupBridge::InvalidFields);
    OwnedReply r = client.call(MilesWire::AIL_startup);
    require(r.result.return_bits != 0, "real startup prerequisite");
    Call c = {};
    c.value[0] = 1;
    r = client.call(MilesWire::AIL_get_preference, c);
    printf("mixer=%I64d\n", MilesStartup::signedValue(r.result.return_bits));
    c.value[0] = 42;
    r = client.call(MilesWire::AIL_get_preference, c);
    const int64_t initial = MilesStartup::signedValue(r.result.return_bits);
    OwnedReply firstError = client.call(MilesWire::AIL_last_error);
    const std::vector<unsigned char> errorSaved = firstError.text;
    OwnedReply secondError = client.call(MilesWire::AIL_last_error);
    require(firstError.text != secondError.text && firstError.text == errorSaved,
            "owned error survives later reply");
    c.value[1] = 16;
    r = client.call(MilesWire::AIL_set_preference, c);
    require(MilesStartup::signedValue(r.result.return_bits) == initial,
            "signed initial preference return");
    c.value[1] = 0;
    r = client.call(MilesWire::AIL_get_preference, c);
    require(MilesStartup::signedValue(r.result.return_bits) == 16, "signed16 readback");
    c.value[1] = 64;
    r = client.call(MilesWire::AIL_set_preference, c);
    require(MilesStartup::signedValue(r.result.return_bits) == 16, "signed previous16 return");
    c.value[1] = 0;
    r = client.call(MilesWire::AIL_get_preference, c);
    require(MilesStartup::signedValue(r.result.return_bits) == 64, "signed64 readback");
    c.value[1] = 0xffffffffu;
    client.call(MilesWire::AIL_set_preference, c, MilesTransport::Bytes(), MilesTransport::Bytes(),
                StartupBridge::InvalidFields);
    c.value[1] = 0;
    r = client.call(MilesWire::AIL_get_preference, c);
    require(MilesStartup::signedValue(r.result.return_bits) == 64,
            "invalid input did not mutate preference");
    c = Call();
    c.value[0] = 22050;
    c.value[1] = 16;
    c.value[2] = 2;
    r = client.call(MilesWire::AIL_open_digital_driver, c);
    const Handle driver = r.result.resource;
    require(driver.kind == Driver && driver.slot, "real driver prerequisite");
    c = Call();
    c.target = driver;
    c.output_mask = 24;
    client.call(MilesWire::AIL_speaker_configuration, c, MilesTransport::Bytes(),
                MilesTransport::Bytes(), StartupBridge::InvalidFields);
    c.output_mask = 8;
    c.target.slot += 1;
    client.call(MilesWire::AIL_speaker_configuration, c, MilesTransport::Bytes(),
                MilesTransport::Bytes(), StartupBridge::InvalidResource);
    c.target = driver;
    r = client.call(MilesWire::AIL_speaker_configuration, c);
    require(r.result.value[3] == 2, "actual stereo speaker output");
    client.call(MilesWire::AIL_shutdown);
    c = Call();
    c.value[0] = 42;
    client.call(MilesWire::AIL_get_preference, c, MilesTransport::Bytes(), MilesTransport::Bytes(),
                StartupBridge::LifecycleRefused);
    client.call(SessionClose);
    require(version.text == versionSaved && directory.text == directorySaved &&
                firstError.text == errorSaved,
            "owned texts survive every later response and shutdown");
    require(client.checks == 23, "exact request count");
    drainSession(cmd, cb, true);
    require(WaitForSingleObject(child.info.hProcess, 10000) == WAIT_OBJECT_0, "host exit wait");
    DWORD exitCode = 99;
    require(GetExitCodeProcess(child.info.hProcess, &exitCode) && exitCode == 0, "host clean exit");
    child.close();
    puts("PASS 23 framed requests; real64to32 startup metadata; no samples/playback");
    return 0;
}
#endif
int main(int argc, char **argv) {
    setvbuf(stdout, 0, _IONBF, 0);
    try {
        pureControls();
#ifdef _WIN64
        return controller(argc, argv);
#else
        return host(argc, argv);
#endif
    } catch (const std::exception &e) {
        printf("FAIL exception=%s\n", e.what());
        return 1;
    }
}
