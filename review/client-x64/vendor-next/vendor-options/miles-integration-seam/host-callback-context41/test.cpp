#include "call_context.h"
#include <atomic>
#include <thread>
#include <cstdio>
#include <stdexcept>
using namespace MilesHostContext;
static void require(bool value) { if(!value)throw std::runtime_error("context assertion"); }
static bool same(const Origin&a,const Origin&b){return a.sessionIncarnation==b.sessionIncarnation&&a.wireRequest==b.wireRequest&&a.lane==b.lane&&a.lease==b.lease&&a.admissionOrdinal==b.admissionOrdinal;}
static void local(){
 const Origin sentinel={91,92,93,94,95};Origin out=sentinel;
 require(snapshot(1,out)==Unsolicited&&same(out,sentinel));
 require(snapshot(0,out)==InvalidSession&&same(out,sentinel));
 Origin good={1,2,3,0,4};
 for(unsigned i=0;i<4;++i){Origin invalid=good;if(i==0)invalid.sessionIncarnation=0;if(i==1)invalid.wireRequest=0;if(i==2)invalid.lane=0;if(i==3)invalid.admissionOrdinal=0;Scope rejected(invalid);require(rejected.result()==InvalidOrigin);require(snapshot(1,out)==Unsolicited&&same(out,sentinel));}
 try {
  Scope outer(good);require(outer.result()==Entered);require(snapshot(1,out)==Ready&&same(out,good));out=sentinel;
  require(snapshot(2,out)==SessionMismatch&&same(out,sentinel));
  {Scope nested(good);require(nested.result()==NestedEntry);Origin foreign=good;foreign.sessionIncarnation=2;Scope rejected(foreign);require(rejected.result()==ForeignSessionEntry);require(snapshot(1,out)==Ready&&same(out,good));}
  require(snapshot(1,out)==Ready&&same(out,good));throw 7;
 }catch(int){}
 out=sentinel;require(snapshot(1,out)==Unsolicited&&same(out,sentinel));
 std::puts("PASS invalid, nested, foreign-session, unchanged-output and unwind scenarios");
}
static void simultaneous(){
 std::atomic<unsigned> arrived(0);std::atomic<bool> release(false),failed(false);
 const auto worker=[&](uint64_t id){
  Origin own={id,id+10,id+20,id+30,id+40};Scope scope(own);
  if(scope.result()!=Entered)failed=true;
  arrived.fetch_add(1);
  while(!release.load())std::this_thread::yield();
  Origin out={0,0,0,0,0};
  if(snapshot(id,out)!=Ready||!same(out,own))failed=true;
  Origin sentinel={1,2,3,4,5};out=sentinel;
  if(snapshot(id+100,out)!=SessionMismatch||!same(out,sentinel))failed=true;
 };
 std::thread first(worker,11),second(worker,22);
 while(arrived.load()!=2)std::this_thread::yield();
 std::thread background([&]{Origin out={1,2,3,4,5},sentinel=out;if(snapshot(11,out)!=Unsolicited||!same(out,sentinel))failed=true;});
 background.join();release=true;first.join();second.join();require(!failed.load());
 Origin out={0,0,0,0,0};require(snapshot(11,out)==Unsolicited);
 std::puts("PASS two simultaneous origins and empty background thread");
}
int main(){try{local();simultaneous();return 0;}catch(const std::exception&e){std::printf("FAIL %s\n",e.what());return 1;}}
