// Prospective authored registry-only tests. No SDK, engine allocator or execution receipt.
#include "../candidate/transport-candidate/resource_registry.h"
#include <cstdio>
#include <cstdlib>
using namespace MilesWire;
using MilesTransport::ResourceRegistry;
namespace {
void check(bool ok) { if (!ok) std::abort(); }
bool same(const Handle &a,const Handle &b) { return a.kind==b.kind && a.slot==b.slot && a.generation==b.generation; }
Handle driver(ResourceRegistry &r,int &object) {
    Handle h={}; ResourceRegistry::Reservation t;
    check(r.reserve(Driver,Handle(),t));check(r.publish(t,&object,h));return h;
}
Handle stream(ResourceRegistry &r,Handle parent,int &object) {
    Handle h={};ResourceRegistry::Reservation t;
    check(r.reserve(Stream,parent,t));check(r.publish(t,&object,h));return h;
}
bool live(ResourceRegistry &r,Handle h) { void *p=0;return r.resolve(h,static_cast<ResourceKind>(h.kind),p); }
void parentsAndAliases() {
    ResourceRegistry r(8);int d=0,s=0,a=0,other=0;Handle out={};
    ResourceRegistry::Reservation invalid;
    check(!r.reserve(Stream,Handle(),invalid));check(!r.insert(Stream,&s,out));
    Handle dh=driver(r,d),sh=stream(r,dh,s),ah={};
    check(r.insertBorrowed(sh,&a,ah));check(live(r,ah));
    check(r.insertBorrowed(sh,&a,out));check(same(ah,out));
    out=Handle();check(!r.insertBorrowed(sh,&other,out));check(!out.kind);
    check(!r.beginClose(ah));check(!r.retire(ah));
    check(r.beginClose(sh));check(!live(r,sh));check(!live(r,ah));
    check(!r.insertBorrowed(sh,&a,out));check(!r.beginClose(sh));
    check(r.retire(sh));check(!r.retire(sh));check(live(r,dh));
    Handle replacement=stream(r,dh,s);check(replacement.slot==sh.slot);check(replacement.generation!=sh.generation);
    check(!live(r,sh));check(!live(r,ah));
    std::puts("PASS parent-alias-close");
}
void driverCascade() {
    ResourceRegistry r(12);int d=0,s1=0,s2=0,a1=0,a2=0,owned=0,unrelated=0;
    Handle dh=driver(r,d),sh1=stream(r,dh,s1),sh2=stream(r,dh,s2),ah1={},ah2={},oh={};
    check(r.insertBorrowed(sh1,&a1,ah1));check(r.insertBorrowed(sh2,&a2,ah2));
    ResourceRegistry::Reservation sample,reservedStream,reservedSample;
    check(r.reserve(OwnedSample,dh,sample));check(r.publish(sample,&owned,oh));
    check(r.reserve(Stream,dh,reservedStream));check(r.reserve(OwnedSample,dh,reservedSample));
    Handle other=driver(r,unrelated);
    check(r.beginClose(sh2));check(r.beginClose(oh));
    check(r.beginClose(dh));check(!live(r,sh1));check(!live(r,ah1));
    check(r.retire(dh));
    check(!live(r,sh1));check(!live(r,sh2));check(!live(r,ah1));check(!live(r,ah2));check(!live(r,oh));check(live(r,other));
    Handle out={};check(!r.publish(reservedStream,&s1,out));check(!r.publish(reservedSample,&owned,out));
    r.cancel(reservedStream);r.cancel(reservedSample);
    std::puts("PASS driver-cascade");
}
void invalidatedTokenCannotCancelReplacement() {
    ResourceRegistry r(3);int d1=0,d2=0,s=0;Handle nextStream={};ResourceRegistry::Reservation replacement;
    {
        ResourceRegistry::Reservation old;
        Handle first=driver(r,d1);check(r.reserve(Stream,first,old));
        check(r.retire(first));Handle second=driver(r,d2);check(second.slot==first.slot);
        check(r.reserve(Stream,second,replacement));
        Handle rejected={};check(!r.publish(old,&s,rejected));
        // old destructor runs while same slot now holds a new generation reservation.
    }
    check(r.publish(replacement,&s,nextStream));check(live(r,nextStream));check(nextStream.slot==2);
    std::puts("PASS late-token-destruction");
}
void cancellationAndExhaustion() {
    int d=0,s=0;ResourceRegistry r(2,1);Handle dh=driver(r,d),sh={};
    {ResourceRegistry::Reservation nullOpen;check(r.reserve(Stream,dh,nullOpen));r.cancel(nullOpen);}
    sh=stream(r,dh,s);check(live(r,sh));check(r.retire(sh));
    ResourceRegistry::Reservation exhausted;check(!r.reserve(Stream,dh,exhausted));
    check(live(r,dh));std::puts("PASS cancel-and-generation-exhaustion");
}
}
int main(){parentsAndAliases();driverCascade();invalidatedTokenCannotCancelReplacement();cancellationAndExhaustion();}
