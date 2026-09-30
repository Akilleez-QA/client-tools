#define _CRT_SECURE_NO_WARNINGS
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#ifdef _WIN64
#define TEST_ADDRESS uintptr_t(0x1234567887654321ull)
#else
#define TEST_ADDRESS uintptr_t(0x87654321u)
#endif
int main(){unsigned checks=0; uintptr_t addresses[]={0,1,~uintptr_t(0),TEST_ADDRESS};for(unsigned i=0;i<4;++i){EXCEPTION_RECORD record={0};record.ExceptionCode=0xc0000005;record.ExceptionAddress=reinterpret_cast<void*>(addresses[i]);EXCEPTION_POINTERS state={&record,0};LPEXCEPTION_POINTERS exceptionPointers=&state;struct {unsigned char before[8];char buffer[128];unsigned char after[8];} guarded;memset(&guarded,0xa5,sizeof(guarded));char *buffer=guarded.buffer;
sprintf(buffer, "Exception %08x(%d)=code %p=addr\n", exceptionPointers->ExceptionRecord->ExceptionCode, exceptionPointers->ExceptionRecord->ExceptionCode, exceptionPointers->ExceptionRecord->ExceptionAddress);
char expected[32];sprintf(expected,"%p=addr\n",record.ExceptionAddress);++checks;if(!strstr(buffer,expected))return 1;for(unsigned n=0;n<8;++n){++checks;if(guarded.before[n]!=0xa5||guarded.after[n]!=0xa5)return 2;}printf("%s",buffer);}printf("checks=%u failures=0 expected=36\n",checks);return checks==36?0:3;}
