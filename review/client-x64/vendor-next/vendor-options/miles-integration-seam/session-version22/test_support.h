#ifndef SESSION_VERSION21_TEST_SUPPORT_H
#define SESSION_VERSION21_TEST_SUPPORT_H
#include "session_version.h"
#include <cstdio>
#include <cstring>
#include <fstream>
#include <iterator>
static unsigned checks=0,failures=0;
static void check(bool value,int line) { ++checks; if(!value) { ++failures; std::printf("FAIL line %d\n",line); } }
#define CHECK(x) check(!!(x),__LINE__)
inline MilesWire::Header request() {
    MilesWire::Header h={}; h.magic=MilesWire::Magic; h.version=MilesWire::Version;
    h.kind=MilesWire::Request; h.opcode=MilesWire::SessionVersion;
    h.request=0x123456789abcdef0ULL; h.lane=0xfedcba9876543210ULL;
    return h;
}
inline MilesTransport::Bytes bytes(const std::vector<unsigned char>& v) {
    return MilesTransport::Bytes(v.empty()?0:&v[0],v.size());
}
inline bool writeFile(const char* path, const void* p, size_t n) {
    std::ofstream f(path,std::ios::binary); f.write(static_cast<const char*>(p),static_cast<std::streamsize>(n));
    f.close(); return !!f;
}
inline bool readFile(const char* path, std::vector<unsigned char>& b) {
    std::ifstream f(path,std::ios::binary); if(!f) return false;
    b.assign(std::istreambuf_iterator<char>(f),std::istreambuf_iterator<char>());
    return !f.bad();
}
#endif
