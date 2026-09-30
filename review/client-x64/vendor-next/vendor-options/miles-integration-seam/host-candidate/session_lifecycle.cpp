#include "session_lifecycle.h"
#include <windows.h>
#include "Mss.h"
#include <new>
#include <stdexcept>
#if !defined(_M_IX86) || _MSC_VER != 1800
#error Original Miles lifecycle candidate requires native v120 x86
#endif
namespace MilesHost {
namespace {
void clear(MilesWire::Handle &h) { h.kind=h.slot=h.generation=0; }
bool same(const MilesWire::Handle &a,const MilesWire::Handle &b) {
    return a.kind==b.kind && a.slot==b.slot && a.generation==b.generation;
}
}
SessionLifecycle::SessionLifecycle(uint32_t limit)
    :registry(limit),thread(GetCurrentThreadId()),started(false) {}
SessionLifecycle::~SessionLifecycle() {} // Explicit shutdown is a required precondition.
bool SessionLifecycle::onThread() const { return thread==GetCurrentThreadId(); }
bool SessionLifecycle::reserveRecord() {
    try { records.reserve(records.size()+1); }
    catch(const std::bad_alloc &) { return false; }
    catch(const std::length_error &) { return false; }
    return true;
}
SessionLifecycle::Status SessionLifecycle::startup(int32_t &result) {
    result=0;
    if(!onThread())return WrongThread;
    if(started)return AlreadyStarted;
    result=::AIL_startup();
    started=result!=0;
    return Ok; // Genuine startup failure is represented by result, not transport status.
}
SessionLifecycle::Status SessionLifecycle::openDriver(uint32_t frequency,int32_t bits,
        int32_t channels,uint32_t flags,MilesWire::Handle &out) {
    clear(out);
    if(!onThread())return WrongThread;
    if(!started)return NotStarted;
    if(!reserveRecord())return StorageFailure;
    HDIGDRIVER driver=::AIL_open_digital_driver(frequency,bits,channels,flags);
    if(!driver)return Ok; // Genuine vendor null, distinct from registry refusal.
    Record record={};record.native=driver;record.sample=false;
    try {
        if(!registry.insert(MilesWire::Driver,driver,record.handle)) {
            ::AIL_close_digital_driver(driver);return CapacityFailure;
        }
    } catch(...) { ::AIL_close_digital_driver(driver);throw; }
    records.push_back(record); // Reserved storage and trivially copyable record; no allocation.
    out=record.handle;return Ok;
}
SessionLifecycle::Status SessionLifecycle::allocateSample(const MilesWire::Handle &driver,
        MilesWire::Handle &out) {
    clear(out);
    if(!onThread())return WrongThread;
    if(!started)return NotStarted;
    void *native=0;
    if(!registry.resolve(driver,MilesWire::Driver,native))return UnknownResource;
    if(!reserveRecord())return StorageFailure;
    HSAMPLE sample=::AIL_allocate_sample_handle(static_cast<HDIGDRIVER>(native));
    if(!sample)return Ok;
    Record record={};record.native=sample;record.parent=driver;record.sample=true;
    try {
        if(!registry.insert(MilesWire::OwnedSample,sample,record.handle)) {
            ::AIL_release_sample_handle(sample);return CapacityFailure;
        }
    } catch(...) { ::AIL_release_sample_handle(sample);throw; }
    records.push_back(record);
    out=record.handle;return Ok;
}
SessionLifecycle::Status SessionLifecycle::releaseSample(const MilesWire::Handle &sample,
        bool callbacksQuiesced) {
    if(!onThread())return WrongThread;
    if(!started)return NotStarted;
    if(!callbacksQuiesced)return QuiescenceRequired;
    void *native=0;
    if(!registry.resolve(sample,MilesWire::OwnedSample,native))return UnknownResource;
    for(size_t i=0;i<records.size();++i)if(records[i].sample && same(records[i].handle,sample)) {
        void *parent=0;
        if(!registry.resolve(records[i].parent,MilesWire::Driver,parent))return UnknownResource;
        if(!registry.beginClose(sample))return UnknownResource;
        ::AIL_release_sample_handle(static_cast<HSAMPLE>(native));
        registry.retire(sample);
        records.erase(records.begin()+i);
        return Ok;
    }
    return UnknownResource;
}
SessionLifecycle::Status SessionLifecycle::shutdown(bool callbacksQuiesced) {
    if(!onThread())return WrongThread;
    if(!started)return NotStarted;
    if(!callbacksQuiesced)return QuiescenceRequired;
    // Global quiescence must include callbacks and all dispatch users, not just EOS.
    for(size_t i=records.size();i>0;--i)if(records[i-1].sample) {
        Record &r=records[i-1];registry.beginClose(r.handle);
        ::AIL_release_sample_handle(static_cast<HSAMPLE>(r.native));registry.retire(r.handle);
    }
    for(size_t i=records.size();i>0;--i)if(!records[i-1].sample) {
        Record &r=records[i-1];registry.beginClose(r.handle);
        ::AIL_close_digital_driver(static_cast<HDIGDRIVER>(r.native));registry.retire(r.handle);
    }
    ::AIL_shutdown();records.clear();started=false;return Ok;
}
}
