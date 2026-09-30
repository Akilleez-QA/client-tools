#include "../ClientMilesStartup.h"
#include <Mss.h>
#include <type_traits>

#if !defined(_WIN64) || _MSC_VER != 1800
#error Requires the actual v120 x64 target and possessed private Miles 7.2a header.
#endif

static_assert(std::is_same<uintptr_t, UINTa>::value, "native file identity width/type");
static_assert(std::is_same<intptr_t, SINTa>::value, "native signed address type");
static_assert(std::is_same<uint32_t, U32>::value, "native count type");
static_assert(std::is_same<int32_t, S32>::value, "native offset/result type");
static_assert(std::is_same<float, F32>::value, "native spatial scalar type");
static_assert(std::is_same<ClientMiles::FileOpenCallback, AIL_file_open_callback>::value,
              "existing reviewed file-open signature");
static_assert(std::is_same<ClientMiles::FileCloseCallback, AIL_file_close_callback>::value,
              "existing reviewed file-close signature");
static_assert(std::is_same<ClientMiles::FileSeekCallback, AIL_file_seek_callback>::value,
              "existing reviewed file-seek signature");
static_assert(std::is_same<ClientMiles::FileReadCallback, AIL_file_read_callback>::value,
              "existing reviewed file-read signature");
static_assert(std::is_same<decltype(&ClientMiles::set_file_callbacks),
                          decltype(&::AIL_set_file_callbacks)>::value, "registration signature");
static_assert(std::is_same<decltype(&ClientMiles::serve), decltype(&::AIL_serve)>::value,
              "serve signature");
// Driver arguments intentionally use the local opaque facade identity. Check
// SDK-facing signatures separately instead of claiming whole-facade ABI equality.
static_assert(std::is_same<decltype(&::AIL_set_listener_3D_position),
                          void (AILCALL *)(::HDIGDRIVER, F32, F32, F32)>::value, "position");
static_assert(std::is_same<decltype(&::AIL_set_listener_3D_velocity_vector),
                          void (AILCALL *)(::HDIGDRIVER, F32, F32, F32)>::value, "velocity");
static_assert(std::is_same<decltype(&::AIL_set_listener_3D_orientation),
                          void (AILCALL *)(::HDIGDRIVER, F32, F32, F32, F32, F32, F32)>::value,
              "orientation");
static_assert(std::is_same<decltype(&::AIL_set_3D_rolloff_factor),
                          void (AILCALL *)(::HDIGDRIVER, F32)>::value, "rolloff");
static_assert(std::is_same<decltype(&::AIL_room_type), S32 (AILCALL *)(::HDIGDRIVER)>::value,
              "room query");
static_assert(std::is_same<decltype(&::AIL_set_room_type),
                          void (AILCALL *)(::HDIGDRIVER, S32)>::value, "room setter");

namespace ClientMiles {
void set_file_callbacks(FileOpenCallback open, FileCloseCallback close,
                        FileSeekCallback seek, FileReadCallback read) {
    ::AIL_set_file_callbacks(open, close, seek, read);
}
void set_listener_3D_position(HDIGDRIVER driver, float x, float y, float z) {
    ::AIL_set_listener_3D_position(reinterpret_cast<::HDIGDRIVER>(driver), x, y, z);
}
void set_listener_3D_velocity_vector(HDIGDRIVER driver, float x, float y, float z) {
    ::AIL_set_listener_3D_velocity_vector(reinterpret_cast<::HDIGDRIVER>(driver), x, y, z);
}
void set_listener_3D_orientation(HDIGDRIVER driver, float x, float y, float z,
                                 float upX, float upY, float upZ) {
    ::AIL_set_listener_3D_orientation(reinterpret_cast<::HDIGDRIVER>(driver),
                                      x, y, z, upX, upY, upZ);
}
void set_3D_rolloff_factor(HDIGDRIVER driver, float factor) {
    ::AIL_set_3D_rolloff_factor(reinterpret_cast<::HDIGDRIVER>(driver), factor);
}
void serve() { ::AIL_serve(); }
int32_t room_type(HDIGDRIVER driver) {
    return ::AIL_room_type(reinterpret_cast<::HDIGDRIVER>(driver));
}
void set_room_type(HDIGDRIVER driver, int32_t room) {
    ::AIL_set_room_type(reinterpret_cast<::HDIGDRIVER>(driver), room);
}
} // namespace ClientMiles
