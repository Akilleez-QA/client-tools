#include "metadata.h"
#include <cstdio>
#include <cstring>
#include <limits>
static unsigned checks,failures;
static void check(bool value,int line){++checks;if(!value){++failures;printf("FAIL line %d\n",line);}}
#define CHECK(x) check(!!(x),__LINE__)
int main() {
 using namespace MilesStartup;uint32_t bits=123;
 CHECK(preferenceValue(-1,bits)&&bits==0xffffffffu&&signedValue(bits)==-1);
 CHECK(preferenceValue(INT32_MIN,bits)&&bits==0x80000000u&&signedValue(bits)==INT32_MIN);
 CHECK(preferenceValue(INT32_MAX,bits)&&bits==0x7fffffffu&&signedValue(bits)==INT32_MAX);
 CHECK(!preferenceValue(int64_t(INT32_MAX)+1,bits)&&bits==0x7fffffffu);
 CHECK(!preferenceValue(int64_t(INT32_MIN)-1,bits)&&bits==0x7fffffffu);
 Reply reply;CHECK(copyText(0,reply)&&reply.result.null_mask==TextNull&&reply.text.empty());
 CHECK(copyText("",reply)&&!reply.result.null_mask&&reply.text.size()==1&&reply.text[0]==0);
 char text[]="old";CHECK(copyText(text,reply));text[0]='n';CHECK(reply.text.size()==4&&reply.text[0]=='o');
 std::vector<char> longText(ReplyTextLimit+1,'a');longText.back()=0;CHECK(!copyText(&longText[0],reply)&&reply.text[0]=='o');
 MilesWire::Header h={};h.magic=MilesWire::Magic;h.version=MilesWire::Version;h.kind=MilesWire::Reply;h.opcode=MilesWire::AIL_last_error;
 std::vector<unsigned char> frame;copyText(0,reply);
 CHECK(MilesTransport::encodeResult(h,reply.result,MilesTransport::Bytes(),MilesTransport::Bytes(),frame)&&frame.size()==128&&frame[116]==1&&frame[112]==0);
 copyText("",reply);
 CHECK(MilesTransport::encodeResult(h,reply.result,MilesTransport::Bytes(),MilesTransport::Bytes(&reply.text[0],reply.text.size()),frame)&&frame.size()==129&&frame[108]==128&&frame[112]==1&&frame[116]==0&&frame[128]==0);
 reply=Reply();reply.result.return_bits=0xffffffffu;
 CHECK(MilesTransport::encodeResult(h,reply.result,MilesTransport::Bytes(),MilesTransport::Bytes(),frame)&&frame[52]==255&&frame[53]==255&&frame[54]==255&&frame[55]==255);
 MilesWire::Call c={};c.value[0]=1;CHECK(validate(MilesWire::AIL_get_preference,c,MilesTransport::Bytes())==Complete);
 c.value[0]=42;CHECK(validate(MilesWire::AIL_get_preference,c,MilesTransport::Bytes())==Complete);
 c.value[0]=999;CHECK(validate(MilesWire::AIL_get_preference,c,MilesTransport::Bytes())==InvalidFields);
 c.value[0]=42;c.value[1]=16;CHECK(validate(MilesWire::AIL_set_preference,c,MilesTransport::Bytes())==Complete);
 c.value[1]=64;CHECK(validate(MilesWire::AIL_set_preference,c,MilesTransport::Bytes())==Complete);
 c.value[1]=0xffffffffu;CHECK(validate(MilesWire::AIL_set_preference,c,MilesTransport::Bytes())==InvalidFields);
 c=MilesWire::Call();c.output_mask=8;CHECK(validate(MilesWire::AIL_speaker_configuration,c,MilesTransport::Bytes())==Complete);
 c.output_mask=24;CHECK(validate(MilesWire::AIL_speaker_configuration,c,MilesTransport::Bytes())==InvalidFields);
 c.output_mask=0;CHECK(validate(MilesWire::AIL_speaker_configuration,c,MilesTransport::Bytes())==InvalidFields);
 c=MilesWire::Call();const char path[]="miles";c.text.length=sizeof path;
 CHECK(validate(MilesWire::AIL_set_redist_directory,c,MilesTransport::Bytes(path,sizeof path))==Complete);
 c.text.length--;CHECK(validate(MilesWire::AIL_set_redist_directory,c,MilesTransport::Bytes(path,sizeof path))==InvalidFields);
 c.text.offset=UINT32_MAX;CHECK(validate(MilesWire::AIL_set_redist_directory,c,MilesTransport::Bytes(path,sizeof path))==InvalidFields);
 c=MilesWire::Call();c.text.length=3;const char embedded[]={'a',0,0};CHECK(validate(MilesWire::AIL_set_redist_directory,c,MilesTransport::Bytes(embedded,3))==InvalidFields);
 c=MilesWire::Call();c.value[7]=1;CHECK(validate(MilesWire::AIL_last_error,c,MilesTransport::Bytes())==InvalidFields);
 c=MilesWire::Call();c.callback=1;CHECK(validate(MilesWire::AIL_last_error,c,MilesTransport::Bytes())==InvalidFields);
 c=MilesWire::Call();c.resource.kind=MilesWire::Buffer;CHECK(validate(MilesWire::AIL_last_error,c,MilesTransport::Bytes())==InvalidFields);
 c=MilesWire::Call();CHECK(validate(MilesWire::AIL_startup,c,MilesTransport::Bytes())==Unsupported);
 h.kind=MilesWire::Request;h.opcode=MilesWire::AIL_set_redist_directory;c=MilesWire::Call();
 std::vector<unsigned char> requestText(RequestTextLimit,'a');requestText.back()=0;
 CHECK(MilesTransport::encodeCall(h,c,MilesTransport::Bytes(),MilesTransport::Bytes(&requestText[0],requestText.size()),frame)&&frame.size()==MilesWire::MaxFrameBytes);
 MilesWire::Header parsedHeader={};MilesWire::Call parsedCall={};
 CHECK(MilesTransport::decodeCall(MilesTransport::Bytes(&frame[0],frame.size()),parsedHeader,parsedCall));
 CHECK(parsedCall.text.offset==136&&parsedCall.text.length==RequestTextLimit&&validate(h.opcode,parsedCall,MilesTransport::Bytes(&frame[0],frame.size()))==Complete);
 requestText.insert(requestText.begin(),'a');
 CHECK(!MilesTransport::encodeCall(h,c,MilesTransport::Bytes(),MilesTransport::Bytes(&requestText[0],requestText.size()),frame));
 c.text.length=static_cast<uint32_t>(requestText.size());CHECK(validate(h.opcode,c,MilesTransport::Bytes(&requestText[0],requestText.size()))==InvalidFields);
 SessionInputs retained;char temporary[]="miles";const char* saved=retained.retain(MilesTransport::Bytes(temporary,sizeof temporary));
 CHECK(saved!=0);temporary[0]='X';CHECK(saved&&!std::strcmp(saved,"miles"));
 CHECK(retained.retainedBytes()==6);CHECK(retained.retain(MilesTransport::Bytes())==0&&retained.retainedBytes()==6);
 printf("%u/%u metadata wire checks\n",checks-failures,checks);return failures||checks!=39?1:0;
}
