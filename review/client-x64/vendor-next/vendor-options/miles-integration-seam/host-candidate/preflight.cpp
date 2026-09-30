#include "registry_resolver.h"
#include <windows.h>
#include <stdio.h>
#include <string.h>
static int checks=0;
static bool check(uint32_t opcode,MilesWire::Call const &call,MilesHost::DispatchStatus expected,MilesHost::Resolver &resolver){
 MilesWire::Result result;memset(&result,0xa5,sizeof(result));
 MilesHost::DispatchStatus status=MilesHost::dispatch(opcode,call,result,resolver);
 MilesWire::Result zero={};zero.transport_status=static_cast<uint32_t>(expected);
 if(status!=expected || memcmp(&result,&zero,sizeof(result)))return false;
 ++checks;return true;
}
int main(){
 if(GetModuleHandleA("mss32.dll"))return 10;
 MilesTransport::ResourceRegistry registry;MilesHost::RegistryResolver resolver(registry);
 MilesWire::Call call={};
 if(!check(0xffffffffu,call,MilesHost::Unsupported,resolver))return 1;
 if(!check(MilesWire::AIL_lock,call,MilesHost::Unsupported,resolver))return 2;
 if(!check(MilesWire::AIL_sample_status,call,MilesHost::InvalidResource,resolver))return 3;
 call.target.kind=MilesWire::OwnedSample;call.target.slot=1;call.target.generation=1;
 if(!check(MilesWire::AIL_sample_status,call,MilesHost::InvalidResource,resolver))return 4;
 call.bytes.offset=1;
 if(!check(MilesWire::AIL_sample_status,call,MilesHost::InvalidFields,resolver))return 5;
 call.bytes.offset=0;call.text.offset=1;
 if(!check(MilesWire::AIL_sample_status,call,MilesHost::InvalidFields,resolver))return 6;
 call.text.offset=0;call.value[7]=1;
 if(!check(MilesWire::AIL_sample_status,call,MilesHost::InvalidFields,resolver))return 7;
 call.value[7]=0;call.output_mask=4;
 if(!check(MilesWire::AIL_sample_reverb_levels,call,MilesHost::InvalidFields,resolver))return 8;
 // Ordinary marker addresses are registry data only; never passed to the SDK.
 int streamMarker=0,sampleMarker=0;
 MilesWire::Handle stream={},alias={},sameAlias={};
 if(!registry.insert(MilesWire::Stream,&streamMarker,stream))return 20;++checks;
 if(!registry.insertBorrowed(stream,&sampleMarker,alias))return 21;++checks;
 if(!registry.insertBorrowed(stream,&sampleMarker,sameAlias) || memcmp(&alias,&sameAlias,sizeof(alias)))return 22;++checks;
 uintptr_t resolved=0;
 if(!resolver.resolve(alias,1u<<MilesWire::BorrowedSample,resolved) || resolved!=reinterpret_cast<uintptr_t>(&sampleMarker))return 23;++checks;
 if(resolver.resolve(alias,1u<<MilesWire::OwnedSample,resolved) || resolved)return 24;++checks;
 call=MilesWire::Call();call.target=alias;
 if(!check(MilesWire::AIL_start_sample,call,MilesHost::InvalidResource,resolver))return 25;
 const uint32_t borrowedOps[]={MilesWire::AIL_set_sample_volume_levels,MilesWire::AIL_set_sample_reverb_levels,MilesWire::AIL_set_sample_playback_rate,MilesWire::AIL_sample_volume_levels,MilesWire::AIL_sample_playback_rate};
 call.value[7]=1;
 for(unsigned i=0;i<5;++i)if(!check(borrowedOps[i],call,MilesHost::InvalidFields,resolver))return 26;
 if(!registry.beginClose(stream))return 27;++checks;
 if(resolver.resolve(alias,1u<<MilesWire::BorrowedSample,resolved) || resolved)return 28;++checks;
 call.value[7]=0;
 for(unsigned i=0;i<5;++i)if(!check(borrowedOps[i],call,MilesHost::InvalidResource,resolver))return 29;
 if(!registry.retire(stream))return 30;++checks;
 if(resolver.resolve(alias,1u<<MilesWire::BorrowedSample,resolved) || resolved)return 31;++checks;
 if(GetModuleHandleA("mss32.dll"))return 11;
 printf("PASS %d rejection/status checks; original vendor DLL not loaded\n",checks);return 0;
}
