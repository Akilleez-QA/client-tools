// Portable-only substitution for Windows job/worker plumbing. No engine runs.
#include "../file-executor33/FileInvocationJob.h"
#include <stdexcept>
#include <vector>
namespace Script36 {
unsigned opens=0,closes=0,reads=0,seeks=0;
int submitFailure=0;
bool throwOpen=false,throwClose=false,dispatchUncertain=false,openFails=false;
std::vector<std::weak_ptr<MilesFileExecutor30::FileInvocationJob> > pending;
ClientAudioFileCallbacks::OpenResult open(const char *){
    ++opens;if(throwOpen)throw std::runtime_error("scripted open uncertainty");
    ClientAudioFileCallbacks::OpenResult r={openFails?0u:7u,{openFails?static_cast<uintptr_t>(0x7654):0}};return r;
}
void close(ClientAudioFileCallbacks::LocalFileHandle h){if(h.value!=0)throw std::runtime_error("A close expected exact zero");++closes;if(throwClose)throw std::runtime_error("scripted close uncertainty");}
int32_t seek(ClientAudioFileCallbacks::LocalFileHandle h,int32_t,uint32_t){if(h.value!=0)throw std::runtime_error("A seek expected exact zero");++seeks;return -17;}
uint32_t read(ClientAudioFileCallbacks::LocalFileHandle h,void *p,uint32_t n){if(h.value!=0)throw std::runtime_error("A read expected exact zero");++reads;for(uint32_t i=0;i<n;++i)static_cast<unsigned char *>(p)[i]=static_cast<unsigned char>(i);return n;}
void pumpFirst(){if(!pending.empty()){auto j=pending.front().lock();if(j)j->wait();pending.erase(pending.begin());}}
void pump(){for(size_t i=0;i<pending.size();++i){auto j=pending[i].lock();if(j)j->wait();}pending.clear();}
}
namespace MilesFileExecutor30 {
EngineFileWorker::EngineFileWorker():impl(0) {}
EngineFileWorker::~EngineFileWorker() {}
EngineFileWorker *EngineFileWorker::create(){return new EngineFileWorker;}
void EngineFileWorker::destroy(EngineFileWorker *p){delete p;}
struct FileInvocationJob::State {
    MilesFileChannel26::Invocation invocation;
    mutable bool done;
    bool uncertain;
    State(const MilesFileChannel26::Request &r,const MilesFileChannel26::FileServices &services,std::shared_ptr<const MilesFileChannel26::Binding> b,std::shared_ptr<void> p)
        :invocation(r,services,b,p),done(false),uncertain(Script36::dispatchUncertain) {}
};
FileInvocationJob::FileInvocationJob(const MilesFileChannel26::Request &r,const MilesFileChannel26::FileServices &services,std::shared_ptr<const MilesFileChannel26::Binding> b,std::shared_ptr<void> p):state(new State(r,services,b,p)) {}
FileInvocationJob::~FileInvocationJob(){delete state;}
std::shared_ptr<FileInvocationJob> FileInvocationJob::enqueueAdmitted(EngineFileWorker &,const MilesFileChannel26::Request &r,const MilesFileChannel26::FileServices &services,std::shared_ptr<const MilesFileChannel26::Binding> b,std::shared_ptr<void> p){
    if(Script36::submitFailure==1)throw std::bad_alloc();
    if(Script36::submitFailure==2)return std::shared_ptr<FileInvocationJob>();
    std::shared_ptr<FileInvocationJob> job(new FileInvocationJob(r,services,b,p));Script36::pending.push_back(job);return job;
}
FileInvocationJob::Status FileInvocationJob::status() const {return !state->done?Pending:state->uncertain?DispatchUncertain:AdapterCompleted;}
bool FileInvocationJob::wait() const {if(!state->done){state->invocation.invokeOnAdmittedExecutor();state->done=true;}return true;}
const MilesFileChannel26::Invocation *FileInvocationJob::completedInvocation() const {return status()==AdapterCompleted?&state->invocation:0;}
}
