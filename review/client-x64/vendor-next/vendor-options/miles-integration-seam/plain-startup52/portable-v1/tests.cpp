#include "../candidate/ClientMiles.h"
#include "../candidate/private/native_startup_calls.h"
#include "../candidate/private/failure_boundary.h"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
unsigned checks = 0, scenarios = 0, reports = 0;
void check(bool b, int line) { ++checks; if (!b) { std::fprintf(stderr,"CHECK:%d\n",line); std::exit(81); } }
#define CHECK(x) check((x),__LINE__)
void scenario(const char* name) { ++scenarios; std::printf("SCENARIO:%s\n",name); }
void mark(const char* text) { std::puts(text); std::fflush(stdout); }
std::string faultOp;
int faultKind = 0, reporterKind = 0;
bool verifyRetainedOnFault = false;
bool forbidNativeEntry = false;
void nativeEntry(const char* op) {
    if (!forbidNativeEntry) return;
    std::printf("UNEXPECTED_NATIVE_ENTRY:%s\n",op); std::fflush(stdout);
    std::exit(86); // Cannot pass the required SIGABRT and exact-marker oracle.
}
std::vector<const char*> retained;
std::vector<std::string> expected;
unsigned starts = 0, stops = 0;
int32_t startupResult = 0, speakerResult = 0;
intptr_t prefResult = 0, seenValue = 0;
uint32_t seenNumber = 0, seenFrequency = 0, seenFlags = 0;
int32_t seenBits = 0, seenChannels = 0;
int driverIdentity;
ClientMiles::HDIGDRIVER driverResult = 0, seenDriver = 0;
char errorSource[80] = "initial error", redistSource[80] = "initial directory";
const char* errorResult = errorSource;
const char* redistResult = redistSource;
const char* callerInput = 0;
char* versionPointer = 0;
int32_t versionCapacity = 0;
int versionMode = 0;
void verifyRetained() {
    CHECK(retained.size() == expected.size());
    for (size_t i=0;i<retained.size();++i) CHECK(std::strcmp(retained[i],expected[i].c_str()) == 0);
}
void maybeThrow(const char* op) {
    if (faultOp != op) return;
    std::printf("NATIVE_THROW:%s\n",op); std::fflush(stdout);
    if (faultKind == 1) throw std::runtime_error("scripted private exception");
    throw 47;
}
void reporter(uint32_t reason, const char* message) {
    ++reports;
    CHECK(message != 0 && *message != 0);
    std::printf("REPORT:%u\n",static_cast<unsigned>(reason)); std::fflush(stdout);
    if (verifyRetainedOnFault) { verifyRetained(); mark("RETAINED_AT_REPORT"); }
    if (reporterKind == 1) throw std::runtime_error("scripted reporter exception");
    if (reporterKind == 2) throw 53;
}
}
namespace ClientMilesNativeCalls52 {
int32_t startup() { nativeEntry("startup"); maybeThrow("startup"); ++starts; return startupResult; }
void shutdown() { nativeEntry("shutdown"); verifyRetained(); maybeThrow("shutdown"); ++stops; retained.clear(); expected.clear(); }
intptr_t get_preference(uint32_t n) { nativeEntry("get_preference"); maybeThrow("get_preference"); seenNumber=n; return prefResult; }
intptr_t set_preference(uint32_t n,intptr_t v) { nativeEntry("set_preference"); maybeThrow("set_preference"); seenNumber=n;seenValue=v;return prefResult; }
const char* last_error() { nativeEntry("last_error"); maybeThrow("last_error"); return errorResult; }
const char* set_redist_directory(const char* input) {
    nativeEntry("set_redist_directory");
    CHECK(input != 0 && input != callerInput);
    retained.push_back(input); expected.push_back(std::string(input));
    maybeThrow("set_redist_directory"); return redistResult;
}
void MSS_version(char* p,int32_t n) {
    nativeEntry("MSS_version");
    maybeThrow("MSS_version");versionPointer=p;versionCapacity=n;
    if(versionMode==0) { CHECK(n>=4);p[0]='v';p[1]='5';p[2]='2';p[3]=0; }
    else if(versionMode==1) p[0]=0;
    else if(versionMode==2) { CHECK(n>=2);p[0]='X';p[1]='Y'; }
    // mode3 deliberately writes nothing, modeling no extra adapter guarantee.
}
ClientMiles::HDIGDRIVER open_digital_driver(uint32_t f,int32_t b,int32_t c,uint32_t flags) {
    nativeEntry("open_digital_driver"); maybeThrow("open_digital_driver");seenFrequency=f;seenBits=b;seenChannels=c;seenFlags=flags;return driverResult;
}
int32_t speaker_configuration_spec(ClientMiles::HDIGDRIVER d) { nativeEntry("speaker_configuration_spec"); maybeThrow("speaker_configuration_spec");seenDriver=d;return speakerResult; }
}
namespace {
void normal() {
    ClientMilesPrivate52::bindFatalReporter(reporter);
    scenario("prestartup-separate-copied-snapshots");
    const char* e=ClientMiles::last_error(); CHECK(std::strcmp(e,"initial error")==0);
    std::strcpy(errorSource,"changed source"); CHECK(std::strcmp(e,"initial error")==0);
    char input[]="miles";callerInput=input;
    const char* r=ClientMiles::set_redist_directory(input);
    CHECK(std::strcmp(r,"initial directory")==0);input[0]='X';verifyRetained();
    std::strcpy(redistSource,"changed directory");CHECK(std::strcmp(r,"initial directory")==0);
    CHECK(std::strcmp(e,"initial error")==0);CHECK(starts==0);
    e=ClientMiles::last_error();CHECK(std::strcmp(e,"changed source")==0);CHECK(std::strcmp(r,"initial directory")==0);

    scenario("self-alias-and-retained-directory-growth");
    callerInput=r;ClientMiles::set_redist_directory(r);CHECK(expected.back()=="initial directory");
    CHECK(std::strcmp(e,"changed source")==0);
    for(unsigned i=0;i<64;++i) { std::string text="directory-"+std::to_string(i);callerInput=text.c_str();ClientMiles::set_redist_directory(text.c_str()); }
    verifyRetained();CHECK(retained.size()==66);

    scenario("null-versus-empty-text");
    errorResult=0;CHECK(ClientMiles::last_error()==0);
    errorResult="";e=ClientMiles::last_error();CHECK(e!=0 && e[0]==0);
    redistResult=0;callerInput="null-result";CHECK(ClientMiles::set_redist_directory(callerInput)==0);
    redistResult="";callerInput="empty-result";r=ClientMiles::set_redist_directory(callerInput);CHECK(r!=0 && r[0]==0);
    CHECK(e[0]==0);

    scenario("native-status-and-pointer-width-preferences");
    CHECK(sizeof(intptr_t)>4);CHECK(ClientMiles::startup()==0);
    startupResult=-29;CHECK(ClientMiles::startup()==-29);
    const intptr_t wide=static_cast<intptr_t>(INT64_C(0x100000001));
    prefResult=-wide;CHECK(ClientMiles::get_preference(UINT32_MAX)==-wide);CHECK(seenNumber==UINT32_MAX);
    prefResult=wide;CHECK(ClientMiles::set_preference(42,-wide)==wide);CHECK(seenValue==-wide && seenNumber==42);
    prefResult=0;CHECK(ClientMiles::set_preference(1,wide)==0);CHECK(seenValue==wide);

    scenario("full-driver-and-speaker-forwarding");
    CHECK(ClientMiles::open_digital_driver(UINT32_MAX,-32,0x90,UINT32_C(0x80000001))==0);
    CHECK(seenFrequency==UINT32_MAX && seenBits==-32 && seenChannels==0x90 && seenFlags==UINT32_C(0x80000001));
    driverResult=reinterpret_cast<ClientMiles::HDIGDRIVER>(&driverIdentity);
    CHECK(ClientMiles::open_digital_driver(48000,24,2,7)==driverResult);
    CHECK(seenFrequency==48000 && seenBits==24 && seenChannels==2 && seenFlags==7);
    speakerResult=-1;CHECK(ClientMiles::speaker_configuration_spec(driverResult)==-1);CHECK(seenDriver==driverResult);
    speakerResult=0;CHECK(ClientMiles::speaker_configuration_spec(0)==0);CHECK(seenDriver==0);

    scenario("version-exact-writes-no-extra-guarantee");
    for(int mode=0;mode<4;++mode) {
        char buffer[8];std::memset(buffer,0x5a,sizeof buffer);char gold[8];std::memset(gold,0x5a,sizeof gold);
        versionMode=mode;
        if(mode==0){gold[1]='v';gold[2]='5';gold[3]='2';gold[4]=0;}
        if(mode==1)gold[1]=0;
        if(mode==2){gold[1]='X';gold[2]='Y';}
        ClientMiles::MSS_version(buffer+1,4);CHECK(versionPointer==buffer+1 && versionCapacity==4);CHECK(std::memcmp(buffer,gold,8)==0);
    }
    scenario("shutdown-retention-and-second-lifecycle");
    ClientMiles::shutdown();CHECK(stops==1 && retained.empty());
    // No stale snapshot is dereferenced after shutdown. A fresh pre-startup call works.
    errorResult="second lifecycle";CHECK(std::strcmp(ClientMiles::last_error(),"second lifecycle")==0);
    callerInput="second";redistResult="second result";CHECK(std::strcmp(ClientMiles::set_redist_directory(callerInput),"second result")==0);
    startupResult=1;CHECK(ClientMiles::startup()==1);ClientMiles::shutdown();CHECK(stops==2);CHECK(reports==0);
    std::printf("PASS:scenarios=%u:checks=%u\n",scenarios,checks);
}
void invoke(const std::string& op) {
    char buffer[8]={};
    if(op=="startup")ClientMiles::startup();
    else if(op=="shutdown")ClientMiles::shutdown();
    else if(op=="get_preference")ClientMiles::get_preference(1);
    else if(op=="set_preference")ClientMiles::set_preference(1,2);
    else if(op=="last_error")ClientMiles::last_error();
    else if(op=="set_redist_directory"){callerInput="fault directory";ClientMiles::set_redist_directory(callerInput);}
    else if(op=="MSS_version")ClientMiles::MSS_version(buffer,8);
    else if(op=="open_digital_driver")ClientMiles::open_digital_driver(1,2,3,4);
    else if(op=="speaker_configuration_spec")ClientMiles::speaker_configuration_spec(0);
    else std::exit(82);
}
void death(const std::string& mode) {
    mark("CHILD_STARTED");
    forbidNativeEntry = mode.find(':') == std::string::npos;
    if(mode=="missing-reporter") { ClientMiles::startup(); return; }
    if(mode=="null-bind") { ClientMilesPrivate52::bindFatalReporter(0); return; }
    ClientMilesPrivate52::bindFatalReporter(reporter);
    if(mode=="duplicate-bind") { ClientMilesPrivate52::bindFatalReporter(reporter);return; }
    if(mode=="null-redist") { ClientMiles::set_redist_directory(0);return; }
    char buffer[8]={};
    if(mode=="null-version") { ClientMiles::MSS_version(0,8);return; }
    if(mode=="zero-version") { ClientMiles::MSS_version(buffer,0);return; }
    if(mode=="negative-version") { ClientMiles::MSS_version(buffer,-1);return; }
    // Matrix mode kind:reporter:operation. No allocator fault injection.
    const size_t first=mode.find(':'), second=mode.find(':',first+1);
    CHECK(first!=std::string::npos && second!=std::string::npos);
    faultKind=std::stoi(mode.substr(0,first));reporterKind=std::stoi(mode.substr(first+1,second-first-1));faultOp=mode.substr(second+1);
    if(faultOp=="shutdown") { callerInput="live until shutdown returns";ClientMiles::set_redist_directory(callerInput);verifyRetainedOnFault=true; }
    if(faultOp=="set_redist_directory") verifyRetainedOnFault=true;
    invoke(faultOp);
}
}
int main(int argc,char** argv) {
    if(argc!=2)return 83;
    try { if(std::strcmp(argv[1],"normal")==0) {normal();return 0;}death(argv[1]); }
    catch(...) { mark("ESCAPED_EXCEPTION");return 84; }
    mark("AFTER_PUBLIC_CALL");return 85;
}
