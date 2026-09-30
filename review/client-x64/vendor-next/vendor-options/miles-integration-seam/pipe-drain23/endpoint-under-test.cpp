// Test-only interposition: application source snapshots are not instrumented.
#include "pipe-transport-candidate/endpoint.h"
BOOL WINAPI Drain23CancelIoEx(HANDLE,LPOVERLAPPED);
BOOL WINAPI Drain23ReadFile(HANDLE,LPVOID,DWORD,LPDWORD,LPOVERLAPPED);
BOOL WINAPI Drain23WriteFile(HANDLE,LPCVOID,DWORD,LPDWORD,LPOVERLAPPED);
BOOL WINAPI Drain23GetOverlappedResult(HANDLE,LPOVERLAPPED,LPDWORD,BOOL);
#define CancelIoEx Drain23CancelIoEx
#define ReadFile Drain23ReadFile
#define WriteFile Drain23WriteFile
#define GetOverlappedResult Drain23GetOverlappedResult
#include "pipe-transport-candidate/endpoint.cpp"
