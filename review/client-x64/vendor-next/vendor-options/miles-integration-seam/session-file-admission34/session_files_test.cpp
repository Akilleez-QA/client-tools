#include "coordinator.h"
#include <cstdio>
static unsigned checks;
static bool check(bool ok,int line){++checks;if(!ok)std::printf("FAIL %d\n",line);return ok;}
#define CHECK(x) if(!check((x),__LINE__))return 1
int main() {
    using namespace MilesCoordinator;
    std::vector<MilesWire::Handle> none;
    MilesWire::Handle nullHandle={0,0,0},badHandle={MilesWire::File,1,0};
    MilesWire::Handle sample={MilesWire::OwnedSample,1,1};
    std::vector<MilesWire::Handle> samples(1,sample);
    Readiness ready={};CallbackId open={},background={},late={},bad={};

    // Pre-driver global file table; no resource handle exists or is fabricated.
    Coordinator c(41);
    CHECK(c.registerSessionFiles(40,1)==StaleSession);
    CHECK(c.registerSessionFiles(41,0)==InvalidIdentity);
    CHECK(c.registerSessionFiles(41,2)==InvalidIdentity);
    CHECK(c.registerSessionFiles(41,1)==Ok);
    CHECK(c.registerSessionFiles(41,1)==InvalidIdentity); // registration replay
    CHECK(c.registerSessionFiles(41,2)==Busy); // unique table; ID not consumed
    CHECK(c.registerCallback(41,2,nullHandle)==InvalidIdentity);
    CHECK(c.registerCallback(41,2,badHandle)==InvalidIdentity);
    CHECK(c.registerCallback(41,2,sample)==Ok); // same monotonic ID space
    CHECK(c.readiness(41,1,ready)==Ok && !ready.requestPins && !ready.callbackPins);
    CHECK(ready.vendorTerminationUnproven && !ready.closing);
    CHECK(c.beginClose(41,1)==WrongState); // must drain ordinary session intake
    CHECK(c.readiness(41,1,ready)==Ok && !ready.closing);

    // A native call with no resource can cause FileOpen before driver creation.
    CHECK(c.admitGame(41,1,7,0,Ordinary,none)==Ok);
    CHECK(c.readiness(41,1,ready)==Ok && ready.requestPins==1);
    CHECK(c.readiness(41,2,ready)==Ok && ready.requestPins==0);
    CHECK(c.admitCallback(41,1,CausalReverseIo,0,bad)==InvalidIdentity);
    CHECK(c.admitCallback(41,1,CausalReverseIo,2,bad)==InvalidIdentity);
    CHECK(c.admitCallback(41,1,Unsolicited,1,bad)==InvalidIdentity);
    CHECK(c.admitCallback(40,1,CausalReverseIo,1,bad)==StaleSession);
    CHECK(c.admitCallback(41,99,Unsolicited,0,bad)==Unknown);
    CHECK(c.admitCallback(41,1,CausalReverseIo,1,open)==Ok);
    CHECK(c.admitCallback(41,1,Unsolicited,0,background)==Ok);
    CHECK(c.completeAdmission(41,1)==PendingCallback);
    CHECK(c.admitGame(41,2,7,0,Ordinary,none)==Busy);
    CHECK(c.readiness(41,1,ready)==Ok && ready.requestPins==1 && ready.callbackPins==2);

    CHECK(c.beginDrain(41)==Ok && c.state()==Draining);
    CHECK(c.beginClose(41,1)==Ok);
    CHECK(c.readiness(41,1,ready)==Ok && ready.closeFrontier==2 && ready.acknowledgedFrontier==0);
    CHECK(c.admitCallback(41,1,Unsolicited,0,late)==Ok); // late observation retained
    CHECK(c.readiness(41,1,ready)==Ok && ready.closeFrontier==3);
    CHECK(c.acknowledge(41,background)==Ok && c.acknowledge(41,late)==Ok);
    CHECK(c.readiness(41,1,ready)==Ok && ready.acknowledgedFrontier==0 && ready.callbackPins==1);
    CHECK(c.completeAdmission(41,1)==PendingCallback);
    CHECK(c.acknowledge(40,open)==StaleSession);
    CHECK(c.acknowledge(41,open)==Ok);
    CHECK(c.readiness(41,1,ready)==Ok && ready.acknowledgedFrontier==3 && !ready.callbackPins);
    CHECK(c.completeAdmission(41,1)==Ok);
    CHECK(c.completeAdmission(41,1)==Unknown); // admission completion replay
    CHECK(c.acknowledge(41,open)==Unknown); // callback ACK replay
    CHECK(c.readiness(41,1,ready)==Ok && !ready.requestPins && ready.vendorTerminationUnproven);
    CHECK(c.registerSessionFiles(41,3)==WrongState);
    CHECK(c.admitGame(41,2,7,0,Ordinary,none)==WrongState);
    CHECK(c.admitCleanup(41,1,7,0,Ordinary,none)==InvalidIdentity); // ordinal replay
    CHECK(c.admitCleanup(41,2,7,0,Ordinary,samples)==Ok);
    CHECK(c.readiness(41,1,ready)==Ok && ready.requestPins==1);
    CHECK(c.readiness(41,2,ready)==Ok && ready.requestPins==1);
    CHECK(c.admitCallback(41,1,CausalReverseIo,2,open)==Ok);
    CHECK(c.completeAdmission(41,2)==PendingCallback);
    CHECK(c.acknowledge(41,open)==Ok && c.completeAdmission(41,2)==Ok);
    CHECK(c.readiness(41,1,ready)==Ok && ready.acknowledgedFrontier==4 && ready.closeFrontier==4);
    CHECK(!ready.requestPins && !ready.callbackPins && ready.vendorTerminationUnproven);

    // ResourceScoped close/admission behavior is unchanged even beside a session table.
    Coordinator resource(42);
    CHECK(resource.registerSessionFiles(42,1)==Ok && resource.registerCallback(42,2,sample)==Ok);
    CHECK(resource.beginClose(42,2)==Ok); // still permitted while Active
    CHECK(resource.admitGame(42,1,1,0,Ordinary,samples)==ClosingResource);
    CHECK(resource.admitGame(42,1,1,0,Ordinary,none)==Ok);
    CHECK(resource.readiness(42,1,ready)==Ok && ready.requestPins==1);
    CHECK(resource.readiness(42,2,ready)==Ok && ready.requestPins==0);
    CHECK(resource.completeAdmission(42,1)==Ok);
    CHECK(resource.registerCallback(42,3,sample)==ClosingResource);

    // Failure retains pins and accepts observations, never new execution admission.
    Coordinator failed(51);
    CHECK(failed.registerSessionFiles(51,1)==Ok);
    CHECK(failed.admitGame(51,1,1,0,Ordinary,none)==Ok);
    CHECK(failed.admitCallback(51,1,CausalReverseIo,1,open)==Ok);
    CHECK(failed.fail(51)==Ok && failed.state()==Failed);
    CHECK(failed.readiness(51,1,ready)==Ok && ready.requestPins==1 && ready.callbackPins==1);
    CHECK(failed.beginClose(51,1)==Ok); // Failed retains existing close accounting
    CHECK(failed.admitCallback(51,1,Unsolicited,0,late)==Ok);
    CHECK(failed.readiness(51,1,ready)==Ok && ready.closeFrontier==2);
    CHECK(failed.admitCleanup(51,2,1,0,Ordinary,none)==WrongState);
    CHECK(failed.registerSessionFiles(51,2)==WrongState);
    CHECK(failed.beginDrain(51)==WrongState);
    CHECK(failed.completeAdmission(51,1)==PendingCallback);
    CHECK(failed.acknowledge(51,open)==Ok && failed.completeAdmission(51,1)==Ok);
    CHECK(failed.state()==Failed);
    CHECK(failed.readiness(51,1,ready)==Ok && !ready.requestPins && ready.callbackPins==1);
    CHECK(failed.acknowledge(51,late)==Ok);
    CHECK(failed.readiness(51,1,ready)==Ok && !ready.callbackPins && ready.vendorTerminationUnproven);
    Coordinator replacement(52);CHECK(replacement.registerSessionFiles(52,1)==Ok);
    CHECK(replacement.acknowledge(51,late)==StaleSession);
    CHECK(replacement.readiness(52,1,ready)==Ok && !ready.callbackPins);

    // Resource/session registrations and callbacks consume the same existing limits.
    Limits limits;limits.registrations=1;limits.callbacks=1;limits.maximumId=2;
    Coordinator bounded(61,limits);
    CHECK(bounded.registerSessionFiles(61,1)==Ok);
    CHECK(bounded.registerCallback(61,2,sample)==Capacity);
    CHECK(bounded.admitCallback(61,1,Unsolicited,0,open)==Ok && open.sequence==1);
    CHECK(bounded.admitCallback(61,1,Unsolicited,0,bad)==Capacity && !bad.sequence);
    CHECK(bounded.acknowledge(61,open)==Ok);
    CHECK(bounded.admitCallback(61,1,Unsolicited,0,late)==Ok && late.sequence==2);
    CHECK(bounded.acknowledge(61,late)==Ok);
    CHECK(bounded.admitCallback(61,1,Unsolicited,0,bad)==Capacity && !bad.sequence);
    Coordinator resourceFirst(62,limits);CHECK(resourceFirst.registerCallback(62,1,sample)==Ok);
    CHECK(resourceFirst.registerSessionFiles(62,2)==Capacity);
    limits.registrations=3;limits.maximumId=1;
    Coordinator exhausted(63,limits);CHECK(exhausted.registerCallback(63,1,sample)==Ok);
    CHECK(exhausted.registerSessionFiles(63,2)==Capacity);

    std::printf("PASS %u session file registration checks; portable state model only\n",checks);
    return 0;
}
