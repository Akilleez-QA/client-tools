#include "metadata.h"
#include "../host-candidate/registry_resolver.h"
#include <Mss.h>
#include <windows.h>
#include <cstdio>
#include <cstring>
static unsigned checks,failures;
static void check(bool value,int line){++checks;if(!value){++failures;printf("FAIL line %d\n",line);}}
#define CHECK(x) check(!!(x),__LINE__)
struct Session {
 bool started,saved;SINTa preference;
 Session():started(false),saved(false),preference(0){}
 ~Session(){if(saved)::AIL_set_preference(DIG_DS_MIX_FRAGMENT_CNT,preference);if(started)::AIL_shutdown();puts("CLEANUP restored preference and shutdown");}
};
int main() {
 using namespace MilesStartup;setvbuf(stdout,0,_IONBF,0);
 char loaded[MAX_PATH]={};GetModuleFileNameA(GetModuleHandleA("mss32.dll"),loaded,MAX_PATH);printf("loaded_dll=%s\n",loaded);
 Session session;
 try {
  MilesTransport::ResourceRegistry registry;MilesHost::RegistryResolver resolver(registry);
  Reply direct,reply;MilesWire::Call c={};const char path[]="miles";
  ::AIL_set_redist_directory(path);CHECK(copyText(::AIL_set_redist_directory(path),direct));
  c.text.length=sizeof path;CHECK(dispatch(MilesWire::AIL_set_redist_directory,c,MilesTransport::Bytes(path,sizeof path),reply,resolver)==Complete);
  CHECK(reply.result.null_mask==direct.result.null_mask&&reply.text==direct.text);printf("redist owned bytes=%u null=%u\n",static_cast<unsigned>(reply.text.size()),reply.result.null_mask);
  session.started=::AIL_startup()!=0;CHECK(session.started);if(!session.started)return 1;
  session.preference=::AIL_get_preference(DIG_DS_MIX_FRAGMENT_CNT);session.saved=true;
  c=MilesWire::Call();c.value[0]=DIG_MIXER_CHANNELS;SINTa mixer=::AIL_get_preference(DIG_MIXER_CHANNELS);
  CHECK(dispatch(MilesWire::AIL_get_preference,c,MilesTransport::Bytes(),reply,resolver)==Complete);
  CHECK(signedValue(reply.result.return_bits)==static_cast<int64_t>(mixer));printf("mixer=%I64d\n",signedValue(reply.result.return_bits));
  c.value[0]=DIG_DS_MIX_FRAGMENT_CNT;CHECK(dispatch(MilesWire::AIL_get_preference,c,MilesTransport::Bytes(),reply,resolver)==Complete);
  CHECK(signedValue(reply.result.return_bits)==static_cast<int64_t>(session.preference));
  ::AIL_set_error("metadata control");CHECK(copyText(::AIL_last_error(),direct));c=MilesWire::Call();
  CHECK(dispatch(MilesWire::AIL_last_error,c,MilesTransport::Bytes(),reply,resolver)==Complete);
  CHECK(reply.text==direct.text&&reply.result.null_mask==direct.result.null_mask);
  ::AIL_set_error("");CHECK(reply.text.size()==17&&!std::memcmp(&reply.text[0],"metadata control",17));
  CHECK(dispatch(MilesWire::AIL_last_error,c,MilesTransport::Bytes(),reply,resolver)==Complete);
  CHECK(reply.text.size()==1&&!reply.text[0]&&!reply.result.null_mask);
  const SINTa values[]={16,64};
  for(unsigned i=0;i<2;++i) {
   SINTa old=::AIL_get_preference(DIG_DS_MIX_FRAGMENT_CNT);SINTa prior=::AIL_set_preference(DIG_DS_MIX_FRAGMENT_CNT,values[i]);::AIL_set_preference(DIG_DS_MIX_FRAGMENT_CNT,old);
   c=MilesWire::Call();c.value[0]=DIG_DS_MIX_FRAGMENT_CNT;c.value[1]=static_cast<uint32_t>(values[i]);
   CHECK(dispatch(MilesWire::AIL_set_preference,c,MilesTransport::Bytes(),reply,resolver)==Complete);
   CHECK(signedValue(reply.result.return_bits)==static_cast<int64_t>(prior));
   CHECK(::AIL_get_preference(DIG_DS_MIX_FRAGMENT_CNT)==values[i]);printf("fragment requested=%ld actual=%I64d previous=%I64d\n",static_cast<long>(values[i]),static_cast<int64_t>(::AIL_get_preference(DIG_DS_MIX_FRAGMENT_CNT)),signedValue(reply.result.return_bits));
  }
  SINTa unchanged=::AIL_get_preference(DIG_DS_MIX_FRAGMENT_CNT);c.value[1]=0xffffffffu;
  CHECK(dispatch(MilesWire::AIL_set_preference,c,MilesTransport::Bytes(),reply,resolver)==InvalidFields);
  CHECK(::AIL_get_preference(DIG_DS_MIX_FRAGMENT_CNT)==unchanged);
  c=MilesWire::Call();c.value[0]=999;CHECK(dispatch(MilesWire::AIL_get_preference,c,MilesTransport::Bytes(),reply,resolver)==InvalidFields);
  c=MilesWire::Call();c.output_mask=24;CHECK(dispatch(MilesWire::AIL_speaker_configuration,c,MilesTransport::Bytes(),reply,resolver)==InvalidFields);
  c.output_mask=8;CHECK(dispatch(MilesWire::AIL_speaker_configuration,c,MilesTransport::Bytes(),reply,resolver)==InvalidResource);
  HDIGDRIVER driver=::AIL_open_digital_driver(22050,16,MSS_MC_STEREO,0);CHECK(driver!=0);if(!driver)return 1;
  MilesWire::Handle id={};CHECK(registry.insert(MilesWire::Driver,driver,id));
  MSS_MC_SPEC spec=MSS_MC_MONO;::AIL_speaker_configuration(driver,0,0,0,&spec);
  c=MilesWire::Call();c.target=id;c.output_mask=8;
  CHECK(dispatch(MilesWire::AIL_speaker_configuration,c,MilesTransport::Bytes(),reply,resolver)==Complete);
  CHECK(spec==MSS_MC_STEREO&&reply.result.value[3]==static_cast<uint32_t>(spec));
  CHECK(!reply.result.value[0]&&!reply.result.value[1]&&!reply.result.value[2]&&!reply.result.return_bits&&reply.text.empty());
  printf("speaker direct=%ld candidate=%u; initial sentinels mono/51-discrete\n",static_cast<long>(spec),reply.result.value[3]);
  ::AIL_set_preference(DIG_DS_MIX_FRAGMENT_CNT,session.preference);
  CHECK(::AIL_get_preference(DIG_DS_MIX_FRAGMENT_CNT)==session.preference);
  printf("%u/%u genuine metadata checks; same-vendor oracle, no playback\n",checks-failures,checks);
  return failures||checks!=31?1:0;
 }catch(...){puts("FAIL exception; normal scope cleanup follows");return 1;}
}
