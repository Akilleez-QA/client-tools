#include <stdio.h>
typedef unsigned char byte;
#define DEBUG_REPORT_LOG_PRINT(condition, args) printf args
void diagnostic(void *block, int cms_freeBlockSize, int i, byte *memory) {
DEBUG_REPORT_LOG_PRINT(true, ("corrupted free pattern at position %3d [membase=0x%x, memaddr=0x%x] = %02x\n", i, reinterpret_cast<unsigned int>(reinterpret_cast<byte *>(block) + cms_freeBlockSize), reinterpret_cast<unsigned int>(reinterpret_cast<byte *>(block) + cms_freeBlockSize + i), static_cast<int>(*memory)));
}
