// Test-only scripted services and executor. Never linked into the game or host.
#include "file_channel.h"
#include "../coordinator-candidate/coordinator.h"
#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <functional>
#include <new>
#include <stdexcept>

// Single targeted test-only allocation failure. No engine/vendor is linked.
static bool failNextAllocation = false;
void *operator new(std::size_t size)
{
    if (failNextAllocation)
    {
        failNextAllocation = false;
        throw std::bad_alloc();
    }
    void *value = std::malloc(size ? size : 1);
    if (!value)
        throw std::bad_alloc();
    return value;
}
void operator delete(void *value) noexcept { std::free(value); }
void *operator new[](std::size_t size) { return ::operator new(size); }
void operator delete[](void *value) noexcept { ::operator delete(value); }

using namespace MilesFileChannel26;
namespace Local = ClientAudioFileCallbacks;
namespace C = MilesCoordinator;
namespace
{
unsigned checks = 0;
void check(bool condition, int line)
{
    ++checks;
    if (!condition)
    {
        std::fprintf(stderr, "FAIL line %d\n", line);
        throw std::runtime_error("test assertion");
    }
}
#define CHECK(value) check((value), __LINE__)

enum Role { Reactor, ScriptedExecutor };
Role role = Reactor;
unsigned calls = 0;
Local::OpenResult openResult = {};
bool throwOnOpen = false;
uintptr_t seenKey = 0;
int32_t seekOffset = 0, seekResult = 0;
uint32_t seekOrigin = 0, readResult = 0, readRequest = 0;
std::string seenName;
std::function<void()> duringRead;

Local::OpenResult testOpen(const char *name)
{
    CHECK(role == ScriptedExecutor);
    ++calls;
    seenName = name;
    if (throwOnOpen)
        throw std::runtime_error("scripted open execution outcome unknown");
    return openResult;
}
void testClose(Local::LocalFileHandle handle)
{
    CHECK(role == ScriptedExecutor);
    ++calls;
    seenKey = handle.value;
}
int32_t testSeek(Local::LocalFileHandle handle, int32_t offset, uint32_t origin)
{
    CHECK(role == ScriptedExecutor);
    ++calls;
    seenKey = handle.value;
    seekOffset = offset;
    seekOrigin = origin;
    return seekResult;
}
uint32_t testRead(Local::LocalFileHandle handle, void *destination, uint32_t requested)
{
    CHECK(role == ScriptedExecutor);
    ++calls;
    seenKey = handle.value;
    readRequest = requested;
    if (duringRead)
        duringRead();
    if (readResult <= requested)
    {
        for (uint32_t i = 0; i < readResult; ++i)
            static_cast<unsigned char *>(destination)[i] = static_cast<unsigned char>(i + 31);
    }
    return readResult;
}
FileServices services = {testOpen, testClose, testSeek, testRead};
MilesWire::Handle file = {MilesWire::File, 7, 11};
MilesWire::Handle noFile = {};
Association expected = {3, 1, 5, 0};

std::vector<unsigned char> frame(uint32_t opcode, uint32_t a = 0, uint32_t b = 0,
                                 const std::string &name = std::string())
{
    MilesWire::Header header = {MilesWire::Magic, MilesWire::Version,
        MilesWire::ReverseRequest, opcode, 0, expected.request, expected.causal,
        expected.lane, expected.lease};
    MilesWire::Call call = {};
    if (opcode != MilesWire::FileOpen)
        call.target = file;
    call.value[0] = a;
    call.value[1] = b;
    std::vector<unsigned char> result;
    MilesTransport::Bytes text;
    if (opcode == MilesWire::FileOpen)
        text = MilesTransport::Bytes(name.c_str(), name.size() + 1);
    CHECK(MilesTransport::encodeCall(header, call, MilesTransport::Bytes(), text, result));
    return result;
}
MilesTransport::Bytes bytes(const std::vector<unsigned char> &value)
{
    return MilesTransport::Bytes(value.empty() ? 0 : &value[0], value.size());
}
Request request(uint32_t opcode, uint32_t a = 0, uint32_t b = 0,
                const std::string &name = std::string())
{
    std::vector<unsigned char> encoded = frame(opcode, a, b, name);
    Request result;
    CHECK(decodeRequest(bytes(encoded), expected, result) == Valid);
    return result;
}
std::shared_ptr<const Binding> binding(uintptr_t key)
{
    Local::LocalFileHandle local = {key};
    return std::make_shared<Binding>(file, local);
}
std::shared_ptr<void> lifetime()
{
    return std::make_shared<int>(99);
}
void invoke(Invocation &work)
{
    role = ScriptedExecutor;
    CHECK(work.invokeOnAdmittedExecutor());
    role = Reactor;
}
void put32(std::vector<unsigned char> &value, size_t offset, uint32_t bits)
{
    for (unsigned i = 0; i < 4; ++i)
        value[offset + i] = static_cast<unsigned char>(bits >> (8 * i));
}

void mapping()
{
    const unsigned initialCalls = calls;
    Request open = request(MilesWire::FileOpen, 0, 0, "MiXeD/path.wav");
    CHECK(calls == initialCalls && open.name() == "MiXeD/path.wav");
    openResult.callbackResult = 7; // Preserve nonzero bits, not a bool rewrite.
    openResult.handle.value = 0;
    Invocation work(open, services, std::shared_ptr<const Binding>(), lifetime());
    std::vector<unsigned char> reply(3, 0x55);
    CHECK(encodeCompletion(work, file, reply) == InvalidResult && reply.size() == 3);
    invoke(work);
    CHECK(work.completion().returnBits == 7 && work.completion().opened.handle.value == 0);
    CHECK(seenName == "MiXeD/path.wav");
    CHECK(encodeCompletion(work, noFile, reply) == InvalidResult && reply.size() == 3);
    CHECK(encodeCompletion(work, file, reply) == Valid);
    OwnedReply decoded;
    CHECK(decodeReply(bytes(reply), open, decoded) == Valid);
    CHECK(decoded.returnBits == 7 && decoded.file.slot == file.slot);
    const unsigned once = calls;
    CHECK(!work.invokeOnAdmittedExecutor() && calls == once);

    openResult.callbackResult = 0;
    openResult.handle.value = static_cast<uintptr_t>(UINT64_C(0x100000003));
    Invocation failed(open, services, std::shared_ptr<const Binding>(), lifetime());
    invoke(failed);
    CHECK(failed.completion().opened.handle.value == openResult.handle.value);
    CHECK(encodeCompletion(failed, file, reply) == InvalidResult);
    CHECK(encodeCompletion(failed, noFile, reply) == Valid);
    CHECK(decodeReply(bytes(reply), open, decoded) == Valid && !decoded.returnBits && !decoded.file.kind);

    const uintptr_t highKey = static_cast<uintptr_t>(UINT64_C(0x100000001));
    static_assert(sizeof(uintptr_t) == 8, "This portable x64 test covers non-narrowed local identity");
    Request seek = request(MilesWire::FileSeek, static_cast<uint32_t>(-123), Local::SeekEnd);
    seekResult = -37;
    Invocation seeking(seek, services, binding(highKey), lifetime());
    invoke(seeking);
    CHECK(seenKey == highKey && seekOffset == -123 && seekOrigin == Local::SeekEnd);
    CHECK(seeking.completion().returnBits == static_cast<uint32_t>(-37));
    CHECK(encodeCompletion(seeking, noFile, reply) == Valid);
    CHECK(decodeReply(bytes(reply), seek, decoded) == Valid);
    CHECK(decoded.returnBits == static_cast<uint32_t>(-37));

    Request read = request(MilesWire::FileRead, 8);
    readResult = 3;
    Invocation reading(read, services, binding(0), lifetime());
    invoke(reading);
    CHECK(seenKey == 0 && readRequest == 8 && reading.completion().bytes.size() == 3);
    CHECK(encodeCompletion(reading, noFile, reply) == Valid);
    CHECK(decodeReply(bytes(reply), read, decoded) == Valid);
    std::fill(reply.begin(), reply.end(), 0);
    unsigned char destination[10];
    std::memset(destination, 0xa5, sizeof(destination));
    CHECK(copyRead(decoded, 8, destination, 7) == InvalidResult && destination[0] == 0xa5);
    CHECK(copyRead(decoded, 8, 0, 8) == InvalidResult);
    CHECK(copyRead(decoded, 2, destination, sizeof(destination)) == InvalidResult);
    CHECK(copyRead(decoded, 8, destination, sizeof(destination)) == Valid);
    CHECK(destination[0] == 31 && destination[2] == 33 && destination[3] == 0xa5 && destination[9] == 0xa5);

    readResult = 0;
    Invocation eof(read, services, binding(0), lifetime());
    invoke(eof);
    CHECK(eof.completion().state == Returned && eof.completion().bytes.empty());
    CHECK(encodeCompletion(eof, noFile, reply) == Valid);
    CHECK(decodeReply(bytes(reply), read, decoded) == Valid && !decoded.returnBits);
    CHECK(copyRead(decoded, 8, destination, sizeof(destination)) == Valid);
    CHECK(destination[0] == 31); // EOF never clears the destination.
    Invocation zero(request(MilesWire::FileRead, 0), services, binding(0), lifetime());
    invoke(zero);
    CHECK(readRequest == 0 && zero.completion().state == Returned);
    CHECK(copyRead(decoded, 0, 0, 0) == Valid);

    readResult = UINT32_MAX; // Original negative int-to-U32 result, not EOF.
    Invocation badRead(read, services, binding(0), lifetime());
    invoke(badRead);
    CHECK(badRead.completion().state == ReadCountOutsideBuffer);
    CHECK(badRead.completion().returnBits == UINT32_MAX && badRead.completion().bytes.empty());
    reply.assign(3, 0x66);
    CHECK(encodeCompletion(badRead, noFile, reply) == InvalidResult && reply[0] == 0x66);

    Request close = request(MilesWire::FileClose);
    Invocation closing(close, services, binding(highKey), lifetime());
    invoke(closing);
    CHECK(seenKey == highKey && closing.completion().returnBits == 0);
    CHECK(encodeCompletion(closing, noFile, reply) == Valid);
    CHECK(decodeReply(bytes(reply), close, decoded) == Valid);
    CHECK(decoded.bytes.empty() && !decoded.file.kind);
    std::puts("PASS native-shaped value mapping, owned bytes and valid local handle zero");
}

void postOpenFailure()
{
    openResult.callbackResult = 1;
    openResult.handle.value = 0;
    Request open = request(MilesWire::FileOpen, 0, 0, "owned-before-publication");
    std::shared_ptr<void> pin = lifetime();
    std::weak_ptr<void> probe(pin);
    Invocation work(open, services, std::shared_ptr<const Binding>(), pin);
    pin.reset();
    invoke(work);
    const unsigned afterOpen = calls;
    std::vector<unsigned char> reply(3, 0x55);
    bool allocationCaught = false;
    failNextAllocation = true;
    try
    {
        encodeCompletion(work, file, reply);
    }
    catch (const std::bad_alloc &)
    {
        allocationCaught = true;
    }
    CHECK(allocationCaught && !failNextAllocation);
    CHECK(work.finished() && work.completion().state == Returned);
    CHECK(work.completion().opened.callbackResult == 1 && work.completion().opened.handle.value == 0);
    CHECK(!probe.expired() && calls == afterOpen);
    CHECK(reply.size() == 3 && reply[0] == 0x55);
    CHECK(!work.invokeOnAdmittedExecutor() && calls == afterOpen);
    // No retry or invented close is used to hide the unpublished ownership gap.

    throwOnOpen = true;
    Invocation unknown(open, services, std::shared_ptr<const Binding>(), lifetime());
    invoke(unknown);
    throwOnOpen = false;
    CHECK(unknown.completion().state == CallThrew);
    CHECK(encodeCompletion(unknown, noFile, reply) == InvalidResult && reply[0] == 0x55);
    CHECK(!unknown.invokeOnAdmittedExecutor() && calls == afterOpen + 1);
    std::puts("PASS post-open encode allocation failure retains ownership; exception stays unknown");
}

void malformed()
{
    unsigned before = calls;
    Request sentinel = request(MilesWire::FileOpen, 0, 0, "keep");
    std::vector<unsigned char> original = frame(MilesWire::FileOpen, 0, 0, "good");
    std::vector<unsigned char> changed = original;
    put32(changed, 116, UINT32_MAX); // Text span starts outside the frame.
    CHECK(decodeRequest(bytes(changed), expected, sentinel) == Malformed);
    CHECK(sentinel.name() == "keep");
    changed = original;
    changed[136] = 0; // Embedded NUL.
    CHECK(decodeRequest(bytes(changed), expected, sentinel) == InvalidFields);
    changed = original;
    changed.back() = 'x';
    CHECK(decodeRequest(bytes(changed), expected, sentinel) == InvalidFields);
    changed = original;
    put32(changed, 120, 1); // Unsupported output mask.
    CHECK(decodeRequest(bytes(changed), expected, sentinel) == InvalidFields);
    changed = original;
    put32(changed, 16, 999);
    CHECK(decodeRequest(bytes(changed), expected, sentinel) == WrongAssociation);
    changed = original;
    put32(changed, 72, 1); // Unused scalar.
    CHECK(decodeRequest(bytes(changed), expected, sentinel) == InvalidFields);
    changed = frame(MilesWire::FileOpen, 0, 0, std::string(512, 'a'));
    CHECK(decodeRequest(bytes(changed), expected, sentinel) == UnsupportedExtent);
    changed = frame(MilesWire::FileOpen, 0, 0, std::string(511, 'b'));
    CHECK(decodeRequest(bytes(changed), expected, sentinel) == Valid && sentinel.name().size() == 511);
    changed = frame(MilesWire::FileRead, UINT32_MAX);
    CHECK(decodeRequest(bytes(changed), expected, sentinel) == UnsupportedExtent);
    changed = frame(MilesWire::FileRead, MilesWire::MaxFrameBytes - 127);
    CHECK(decodeRequest(bytes(changed), expected, sentinel) == UnsupportedExtent);
    changed = frame(MilesWire::FileSeek, 0, 3);
    CHECK(decodeRequest(bytes(changed), expected, sentinel) == InvalidFields);
    changed = frame(MilesWire::FileClose);
    put32(changed, 48, MilesWire::Driver);
    CHECK(decodeRequest(bytes(changed), expected, sentinel) == InvalidFields);
    CHECK(calls == before);

    Request read = request(MilesWire::FileRead, 4);
    readResult = 2;
    Invocation reading(read, services, binding(0), lifetime());
    invoke(reading);
    CHECK(encodeCompletion(reading, noFile, original) == Valid);
    OwnedReply saved;
    saved.returnBits = 99;
    saved.bytes.assign(1, 0x77);
    const size_t badOffsets[] = {16, 24, 32, 40}; // Exact association on every component.
    for (size_t i = 0; i < 4; ++i)
    {
        changed = original;
        put32(changed, badOffsets[i], 991);
        CHECK(decodeReply(bytes(changed), read, saved) == WrongAssociation);
        CHECK(saved.returnBits == 99 && saved.bytes[0] == 0x77);
    }
    changed = original;
    put32(changed, 52, 5); // actual > requested.
    CHECK(decodeReply(bytes(changed), read, saved) == InvalidResult);
    changed = original;
    put32(changed, 52, 1); // actual != exact byte payload.
    CHECK(decodeReply(bytes(changed), read, saved) == InvalidResult);
    changed = original;
    put32(changed, 48, 1); // A transport error is not an ordinary native reply.
    CHECK(decodeReply(bytes(changed), read, saved) == InvalidResult);
    CHECK(saved.returnBits == 99 && saved.bytes[0] == 0x77);
    std::puts("PASS strict request/reply validation and unchanged output on rejection");
}

// This script models admission/execution/observation distinctly. The role label
// is a test assertion, not proof of a real engine thread or TLS route.
void executorPins()
{
    C::Coordinator coordinator(90);
    CHECK(coordinator.registerCallback(90, 1, file) == C::Ok);
    std::vector<MilesWire::Handle> resources(1, file);
    CHECK(coordinator.admitGame(90, 1, 5, 0, C::Ordinary, resources) == C::Ok);
    C::CallbackId queuedId = {}, runningId = {}, bad = {};
    CHECK(coordinator.admitCallback(89, 1, C::CausalReverseIo, 1, bad) == C::StaleSession);
    CHECK(coordinator.admitCallback(90, 1, C::CausalReverseIo, 9, bad) == C::InvalidIdentity);
    CHECK(coordinator.admitCallback(90, 1, C::CausalReverseIo, 1, queuedId) == C::Ok);
    Request read = request(MilesWire::FileRead, 4);
    unsigned before = calls;
    std::shared_ptr<Invocation> queued = std::make_shared<Invocation>(read, services, binding(0), lifetime());
    // Test scheduler cancels before dispatch: no side effect, then explicit ack.
    queued.reset();
    CHECK(calls == before);
    CHECK(coordinator.acknowledge(90, queuedId) == C::Ok);
    CHECK(coordinator.acknowledge(90, queuedId) == C::Unknown);

    CHECK(coordinator.admitCallback(90, 1, C::CausalReverseIo, 1, runningId) == C::Ok);
    std::shared_ptr<void> context = lifetime();
    std::shared_ptr<const Binding> fileBinding = binding(0);
    std::weak_ptr<void> contextProbe(context);
    std::weak_ptr<const Binding> bindingProbe(fileBinding);
    queued = std::make_shared<Invocation>(read, services, fileBinding, context);
    context.reset();
    fileBinding.reset();
    std::shared_ptr<Invocation> executing = queued; // Actual executor's storage pin.
    C::Readiness readiness = {};
    bool cancelled = false;
    duringRead = [&]() {
        cancelled = true;
        queued.reset(); // Client outcome abandonment cannot release the executing call.
        CHECK(coordinator.fail(90) == C::Ok);
        CHECK(!contextProbe.expired() && !bindingProbe.expired());
        CHECK(coordinator.readiness(90, 1, readiness) == C::Ok);
        CHECK(readiness.requestPins == 1 && readiness.callbackPins == 1);
        CHECK(coordinator.completeAdmission(90, 1) == C::PendingCallback);
        CHECK(coordinator.admitGame(90, 2, 5, 0, C::Ordinary, resources) == C::WrongState);
        CHECK(!executing->invokeOnAdmittedExecutor()); // Reentry cannot repeat read.
    };
    readResult = 2;
    invoke(*executing);
    duringRead = std::function<void()>();
    CHECK(cancelled && calls == before + 1 && executing->finished());
    CHECK(executing->completion().bytes.size() == 2);
    CHECK(!contextProbe.expired() && !bindingProbe.expired());
    CHECK(coordinator.readiness(90, 1, readiness) == C::Ok && readiness.callbackPins == 1);
    CHECK(coordinator.acknowledge(89, runningId) == C::StaleSession);
    CHECK(coordinator.readiness(90, 1, readiness) == C::Ok && readiness.callbackPins == 1);
    // Late actual return is recorded but is not delivered as a successful client
    // outcome. Existing coordinator may now observe completion even in Failed.
    unsigned delivered = 0;
    if (!cancelled)
        ++delivered;
    CHECK(delivered == 0);
    CHECK(coordinator.acknowledge(90, runningId) == C::Ok);
    CHECK(coordinator.acknowledge(90, runningId) == C::Unknown);
    CHECK(coordinator.completeAdmission(90, 1) == C::Ok);
    CHECK(coordinator.state() == C::Failed);
    CHECK(coordinator.readiness(90, 1, readiness) == C::Ok);
    CHECK(!readiness.requestPins && !readiness.callbackPins && readiness.vendorTerminationUnproven);
    CHECK(!executing->invokeOnAdmittedExecutor() && calls == before + 1);
    executing.reset();
    CHECK(contextProbe.expired() && bindingProbe.expired());
    // Neither destruction nor any cancellation path invoked close.
    CHECK(calls == before + 1);
    std::puts("PASS scripted cancel/stale/duplicate/late completion and retained execution pins");
}
}

int main()
{
    try
    {
        mapping();
        postOpenFailure();
        malformed();
        executorPins();
        std::printf("PASS %u assertions; scripted services only, no engine or vendor\n", checks);
        return 0;
    }
    catch (const std::exception &error)
    {
        std::fprintf(stderr, "FAIL %s after %u assertions\n", error.what(), checks);
        return 1;
    }
}
