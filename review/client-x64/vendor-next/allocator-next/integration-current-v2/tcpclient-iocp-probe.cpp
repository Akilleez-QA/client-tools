#include <windows.h>
#include <stdio.h>
int main() {
 HANDLE port=CreateIoCompletionPort(INVALID_HANDLE_VALUE,0,0,1);
 if(!port)return 1;
 ULONG_PTR expected=static_cast<ULONG_PTR>(0xabcdef01UL);
#ifdef _WIN64
 expected|=static_cast<ULONG_PTR>(0x12345678UL)<<32;
#endif
 OVERLAPPED operation={};
 if(!PostQueuedCompletionStatus(port,37,expected,&operation)){CloseHandle(port);return 2;}
 struct GuardedKey {ULONG_PTR before,key,after;} got={123,0,456};
 DWORD bytes=0;LPOVERLAPPED returned=0;
 if(!GetQueuedCompletionStatus(port,&bytes,&got.key,&returned,1000)){CloseHandle(port);return 3;}
 if(bytes!=37 || got.key!=expected || returned!=&operation || got.before!=123 || got.after!=456){CloseHandle(port);return 4;}
 CloseHandle(port);
 puts("PASS real IOCP posted key, byte count, overlapped identity, and adjacent guards");
 return 0;
}
