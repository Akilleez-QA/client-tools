#include "../ClientMilesStartup.h"
#include "../../reverse-file-seam20/ClientAudioFileCallbacks.h"
#include <type_traits>
using namespace ClientMiles;
static_assert(std::is_same<decltype(ClientAudioFileCallbacks::LocalFileHandle::value),
                          uintptr_t>::value, "existing local file service identity");
static_assert(std::is_same<decltype(ClientAudioFileCallbacks::OpenResult::callbackResult),
                          uint32_t>::value, "existing open status remains separate");
static_assert(std::is_same<decltype(&serve), void (*)()>::value, "serve granularity");
static_assert(std::is_same<decltype(&set_file_callbacks),
              void (*)(FileOpenCallback, FileCloseCallback, FileSeekCallback, FileReadCallback)>::value,
              "callback registration remains four typed local callbacks");
static_assert(std::is_same<decltype(&set_listener_3D_position),
                          void (*)(HDIGDRIVER, float, float, float)>::value, "position");
static_assert(std::is_same<decltype(&set_listener_3D_velocity_vector),
                          void (*)(HDIGDRIVER, float, float, float)>::value, "velocity");
static_assert(std::is_same<decltype(&set_listener_3D_orientation),
                          void (*)(HDIGDRIVER, float, float, float, float, float, float)>::value,
              "orientation");
static_assert(std::is_same<decltype(&set_3D_rolloff_factor),
                          void (*)(HDIGDRIVER, float)>::value, "rolloff");
static_assert(std::is_same<decltype(&room_type), int32_t (*)(HDIGDRIVER)>::value, "room query");
static_assert(std::is_same<decltype(&set_room_type),
                          void (*)(HDIGDRIVER, int32_t)>::value, "room setter");
