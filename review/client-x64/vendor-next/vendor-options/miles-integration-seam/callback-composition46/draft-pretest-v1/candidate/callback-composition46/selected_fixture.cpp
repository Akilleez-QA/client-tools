// Test callbacks only. Production retain/Invocation/owner/mapper remain real.
#include "selected_fixture.h"
#include <stdexcept>
namespace Script36 {
ClientAudioFileCallbacks::OpenResult open(const char *);
void close(ClientAudioFileCallbacks::LocalFileHandle);
int32_t seek(ClientAudioFileCallbacks::LocalFileHandle,int32_t,uint32_t);
uint32_t read(ClientAudioFileCallbacks::LocalFileHandle,void *,uint32_t);
}
namespace Script46 {
unsigned opensB=0,closesB=0,seeksB=0,readsB=0;
namespace {
uint32_t openA(const char *name,ClientMiles::FileHandle *handle) {
    const ClientAudioFileCallbacks::OpenResult r=Script36::open(name);
    *handle=r.handle.value;return r.callbackResult;
}
void closeA(ClientMiles::FileHandle handle) {Script36::close(ClientAudioFileCallbacks::LocalFileHandle{handle});}
int32_t seekA(ClientMiles::FileHandle handle,int32_t offset,uint32_t origin) {
    return Script36::seek(ClientAudioFileCallbacks::LocalFileHandle{handle},offset,origin);
}
uint32_t readA(ClientMiles::FileHandle handle,void *buffer,uint32_t n) {
    return Script36::read(ClientAudioFileCallbacks::LocalFileHandle{handle},buffer,n);
}
const ClientMiles::FileHandle otherHandle=static_cast<ClientMiles::FileHandle>(UINT64_C(0x100000007));
void checkB(ClientMiles::FileHandle h) {if(h!=otherHandle)throw std::runtime_error("B local handle mismatch");}
uint32_t openB(const char *,ClientMiles::FileHandle *h) {++opensB;*h=otherHandle;return UINT32_C(0x80000001);}
void closeB(ClientMiles::FileHandle h) {checkB(h);++closesB;}
int32_t seekB(ClientMiles::FileHandle h,int32_t,uint32_t) {checkB(h);++seeksB;return INT32_MIN;}
uint32_t readB(ClientMiles::FileHandle h,void *p,uint32_t n) {
    checkB(h);++readsB;for(uint32_t i=0;i<n;++i)static_cast<unsigned char *>(p)[i]=static_cast<unsigned char>(0xa0+i);return n;
}
}
MilesFileChannel26::FileServices selected(bool alternate,std::shared_ptr<void> pin) {
    return alternate?MilesSelectedFileServices44::retain(&openB,&closeB,&seekB,&readB,pin)
                    :MilesSelectedFileServices44::retain(&openA,&closeA,&seekA,&readA,pin);
}
}
