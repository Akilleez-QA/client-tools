#include "../candidate/host-file-consumption49/reply_transaction.h"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <exception>
#include <stdexcept>
#include <string>
using namespace MilesHostFiles49;
using namespace MilesFileChannel26;
static unsigned checks=0;
static bool deathArmed=false;
static const char *deathMode=0;
#define CHECK(x) do { ++checks; if(!(x)) throw std::runtime_error(std::string("line ")+std::to_string(__LINE__)+": "+#x); } while(0)
static MilesTransport::Bytes bytes(const std::vector<unsigned char> &v){return MilesTransport::Bytes(v.data(),v.size());}
static MilesWire::Handle file(uint32_t slot=777,uint32_t generation=91){MilesWire::Handle h={MilesWire::File,slot,generation};return h;}
static bool same(const MilesWire::Handle &a,const MilesWire::Handle &b){return a.kind==b.kind && a.slot==b.slot && a.generation==b.generation;}
static Request request(uint32_t opcode,MilesWire::Handle target=MilesWire::Handle(),uint32_t value=0){
    static uint64_t next=300;
    MilesWire::Header h={};h.magic=MilesWire::Magic;h.version=MilesWire::Version;
    h.kind=MilesWire::ReverseRequest;h.opcode=opcode;h.request=++next;h.causal_request=55;h.lane=8;h.lock_lease=4;
    MilesWire::Call c={};c.target=target;c.value[0]=value;
    std::vector<unsigned char> wire;
    CHECK(MilesTransport::encodeCall(h,c,MilesTransport::Bytes(),opcode==MilesWire::FileOpen?MilesTransport::Bytes("x",2):MilesTransport::Bytes(),wire));
    Association a={h.request,h.causal_request,h.lane,h.lock_lease};Request r;
    CHECK(decodeRequest(bytes(wire),a,r)==Valid);return r;
}
static std::vector<unsigned char> reply(const Request &r,uint32_t bits=0,
    MilesWire::Handle remote=MilesWire::Handle(),MilesTransport::Bytes data=MilesTransport::Bytes(),
    uint32_t status=0,bool wrongContext=false){
    MilesWire::Header h=r.header();h.kind=MilesWire::ReverseReply;if(wrongContext)++h.request;
    MilesWire::Result result={};result.return_bits=bits;result.resource=remote;result.transport_status=status;
    std::vector<unsigned char> out;CHECK(MilesTransport::encodeResult(h,result,data,MilesTransport::Bytes(),out));return out;
}
static void noResult(ReplyTransaction &tx){uint32_t bits=19,token=23;CHECK(!tx.result(bits,token));CHECK(bits==19 && token==23);}
static void ack(ReplyTransaction &tx,const Request &r){
    MilesFileProtocol48::FileAckExpected expected;
    CHECK(MilesFileProtocol48::expectFileAck(r,99,expected));
    CHECK(tx.ack().size==136);CHECK(MilesFileProtocol48::validateFileConsumptionAck(tx.ack(),expected));
    CHECK(tx.observeAckWriteComplete());CHECK(tx.ack().size==0);
}
static uint32_t open(FileTokens &tokens,MilesWire::Handle remote,uint32_t status=7){
    Request r=request(MilesWire::FileOpen);ReplyTransaction tx(tokens,r,99,0);
    CHECK(tx.state()==ReplyTransaction::Prepared && !tx.ack().size);noResult(tx);
    CHECK(!tx.observeAckWriteComplete());CHECK(tx.beginSend());CHECK(!tx.ack().size);noResult(tx);
    auto frame=reply(r,status,remote);CHECK(tx.consume(bytes(frame)));noResult(tx);ack(tx,r);
    uint32_t bits=0,token=0;CHECK(tx.result(bits,token));CHECK(bits==status && token!=0);return token;
}
static void close(FileTokens &tokens,uint32_t token,MilesWire::Handle remote){
    Request r=request(MilesWire::FileClose,remote);ReplyTransaction tx(tokens,r,99,token);
    CHECK(tx.beginSend());MilesWire::Handle out={};CHECK(!tokens.resolve(token,out));
    auto frame=reply(r);CHECK(tx.consume(bytes(frame)));CHECK(!tokens.resolve(token,out));
    noResult(tx);ack(tx,r);uint32_t bits=19,opened=19;CHECK(tx.result(bits,opened));CHECK(!bits && !opened);
}
static void positive(){
    {
        FileTokens tokens(1);const auto remote=file();uint32_t first=open(tokens,remote,UINT32_C(0x80000001));
        MilesWire::Handle resolved={};CHECK(tokens.resolve(first,resolved) && same(resolved,remote));
        close(tokens,first,remote);
        const auto nextRemote=file(888,92);uint32_t second=open(tokens,nextRemote);
        CHECK(second>first && !tokens.resolve(first,resolved));CHECK(tokens.resolve(second,resolved) && same(resolved,nextRemote));
        close(tokens,second,nextRemote);
    }
    std::puts("PASS separate SDK token host registry and client wire identities with stale-token refusal");
    {
        FileTokens tokens(1);Request r=request(MilesWire::FileOpen);ReplyTransaction failed(tokens,r,99,0);
        CHECK(failed.beginSend());auto frame=reply(r);CHECK(failed.consume(bytes(frame)));ack(failed,r);
        uint32_t bits=19,token=19;CHECK(failed.result(bits,token));CHECK(!bits && !token);
        uint32_t success=open(tokens,file(),7);CHECK(success>1);close(tokens,success,file());
    }
    std::puts("PASS failed open publishes no token and non1 status stays exact");
    {
        FileTokens tokens(1);Request r=request(MilesWire::FileOpen);
        {ReplyTransaction tx(tokens,r,99,0);CHECK(tx.cancelBeforeSend());CHECK(tx.state()==ReplyTransaction::Cancelled);}
        {ReplyTransaction tx(tokens,r,99,0);} // Prepared destructor cancels only before any send.
        uint32_t token=open(tokens,file());CHECK(token>2);close(tokens,token,file());
    }
    std::puts("PASS explicit and destructor presend cancellation permit slot reuse without token reuse");
    {
        FileTokens tokens(1);uint32_t token=open(tokens,file());
        unsigned char storage[7];std::memset(storage,0xee,sizeof storage);
        const unsigned char data[3]={4,5,6};Request r=request(MilesWire::FileRead,file(),5);
        ReplyTransaction tx(tokens,r,99,token,storage+1,5);CHECK(tx.beginSend());
        auto frame=reply(r,3,MilesWire::Handle(),MilesTransport::Bytes(data,3));
        CHECK(tx.consume(bytes(frame)));CHECK(storage[0]==0xee && storage[1]==4 && storage[2]==5 && storage[3]==6);
        CHECK(storage[4]==0xee && storage[5]==0xee && storage[6]==0xee);noResult(tx);ack(tx,r);
        uint32_t bits=0,opened=1;CHECK(tx.result(bits,opened));CHECK(bits==3 && !opened);
        Request zero=request(MilesWire::FileRead,file(),0);ReplyTransaction empty(tokens,zero,99,token,0,0);
        CHECK(empty.beginSend());frame=reply(zero);CHECK(empty.consume(bytes(frame)));ack(empty,zero);
        CHECK(empty.result(bits,opened));CHECK(!bits && !opened);close(tokens,token,file());
    }
    std::puts("PASS exact bounded read copy short read zero read and ACK result ordering");
    {
        FileTokens tokens(1);uint32_t token=open(tokens,file());unsigned char buffer[3]={};
        for(unsigned mode=0;mode<3;++mode){
            bool rejected=false;
            try {Request r=request(MilesWire::FileRead,mode==2?file(999):file(),3);
                ReplyTransaction bad(tokens,r,99,token,mode==0?0:buffer,mode==1?2:3);}
            catch(const std::invalid_argument &){rejected=true;}CHECK(rejected);
            MilesWire::Handle resolved={};CHECK(tokens.resolve(token,resolved));
        }
        close(tokens,token,file());
    }
    std::puts("PASS read buffer and remote target rejected before any send");
    {
        FileTokens tokens(1);uint32_t token=open(tokens,file());Request r=request(MilesWire::FileSeek,file(),UINT32_C(0x80000000));
        CHECK(r.offset()==INT32_MIN);ReplyTransaction tx(tokens,r,99,token);CHECK(tx.beginSend());
        auto frame=reply(r,UINT32_C(0x80000000));CHECK(tx.consume(bytes(frame)));ack(tx,r);
        uint32_t bits=0,opened=1;CHECK(tx.result(bits,opened));CHECK(bits==UINT32_C(0x80000000) && !opened);
        int32_t signedResult=0;std::memcpy(&signedResult,&bits,sizeof signedResult);CHECK(signedResult==INT32_MIN);
        close(tokens,token,file());
    }
    std::puts("PASS signed seek bits preserved through real reply decoder");
    {
        FileTokens tokens(1);uint32_t token=0;CHECK(tokens.reserveOpen(token));uint32_t unchanged=17;
        CHECK(!tokens.reserveOpen(unchanged));CHECK(unchanged==17);CHECK(tokens.cancelOpen(token));
    }
    std::puts("PASS live capacity fails before another reservation and preserves output");
    std::printf("PASS %u positive host49 checks; no Endpoint SDK or engine\n",checks);
}
static void terminateExpected(){
    if(deathArmed){std::fprintf(stderr,"EXPECTED_TERMINATE %s checks=%u\n",deathMode,checks);std::fflush(stderr);std::_Exit(73);}
    std::fputs("UNEXPECTED_TERMINATE before prospective oracle armed\n",stderr);std::fflush(stderr);std::_Exit(74);
}
static void death(const char *mode){
    deathMode=mode;std::set_terminate(&terminateExpected);
    FileTokens tokens(1);
    const bool read=std::strcmp(mode,"failed-read")==0 || std::strcmp(mode,"consumed-ack-uncertain")==0;
    const bool closing=std::strcmp(mode,"failed-close")==0;
    uint32_t token=(read || closing)?open(tokens,file()):0;
    Request r=request(read?MilesWire::FileRead:closing?MilesWire::FileClose:MilesWire::FileOpen,
        token?file():MilesWire::Handle(),read?3:0);
    unsigned char buffer[5];std::memset(buffer,0xee,sizeof buffer);
    {
        ReplyTransaction tx(tokens,r,99,token,read?buffer+1:0,read?3:0);CHECK(tx.beginSend());
        if(std::strcmp(mode,"issued")==0){
            CHECK(tx.state()==ReplyTransaction::Issued);CHECK(!tx.cancelBeforeSend());
            uint32_t other=0;CHECK(!tokens.reserveOpen(other));
        } else if(std::strcmp(mode,"consumed-ack-uncertain")==0){
            const unsigned char data[2]={8,9};auto frame=reply(r,2,MilesWire::Handle(),MilesTransport::Bytes(data,2));
            CHECK(tx.consume(bytes(frame)));CHECK(tx.state()==ReplyTransaction::Consumed);
            CHECK(buffer[0]==0xee && buffer[1]==8 && buffer[2]==9 && buffer[3]==0xee && buffer[4]==0xee);
            CHECK(tx.ack().size==136);CHECK(!tx.cancelBeforeSend());
        } else {
            std::vector<unsigned char> frame;
            if(read){const unsigned char bad[4]={1,2,3,4};frame=reply(r,4,MilesWire::Handle(),MilesTransport::Bytes(bad,4));}
            else if(closing)frame=reply(r,1); // close has no scalar result
            else if(std::strcmp(mode,"failed-context")==0)frame=reply(r,7,file(),MilesTransport::Bytes(),0,true);
            else if(std::strcmp(mode,"failed-status")==0)frame=reply(r,0,MilesWire::Handle(),MilesTransport::Bytes(),1);
            else throw std::runtime_error("unknown death mode");
            CHECK(!tx.consume(bytes(frame)));CHECK(tx.state()==ReplyTransaction::Failed);
            if(read)for(unsigned i=0;i<5;++i)CHECK(buffer[i]==0xee);
            CHECK(!tx.ack().size);CHECK(!tx.cancelBeforeSend());
            auto valid=reply(r,read?0:closing?0:7,token?MilesWire::Handle():file());
            CHECK(!tx.consume(bytes(valid)));CHECK(tx.state()==ReplyTransaction::Failed);
            uint32_t other=0;CHECK(!tokens.reserveOpen(other)); // ownership not rolled back
        }
        noResult(tx);
        deathArmed=true; // Only now may destruction be counted as expected termination.
    }
    deathArmed=false;throw std::runtime_error("unsettled destructor returned");
}
int main(int argc,char **argv){
    try {if(argc==1)positive();else if(argc==2)death(argv[1]);else return 2;return 0;}
    catch(const std::exception &e){std::fprintf(stderr,"FAIL %s\n",e.what());return 1;}
}
