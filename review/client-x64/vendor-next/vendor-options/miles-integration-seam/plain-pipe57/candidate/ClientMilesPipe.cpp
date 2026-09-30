#include "ClientMiles.h"
#include "PipeCore.h"
#include "../../plain-startup52/candidate/private/failure_boundary.h"
#include "../../client-runtime53/candidate/callback-reentry47/invocation_guard.h"
#include <exception>

namespace {
namespace Boundary = ClientMilesPrivate52;
namespace Core = ClientMilesPipeCore57;
template<class Result, class Action> Result guarded(Action action) {
    try {
        Boundary::requireFatalReporter();
        // Before selected Session access, any request or local proxy mutation.
        MilesCallbackGuard47::requireForwardAllowed();
        return action();
    } catch (const std::exception &error) {
        Boundary::fail(Boundary::PrivateException,error.what());
    } catch (...) {
        Boundary::fail(Boundary::UnknownException,"exception in private Miles pipe adapter");
    }
}
}
// Exactly eight callback-free lifecycle entrypoints. Link this implementation
// instead of the old public pipe definitions or direct-native implementations.
namespace ClientMiles {
int32_t startup() {
    return guarded<int32_t>([]() -> int32_t { return Core::startup(); });
}
void shutdown() {
    guarded<void>([]() -> void { Core::shutdown(); });
}
HDIGDRIVER open_digital_driver(uint32_t frequency,int32_t bits,int32_t channels,uint32_t flags) {
    return guarded<HDIGDRIVER>([=]() -> HDIGDRIVER { return Core::open_digital_driver(frequency,bits,channels,flags); });
}
HSAMPLE allocate_sample_handle(HDIGDRIVER driver) {
    return guarded<HSAMPLE>([=]() -> HSAMPLE { return Core::allocate_sample_handle(driver); });
}
void release_sample_handle(HSAMPLE sample) {
    guarded<void>([=]() -> void { Core::release_sample_handle(sample); });
}
HSTREAM open_stream(HDIGDRIVER driver,const char *filename,int32_t streamMem) {
    return guarded<HSTREAM>([=]() -> HSTREAM { return Core::open_stream(driver,filename,streamMem); });
}
void close_stream(HSTREAM stream) {
    guarded<void>([=]() -> void { Core::close_stream(stream); });
}
HSAMPLE stream_sample_handle(HSTREAM stream) {
    return guarded<HSAMPLE>([=]() -> HSAMPLE { return Core::stream_sample_handle(stream); });
}
}
