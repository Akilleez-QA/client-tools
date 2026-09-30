#include <xmmintrin.h>
#include <stdio.h>
#include <stddef.h>
struct Before { char c; __m128 v; };
#pragma pack(show)
#include "C:/crypto-packing-input/FirstCrypto.h"
#pragma pack(show)
struct After { char c; __m128 v; };
static_assert(sizeof(Before) == sizeof(After), "crypto headers leaked pack state");
static_assert(offsetof(Before,v) == offsetof(After,v), "crypto headers changed member packing");
int main()
{
 printf("before=%u/%u after=%u/%u string=%u buffered=%u\n", unsigned(sizeof(Before)), unsigned(offsetof(Before,v)), unsigned(sizeof(After)), unsigned(offsetof(After,v)), unsigned(sizeof(std::string)), unsigned(sizeof(CryptoPP::BufferedTransformation)));
 return 0;
}
