#include "sound-info-codec.h"
#include <stdio.h>
#include <string.h>
using namespace MilesTransport;
using MilesWire::SoundInfo;
static int total=0,failed=0;
static void check(bool ok,int line){++total;if(!ok){++failed;printf("FAIL %d line %d\n",total,line);}}
#define CHECK(x) check(!!(x),__LINE__)
int main(){
    SoundInfo s={-1,4,8,0x12345678,INT32_MIN,INT32_MAX,0x87654321,UINT32_MAX,0x10203040,2,0};
    const unsigned char golden[]={
        255,255,255,255,4,0,0,0,8,0,0,0,0x78,0x56,0x34,0x12,
        0,0,0,128,255,255,255,127,0x21,0x43,0x65,0x87,
        255,255,255,255,0x40,0x30,0x20,0x10,2,0,0,0,0,0,0,0};
    std::vector<unsigned char> b;CHECK(encodeSoundInfo(s,16,b));
    CHECK(b.size()==44&&memcmp(&b[0],golden,44)==0);
    SoundInfo d={};CHECK(decodeSoundInfo(Bytes(golden,44),16,d));
    CHECK(d.format==-1&&d.bits==INT32_MIN&&d.channels==INT32_MAX);
    CHECK(d.data_offset==4&&d.data_length==8&&d.rate==0x12345678);
    CHECK(d.channel_mask==0x87654321&&d.samples==UINT32_MAX&&d.block_size==0x10203040);
    CHECK(d.initial_offset==2&&d.null_mask==0);
    CHECK(encodeSoundInfo(d,16,b)&&memcmp(&b[0],golden,44)==0);
    for(size_t n=0;n<44;++n){d.format=123;CHECK(!decodeSoundInfo(Bytes(golden,n),16,d)&&d.format==123);}
    unsigned char extra[45]={};memcpy(extra,golden,44);CHECK(!decodeSoundInfo(Bytes(extra,45),16,d));
    CHECK(!decodeSoundInfo(Bytes(0,44),16,d));
    const size_t changed[]={4,8,36,40};
    for(size_t i=0;i<4;++i){memcpy(extra,golden,44);memset(extra+changed[i],255,4);CHECK(!decodeSoundInfo(Bytes(extra,44),16,d));}
    SoundInfo bad=s;bad.data_offset=15;bad.data_length=2;CHECK(!validateSoundInfo(bad,16));
    bad=s;bad.data_offset=UINT32_MAX;bad.data_length=2;CHECK(!validateSoundInfo(bad,UINT32_MAX));
    bad=s;bad.data_offset=UINT32_MAX-1;bad.data_length=2;CHECK(!validateSoundInfo(bad,UINT32_MAX));
    bad=s;bad.data_offset=UINT32_MAX-1;bad.data_length=1;CHECK(validateSoundInfo(bad,UINT32_MAX));
    bad=s;bad.data_offset=16;bad.data_length=0;CHECK(validateSoundInfo(bad,16));
    bad.data_offset=17;CHECK(!validateSoundInfo(bad,16));
    bad=s;bad.initial_offset=16;CHECK(!validateSoundInfo(bad,16));
    bad=s;bad.data_length=12;CHECK(validateSoundInfo(bad,16));bad.data_length=13;CHECK(!validateSoundInfo(bad,16));
    bad=s;bad.null_mask=DataIsNull;CHECK(!validateSoundInfo(bad,16));
    bad.data_offset=0;CHECK(!validateSoundInfo(bad,16));bad.data_length=0;CHECK(validateSoundInfo(bad,16));
    bad.null_mask=3;CHECK(!validateSoundInfo(bad,16));bad.initial_offset=0;CHECK(validateSoundInfo(bad,0));
    bad.null_mask=7;CHECK(!validateSoundInfo(bad,0));
    b.assign(1,42);CHECK(!encodeSoundInfo(bad,0,b)&&b.size()==1&&b[0]==42);
#if SIZE_MAX > UINT32_MAX
    size_t big=static_cast<size_t>(UINT32_MAX);++big;CHECK(!validateSoundInfo(s,big));
#else
    puts("SKIP retained size above UINT32_MAX is not representable");
#endif
    unsigned char retained[16]={};SoundInfoPointers local={retained+4,retained+2};
    CHECK(mapSoundInfoPointers(s,Bytes(retained,16),local,d));
    CHECK(d.data_offset==4&&d.initial_offset==2&&d.null_mask==0&&d.format==-1);
    SoundInfoPointers restored={};CHECK(resolveSoundInfoPointers(d,Bytes(retained,16),restored));
    CHECK(restored.data==local.data&&restored.initial==local.initial);
    CHECK(encodeSoundInfo(d,16,b)&&memcmp(&b[0],golden,44)==0);
    local.data=retained+16;bad=s;bad.data_length=0;CHECK(mapSoundInfoPointers(bad,Bytes(retained,16),local,d));
    CHECK(resolveSoundInfoPointers(d,Bytes(retained,16),restored)&&restored.data==retained+16);
    local.initial=retained+16;CHECK(!mapSoundInfoPointers(bad,Bytes(retained,16),local,d));
    local.data=0;local.initial=0;CHECK(mapSoundInfoPointers(bad,Bytes(retained,16),local,d)&&d.null_mask==3);
    CHECK(resolveSoundInfoPointers(d,Bytes(retained,16),restored)&&!restored.data&&!restored.initial);
    CHECK(mapSoundInfoPointers(bad,Bytes(),local,d));CHECK(resolveSoundInfoPointers(d,Bytes(),restored));
    CHECK(!mapSoundInfoPointers(s,Bytes(retained,16),local,d)); // null data cannot claim bytes
    local.data=retained+4;local.initial=retained+2;
    CHECK(!mapSoundInfoPointers(s,Bytes(0,16),local,d));
    unsigned char other[8]={};local.data=other;CHECK(!mapSoundInfoPointers(s,Bytes(retained,16),local,d));
    local.data=retained+4;local.initial=other;CHECK(!mapSoundInfoPointers(s,Bytes(retained,16),local,d));
    restored.data=other;restored.initial=other;
    CHECK(!resolveSoundInfoPointers(s,Bytes(retained,5),restored)&&restored.data==other&&restored.initial==other);
    d.format=456;CHECK(!mapSoundInfoPointers(s,Bytes(retained,5),local,d)&&d.format==456);
    printf("%d/%d sound-info checks passed\n",total-failed,total);return failed?1:0;
}
