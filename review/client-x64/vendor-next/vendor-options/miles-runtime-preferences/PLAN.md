# Original DLL preference and startup control-state observation

Prospective, 2026-09-30. This is a narrow discriminator for contradictory header interpretations, not a game/audio fidelity test or a retry of the failed engine/allocator workload.

Artifact: original SWG Source v3 Mss32.dll SHA256 0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe; v120 Win32 standalone executable compiled against the existing genuine Mss.h. Native Windows VM, no audio device opened, no callbacks, assets, playback or allocator injection. Three fresh processes: inherited FPU state, explicit PC24, explicit PC64, changing only the x87 precision bits before DLL load. Raw x87 control/status and MXCSR recorded before/after load, startup, preference reads, shutdown and unload. Restore the original control word before exit.

Prediction from the matching Windows header: AIL_LOCK_PROTECTION(18)=0 and AIL_MUTEX_PROTECTION(44)=1 after successful startup in all three processes. These readings do not prove absence of every suspension path, behavior after device creation, game configuration, worker-thread FPU state or numerical fidelity. No prediction of FPU-state preservation: record any change without silently adjusting the host policy.

Oracle: exact load identity, startup nonzero, both actual preference values, each process exits normally after shutdown/unload. Header disagreement is retained as a failed prediction; it is not hidden by a generic process-success result. Stop on startup failure or unexpected crash; no retries or alteration to force a result. Native scratch is isolated, no VM drive mappings or shared source edited. Vendor DLL/header remain private; publish only authored source, command logs, hashes and measurements.

Context research: Microsoft _controlfp_s and _control87 documentation distinguish x87 precision from x64 MXCSR; this probe uses raw x87 instructions in a Win32 process, not an x64 imitation. RAD's current Miles development-history page describes different releases; it cannot establish behavior of the 7.2a binary. URLs and date recorded in RESULTS.

Compile attempt v1 did not execute: standalone use of DEFAULT_ALP/DEFAULT_AMPR expanded to SDK-private NO/YES tokens not declared by the public header. The successor prints and compares the predeclared 0/1 prediction explicitly; it does not redefine the SDK or alter vendor preferences. Original source and compiler failure retained.
