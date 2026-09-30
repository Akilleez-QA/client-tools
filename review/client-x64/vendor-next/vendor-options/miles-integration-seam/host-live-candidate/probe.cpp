#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <vector>
#include <Mss.h>
#include "../host-candidate/host_dispatch.h"
#include "../host-candidate/registry_resolver.h"
static int checks=0,failures=0;static unsigned touched[62]={};
static void check(bool ok,const char* label){++checks;printf("%s %d %s\n",ok?"PASS":"FAIL",checks,label);if(!ok)++failures;}
static uint32_t fb(float f){uint32_t r;memcpy(&r,&f,4);return r;}
static uint32_t sb(S32 s){uint32_t r;memcpy(&r,&s,4);return r;}
static MilesWire::Result dispatch(uint32_t op,MilesWire::Call c,MilesHost::Resolver& r){
 MilesWire::Result out={};MilesHost::DispatchStatus status=MilesHost::dispatch(op,c,out,r);++touched[op];check(status==MilesHost::Complete,"dispatch complete");return out;
}
int main(int argc,char** argv){
 setvbuf(stdout,0,_IONBF,0);if(argc!=2)return 2;
 char dllpath[MAX_PATH]={};HMODULE dll=GetModuleHandleA("mss32.dll");if(!dll||!GetModuleFileNameA(dll,dllpath,MAX_PATH))return 3;printf("loaded_dll=%s\n",dllpath);
 FILE* f=0;if(fopen_s(&f,argv[1],"rb")||!f)return 4;fseek(f,0,SEEK_END);long length=ftell(f);rewind(f);
 if(length<=0||length>1024*1024){fclose(f);return 5;}std::vector<unsigned char> bytes(static_cast<size_t>(length));if(fread(&bytes[0],1,bytes.size(),f)!=bytes.size()){fclose(f);return 6;}fclose(f);
 if(!AIL_startup()){puts("BLOCKED startup");return 7;}
 HDIGDRIVER driver=AIL_open_digital_driver(22050,16,MSS_MC_STEREO,0);
 if(!driver){printf("BLOCKED driver: %s\n",AIL_last_error());AIL_shutdown();return 8;}
 HSAMPLE control=AIL_allocate_sample_handle(driver),candidate=AIL_allocate_sample_handle(driver);
 HSTREAM controlStream=0,candidateStream=0;int setupFailure=0;
 if(!control||!candidate)setupFailure=9;
 else if(!AIL_set_named_sample_file(control,".wav",&bytes[0],length,0)||!AIL_set_named_sample_file(candidate,".wav",&bytes[0],length,0))setupFailure=10;
 if(!setupFailure){controlStream=AIL_open_stream(driver,argv[1],0);candidateStream=AIL_open_stream(driver,argv[1],0);if(!controlStream||!candidateStream)setupFailure=11;}
 if(!setupFailure){
 MilesTransport::ResourceRegistry registry;MilesWire::Handle sample={},stream={};
 check(registry.insert(MilesWire::OwnedSample,candidate,sample),"register real sample");check(registry.insert(MilesWire::Stream,candidateStream,stream),"register real stream");MilesHost::RegistryResolver resolver(registry);
 MilesWire::Call call={};call.target=sample;
 for(unsigned j=0;j<2;++j){
 float left=j?.75f:.25f,right=j?.25f:.75f;AIL_set_sample_volume_levels(control,left,right);call.value[0]=fb(left);call.value[1]=fb(right);
 dispatch(MilesWire::AIL_set_sample_volume_levels,call,resolver);call.value[0]=call.value[1]=0;
 for(unsigned mask=0;mask<4;++mask){printf("CONTROL volume mask=%u\n",mask);float l=0,r=0;AIL_sample_volume_levels(control,(mask&1)?&l:0,(mask&2)?&r:0);call.output_mask=mask;MilesWire::Result out=dispatch(MilesWire::AIL_sample_volume_levels,call,resolver);
 printf("volume mask=%u expected=%08x,%08x observed=%08x,%08x\n",mask,fb(l),fb(r),out.value[0],out.value[1]);check(out.value[0]==fb(l)&&out.value[1]==fb(r),"volume bits and out presence");}call.output_mask=0;
 S32 rate=j?22050:11025;AIL_set_sample_playback_rate(control,rate);call.value[0]=sb(rate);dispatch(MilesWire::AIL_set_sample_playback_rate,call,resolver);call.value[0]=0;
 check(dispatch(MilesWire::AIL_sample_playback_rate,call,resolver).return_bits==sb(AIL_sample_playback_rate(control)),"real playback rate");
 S32 loops=j?3:1;AIL_set_sample_loop_count(control,loops);call.value[0]=sb(loops);dispatch(MilesWire::AIL_set_sample_loop_count,call,resolver);call.value[0]=0;printf("loop-count control=%ld candidate=%ld\n",AIL_sample_loop_count(control),AIL_sample_loop_count(candidate));check(AIL_sample_loop_count(control)==AIL_sample_loop_count(candidate),"real loop count effect");
 S32 start=j?128:0,end=j?1024:-1;AIL_set_sample_loop_block(control,start,end);call.value[0]=sb(start);call.value[1]=sb(end);dispatch(MilesWire::AIL_set_sample_loop_block,call,resolver);call.value[0]=call.value[1]=0;
 S32 ca=0,cb=0,da=0,db=0;S32 cr=AIL_sample_loop_block(control,&ca,&cb),dr=AIL_sample_loop_block(candidate,&da,&db);printf("loop-block control=%ld,%ld,%ld candidate=%ld,%ld,%ld\n",cr,ca,cb,dr,da,db);check(cr==dr&&ca==da&&cb==db,"real loop block effect");
 U32 pos=j?128:0;AIL_set_sample_position(control,pos);call.value[0]=pos;dispatch(MilesWire::AIL_set_sample_position,call,resolver);call.value[0]=0;check(dispatch(MilesWire::AIL_sample_position,call,resolver).return_bits==AIL_sample_position(control),"real byte position");
 S32 ms=j?10:0;AIL_set_sample_ms_position(control,ms);call.value[0]=sb(ms);dispatch(MilesWire::AIL_set_sample_ms_position,call,resolver);call.value[0]=0;
 for(unsigned mask=0;mask<4;++mask){printf("CONTROL sample-ms mask=%u\n",mask);S32 total=0,current=0;AIL_sample_ms_position(control,(mask&1)?&total:0,(mask&2)?&current:0);call.output_mask=mask;MilesWire::Result out=dispatch(MilesWire::AIL_sample_ms_position,call,resolver);check(out.value[0]==sb(total)&&out.value[1]==sb(current),"real sample ms and out presence");}call.output_mask=0;
 check(dispatch(MilesWire::AIL_sample_status,call,resolver).return_bits==AIL_sample_status(control),"quiescent sample status");
 }
 call.target=stream;check(dispatch(MilesWire::AIL_stream_status,call,resolver).return_bits==sb(AIL_stream_status(controlStream)),"quiescent stream status");
 for(unsigned mask=0;mask<4;++mask){printf("CONTROL stream-ms mask=%u\n",mask);S32 total=0,current=0;AIL_stream_ms_position(controlStream,(mask&1)?&total:0,(mask&2)?&current:0);call.output_mask=mask;MilesWire::Result out=dispatch(MilesWire::AIL_stream_ms_position,call,resolver);check(out.value[0]==sb(total)&&out.value[1]==sb(current),"real stream ms and out presence");}
 call= MilesWire::Call();call.target=sample;call.value[0]=fb(.5f);call.value[1]=fb(.5f);float l=0,r=0;AIL_sample_volume_levels(candidate,&l,&r);MilesWire::Result rejected={};++call.target.generation;
 check(MilesHost::dispatch(MilesWire::AIL_set_sample_volume_levels,call,rejected,resolver)==MilesHost::InvalidResource,"stale ID rejected");call.target=sample;call.value[7]=1;
 check(MilesHost::dispatch(MilesWire::AIL_set_sample_volume_levels,call,rejected,resolver)==MilesHost::InvalidFields,"unused field rejected");float afterL=0,afterR=0;AIL_sample_volume_levels(candidate,&afterL,&afterR);check(fb(l)==fb(afterL)&&fb(r)==fb(afterR),"rejected setters leave vendor volume intact");
 }
 if(candidateStream)AIL_close_stream(candidateStream);if(controlStream)AIL_close_stream(controlStream);
 if(candidate)AIL_release_sample_handle(candidate);if(control)AIL_release_sample_handle(control);
 AIL_close_digital_driver(driver);AIL_shutdown();puts("CLEANUP complete");
 unsigned arms=0;for(unsigned i=1;i<62;++i)if(touched[i]){++arms;printf("arm=%u calls=%u\n",i,touched[i]);}
 printf("%d/%d checks; %u distinct dispatched arms\n",checks-failures,checks,arms);
 return setupFailure?setupFailure:((failures||checks!=75||arms!=13)?1:0);
}
