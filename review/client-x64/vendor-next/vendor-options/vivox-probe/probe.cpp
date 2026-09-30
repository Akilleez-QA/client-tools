#include <windows.h>
#include <cstdio>
#include <cstring>
#include "Vxc.h"
#include "VxcRequests.h"
char const *names[]={
#include "exports.inc"
};
int main() {
 std::setvbuf(stdout,0,_IONBF,0);HMODULE dll=LoadLibraryA("vivoxsdk.dll");if(!dll){printf("load=failed error=%lu pointer_bits=%u\n",GetLastError(),unsigned(sizeof(void*)*8));return 2;}
 unsigned count=0,missing=0;for(unsigned i=0;i<sizeof(names)/sizeof(names[0]);++i){bool ok=GetProcAddress(dll,names[i])!=0;++count;if(!ok)++missing;printf("export=%s resolved=%d\n",names[i],ok);}
#define BIND(f) decltype(&f) p_##f=reinterpret_cast<decltype(&f)>(GetProcAddress(dll,#f));if(!p_##f)return 3;
 BIND(vx_strdup);BIND(vx_free);BIND(vx_req_aux_get_render_devices_create);BIND(destroy_req);
 char *s=p_vx_strdup("local-lifecycle-probe");if(!s||strcmp(s,"local-lifecycle-probe"))return 4;p_vx_free(s);
 vx_req_aux_get_render_devices_t *request=0;p_vx_req_aux_get_render_devices_create(&request);if(!request)return 5;
 printf("request-type=%d expected=%d\n",int(request->base.type),int(req_aux_get_render_devices));bool valid=request->base.type==req_aux_get_render_devices;p_destroy_req(&request->base);
 printf("exports=%u missing=%u local_lifecycle=%d pointer_bits=%u no_request_issued=1\n",count,missing,valid,unsigned(sizeof(void*)*8));FreeLibrary(dll);return missing||!valid?6:0;
}
