#ifndef INCLUDED_ClientMilesFileCallbacks_H
#define INCLUDED_ClientMilesFileCallbacks_H

// Plain engine-facing declarations: no SDK header, STL container or ownership.
#include <stdint.h>
#if !defined(_WIN32) || !defined(_MSC_VER)
#error This callback interface requires the Windows MSVC calling convention.
#endif

namespace ClientMiles
{
// Local native-width value, never a wire handle; successful open may return zero.
typedef uintptr_t FileHandle;
typedef uint32_t (__stdcall *FileOpenCallback)(char const *filename, FileHandle *handle);
typedef void (__stdcall *FileCloseCallback)(FileHandle handle);
typedef int32_t (__stdcall *FileSeekCallback)(FileHandle handle, int32_t offset, uint32_t origin);
typedef uint32_t (__stdcall *FileReadCallback)(FileHandle handle, void *buffer, uint32_t bytes);

// Ordinary C++ facade call; the private implementation uses SDK AILCALL.
// Direct backend forwards the four pointers without wrappers or thread changes.
// Caller owns callback code/state through vendor shutdown and proven quiescence.
// No registration token, TLS setup, lock, copy, or destruction is supplied here.
void set_file_callbacks(FileOpenCallback open, FileCloseCallback close,
                        FileSeekCallback seek, FileReadCallback read);
}
#endif
