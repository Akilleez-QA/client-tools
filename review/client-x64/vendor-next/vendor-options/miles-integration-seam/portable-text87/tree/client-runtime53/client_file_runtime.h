#ifndef TEST_ONLY_RUNTIME66_H
#define TEST_ONLY_RUNTIME66_H
#include "../native-file-callbacks35/ClientMilesFileCallbacks.h"
#include <memory>
#include <stdexcept>
namespace MilesClientRuntime53 {
// Only unavailable dependency replaced. No worker, Win32, Endpoint or returned API.
struct Runtime {
    unsigned failures;
    Runtime():failures(0){}
    void fail(){++failures;}
    bool prepare(uint64_t,ClientMiles::FileOpenCallback,ClientMiles::FileCloseCallback,
        ClientMiles::FileSeekCallback,ClientMiles::FileReadCallback,std::shared_ptr<void>){
        throw std::logic_error("file preparation forbidden in portable66");
    }
};
}
#endif
