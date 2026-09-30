#include "transport-candidate/resource_registry.h"
#include <cassert>
#include <cstdio>
using namespace MilesTransport;
using namespace MilesWire;
static Handle driver(ResourceRegistry &r, void *p) {
    ResourceRegistry::Reservation t;
    Handle h={};
    assert(r.reserve(Driver,Handle(),t));
    assert(r.publish(t,p,h));
    return h;
}
int main() {
    int d1=1,d2=2,s1=3,s2=4;
    ResourceRegistry r(3),other;
    Handle d=driver(r,&d1),out={OwnedSample,99,99};
    void *p=0;
    {
        ResourceRegistry::Reservation t;
        assert(r.reserve(OwnedSample,d,t));
        assert(!r.publish(t,0,out));
        assert(out.slot==99); // failed publication preserves output
        assert(!other.publish(t,&s1,out));
        Handle guessed={OwnedSample,2,1};
        assert(!r.resolve(guessed,OwnedSample,p));
        assert(!r.beginClose(guessed) && !r.retire(guessed));
    } // cancellation frees the unexposed slot, without burning generation
    Handle previous={};
    for(unsigned i=0;i<64;++i) {
        ResourceRegistry::Reservation t;
        assert(r.reserve(OwnedSample,d,t));
        assert(r.publish(t,&s1,out));
        assert(out.slot==2 && out.generation==i+1);
        assert(r.resolve(out,OwnedSample,p) && p==&s1);
        if(previous.slot) assert(!r.resolve(previous,OwnedSample,p));
        previous=out;
        assert(r.retire(out));
        assert(!r.retire(out) && !r.resolve(out,OwnedSample,p));
    }
    Handle secondDriver=driver(r,&d2),child={};
    {
        ResourceRegistry::Reservation t;
        assert(r.reserve(OwnedSample,secondDriver,t));
        assert(r.publish(t,&s2,child));
    }
    assert(r.retire(d)); // unrelated parent retirement leaves child available
    assert(r.resolve(child,OwnedSample,p) && p==&s2);
    assert(r.beginClose(secondDriver));
    assert(!r.resolve(child,OwnedSample,p));
    assert(r.retire(secondDriver));
    assert(!r.resolve(child,OwnedSample,p));
    ResourceRegistry limited(2,2);
    Handle ld=driver(limited,&d1);
    for(unsigned generation=1;generation<=2;++generation) {
        ResourceRegistry::Reservation t;
        assert(limited.reserve(OwnedSample,ld,t));
        assert(limited.publish(t,&s1,out));
        assert(out.generation==generation);
        assert(limited.retire(out));
    }
    ResourceRegistry::Reservation exhausted;
    assert(!limited.reserve(OwnedSample,ld,exhausted));
    puts("PASS bounded actual-header registry checks; no vendor/host/native execution");
}
