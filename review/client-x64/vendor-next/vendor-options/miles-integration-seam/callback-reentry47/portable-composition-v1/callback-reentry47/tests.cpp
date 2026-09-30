#include "invocation_guard.h"
#include "../file-channel26/file_channel.h"
#include "../backend-boundary24/pipe/Session.h"
#include <future>
#include <thread>
#include <stdexcept>
#include <cstdio>
#define CHECK(x) do { if (!(x)) throw std::runtime_error(#x); } while (0)
namespace {
struct Channel : ClientMilesPipe::Channel {
    unsigned calls, finishes;
    Channel() : calls(0), finishes(0) {}
    StartupBridge::OwnedReply call(uint32_t, const MilesWire::Call &, MilesTransport::Bytes) override {
        ++calls;
        StartupBridge::OwnedReply r;
        r.result.return_bits = 1;
        return r;
    }
    void finish() override { ++finishes; }
};
void denied(void (*action)()) {
    bool caught = false;
    try { action(); } catch (const MilesCallbackGuard47::ReentryDenied &) { caught = true; }
    CHECK(caught);
}
void forward() { (void)ClientMiles::startup(); }
struct Context { unsigned calls; unsigned mode; Context() : calls(0), mode(0) {} };
ClientAudioFileCallbacks::OpenResult open(const void *, const char *) {
    ClientAudioFileCallbacks::OpenResult r = {}; return r;
}
void close(const void *, ClientAudioFileCallbacks::LocalFileHandle) {}
int32_t seek(const void *, ClientAudioFileCallbacks::LocalFileHandle, int32_t, uint32_t) { return 0; }
uint32_t read(const void *p, ClientAudioFileCallbacks::LocalFileHandle, void *, uint32_t) {
    Context &c = *static_cast<Context *>(const_cast<void *>(p)); ++c.calls;
    if (c.mode == 1) denied(forward); // Deliberately swallow guard exception.
    if (c.mode == 2) throw std::runtime_error("callback exception");
    if (c.mode == 3) {
        MilesCallbackGuard47::Scope nested;
        CHECK(!nested.admitted() && nested.violated());
    }
    return 0;
}
void invocationCases() {
    using namespace MilesFileChannel26;
    MilesWire::Header h = {};
    h.magic=MilesWire::Magic; h.version=MilesWire::Version; h.kind=MilesWire::ReverseRequest;
    h.opcode=MilesWire::FileRead; h.request=1; h.causal_request=2; h.lane=3;
    MilesWire::Call c = {}; c.target= MilesWire::Handle{MilesWire::File,1,1}; c.value[0]=1;
    std::vector<unsigned char> frame;
    CHECK(MilesTransport::encodeCall(h,c,MilesTransport::Bytes(),MilesTransport::Bytes(),frame));
    Request request; Association a = {1,2,3,0};
    CHECK(decodeRequest(MilesTransport::Bytes(&frame[0],frame.size()),a,request)==Valid);
    std::shared_ptr<Context> context(new Context);
    FileServices services = {context,open,close,seek,read};
    ClientAudioFileCallbacks::LocalFileHandle local = {0};
    std::shared_ptr<const Binding> binding(new Binding(c.target,local));
    for (unsigned mode=0; mode!=4; ++mode) {
        context->mode=mode;
        Invocation work(request,services,binding,context);
        CHECK(work.invokeOnAdmittedExecutor());
        CHECK(work.completion().state==(mode ? CallThrew : Returned));
        std::vector<unsigned char> output(1,77);
        if (mode) {
            CHECK(encodeCompletion(work,MilesWire::Handle{},output)==InvalidResult);
            CHECK(output.size()==1 && output[0]==77);
        } else CHECK(encodeCompletion(work,MilesWire::Handle{},output)==Valid);
        CHECK(!work.invokeOnAdmittedExecutor());
        MilesCallbackGuard47::requireForwardAllowed();
    }
    CHECK(context->calls==4);
    // Actual nested Invocation must not execute its selected service.
    { MilesCallbackGuard47::Scope outer;
      Invocation work(request,services,binding,context);
      CHECK(work.invokeOnAdmittedExecutor());
      CHECK(work.completion().state==CallThrew && context->calls==4 && outer.violated()); }
}
}
int main() {
    Channel *channel=new Channel;
    ClientMilesPipe::Session session{std::unique_ptr<ClientMilesPipe::Channel>(channel)};
    { MilesCallbackGuard47::Scope scope;
      denied(forward);
      bool requestDenied=false, closeDenied=false;
      try { session.request(MilesWire::AIL_startup,MilesWire::Call{}); }
      catch (const MilesCallbackGuard47::ReentryDenied &) { requestDenied=true; }
      try { session.close(); }
      catch (const MilesCallbackGuard47::ReentryDenied &) { closeDenied=true; }
      CHECK(requestDenied && closeDenied && scope.violated());
      CHECK(!session.started && !session.stopped && !session.uncertain());
      CHECK(channel->calls==0 && channel->finishes==0); }
    invocationCases(); CHECK(channel->calls==0);
    std::promise<void> entered, release;
    std::future<void> ready=entered.get_future(), done=release.get_future();
    std::thread callback([&] { MilesCallbackGuard47::Scope scope; entered.set_value(); done.wait();
        CHECK(scope.admitted() && !scope.violated()); });
    ready.wait();
    CHECK(ClientMiles::startup()==1); // Different thread's scope must not block this thread.
    release.set_value(); callback.join();
    CHECK(channel->calls==1);
    try { MilesCallbackGuard47::Scope scope; throw 1; } catch (int) {}
    MilesCallbackGuard47::requireForwardAllowed();
    std::puts("guard47: ingress, sticky caught failure, callback throw, nested invocation, two-thread isolation, unwind scenarios passed");
}
