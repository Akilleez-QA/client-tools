#include "tree/transport-candidate/resource_registry.h"
#include <cstdio>
#include <cstdlib>
using MilesTransport::ResourceRegistry;
using namespace MilesWire;
namespace {
unsigned assertions=0;
void check(bool ok){++assertions;if(!ok){std::fprintf(stderr,"FAIL registry assertion %u\n",assertions);std::abort();}}
bool same(const Handle&a,const Handle&b){return a.kind==b.kind&&a.slot==b.slot&&a.generation==b.generation;}
Handle sentinel(){Handle h={File,99,77};return h;}
Handle publish(ResourceRegistry&r,ResourceKind kind,const Handle&parent,void*identity){ResourceRegistry::Reservation token;Handle h=sentinel();check(r.reserve(kind,parent,token));check(r.publish(token,identity,h));return h;}
void resolves(ResourceRegistry&r,const Handle&h,ResourceKind kind,void*identity){void*out=0;check(r.resolve(h,kind,out));check(out==identity);}
void absent(ResourceRegistry&r,const Handle&h,ResourceKind kind){int marker=0;void*out=&marker;check(!r.resolve(h,kind,out));check(out==0);}
void reservationRules(){
 ResourceRegistry r(5);int identities[5]={};Handle nil={};ResourceRegistry::Reservation stream;
 check(!r.reserve(Stream,nil,stream));Handle file={};check(r.insert(File,&identities[0],file));check(!r.reserve(Stream,file,stream));
 Handle driver=publish(r,Driver,nil,&identities[1]);check(r.reserve(Stream,driver,stream));
 // On this fresh registry the next row is known; final publication confirms the
 // probe was exactly the unpublished identity, not a guessed unrelated handle.
 Handle unpublished={Stream,driver.slot+1,1};absent(r,unpublished,Stream);check(!r.beginClose(unpublished));check(!r.retire(unpublished));
 Handle out=sentinel();check(!r.publish(stream,0,out));check(same(out,sentinel()));check(!r.reserve(Stream,driver,stream));
 check(r.publish(stream,&identities[2],out));check(same(out,unpublished));resolves(r,out,Stream,&identities[2]);
 ResourceRegistry::Reservation rejected;check(r.beginClose(driver));check(!r.reserve(Stream,driver,rejected));absent(r,out,Stream);
 check(!r.insert(Stream,&identities[3],file));
 std::puts("PASS reservation-parent-and-publication");
}
void aliasesAndClose(){
 ResourceRegistry r(8);int identities[8]={};Handle nil={};Handle driver=publish(r,Driver,nil,&identities[0]);Handle stream=publish(r,Stream,driver,&identities[1]);Handle alias={};
 check(r.insertBorrowed(stream,&identities[2],alias));Handle repeated=sentinel();check(r.insertBorrowed(stream,&identities[2],repeated));check(same(alias,repeated));resolves(r,alias,BorrowedSample,&identities[2]);
 Handle refused=sentinel();check(!r.insertBorrowed(stream,&identities[3],refused));check(same(refused,sentinel()));check(!r.beginClose(alias));check(!r.retire(alias));
 check(r.beginClose(stream));absent(r,stream,Stream);absent(r,alias,BorrowedSample);check(!r.insertBorrowed(stream,&identities[2],refused));check(same(refused,sentinel()));
 check(r.retire(stream));absent(r,stream,Stream);absent(r,alias,BorrowedSample);Handle replacement=publish(r,Stream,driver,&identities[4]);check(replacement.slot==stream.slot);check(replacement.generation!=stream.generation);
 Handle nextAlias={};check(r.insertBorrowed(replacement,&identities[2],nextAlias));check(nextAlias.slot==alias.slot);check(nextAlias.generation!=alias.generation);absent(r,alias,BorrowedSample);resolves(r,nextAlias,BorrowedSample,&identities[2]);
 std::puts("PASS borrowed-identity-and-close");
}
void cascade(){
 ResourceRegistry r(11);int identities[20]={};Handle nil={};Handle driver=publish(r,Driver,nil,&identities[0]);Handle owned=publish(r,OwnedSample,driver,&identities[1]);Handle stream=publish(r,Stream,driver,&identities[2]);Handle alias={};check(r.insertBorrowed(stream,&identities[3],alias));
 Handle closing=publish(r,Stream,driver,&identities[4]);Handle closingAlias={};check(r.insertBorrowed(closing,&identities[5],closingAlias));check(r.beginClose(closing));
 ResourceRegistry::Reservation pendingOwned,pendingStream;check(r.reserve(OwnedSample,driver,pendingOwned));check(r.reserve(Stream,driver,pendingStream));
 Handle survivorFile={};check(r.insert(File,&identities[6],survivorFile));Handle otherDriver=publish(r,Driver,nil,&identities[7]);Handle otherOwned=publish(r,OwnedSample,otherDriver,&identities[8]);
 check(r.retire(driver));absent(r,driver,Driver);absent(r,owned,OwnedSample);absent(r,stream,Stream);absent(r,alias,BorrowedSample);absent(r,closing,Stream);absent(r,closingAlias,BorrowedSample);
 Handle refused=sentinel();check(!r.publish(pendingOwned,&identities[9],refused));check(same(refused,sentinel()));check(!r.publish(pendingStream,&identities[10],refused));check(same(refused,sentinel()));
 resolves(r,survivorFile,File,&identities[6]);resolves(r,otherDriver,Driver,&identities[7]);resolves(r,otherOwned,OwnedSample,&identities[8]);
 // Exactly eight slots were driver/children/aliases/reservations; all are reusable.
 for(unsigned i=0;i<8;++i){Handle fresh={};check(r.insert(File,&identities[11+i],fresh));}
 Handle full=sentinel();check(!r.insert(File,&identities[19],full));check(same(full,sentinel()));r.cancel(pendingOwned);r.cancel(pendingStream);
 resolves(r,otherOwned,OwnedSample,&identities[8]);
 std::puts("PASS driver-retirement-cascade");
}
void staleReservation(bool explicitCancel){
 ResourceRegistry r(2);int identities[4]={};Handle nil={};ResourceRegistry::Reservation replacement;Handle newDriver={};
 {
  ResourceRegistry::Reservation old;Handle driver=publish(r,Driver,nil,&identities[0]);check(r.reserve(Stream,driver,old));check(r.retire(driver));newDriver=publish(r,Driver,nil,&identities[1]);check(newDriver.slot==driver.slot);check(newDriver.generation!=driver.generation);check(r.reserve(Stream,newDriver,replacement));
  Handle out=sentinel();check(!r.publish(old,&identities[2],out));check(same(out,sentinel()));
  if(explicitCancel)r.cancel(old);
 } // Old destructor must not cancel the live replacement reservation.
 Handle stream={};check(r.publish(replacement,&identities[3],stream));resolves(r,stream,Stream,&identities[3]);resolves(r,newDriver,Driver,&identities[1]);
}
void tokenGeneration(){staleReservation(true);staleReservation(false);std::puts("PASS stale-token-cancel-generation");}
void capacity(){
 ResourceRegistry r(2);int identities[3]={};Handle nil={};Handle driver=publish(r,Driver,nil,&identities[0]);ResourceRegistry::Reservation reserved,excess;check(r.reserve(Stream,driver,reserved));check(!r.reserve(Stream,driver,excess));
 Handle out=sentinel();check(!r.publish(excess,&identities[1],out));check(same(out,sentinel()));check(r.publish(reserved,&identities[1],out));resolves(r,out,Stream,&identities[1]);
 Handle alias=sentinel();check(!r.insertBorrowed(out,&identities[2],alias));check(same(alias,sentinel()));check(r.retire(out));check(r.reserve(Stream,driver,excess));r.cancel(excess);check(r.reserve(Stream,driver,excess));check(r.publish(excess,&identities[2],out));resolves(r,out,Stream,&identities[2]);
 std::puts("PASS capacity-before-publication");
}
void exhaustion(){
 int identities[3]={};Handle nil={};ResourceRegistry r(1,2);Handle old={};check(r.insert(File,&identities[0],old));check(old.generation==1);check(r.retire(old));Handle current={};check(r.insert(File,&identities[1],current));check(current.slot==old.slot&&current.generation==2);absent(r,old,File);check(!r.retire(old));resolves(r,current,File,&identities[1]);check(r.retire(current));absent(r,current,File);Handle refused=sentinel();check(!r.insert(File,&identities[2],refused));check(same(refused,sentinel()));ResourceRegistry::Reservation token;check(!r.reserve(File,nil,token));
 ResourceRegistry parents(3,1);Handle driver=publish(parents,Driver,nil,&identities[0]);Handle stream=publish(parents,Stream,driver,&identities[1]);Handle alias={};check(parents.insertBorrowed(stream,&identities[2],alias));check(parents.retire(driver));absent(parents,alias,BorrowedSample);check(!parents.reserve(Driver,nil,token));
 std::puts("PASS generation-exhaustion");
}
}
int main(){reservationRules();aliasesAndClose();cascade();tokenGeneration();capacity();exhaustion();std::printf("PASS registry assertions=%u\n",assertions);}
