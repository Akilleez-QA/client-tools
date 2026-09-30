#include "common.h"
#include "admission.h"
#include <memory>
#ifndef _WIN64
#include <Mss.h>
#include <xmmintrin.h>
#include "../host-candidate/host_dispatch.h"
#include "../host-candidate/registry_resolver.h"
#include "../host-candidate/retained_buffers.h"
#include "../buffer-upload-candidate/buffer_upload.h"
#endif
using namespace MilesWire;
static uint32_t floatBits(float v){uint32_t b;memcpy(&b,&v,4);return b;}
inline uint64_t incarnation(const std::string& n){uint64_t x=0;for(unsigned i=0;i<16;++i)x=(x<<4)|static_cast<uint64_t>(n[i]<='9'?n[i]-'0':n[i]-'a'+10);return x?x:1;}
inline bool zeroHandle(const Handle& h){return !h.kind&&!h.slot&&!h.generation;}
inline bool same(const Handle& a,const Handle& b){return a.kind==b.kind&&a.slot==b.slot&&a.generation==b.generation;}
inline std::vector<unsigned char> readFile(const char* name){FILE* f=0;require(!fopen_s(&f,name,"rb")&&f,"file open");fseek(f,0,SEEK_END);long n=ftell(f);rewind(f);require(n==9020,"known PCM size");std::vector<unsigned char>b(static_cast<size_t>(n));require(fread(&b[0],1,b.size(),f)==b.size(),"file read");fclose(f);return b;}
#ifndef _WIN64
static bool knownPcm(const std::vector<unsigned char>& b){
 HCRYPTPROV p=0;HCRYPTHASH h=0;require(CryptAcquireContextA(&p,0,0,PROV_RSA_AES,CRYPT_VERIFYCONTEXT)!=0,"sha provider");
 require(CryptCreateHash(p,CALG_SHA_256,0,0,&h)!=0,"sha hash");require(CryptHashData(h,&b[0],static_cast<DWORD>(b.size()),0)!=0,"sha data");
 unsigned char d[32];DWORD n=32;require(CryptGetHashParam(h,HP_HASHVAL,d,&n,0)!=0,"sha result");CryptDestroyHash(h);CryptReleaseContext(p,0);
 const char* expected="ad880479382433a16f99e60d5d5248c30446a44ccc692bfaabb1d012c607a7a9";const char hex[]="0123456789abcdef";
 for(unsigned i=0;i<32;++i)if(hex[d[i]>>4]!=expected[2*i]||hex[d[i]&15]!=expected[2*i+1])return false;return true;
}
struct Backend {
 MilesTransport::ResourceRegistry registry;MilesHost::RegistryResolver resolver;MilesHost::RetainedBuffers retained;
 std::unique_ptr<MilesHost::BufferUpload> upload;Handle driverId,sampleId,bufferId,controlId;
 HDIGDRIVER driver;HSAMPLE sample,control;bool started,bound,attempted,shutdown;
 Backend():resolver(registry),retained(32768,1),driver(0),sample(0),control(0),started(false),bound(false),attempted(false),shutdown(false){driverId=sampleId=bufferId=controlId=Handle();}
 // Emergency cleanup is deliberately not counted as a successful ordered shutdown.
 ~Backend(){if(started){if(sample)::AIL_release_sample_handle(sample);if(control)::AIL_release_sample_handle(control);::AIL_shutdown();puts("FAIL emergency vendor cleanup");}}
 Result execute(uint32_t op,const Call& c,const std::vector<unsigned char>& frame){
 Result r={};r.transport_status=3;
 if(c.callback||c.reserved)return r;
 unsigned values=0;bool target=false,resource=false,text=false,payload=false;
 switch(op){case MilesWire::AIL_open_digital_driver:values=4;break;case BufferBegin:values=1;break;case BufferChunk:values=1;target=true;payload=true;break;case BufferSeal:case BufferRelease:case MilesWire::AIL_allocate_sample_handle:case MilesWire::AIL_release_sample_handle:case MilesWire::AIL_end_sample:target=true;break;case MilesWire::AIL_set_named_sample_file:target=resource=text=true;values=2;break;case MilesWire::AIL_set_sample_volume_levels:target=true;values=2;break;case MilesWire::AIL_set_sample_playback_rate:target=true;values=1;break;case MilesWire::AIL_sample_volume_levels:case MilesWire::AIL_sample_playback_rate:case MilesWire::AIL_sample_ms_position:target=true;break;case MilesWire::AIL_startup:case MilesWire::AIL_shutdown:case SessionClose:break;default:r.transport_status=1;return r;}
 for(unsigned i=values;i<8;++i)if(c.value[i])return r;
 if((!target&&!zeroHandle(c.target))||(!resource&&!zeroHandle(c.resource))||(!text&&c.text.length)||(!payload&&c.bytes.length))return r;
 const bool outputs=op==MilesWire::AIL_sample_volume_levels||op==MilesWire::AIL_sample_ms_position;
 if(c.output_mask&~(outputs?3u:0u))return r;
 r.transport_status=4;
 if(op==MilesWire::AIL_startup){if(started||shutdown)return r;S32 v=::AIL_startup();r.return_bits=static_cast<uint32_t>(v);r.transport_status=0;started=v!=0;printf("vendor startup=%ld\n",v);return r;}
 if(op==SessionClose){if(!shutdown||started||sample||control||upload)return r;r.transport_status=0;return r;}
 if(!started||shutdown)return r;
 if(op==MilesWire::AIL_open_digital_driver){if(driver||c.value[0]!=22050||c.value[1]!=16||c.value[2]!=2||c.value[3])return r;driver=::AIL_open_digital_driver(c.value[0],16,MSS_MC_STEREO,0);if(driver)require(registry.insert(Driver,driver,driverId),"register driver");r.resource=driverId;r.transport_status=0;printf("vendor driver_nonnull=%u\n",driver?1:0);return r;}
 if(op==MilesWire::AIL_allocate_sample_handle){if(!driver||sample)return r;void* p=0;if(!registry.resolve(c.target,Driver,p)){r.transport_status=2;return r;}sample=::AIL_allocate_sample_handle(driver);if(sample)require(registry.insert(OwnedSample,sample,sampleId),"register sample");r.resource=sampleId;r.transport_status=0;return r;}
 if(op==BufferBegin){if(upload||c.value[0]!=9020||c.value[0]*3u+5u>32768u)return r;upload.reset(new MilesHost::BufferUpload(c.value[0],9020));require(registry.insert(Buffer,upload.get(),bufferId),"register upload");r.resource=bufferId;r.transport_status=0;return r;}
 if(op==BufferChunk||op==BufferSeal||op==BufferRelease){void* p=0;if(!registry.resolve(c.target,Buffer,p)){r.transport_status=2;return r;}
  if(op==BufferChunk){if(!upload->append(c.value[0],&frame[c.bytes.offset],c.bytes.length)){r.transport_status=3;return r;}}
  if(op==BufferSeal&&!upload->seal()){r.transport_status=3;return r;}
  if(op==BufferRelease){if(sample||control)return r;require(registry.retire(bufferId),"retire buffer");upload.reset();}r.transport_status=0;return r;}
 if(op==MilesWire::AIL_shutdown){if(sample||control||upload)return r;::AIL_shutdown();started=false;shutdown=true;if(driver){require(registry.retire(driverId),"retire driver");driver=0;}retained.deactivate();puts("vendor shutdown complete; retained image still alive");r.transport_status=0;return r;}
 void* p=0;if(!registry.resolve(c.target,OwnedSample,p)||!same(c.target,sampleId)){r.transport_status=2;return r;}
 if(op==MilesWire::AIL_set_named_sample_file){void* buffer=0;if(!registry.resolve(c.resource,Buffer,buffer)){r.transport_status=2;return r;}
  if(attempted||c.value[0]!=9020||c.value[1]||c.text.length!=5||memcmp(&frame[c.text.offset],".wav",5))return r;
  std::vector<unsigned char> sealed;if(!upload->copySealed(sealed)||!knownPcm(sealed))return r;attempted=true;
  MilesHost::RetainedBuffers::Token token=0;require(retained.stage(MilesHost::RetainedBuffers::Binary,&sealed[0],sealed.size(),0,sealed.size(),token),"retain image");MilesHost::RetainedBuffers::View view;require(retained.view(token,view),"view retained image");
  control=::AIL_allocate_sample_handle(driver);require(control!=0&&registry.insert(OwnedSample,control,controlId),"direct control allocate");
  S32 expected=::AIL_set_named_sample_file(control,".wav",view.data,view.size,0);require(expected!=0,"direct control bind");
  S32 actual=::AIL_set_named_sample_file(sample,".wav",view.data,view.size,0);r.return_bits=static_cast<uint32_t>(actual);r.transport_status=0;bound=actual!=0;if(bound)require(retained.commit(token),"publish binding");printf("vendor bind direct=%ld framed=%ld\n",expected,actual);return r;
 }
 if(op==MilesWire::AIL_release_sample_handle){if(sample){::AIL_release_sample_handle(sample);sample=0;require(registry.retire(sampleId),"retire sample");}if(control){::AIL_end_sample(control);::AIL_release_sample_handle(control);control=0;require(registry.retire(controlId),"retire control");}bound=false;r.transport_status=0;puts("vendor sample release complete; bytes retained");return r;}
 if(!bound)return r;
 if(op==MilesWire::AIL_set_sample_volume_levels){float l=0,rr=0;memcpy(&l,&c.value[0],4);memcpy(&rr,&c.value[1],4);::AIL_set_sample_volume_levels(control,l,rr);}
 if(op==MilesWire::AIL_set_sample_playback_rate)::AIL_set_sample_playback_rate(control,static_cast<S32>(c.value[0]));
 MilesHost::DispatchStatus status=MilesHost::dispatch(op,c,r,resolver);if(status!=MilesHost::Complete)return r;
 if(op==MilesWire::AIL_sample_volume_levels){float l=0,rr=0;::AIL_sample_volume_levels(control,(c.output_mask&1)?&l:0,(c.output_mask&2)?&rr:0);if(r.value[0]!=floatBits(l)||r.value[1]!=floatBits(rr))r.transport_status=5;printf("vendor volume direct=%08x,%08x framed=%08x,%08x\n",floatBits(l),floatBits(rr),r.value[0],r.value[1]);}
 if(op==MilesWire::AIL_sample_ms_position){S32 total=0,current=0;::AIL_sample_ms_position(control,(c.output_mask&1)?&total:0,(c.output_mask&2)?&current:0);if(r.value[0]!=static_cast<uint32_t>(total)||r.value[1]!=static_cast<uint32_t>(current))r.transport_status=5;printf("vendor duration direct=%ld,%ld framed=%u,%u\n",total,current,r.value[0],r.value[1]);}
 if(op==MilesWire::AIL_sample_playback_rate){S32 rate=::AIL_sample_playback_rate(control);if(r.return_bits!=static_cast<uint32_t>(rate))r.transport_status=5;printf("vendor rate direct=%ld framed=%u\n",rate,r.return_bits);}
 return r;
 }
};
#endif
#ifndef _WIN64
static int host(int argc,char** argv){
 require(argc==6,"host arguments");FILE* log=0;require(!freopen_s(&log,"host.log","w",stdout),"host log");setvbuf(stdout,0,_IONBF,0);
 char loaded[MAX_PATH]={};require(GetModuleFileNameA(GetModuleHandleA("mss32.dll"),loaded,MAX_PATH)!=0,"loaded original DLL");printf("loaded_dll=%s\n",loaded);
 unsigned short cw=0;__asm fnstcw cw
 printf("entry cw=%04x mxcsr=%08x\n",cw,_mm_getcsr());
 HANDLE a=CreateFileA(argv[2],GENERIC_READ|GENERIC_WRITE,0,0,OPEN_EXISTING,FILE_FLAG_OVERLAPPED,0);require(a!=INVALID_HANDLE_VALUE,"host command pipe");
 HANDLE b=CreateFileA(argv[3],GENERIC_READ|GENERIC_WRITE,0,0,OPEN_EXISTING,FILE_FLAG_OVERLAPPED,0);require(b!=INVALID_HANDLE_VALUE,"host callback pipe");
 ULONG parent=0;BOOL identified=GetNamedPipeServerProcessId(a,&parent);if(identified)require(parent==strtoul(argv[5],0,10),"server PID binding");else printf("LIMIT server PID query unavailable error=%lu\n",GetLastError());
 Endpoint cmd(a,17),cb(b,19);Backend backend;std::string nonceText=argv[4];MilesCoordinator::Coordinator coordinator(incarnation(nonceText));uint64_t last=0,admission=0;bool hello=false,done=false;
 while(!done){std::vector<unsigned char> frame=receive(cmd,&cb),unexpected;require(!cb.takeFrame(unexpected),"no callbacks enabled");Header h={};Call c={};require(MilesTransport::decodeCall(bytes(frame),h,c),"decode request");require(h.kind==Request&&h.request==last+1&&h.lane==1&&!h.lock_lease&&!h.causal_request,"request correlation/lane");last=h.request;Result result={};
 if(!hello){require(h.opcode==Hello&&c.bytes.length==32&&!c.text.length&&zeroHandle(c.target)&&zeroHandle(c.resource)&&!c.output_mask&&!c.callback&&!c.reserved,"hello shape");for(unsigned i=0;i<8;++i)require(!c.value[i],"hello values");require(!memcmp(&frame[c.bytes.offset],nonceText.data(),32),"full nonce handshake");hello=true;}
 else {
  bool live=true;std::vector<Handle> resources;if(!zeroHandle(c.target)){void* local=0;live=backend.registry.resolve(c.target,static_cast<ResourceKind>(c.target.kind),local);resources.push_back(c.target);}if(!zeroHandle(c.resource)){void* local=0;live=live&&backend.registry.resolve(c.resource,static_cast<ResourceKind>(c.resource.kind),local);resources.push_back(c.resource);}
  if(!live)result.transport_status=2;
  else {
   MilesCoordinator::Error admitted=LiveBridge::admitNext(coordinator,incarnation(nonceText),admission,h.opcode,resources);
   if(admitted!=MilesCoordinator::Ok)result.transport_status=4;
   else { result=backend.execute(h.opcode,c,frame);require(LiveBridge::complete(coordinator,incarnation(nonceText),admission,h.opcode,result.transport_status)==MilesCoordinator::Ok,"observed operation return"); }}
 }
 Header reply=h;reply.kind=Reply;std::vector<unsigned char> encoded;require(MilesTransport::encodeResult(reply,result,MilesTransport::Bytes(),MilesTransport::Bytes(),encoded),"encode result");require(cmd.send(bytes(encoded)),"send reply");sent(cmd);
 printf("request=%I64u opcode=%u transport=%u vendor=%u\n",h.request,h.opcode,result.transport_status,result.return_bits);done=h.opcode==SessionClose&&result.transport_status==0;
 }
 drainSession(cmd,cb,true);puts("PASS host ordered shutdown; no callback registrations");return 0;
}
#else
struct Client {
private:
 Client& operator=(const Client&);
public:
 Endpoint& cmd;Endpoint& cb;uint64_t next;unsigned checks;
 Client(Endpoint& a,Endpoint& b):cmd(a),cb(b),next(0),checks(0){}
 Result call(uint32_t op,const Call& c=Call(),MilesTransport::Bytes payload=MilesTransport::Bytes(),MilesTransport::Bytes text=MilesTransport::Bytes(),uint32_t expected=0){
 Header h={};h.magic=Magic;h.version=Version;h.kind=Request;h.opcode=op;h.request=++next;h.lane=1;std::vector<unsigned char> frame;require(MilesTransport::encodeCall(h,c,payload,text,frame),"encode call");require(cmd.send(bytes(frame)),"send call");frame=receive(cmd,&cb,op==SessionClose);std::vector<unsigned char> unexpected;require(!cb.takeFrame(unexpected),"no callback traffic");Header response={};Result r={};require(MilesTransport::decodeResult(bytes(frame),response,r),"decode reply");require(response.kind==Reply&&response.request==next&&response.opcode==op&&response.lane==1&&!response.causal_request&&!response.lock_lease,"reply correlation");require(r.transport_status==expected,"transport result");++checks;return r;
 }
};
static int controller(int argc,char** argv){
 require(argc==3,"controller arguments");std::vector<unsigned char> image=readFile(argv[2]);std::string random=nonce(),base="\\\\.\\pipe\\swg-live-"+random,commandName=base+"-cmd",callbackName=base+"-cb";
 PSECURITY_DESCRIPTOR sd=userDescriptor();SECURITY_ATTRIBUTES sa={sizeof sa,sd,FALSE};ServerPipe a(commandName,sa),b(callbackName,sa);LocalFree(sd);
 char pid[32];sprintf_s(pid,"%lu",GetCurrentProcessId());std::string args="\""+std::string(argv[1])+"\" --host "+commandName+" "+callbackName+" "+random+" "+pid;std::vector<char> line(args.begin(),args.end());line.push_back(0);
 ChildProcess child;child.create(argv[1],&line[0]);child.assignAndResume(child.job);
 try{
 a.connected();b.connected();ULONG actual=0;require(GetNamedPipeClientProcessId(a.pipe,&actual)&&actual==child.info.dwProcessId,"child command PID binding");require(GetNamedPipeClientProcessId(b.pipe,&actual)&&actual==child.info.dwProcessId,"child callback PID binding");Endpoint cmd(a.take(),23),cb(b.take(),29);Client client(cmd,cb);client.call(Hello,Call(),MilesTransport::Bytes(random.data(),random.size()));Result r=client.call(MilesWire::AIL_startup);require(r.return_bits!=0,"real startup prerequisite");
 Call c={};c.value[0]=22050;c.value[1]=16;c.value[2]=2;r=client.call(MilesWire::AIL_open_digital_driver,c);Handle driver=r.resource;require(driver.kind==Driver&&driver.slot,"real driver prerequisite");c=Call();c.target=driver;r=client.call(MilesWire::AIL_allocate_sample_handle,c);Handle sample=r.resource;require(sample.kind==OwnedSample&&sample.slot,"real sample prerequisite");
 c=Call();c.value[0]=9020;r=client.call(BufferBegin,c);Handle upload=r.resource;c=Call();c.target=upload;client.call(BufferChunk,c,bytes(image));client.call(BufferSeal,c);
 c=Call();c.target=sample;c.resource=upload;c.value[0]=9020;r=client.call(MilesWire::AIL_set_named_sample_file,c,MilesTransport::Bytes(),MilesTransport::Bytes(".wav",5));require(r.return_bits!=0,"genuine bind success");
 c=Call();c.target=sample;c.output_mask=3;r=client.call(MilesWire::AIL_sample_ms_position,c);require(r.value[0]>0&&r.value[1]==0,"image-derived duration before playback");printf("initial duration=%u current=%u\n",r.value[0],r.value[1]);c.output_mask=0;r=client.call(MilesWire::AIL_sample_playback_rate,c);require(r.return_bits==22050,"original rate");
 c.value[0]=floatBits(.25f);c.value[1]=floatBits(.75f);client.call(MilesWire::AIL_set_sample_volume_levels,c);c.value[0]=c.value[1]=0;c.output_mask=3;r=client.call(MilesWire::AIL_sample_volume_levels,c);require(r.value[0]==floatBits(.25f)&&r.value[1]==floatBits(.75f),"real framed volume");
 c.output_mask=0;c.value[0]=11025;client.call(MilesWire::AIL_set_sample_playback_rate,c);c.value[0]=0;r=client.call(MilesWire::AIL_sample_playback_rate,c);require(r.return_bits==11025,"real framed rate");c.output_mask=3;client.call(MilesWire::AIL_sample_ms_position,c);c.output_mask=0;
 client.call(MilesWire::AIL_end_sample,c);client.call(MilesWire::AIL_release_sample_handle,c);client.call(MilesWire::AIL_sample_playback_rate,c,MilesTransport::Bytes(),MilesTransport::Bytes(),2);
 c=Call();c.target=upload;client.call(BufferRelease,c);client.call(MilesWire::AIL_shutdown);client.call(SessionClose);
 require(client.checks==21,"exact request count");drainSession(cmd,cb,true);require(WaitForSingleObject(child.info.hProcess,10000)==WAIT_OBJECT_0,"host exit wait");DWORD exitCode=99;require(GetExitCodeProcess(child.info.hProcess,&exitCode)&&exitCode==0,"host clean exit");child.close();printf("PASS 21 framed requests; real64to32 no-playback slice\n");return 0;
 }catch(...){throw;}
}
#endif
int main(int argc,char** argv){setvbuf(stdout,0,_IONBF,0);try{
#ifdef _WIN64
return controller(argc,argv);
#else
return host(argc,argv);
#endif
}catch(const std::exception& e){printf("FAIL exception=%s\n",e.what());return 1;}}
