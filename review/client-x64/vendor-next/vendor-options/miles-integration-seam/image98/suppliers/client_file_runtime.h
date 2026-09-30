#ifndef IMAGE98_TEST_ONLY_RUNTIME_H
#define IMAGE98_TEST_ONLY_RUNTIME_H
#include "../backend-boundary24/ClientMiles.h"
#include <memory>
#include <stdexcept>
namespace MilesClientRuntime53 {
// Test-only missing dependency. Not the real Runtime, worker or ACK join.
struct Runtime {
    unsigned failures;
    Runtime():failures(0){}
    void fail(){++failures;}
    bool prepare(uint64_t,ClientMiles::FileOpenCallback,ClientMiles::FileCloseCallback,
        ClientMiles::FileSeekCallback,ClientMiles::FileReadCallback,std::shared_ptr<void>){
        throw std::logic_error("file preparation forbidden in image98");
    }
};
}
#endif
