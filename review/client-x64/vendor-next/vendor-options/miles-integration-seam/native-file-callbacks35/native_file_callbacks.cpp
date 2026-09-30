#include "ClientMilesFileCallbacks.h"
#include <Mss.h>
#include <type_traits>

#if !defined(_WIN64) || _MSC_VER != 1800
#error Requires actual v120 x64 and the pinned private Miles 7.2a header.
#endif

static_assert(std::is_same<ClientMiles::FileHandle, UINTa>::value, "exact native handle type");
static_assert(std::is_same<int32_t, S32>::value, "exact signed seek type");
static_assert(std::is_same<uint32_t, U32>::value, "exact unsigned result/count type");
static_assert(std::is_same<char, MSS_FILE>::value, "native filename character type");
static_assert(std::is_same<ClientMiles::FileOpenCallback, AIL_file_open_callback>::value, "open callback ABI");
static_assert(std::is_same<ClientMiles::FileCloseCallback, AIL_file_close_callback>::value, "close callback ABI");
static_assert(std::is_same<ClientMiles::FileSeekCallback, AIL_file_seek_callback>::value, "seek callback ABI");
static_assert(std::is_same<ClientMiles::FileReadCallback, AIL_file_read_callback>::value, "read callback ABI");
static_assert(std::is_same<decltype(&::AIL_set_file_callbacks),
    void (AILCALL *)(AIL_file_open_callback, AIL_file_close_callback,
                     AIL_file_seek_callback, AIL_file_read_callback)>::value,
    "actual native registration signature");

namespace ClientMiles
{
void set_file_callbacks(FileOpenCallback open, FileCloseCallback close,
                        FileSeekCallback seek, FileReadCallback read)
{
    ::AIL_set_file_callbacks(open, close, seek, read);
}
}
