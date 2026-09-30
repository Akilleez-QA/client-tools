#include "../transport-candidate/resource_registry.h"
#include <cstdlib>
#include <cstdio>
#include <new>
#include <type_traits>
static bool forbid = false;
void *operator new(std::size_t n) {
    if (forbid) throw std::bad_alloc();
    void *p = std::malloc(n ? n : 1);
    if (!p) throw std::bad_alloc();
    return p;
}
void operator delete(void *p) throw() { std::free(p); }
void *operator new[](std::size_t n) { return ::operator new(n); }
void operator delete[](void *p) throw() { ::operator delete(p); }
using namespace MilesWire;
using MilesTransport::ResourceRegistry;
static unsigned checks = 0;
#define CHECK(x) do { ++checks; if (!(x)) { std::printf("FAIL line %u: %s\n", __LINE__, #x); std::exit(1); } } while (0)
static Handle driver(ResourceRegistry &r, int &native) {
    ResourceRegistry::Reservation token;
    Handle h = {};
    CHECK(r.reserve(Driver, Handle(), token));
    CHECK(r.publish(token, &native, h));
    return h;
}
int main() {
    static_assert(!std::is_copy_constructible<ResourceRegistry::Reservation>::value, "unforgeable copy");
    static_assert(!std::is_copy_assignable<ResourceRegistry::Reservation>::value, "unforgeable assignment");
    int a=1,b=2,c=3; void *local=0;
    {
        ResourceRegistry r(2); Handle d=driver(r,a), s={};
        ResourceRegistry::Reservation token;
        CHECK(!r.reserve(OwnedSample,Handle(),token));
        Handle wrong=d; wrong.generation++;
        CHECK(!r.reserve(OwnedSample,wrong,token));
        CHECK(!r.reserve(BorrowedSample,d,token));
        CHECK(r.reserve(OwnedSample,d,token));
        CHECK(!r.reserve(OwnedSample,d,token));
        Handle guessed={OwnedSample,2,1};
        CHECK(!r.resolve(guessed,OwnedSample,local));
        ResourceRegistry other;
        CHECK(!other.publish(token,&b,s));
        CHECK(!s.kind);
        CHECK(!r.publish(token,0,s));
        forbid=true;
        CHECK(r.publish(token,&b,s));
        CHECK(!r.publish(token,&b,s));
        forbid=false;
        CHECK(s.slot==2 && s.generation==1);
        CHECK(r.resolve(s,OwnedSample,local) && local==&b);
        CHECK(!r.resolve(s,BorrowedSample,local));
        CHECK(r.beginClose(d));
        CHECK(!r.resolve(s,OwnedSample,local));
        CHECK(r.retire(d));
        CHECK(!r.resolve(s,OwnedSample,local));
        CHECK(!r.retire(s));
    }
    {
        ResourceRegistry r(2);Handle d=driver(r,a),s={};
        for(unsigned i=0;i<256;++i) {
            { ResourceRegistry::Reservation nullResult;CHECK(r.reserve(OwnedSample,d,nullResult)); }
            ResourceRegistry::Reservation t;CHECK(r.reserve(OwnedSample,d,t));
            CHECK(r.publish(t,&b,s));CHECK(s.slot==2 && s.generation==i+1);
            const Handle stale=s;
            forbid=true;CHECK(r.retire(s));forbid=false;
            CHECK(!r.resolve(stale,OwnedSample,local));
        }
        CHECK(r.retire(d));
    }
    {
        ResourceRegistry r(4);Handle d=driver(r,a),x={},y={};
        ResourceRegistry::Reservation t,u;
        CHECK(r.reserve(OwnedSample,d,t));CHECK(r.reserve(OwnedSample,d,u));
        forbid=true;CHECK(r.publish(t,&b,x));CHECK(r.publish(u,&c,y));forbid=false;
        CHECK(x.slot!=y.slot);CHECK(r.resolve(x,OwnedSample,local)&&local==&b);
        CHECK(r.resolve(y,OwnedSample,local)&&local==&c);
        forbid=true;CHECK(r.retire(d));forbid=false;
        CHECK(!r.resolve(x,OwnedSample,local));CHECK(!r.resolve(y,OwnedSample,local));
    }
    {
        ResourceRegistry r(2);ResourceRegistry::Reservation t;unsigned simulatedVendorCalls=0;
        bool failed=false;forbid=true;
        try { if(r.reserve(Driver,Handle(),t)) ++simulatedVendorCalls; }
        catch(const std::bad_alloc &) { failed=true; }
        forbid=false;CHECK(failed && simulatedVendorCalls==0);
        CHECK(r.reserve(Driver,Handle(),t));forbid=true;r.cancel(t);forbid=false;
        CHECK(r.reserve(Driver,Handle(),t));Handle d={};CHECK(r.publish(t,&a,d));
        CHECK(d.slot==1 && d.generation==1);
    }
    {
        ResourceRegistry r(2,2);Handle d=driver(r,a),s={};
        for(unsigned i=0;i<2;++i) {ResourceRegistry::Reservation t;CHECK(r.reserve(OwnedSample,d,t));CHECK(r.publish(t,&b,s));CHECK(r.retire(s));}
        ResourceRegistry::Reservation t;CHECK(!r.reserve(OwnedSample,d,t));
        CHECK(r.resolve(d,Driver,local));
    }
    {
        ResourceRegistry r(3);Handle stream={},alias={};
        CHECK(r.insert(Stream,&a,stream));CHECK(r.insertBorrowed(stream,&b,alias));
        CHECK(r.resolve(alias,BorrowedSample,local)&&local==&b);
        CHECK(!r.beginClose(alias));CHECK(r.retire(stream));CHECK(!r.resolve(alias,BorrowedSample,local));
    }
    std::printf("PASS %u registry checks; authored only; no vendor calls\n",checks);
}
