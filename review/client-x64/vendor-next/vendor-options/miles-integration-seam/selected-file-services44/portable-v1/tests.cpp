#include "../candidate/selected-file-services44/selected_services.h"
#include <cstdio>
#include <cstring>
#include <limits>
#include <stdexcept>
#include <string>
using namespace MilesFileChannel26;
static unsigned checks = 0;
static void check(bool ok, int line, const char *expr) {
    ++checks;
    if (!ok) throw std::runtime_error(std::string("line ")+std::to_string(line)+": "+expr);
}
#define CHECK(x) check(!!(x), __LINE__, #x)
struct Script {
    unsigned calls[4];
    ClientMiles::FileHandle handle;
    uint32_t openStatus, readResult;
    int32_t seekResult, offset;
    uint32_t origin, count;
    int throwing;
    bool observeLifetime;
    std::weak_ptr<void> lifetime;
    Script():calls(),handle(0),openStatus(7),readResult(0),seekResult(-1),offset(0),
        origin(0),count(0),throwing(-1),observeLifetime(false) {}
};
static Script scripts[2];
template<unsigned I> static void entered(unsigned op) {
    ++scripts[I].calls[op];
    if (scripts[I].observeLifetime) CHECK(!scripts[I].lifetime.expired());
    if (scripts[I].throwing == static_cast<int>(op)) throw std::runtime_error("callback uncertainty");
}
template<unsigned I> static uint32_t openCallback(const char *name, ClientMiles::FileHandle *out) {
    CHECK(std::strcmp(name,"selected.bin")==0); CHECK(out!=0); entered<I>(0);
    *out=scripts[I].handle; return scripts[I].openStatus;
}
template<unsigned I> static void closeCallback(ClientMiles::FileHandle handle) {
    CHECK(handle==scripts[I].handle); entered<I>(1);
}
template<unsigned I> static int32_t seekCallback(ClientMiles::FileHandle handle,int32_t off,uint32_t origin) {
    CHECK(handle==scripts[I].handle); CHECK(off==scripts[I].offset); CHECK(origin==scripts[I].origin);
    entered<I>(2); return scripts[I].seekResult;
}
template<unsigned I> static uint32_t readCallback(ClientMiles::FileHandle handle,void *buffer,uint32_t count) {
    CHECK(handle==scripts[I].handle); CHECK(count==scripts[I].count); CHECK(buffer!=0);
    entered<I>(3);
    // Deliberately invalid returned extent does not itself write out of bounds.
    for(uint32_t i=0;i<count;++i) static_cast<unsigned char *>(buffer)[i]=static_cast<unsigned char>(I*64+i);
    return scripts[I].readResult;
}
template<unsigned I> static FileServices selected(std::shared_ptr<void> lifetime) {
    return MilesSelectedFileServices44::retain(&openCallback<I>,&closeCallback<I>,
        &seekCallback<I>,&readCallback<I>,lifetime);
}
static uint64_t nextRequest=0;
static MilesWire::Handle wire(unsigned slot) { MilesWire::Handle h={MilesWire::File,slot,9};return h; }
static Request request(uint32_t opcode, MilesWire::Handle target=MilesWire::Handle(),
                       uint32_t value=0,uint32_t origin=0) {
    MilesWire::Header h={}; h.magic=MilesWire::Magic;h.version=MilesWire::Version;
    h.kind=MilesWire::ReverseRequest;h.opcode=opcode;h.request=++nextRequest;h.lane=8;
    MilesWire::Call c={};c.target=target;c.value[0]=value;c.value[1]=origin;
    std::vector<unsigned char> f;
    const char name[]="selected.bin";
    CHECK(MilesTransport::encodeCall(h,c,MilesTransport::Bytes(),
        opcode==MilesWire::FileOpen?MilesTransport::Bytes(name,sizeof name):MilesTransport::Bytes(),f));
    Request out;Association a={h.request,0,8,0};
    CHECK(decodeRequest(MilesTransport::Bytes(f.data(),f.size()),a,out)==Valid);return out;
}
static std::shared_ptr<const Binding> binding(unsigned i) {
    ClientAudioFileCallbacks::LocalFileHandle local={scripts[i].handle};
    return std::make_shared<Binding>(wire(i+1),local);
}
static OwnedReply roundtrip(const Invocation &inv,MilesWire::Handle published=MilesWire::Handle()) {
    std::vector<unsigned char> buffer(128+inv.completion().bytes.size());size_t written=0;
    CHECK(encodeCompletionInto(inv,published,buffer.data(),buffer.size(),written)==Valid);
    OwnedReply out;CHECK(decodeReply(MilesTransport::Bytes(buffer.data(),written),inv.request(),out)==Valid);return out;
}
static void throwsCannotReply(Invocation &inv) {
    CHECK(inv.invokeOnAdmittedExecutor());CHECK(inv.completion().state==CallThrew);
    CHECK(!inv.invokeOnAdmittedExecutor());
    unsigned char buffer[256];std::memset(buffer,0x5a,sizeof buffer);size_t written=123;
    CHECK(encodeCompletionInto(inv,MilesWire::Handle(),buffer,sizeof buffer,written)==InvalidResult);
    CHECK(written==123);CHECK(buffer[0]==0x5a);
}
int main() {
 try {
    CHECK(sizeof(uintptr_t)>sizeof(uint32_t));
    scripts[0].handle=0;scripts[1].handle=static_cast<uintptr_t>(UINT64_C(0x100000023));
    scripts[1].openStatus=UINT32_C(0x80000001);
    std::shared_ptr<void> engine=std::make_shared<int>(3);
    std::shared_ptr<void> lifeA=std::make_shared<int>(10),lifeB=std::make_shared<int>(20);
    FileServices a=selected<0>(lifeA);
    Invocation openA(request(MilesWire::FileOpen),a,std::shared_ptr<const Binding>(),engine);
    // Construct/select B after A, then execute A first: latest-global-table bug fails.
    FileServices b=selected<1>(lifeB);
    Invocation openB(request(MilesWire::FileOpen),b,std::shared_ptr<const Binding>(),engine);
    CHECK(openA.invokeOnAdmittedExecutor());CHECK(openB.invokeOnAdmittedExecutor());
    CHECK(scripts[0].calls[0]==1 && scripts[1].calls[0]==1);
    CHECK(openA.completion().opened.handle.value==0);CHECK(openB.completion().opened.handle.value==scripts[1].handle);
    OwnedReply oa=roundtrip(openA,wire(1)),ob=roundtrip(openB,wire(2));
    CHECK(oa.returnBits==7 && oa.file.slot==1);CHECK(ob.returnBits==UINT32_C(0x80000001) && ob.file.slot==2);
    scripts[0].openStatus=0;
    Invocation failed(request(MilesWire::FileOpen),a,std::shared_ptr<const Binding>(),engine);
    CHECK(failed.invokeOnAdmittedExecutor());CHECK(roundtrip(failed).returnBits==0);
    unsigned char denied[128];size_t deniedWritten=0;
    CHECK(encodeCompletionInto(failed,wire(1),denied,sizeof denied,deniedWritten)==InvalidResult);
    CHECK(scripts[0].calls[1]==0);scripts[0].openStatus=7;
    for(uint32_t origin=0;origin<3;++origin) {
      scripts[0].offset=-17;scripts[0].origin=origin;scripts[0].seekResult=std::numeric_limits<int32_t>::min();
      scripts[1].offset=std::numeric_limits<int32_t>::min();scripts[1].origin=origin;scripts[1].seekResult=-1;
      Invocation sa(request(MilesWire::FileSeek,wire(1),static_cast<uint32_t>(scripts[0].offset),origin),a,binding(0),engine);
      Invocation sb(request(MilesWire::FileSeek,wire(2),static_cast<uint32_t>(scripts[1].offset),origin),b,binding(1),engine);
      CHECK(sb.invokeOnAdmittedExecutor());CHECK(sa.invokeOnAdmittedExecutor());
      CHECK(roundtrip(sa).returnBits==UINT32_C(0x80000000));CHECK(roundtrip(sb).returnBits==UINT32_MAX);
    }
    for(uint32_t count=0;count<5;++count) {
      scripts[0].count=count;scripts[0].readResult=count?count-1:0;
      scripts[1].count=count;scripts[1].readResult=count;
      Invocation ra(request(MilesWire::FileRead,wire(1),count),a,binding(0),engine);
      Invocation rb(request(MilesWire::FileRead,wire(2),count),b,binding(1),engine);
      CHECK(ra.invokeOnAdmittedExecutor());CHECK(rb.invokeOnAdmittedExecutor());
      OwnedReply ar=roundtrip(ra),br=roundtrip(rb);
      CHECK(ar.returnBits==scripts[0].readResult && br.returnBits==count);
      unsigned char dest[8];std::memset(dest,0xee,sizeof dest);
      CHECK(copyRead(br,count,dest,sizeof dest)==Valid);
      for(uint32_t j=0;j<count;++j)CHECK(dest[j]==static_cast<unsigned char>(64+j));
      CHECK(dest[count]==0xee);
      for(size_t j=0;j<ar.bytes.size();++j)CHECK(ar.bytes[j]==j);
    }
    scripts[0].count=2;scripts[0].readResult=3;
    Invocation tooMuch(request(MilesWire::FileRead,wire(1),2),a,binding(0),engine);
    CHECK(tooMuch.invokeOnAdmittedExecutor());CHECK(tooMuch.completion().state==ReadCountOutsideBuffer);
    CHECK(encodeCompletionInto(tooMuch,MilesWire::Handle(),denied,sizeof denied,deniedWritten)==InvalidResult);
    Invocation ca(request(MilesWire::FileClose,wire(1)),a,binding(0),engine);
    Invocation cb(request(MilesWire::FileClose,wire(2)),b,binding(1),engine);
    CHECK(cb.invokeOnAdmittedExecutor());CHECK(ca.invokeOnAdmittedExecutor());CHECK(!ca.invokeOnAdmittedExecutor());
    CHECK(roundtrip(ca).returnBits==0 && roundtrip(cb).returnBits==0);
    CHECK(scripts[0].calls[1]==1 && scripts[1].calls[1]==1);
    // Lifetime is independently owned by each operation after caller's references go away.
    const uint32_t opcodes[]={MilesWire::FileOpen,MilesWire::FileClose,MilesWire::FileSeek,MilesWire::FileRead};
    for(int throwing=-1;throwing<4;++throwing) {
      scripts[0].throwing=throwing;scripts[0].observeLifetime=true;
      scripts[0].count=0;scripts[0].readResult=0;scripts[0].offset=0;scripts[0].origin=0;
      std::shared_ptr<void> lifetime=std::make_shared<int>(33);scripts[0].lifetime=lifetime;
      std::shared_ptr<void> context=std::make_shared<int>(44);std::weak_ptr<void> contextWatch=context;
      {
        FileServices retained=selected<0>(lifetime);const unsigned op=throwing<0?0:static_cast<unsigned>(throwing);
        Invocation inv(request(opcodes[op],op?wire(1):MilesWire::Handle()),retained,
            op?binding(0):std::shared_ptr<const Binding>(),context);
        retained=FileServices();lifetime.reset();context.reset();
        CHECK(!scripts[0].lifetime.expired());CHECK(!contextWatch.expired());
        const unsigned before=scripts[0].calls[op];
        if(throwing>=0) throwsCannotReply(inv);
        else {CHECK(inv.invokeOnAdmittedExecutor());CHECK(roundtrip(inv,wire(1)).returnBits==7);}
        CHECK(scripts[0].calls[op]==before+1);CHECK(!scripts[0].lifetime.expired());CHECK(!contextWatch.expired());
      }
      CHECK(scripts[0].lifetime.expired());CHECK(contextWatch.expired());
    }
    scripts[0].throwing=-1;scripts[0].observeLifetime=false;
    const unsigned before=scripts[0].calls[0]+scripts[0].calls[1]+scripts[0].calls[2]+scripts[0].calls[3];
    for(unsigned missing=0;missing<5;++missing) {
      bool rejected=false;
      try {MilesSelectedFileServices44::retain(missing==0?0:&openCallback<0>,missing==1?0:&closeCallback<0>,
          missing==2?0:&seekCallback<0>,missing==3?0:&readCallback<0>,missing==4?std::shared_ptr<void>():lifeA);}
      catch(const std::invalid_argument &){rejected=true;}CHECK(rejected);
    }
    CHECK(before==scripts[0].calls[0]+scripts[0].calls[1]+scripts[0].calls[2]+scripts[0].calls[3]);
    bool rejected=false;
    try {Invocation invalid(request(MilesWire::FileOpen),FileServices(),std::shared_ptr<const Binding>(),engine);}
    catch(const std::invalid_argument &){rejected=true;}CHECK(rejected);
    std::printf("PASS selected44 portable value/ownership gate: %u checks; no ABI/engine/Windows evidence\n",checks);
    return 0;
 } catch(const std::exception &e) {std::fprintf(stderr,"FAIL %s\n",e.what());return 1;}
}
