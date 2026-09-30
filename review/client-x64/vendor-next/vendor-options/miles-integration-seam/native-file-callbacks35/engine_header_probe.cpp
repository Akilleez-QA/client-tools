// Compile with original engine STLport includes; this is not linked or executed.
#include "sharedFoundation/FirstSharedFoundation.h"
#include "ClientMilesFileCallbacks.h"
#include "../file-executor29/ClientAudioFileCallbacks.h"

// Exact original Audio callback shapes expressed without the private SDK.
extern uint32_t __stdcall fileOpenCallBack(char const *, uintptr_t *);
extern void __stdcall fileCloseCallBack(uintptr_t);
extern int32_t __stdcall fileSeekCallBack(uintptr_t, int32_t, uint32_t);
extern uint32_t __stdcall fileReadCallBack(uintptr_t, void *, uint32_t);
void compileOriginalFileCallbackRegistration()
{
    ClientMiles::set_file_callbacks(fileOpenCallBack, fileCloseCallBack,
                                    fileSeekCallBack, fileReadCallBack);
}
