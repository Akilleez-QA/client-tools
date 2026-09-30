// Compile against the checkout's unmodified production headers; no wrapper stubs.
// SOCKET_PROBE_UDP: 0=no UDP header, 1=main UDP header, 2=VChat UDP header.
// SOCKET_PROBE_WINSOCK_FIRST: exercise both include orders.
#ifndef SOCKET_PROBE_SOCK
#define SOCKET_PROBE_SOCK 1
#endif
#ifndef SOCKET_PROBE_UDP
#define SOCKET_PROBE_UDP 1
#endif
#ifndef SOCKET_PROBE_WINSOCK_FIRST
#define SOCKET_PROBE_WINSOCK_FIRST 1
#endif
#ifndef WIN32
#error Build this probe with /DWIN32, including when targeting amd64.
#endif
#define WIN32_LEAN_AND_MEAN
#define NOMINMAX
#if SOCKET_PROBE_WINSOCK_FIRST
#include <winsock2.h>
#include <windows.h>
#endif
#if SOCKET_PROBE_SOCK
#include "engine/shared/library/sharedNetwork/src/win32/Sock.h"
#endif
#if SOCKET_PROBE_UDP == 1
#include "external/3rd/library/udplibrary/UdpLibrary.hpp"
#elif SOCKET_PROBE_UDP == 2
#include "external/3rd/library/soePlatform/VChatAPI/utils2.0/utils/UdpLibrary/UdpLibrary.hpp"
#elif SOCKET_PROBE_UDP != 0
#error Invalid SOCKET_PROBE_UDP value
#endif
#if !SOCKET_PROBE_WINSOCK_FIRST
#include <winsock2.h>
#include <windows.h>
#endif
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// An unevaluated reference to the production protected member, no construction,
// implementation substitute, fake object storage, or call through an invalid object.
#if SOCKET_PROBE_SOCK
struct SockLayoutProbe : Sock {
 static void verify() {
 static_assert(sizeof(((SockLayoutProbe *)0)->handle) == sizeof(SOCKET), "Sock::handle truncates SOCKET");
 static_assert(sizeof(((SockLayoutProbe *)0)->handle) == sizeof(void *), "Sock::handle must be pointer-sized");
 }
};
static_assert(sizeof(SOCK_ERROR) == 4, "SOCK_ERROR is an API result, not a handle");
static_assert(SOCK_ERROR == 0xffffffffU, "legacy recvfrom failure sentinel");
#endif
static_assert(sizeof(SOCKET) == sizeof(void *), "SOCKET width");

static int checks = 0;
static void require(bool condition, char const *name) {
 if (!condition) {
  fprintf(stderr,"FAIL %s winerr=%lu wsaerr=%d\n",name,GetLastError(),WSAGetLastError());
  exit(1);
 }
 ++checks;
 printf("PASS %s\n",name);
}
static void udp() {
 WSADATA data;
 require(WSAStartup(MAKEWORD(2,2),&data)==0,"WSAStartup");
 SOCKET receiveSocket=socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP);
 require(receiveSocket!=INVALID_SOCKET,"UDP receiver socket");
 SOCKET sendSocket=socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP);
 require(sendSocket!=INVALID_SOCKET,"UDP sender socket");
 DWORD timeout=3000;
 require(setsockopt(receiveSocket,SOL_SOCKET,SO_RCVTIMEO,reinterpret_cast<char const *>(&timeout),sizeof(timeout))==0,"UDP bounded receive timeout");
 sockaddr_in address;
 memset(&address,0,sizeof(address));
 address.sin_family=AF_INET;
 address.sin_addr.s_addr=htonl(INADDR_LOOPBACK);
 address.sin_port=0;
 require(bind(receiveSocket,reinterpret_cast<sockaddr *>(&address),sizeof(address))==0,"UDP bind loopback ephemeral");
 int addressLength=sizeof(address);
 require(getsockname(receiveSocket,reinterpret_cast<sockaddr *>(&address),&addressLength)==0 && address.sin_port!=0,"UDP getsockname");
 char const payload[]="production-header socket probe";
 require(sendto(sendSocket,payload,sizeof(payload),0,reinterpret_cast<sockaddr *>(&address),sizeof(address))==sizeof(payload),"UDP sendto");
 char output[128]={0};
 sockaddr_in source;
 int sourceLength=sizeof(source);
 int length=recvfrom(receiveSocket,output,sizeof(output),0,reinterpret_cast<sockaddr *>(&source),&sourceLength);
 require(length==sizeof(payload) && memcmp(output,payload,sizeof(payload))==0,"UDP recvfrom bytes");
 require(source.sin_addr.s_addr==htonl(INADDR_LOOPBACK),"UDP source loopback");
 require(closesocket(sendSocket)==0,"UDP close sender");
 require(closesocket(receiveSocket)==0,"UDP close receiver");
 require(WSACleanup()==0,"WSACleanup");
}
static void completionPorts() {
 HANDLE port=CreateIoCompletionPort(INVALID_HANDLE_VALUE,NULL,0,1);
 require(port!=NULL,"IOCP create");
 ULONG_PTR keys[2]={0,0};
#ifdef _WIN64
 keys[1]=static_cast<ULONG_PTR>(0x12345678abcdef01ULL);
#else
 keys[1]=static_cast<ULONG_PTR>(0xabcdef01UL);
#endif
 for (int i=0;i!=2;++i) {
  OVERLAPPED submitted;
  memset(&submitted,0,sizeof(submitted));
  DWORD const sent=static_cast<DWORD>(17+i);
  require(PostQueuedCompletionStatus(port,sent,keys[i],&submitted)!=FALSE,"IOCP post");
  DWORD bytes=0;
  ULONG_PTR key=0;
  OVERLAPPED *received=NULL;
  require(GetQueuedCompletionStatus(port,&bytes,&key,&received,3000)!=FALSE,"IOCP get");
  require(bytes==sent && key==keys[i] && received==&submitted,"IOCP exact bytes/key/overlapped");
 }
 require(CloseHandle(port)!=FALSE,"IOCP close");
}
int main() {
 udp();
 completionPorts();
 require(checks==20,"expected prior check count");
 printf("SUMMARY PASS checks=%d pointer_bytes=%u udp_header=%d winsock_first=%d\n",checks,static_cast<unsigned>(sizeof(void *)),SOCKET_PROBE_UDP,SOCKET_PROBE_WINSOCK_FIRST);
 return 0;
}
