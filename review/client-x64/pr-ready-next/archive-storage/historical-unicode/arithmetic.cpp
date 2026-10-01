#include "ArchiveCount.h"
#include <cstdio>
namespace Unicode { typedef unsigned short unicode_char_t; }
// Exact production arithmetic extracted; no Unicode string or writer is exercised.
unsigned int bytes(size_t codeUnits) {
const unsigned int size = ArchiveCount::fromSize<unsigned int>(codeUnits);
		if (size > (std::numeric_limits<unsigned int>::max)() / sizeof(Unicode::unicode_char_t))
			throw std::out_of_range("Unicode payload exceeds ByteStream byte count range");
		unsigned int const byteSize = size * static_cast<unsigned int>(sizeof(Unicode::unicode_char_t));
		return byteSize;
}
int main() {
 unsigned checks=0; unsigned int const top=(std::numeric_limits<unsigned int>::max)();
 size_t const limit=top/sizeof(Unicode::unicode_char_t);
 size_t const values[]={0,1,3,limit};
 for(unsigned i=0;i<4;++i){if(bytes(values[i])!=values[i]*2)return 1;++checks;}
 size_t const bad[]={limit+1,static_cast<size_t>(top)};
 for(unsigned i=0;i<2;++i){bool caught=false;try{bytes(bad[i]);}catch(std::out_of_range const&){caught=true;}if(!caught)return 2;++checks;}
 std::printf("PASS: %u extracted arithmetic checks (not real-string runtime coverage)\n",checks);return 0;
}
