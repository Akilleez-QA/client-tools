// Header compatibility only; not actual Audio bodies, linked, or executed.
#include "sharedFoundation/FirstSharedFoundation.h"
#include "candidate/ClientMiles.h"
extern uint32_t __stdcall plainProbeOpen(const char *, uintptr_t *);
extern void __stdcall plainProbeClose(uintptr_t);
extern int32_t __stdcall plainProbeSeek(uintptr_t, int32_t, uint32_t);
extern uint32_t __stdcall plainProbeRead(uintptr_t, void *, uint32_t);
void probePlainStartupHeader()
{
    char version[256];
    ClientMiles::MSS_version(version, 256);
    (void)ClientMiles::startup();
    (void)ClientMiles::last_error();
    (void)ClientMiles::set_redist_directory("miles");
    intptr_t value=ClientMiles::get_preference(ClientMiles::MixerChannels);
    (void)ClientMiles::set_preference(ClientMiles::MixerChannels,value);
    ClientMiles::set_file_callbacks(plainProbeOpen,plainProbeClose,plainProbeSeek,plainProbeRead);
    ClientMiles::shutdown();
}
