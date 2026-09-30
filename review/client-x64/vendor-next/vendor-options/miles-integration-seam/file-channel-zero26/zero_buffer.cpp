// Test-only callback table; no engine/vendor implementation is linked.
#include "../file-channel26/file_channel.h"
#include <cstdio>
#include <stdexcept>

namespace F = MilesFileChannel26;
namespace L = ClientAudioFileCallbacks;
namespace
{
unsigned readCalls = 0;
bool sawNonNull = false;
bool exactArguments = false;
L::OpenResult noOpen(const char *) { throw std::logic_error("unexpected open"); }
void noClose(L::LocalFileHandle) { throw std::logic_error("unexpected close"); }
int32_t noSeek(L::LocalFileHandle, int32_t, uint32_t)
{
    throw std::logic_error("unexpected seek");
}
uint32_t zeroRead(L::LocalFileHandle handle, void *destination, uint32_t requested)
{
    ++readCalls;
    sawNonNull = destination != 0;
    exactArguments = handle.value == 0 && requested == 0;
    return 0;
}
}

int main()
{
    MilesWire::Header header = {MilesWire::Magic, MilesWire::Version,
        MilesWire::ReverseRequest, MilesWire::FileRead, 0, 9, 2, 4, 0};
    MilesWire::Call call = {};
    call.target.kind = MilesWire::File;
    call.target.slot = 1;
    call.target.generation = 3;
    std::vector<unsigned char> encoded;
    if (!MilesTransport::encodeCall(header, call, MilesTransport::Bytes(),
                                    MilesTransport::Bytes(), encoded))
        return 2;
    F::Request request;
    F::Association association = {9, 2, 4, 0};
    if (F::decodeRequest(MilesTransport::Bytes(&encoded[0], encoded.size()),
                         association, request) != F::Valid)
        return 3;
    L::LocalFileHandle key = {0};
    std::shared_ptr<const F::Binding> binding = std::make_shared<F::Binding>(call.target, key);
    F::FileServices services = {noOpen, noClose, noSeek, zeroRead};
    F::Invocation invocation(request, services, binding, std::make_shared<int>(1));
    if (!invocation.invokeOnAdmittedExecutor())
        return 4;
    if (!sawNonNull)
    {
        std::puts("FAIL zero-count read callback received null destination");
        return 1;
    }
    if (readCalls != 1 || !exactArguments || invocation.completion().state != F::Returned ||
        invocation.completion().returnBits != 0 || !invocation.completion().bytes.empty())
        return 5;
    MilesWire::Handle noFile = {};
    if (F::encodeCompletion(invocation, noFile, encoded) != F::Valid)
        return 6;
    F::OwnedReply reply;
    if (F::decodeReply(MilesTransport::Bytes(&encoded[0], encoded.size()), request, reply) != F::Valid ||
        reply.returnBits || !reply.bytes.empty() || encoded.size() != 128)
        return 7;
    std::puts("PASS zero-count read invoked once with nonnull storage and no returned bytes");
    return 0;
}
