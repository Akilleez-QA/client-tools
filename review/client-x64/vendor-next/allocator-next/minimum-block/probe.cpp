#include "MemoryManager-candidate.h"
#include "sharedMemoryManager/FirstSharedMemoryManager.h"
#include "MemoryManager-diagnostic.cpp"
#include <stdio.h>
#include <string.h>
static unsigned checks, failures;
#define CHECK(x) do { ++checks; if (!(x)) { ++failures; printf("FAIL line=%d\n", __LINE__); } } while (0)
using namespace MemoryManagerNamespace;
static bool chainOkay()
{
    for (SystemAllocation *region = ms_firstSystemAllocation; region; region = region->getNext()) {
        Block *previous = region->getFirstMemoryBlock();
        Block *last = region->getLastMemoryBlock();
        unsigned iterations = 0;
        for (Block *block = previous->getNext(); block != last; block = block->getNext()) {
            if (++iterations > 100000 || block <= previous || block >= last)
                return false;
            if (block->getPrevious() != previous || block->getNext() <= block || block->getNext() > last)
                return false;
            if (block->getSize() < cms_freeBlockSize)
                return false;
            previous = block;
        }
        if (last->getPrevious() != previous)
            return false;
    }
    return true;
}
int main()
{
    MemoryManager::setReportAllocations(false);
    printf("layout pointer=%u block=%u free=%u allocated=%u rounded_free=%d\n",
           unsigned(sizeof(void*)), unsigned(sizeof(Block)), unsigned(sizeof(FreeBlock)),
           unsigned(sizeof(AllocatedBlock)), cms_freeBlockSize);
    for (size_t size = 0; size <= 512; ++size) {
        int rounded = 0;
        CHECK(calculateAllocationSize(size, rounded));
        CHECK(rounded >= cms_freeBlockSize && rounded % 16 == 0);
#ifndef _WIN64
        int const legacy = int((cms_allocatedBlockSize + 2 * cms_guardBandSize + (size ? size : 1) + 15) & ~size_t(15));
        CHECK(rounded == legacy);
#else
        CHECK(rounded >= int(cms_allocatedBlockSize + 2 * cms_guardBandSize + size));
#endif
    }
    CHECK(chainOkay());
    size_t const sizes[] = {0,1,15,16,17,31,32,33,63,64,65,255,256,257,4096,65535};
    void *blocks[16] = {};
    for (int i = 0; i != 16; ++i) {
        blocks[i] = MemoryManager::allocate(sizes[i], 123, false, false);
        if (sizes[i]) memset(blocks[i], i+1, sizes[i]);
        CHECK(blocks[i] != 0);
        CHECK(chainOkay());
    }
    for (int i = 0; i != 16; i += 2) {
        MemoryManager::free(blocks[i], false);
        CHECK(chainOkay());
    }
    for (int i = 1; i < 16; i += 2) {
        blocks[i] = MemoryManager::reallocate(blocks[i], sizes[i] + 1024);
        bool preserved = true;
        for (size_t j=0; j<sizes[i]; ++j)
            if (static_cast<unsigned char *>(blocks[i])[j] != i+1) preserved = false;
        CHECK(preserved);
        CHECK(chainOkay());
        MemoryManager::free(blocks[i], false);
        CHECK(chainOkay());
    }
    // Candidate-only region-edge sizes; each request is bounded below 4 MiB.
    for (int delta = -64; delta <= 64; delta += 16) {
        void *p = MemoryManager::allocate(size_t(4194128 + delta), 123, false, false);
        CHECK(chainOkay());
        MemoryManager::free(p, false);
        CHECK(chainOkay());
    }
    unsigned const expected = 1622;
    printf("checks=%u failures=%u expected=%u\n", checks, failures, expected);
    return failures || checks != expected;
}
