// Diagnostic reproduction only; compile with VS2013 x86 and amd64 cl.
// /DORIGINAL demonstrates the original overload-body error.
// /DBODY_ONLY demonstrates remaining uint/ptrdiff_t call ambiguity.
#include <stddef.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#if defined(ORIGINAL) || defined(BODY_ONLY)
inline void *memmove(void *d, const void *s, int n) {
 if (!d || !s) abort();
#ifdef ORIGINAL
 return memmove(d,s,static_cast<unsigned int>(n));
#else
 return memmove(d,s,static_cast<size_t>(n));
#endif
}
#else
inline void *imemmove(void *d, const void *s, int n) {
 if (!d || !s) abort();
 return memmove(d,s,static_cast<size_t>(n));
}
#endif
int passes=0;
void check(bool b) { if (!b) exit(1); ++passes; }
template<class N> void probe() {
 char a[]="abcdef";
 check(memmove(a+1,a,N(5))==a+1 && memcmp(a,"aabcde",6)==0);
 char b[]="abcdef";
 check(memmove(b,b+1,N(5))==b && memcmp(b,"bcdeff",6)==0);
 check(memmove(b,b,N(0))==b && memcmp(b,"bcdeff",6)==0);
}
int main() {
 probe<int>(); probe<unsigned int>(); probe<size_t>(); probe<ptrdiff_t>();
#if !defined(ORIGINAL) && !defined(BODY_ONLY)
 char a[]="abcdef";
 check(imemmove(a+1,a,5)==a+1 && memcmp(a,"aabcde",6)==0);
#endif
 printf("PASS %d pointer_bytes=%u\n",passes,static_cast<unsigned>(sizeof(void*)));
 return 0;
}
