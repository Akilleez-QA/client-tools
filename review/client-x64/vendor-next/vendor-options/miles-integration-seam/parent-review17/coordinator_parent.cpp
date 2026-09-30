#include "../coordinator-candidate/coordinator.h"
#include <cstdio>
#define REQUIRE(expr) do { ++checks; if (!(expr)) { std::printf("FAIL parent line %d\n",__LINE__); return 1; } } while(0)
int main() {
 using namespace MilesCoordinator;
 unsigned checks=0;
 MilesWire::Handle one={MilesWire::OwnedSample,2,5},two={MilesWire::Stream,3,8};
 std::vector<MilesWire::Handle> pin(1,one);
 Coordinator c(77); Readiness a={},b={}; CallbackId ca={},cb={},cc={};
 REQUIRE(c.registerCallback(77,1,one)==Ok);
 REQUIRE(c.registerCallback(77,2,two)==Ok);
 REQUIRE(c.beginClose(77,2)==Ok);
 REQUIRE(c.readiness(77,2,b)==Ok && b.vendorTerminationUnproven && b.callbackPins==0 && b.requestPins==0 && b.closeFrontier==0);
 REQUIRE(c.admitGame(77,1,10,0,Ordinary,pin)==Ok);
 REQUIRE(c.admitCallback(77,1,CausalReverseIo,1,ca)==Ok);
 REQUIRE(c.admitCallback(77,2,Unsolicited,0,cb)==Ok);
 REQUIRE(c.admitCallback(77,1,Unsolicited,0,cc)==Ok);
 REQUIRE(c.beginClose(77,1)==Ok);
 REQUIRE(c.acknowledge(77,ca)==Ok);
 REQUIRE(c.completeAdmission(77,1)==Ok); // unrelated callback does not invent causal parent.
 REQUIRE(c.readiness(77,1,a)==Ok && a.requestPins==0 && a.callbackPins==1 && a.acknowledgedFrontier==1 && a.closeFrontier==2);
 REQUIRE(c.readiness(77,2,b)==Ok && b.callbackPins==1 && b.acknowledgedFrontier==0 && b.closeFrontier==1);
 REQUIRE(c.acknowledge(77,cc)==Ok);
 REQUIRE(c.readiness(77,1,a)==Ok && a.callbackPins==0 && a.acknowledgedFrontier==2 && a.vendorTerminationUnproven);
 REQUIRE(c.readiness(77,2,b)==Ok && b.callbackPins==1 && b.acknowledgedFrontier==0);
 REQUIRE(c.fail(77)==Ok);
 REQUIRE(c.completeAdmission(77,1)==Unknown);
 REQUIRE(c.acknowledge(78,cb)==StaleSession);
 REQUIRE(c.readiness(77,2,b)==Ok && b.callbackPins==1);
 REQUIRE(c.acknowledge(77,cb)==Ok);
 REQUIRE(c.readiness(77,2,b)==Ok && b.callbackPins==0 && b.acknowledgedFrontier==1 && b.vendorTerminationUnproven);
 REQUIRE(c.state()==Failed);
 // Grok17 challenge: failure during unlock must not fabricate a completed unlock.
 Coordinator failedUnlock(88);
 std::vector<MilesWire::Handle> empty;
 REQUIRE(failedUnlock.admitGame(88,1,7,0,AcquireLock,empty)==Ok);
 REQUIRE(failedUnlock.completeAdmission(88,1)==Ok);
 Id const heldLease=failedUnlock.lease();
 REQUIRE(heldLease!=0 && failedUnlock.leaseDepth()==1 && failedUnlock.leaseOwner()==7);
 REQUIRE(failedUnlock.admitGame(88,2,7,heldLease,ReleaseLock,empty)==Ok);
 REQUIRE(failedUnlock.fail(88)==Ok);
 REQUIRE(failedUnlock.completeAdmission(88,2)==Ok);
 REQUIRE(failedUnlock.state()==Failed && failedUnlock.leaseDepth()==1 && failedUnlock.lease()==heldLease && failedUnlock.leaseOwner()==7);
 std::printf("PASS %u parent coordinator mechanism checks; no vendor calls\n",checks);
 return 0;
}
