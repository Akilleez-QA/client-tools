#include "retained_buffers.h"
#include <cstdio>
#include <cstring>
#include <limits>
static unsigned checks;
static bool check(bool ok, int line) { ++checks; if(!ok)std::printf("FAIL %d\n",line); return ok; }
#define CHECK(x) if(!check((x),__LINE__))return 1
int main() {
    using MilesHost::RetainedBuffers;
    typedef RetainedBuffers B;
    B b(12,4); B::Token a=0,c=0,rejected=999; B::View v={};
    unsigned char input[]={9,1,0,3,8};
    CHECK(b.stage(B::Binary,input,sizeof input,1,3,a));
    B other(12,4); B::Token otherToken=0;
    CHECK(other.stage(B::Binary,input,sizeof input,0,1,otherToken));
    CHECK(otherToken!=a);
    CHECK(!other.commit(a) && !other.retire(a) && !other.view(a,v));
    CHECK(!b.commit(otherToken) && !b.retire(otherToken) && !b.view(otherToken,v));
    CHECK(b.commit(a)); CHECK(b.view(a,v));
    const unsigned char *old=v.data;
    CHECK(v.size==3 && old[0]==1 && old[1]==0 && old[2]==3);
    input[1]=99; CHECK(old[0]==1);
    CHECK(!b.stage(B::Binary,input,sizeof input,4,2,rejected));
    CHECK(rejected==999 && b.active()==a && b.bytes()==3);
    CHECK(!b.stage(B::Binary,input,sizeof input,(std::numeric_limits<size_t>::max)(),2,rejected));
    CHECK(!b.stage(B::Binary,0,5,0,3,rejected));
    CHECK(b.stage(B::Binary,input,sizeof input,0,5,c));
    CHECK(b.active()==a && old[0]==1 && old[2]==3); // Simulated vendor failure: do not commit.
    CHECK(b.commit(c)); CHECK(b.view(a,v) && v.data==old && old[0]==1);
    CHECK(!b.retire(c)); CHECK(!b.commit(999) && b.active()==c);
    CHECK(b.retire(a)); CHECK(!b.view(a,v)); CHECK(!b.retire(a));
    CHECK(b.bytes()==5); b.deactivate(); CHECK(b.retire(c) && b.bytes()==0);
    B::Token empty=0,nullText=0,text=0;
    const char s[]="abc";
    CHECK(b.stage(B::Text,s,sizeof s,0,sizeof s,text));
    CHECK(b.view(text,v) && v.size==4 && !std::memcmp(v.data,s,4));
    CHECK(b.stage(B::Text,"",1,0,1,empty));
    CHECK(b.view(empty,v) && v.kind==B::Text && v.size==1 && v.data[0]==0);
    CHECK(b.stage(B::NullText,0,0,0,0,nullText));
    CHECK(b.view(nullText,v) && v.kind==B::NullText && !v.data && !v.size);
    CHECK(!b.stage(B::Text,s,4,0,3,rejected));
    const char embedded[]={'a',0,'b',0};
    CHECK(!b.stage(B::Text,embedded,4,0,4,rejected));
    CHECK(!b.stage(B::NullText,s,4,1,0,rejected));
    CHECK(!b.stage(B::Binary,s,4,0,0,rejected));
    CHECK(!b.stage(static_cast<B::Kind>(99),s,4,0,4,rejected));
    B bounded(3,1); B::Token token=0;
    CHECK(bounded.stage(B::Binary,s,4,0,3,token));
    CHECK(!bounded.stage(B::NullText,0,0,0,0,rejected));
    CHECK(bounded.bytes()==3 && rejected==999);
    CHECK(bounded.retire(token));
    CHECK(!bounded.stage(B::Binary,s,4,0,4,rejected));
    B zero(0,1); CHECK(zero.stage(B::NullText,0,0,0,0,token));
    std::printf("PASS %u ownership checks\n",checks);return 0;
}
