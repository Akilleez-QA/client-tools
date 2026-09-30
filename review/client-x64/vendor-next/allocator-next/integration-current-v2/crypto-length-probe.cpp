#include "FirstCrypto.h"
#include "filters.h"
#include <stdio.h>
#include <limits.h>
struct LengthView {
 size_t n;
 const char *data() const { return "abc"; }
 size_t length() const { return n; }
 char operator[](unsigned) const { return 'a'; }
};
int main() {
 int checks=0;
 {
  CryptoPP::StringSource source("abc",true);
  unsigned char got[3]={0,0,0};
  if(source.Get(got,3)!=3 || got[0]!='a' || got[1]!='b' || got[2]!='c') return 1;
  ++checks;
 }
 {
  LengthView view={3}; CryptoPP::StringSource source(view,true);
  unsigned char got[3]={0,0,0};
  if(source.Get(got,3)!=3 || got[0]!='a' || got[1]!='b' || got[2]!='c') return 2;
  ++checks;
 }
 {
  const unsigned char bytes[]={0,1,255};CryptoPP::StringSource source(bytes,3,true);
  unsigned char got[3]={0,0,0};
  if(source.Get(got,3)!=3 || got[0]!=0 || got[1]!=1 || got[2]!=255) return 3;
  ++checks;
 }
 // Only constructor acceptance is exercised for a synthetic large view. No bytes
 // are read and no huge backing allocation or transfer is claimed.
 { LengthView view={UINT_MAX};CryptoPP::StringStore store(view);++checks; }
#ifdef _WIN64
 { LengthView view={static_cast<size_t>(UINT_MAX)+1};bool rejected=false;
   try {CryptoPP::StringStore store(view);} catch(CryptoPP::Exception const &e) {rejected=strcmp(e.what(),"StringStore: input exceeds unsigned int length range")==0;}
   if(!rejected)return 4; ++checks;
 }
#endif
 printf("PASS %d crypto checks; synthetic limit view never transferred\n",checks);
 return 0;
}
