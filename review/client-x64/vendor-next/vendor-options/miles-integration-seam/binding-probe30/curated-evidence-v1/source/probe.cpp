// SOURCE ONLY until separate parent approval of the frozen build and runtime.
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <Mss.h>
#include <cstdio>
#include <cstring>
#include <stdexcept>
#include <vector>
#if !defined(_M_IX86) || _MSC_VER != 1800
#error This probe requires actual VS2013 v120 x86 and the possessed Miles header.
#endif
static_assert(sizeof(S32)==4 && sizeof(U32)==4, "exact native scalar widths");
static void require(bool ok, const char *why) {
    if (!ok) throw std::runtime_error(why);
}
static void put16(std::vector<unsigned char> &v, size_t at, unsigned value) {
    v[at]=static_cast<unsigned char>(value);
    v[at+1]=static_cast<unsigned char>(value>>8);
}
static void put32(std::vector<unsigned char> &v, size_t at, U32 value) {
    for(unsigned i=0;i<4;++i) v[at+i]=static_cast<unsigned char>(value>>(8*i));
}
struct Input {
    std::vector<unsigned char> image;
    char suffix[5];
    Input(U32 frames, unsigned tag) : image(44+frames*2,0) {
        std::memcpy(suffix,".wav",5);
        std::memcpy(&image[0],"RIFF",4); put32(image,4,static_cast<U32>(image.size()-8));
        std::memcpy(&image[8],"WAVEfmt ",8); put32(image,16,16);
        put16(image,20,tag); put16(image,22,1); put32(image,24,22050);
        put32(image,28,44100); put16(image,32,2); put16(image,34,16);
        std::memcpy(&image[36],"data",4); put32(image,40,frames*2);
    }
};
struct OwnedError {
    bool isNull, terminated;
    unsigned length;
    char text[8192];
    void capture() {
        const char *p=::AIL_last_error(); // immediately after bind, before any other SDK call
        isNull=(p==0); terminated=isNull; length=0;
        if(p) {
            while(length<sizeof(text) && p[length]) { text[length]=p[length]; ++length; }
            terminated=(length<sizeof(text));
            if(terminated) text[length]=0;
        }
    }
    void print() const {
        std::printf(" error_null=%u error_terminated=%u error_bytes=%u error_hex=",
            static_cast<unsigned>(isNull),static_cast<unsigned>(terminated),length);
        if(!length) std::printf("-");
        for(unsigned i=0;i<length;++i)
            std::printf("%02x",static_cast<unsigned>(static_cast<unsigned char>(text[i])));
        std::puts("");
    }
};
struct Lifetime {
    bool started, bound;
    HDIGDRIVER driver;
    HSAMPLE sample;
    Lifetime() : started(false),bound(false),driver(0),sample(0) {}
    void finish() {
        if(sample) {
            if(bound) { ::AIL_end_sample(sample); bound=false; std::puts("end_returned"); }
            ::AIL_release_sample_handle(sample); sample=0;
            std::puts("release_returned");
        }
        if(started) { ::AIL_shutdown(); started=false; driver=0; std::puts("shutdown_returned"); }
    }
    ~Lifetime() { if(sample || started) { std::puts("failure_cleanup_begin"); finish(); } }
  private:
    Lifetime(const Lifetime &);
    Lifetime &operator=(const Lifetime &);
};
static S32 bind(Lifetime &life, const char *label, const Input &input) {
    OwnedError error; // all result storage exists before the side effect
    S32 value=::AIL_set_named_sample_file(life.sample,input.suffix,&input.image[0],
                                          static_cast<U32>(input.image.size()),0);
    error.capture();
    life.bound=(value!=0); // only tracks whether end/query is permitted by this probe
    std::printf("bind=%s sample=%p bytes=%lu return_s32=%ld return_bits=%08lx",
        label,static_cast<void *>(life.sample),static_cast<unsigned long>(input.image.size()),
        static_cast<long>(value),static_cast<unsigned long>(static_cast<U32>(value)));
    error.print();
    require(error.terminated,"last_error exceeded preallocated capture; stop without retuning");
    return value;
}
static void queryAndEnd(Lifetime &life, const char *label, S32 expected) {
    require(life.bound,"query only after observed successful PCM bind");
    S32 total=-19001,current=-19002;
    ::AIL_sample_ms_position(life.sample,&total,&current);
    std::printf("query=%s total_s32=%ld total_bits=%08lx current_s32=%ld current_bits=%08lx expected_total=%ld expected_current=0\n",
        label,static_cast<long>(total),static_cast<unsigned long>(static_cast<U32>(total)),
        static_cast<long>(current),static_cast<unsigned long>(static_cast<U32>(current)),
        static_cast<long>(expected));
    require(total==expected && current==0,"precommitted PCM milliseconds mismatch; stop without retuning");
    ::AIL_end_sample(life.sample); life.bound=false;
    std::printf("end=%s returned=1\n",label);
}
int main(int argc, char **argv) {
    setvbuf(stdout,0,_IONBF,0);
    try {
        require(argc==3,"usage: probe.exe exact-original-dll-path private-redist-directory");
        HMODULE loaded=0;
        require(GetModuleHandleExA(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS|GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
            reinterpret_cast<LPCSTR>(&::AIL_startup),&loaded)!=0,"identify imported module");
        char path[MAX_PATH]={}; DWORD length=GetModuleFileNameA(loaded,path,MAX_PATH);
        require(length && length<MAX_PATH && !_stricmp(path,argv[1]),"imported DLL path mismatch");
        std::printf("loaded_dll=%s sdk_header_version=%s compiler=%d\n",path,MSS_VERSION,_MSC_FULL_VER);
        // Every image/suffix exists before startup and outlives even failure shutdown.
        Input a(22050,1),b(44100,1),f(22050,0x7fff);
        require(a.image.size()==44144 && b.image.size()==88244 && f.image.size()==44144,"fixed fixture lengths");
        Lifetime life;
        ::AIL_set_redist_directory(argv[2]);
        S32 started=::AIL_startup(); life.started=(started!=0);
        std::printf("startup_s32=%ld startup_bits=%08lx\n",static_cast<long>(started),
                    static_cast<unsigned long>(static_cast<U32>(started)));
        require(life.started,"startup prerequisite");
        life.driver=::AIL_open_digital_driver(22050,16,MSS_MC_STEREO,0);
        require(life.driver!=0,"driver prerequisite");
        life.sample=::AIL_allocate_sample_handle(life.driver);
        require(life.sample!=0,"sample allocation prerequisite");
        require(bind(life,"A1",a)!=0,"valid A1 binding prerequisite"); queryAndEnd(life,"A1",1000);
        require(bind(life,"B1",b)!=0,"valid B1 binding prerequisite"); queryAndEnd(life,"B1",2000);
        require(bind(life,"A2",a)!=0,"valid A2 binding prerequisite"); queryAndEnd(life,"A2",1000);
        require(bind(life,"F",f)==0,"failed-bind prerequisite: unsupported tag unexpectedly accepted; no retuning");
        // No query/status/end after failed bind. Preserve every buffer, then rebind B.
        require(bind(life,"B2-after-F",b)!=0,"known-valid B recovery prerequisite");
        queryAndEnd(life,"B2-after-F",2000);
        life.finish();
        std::puts("PASS fixed same-sample PCM rebind characterization; all inputs alive through shutdown; no retirement proof");
        return 0;
    } catch(const std::exception &e) {
        std::printf("FAIL %s\n",e.what()); return 1;
    }
}
