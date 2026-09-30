#ifndef CLIENT_MILES_NATIVE_STARTUP25_H
#define CLIENT_MILES_NATIVE_STARTUP25_H
#include "../backend-boundary24/ClientMiles.h"

#if defined(_WIN32)
#define CLIENT_MILES25_CALLBACK __stdcall
#else
#define CLIENT_MILES25_CALLBACK
#endif

namespace ClientMiles {
// Same callback shapes as the existing reviewed SDK signature checks. These
// are process-local callbacks; see CALLBACK-ADAPTATION.md before integration.
typedef uint32_t (CLIENT_MILES25_CALLBACK *FileOpenCallback)(char const *, uintptr_t *);
typedef void (CLIENT_MILES25_CALLBACK *FileCloseCallback)(uintptr_t);
typedef int32_t (CLIENT_MILES25_CALLBACK *FileSeekCallback)(uintptr_t, int32_t, uint32_t);
typedef uint32_t (CLIENT_MILES25_CALLBACK *FileReadCallback)(uintptr_t, void *, uint32_t);

void set_file_callbacks(FileOpenCallback open, FileCloseCallback close,
                        FileSeekCallback seek, FileReadCallback read);
void set_listener_3D_position(HDIGDRIVER driver, float x, float y, float z);
void set_listener_3D_velocity_vector(HDIGDRIVER driver, float x, float y, float z);
void set_listener_3D_orientation(HDIGDRIVER driver, float faceX, float faceY, float faceZ,
                                 float upX, float upY, float upZ);
void set_3D_rolloff_factor(HDIGDRIVER driver, float factor);
void serve();
int32_t room_type(HDIGDRIVER driver);
void set_room_type(HDIGDRIVER driver, int32_t room);
} // namespace ClientMiles
#endif
