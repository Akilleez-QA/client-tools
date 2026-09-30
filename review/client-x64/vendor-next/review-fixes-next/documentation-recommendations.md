# Read-only documentation recommendations

Assessed client HEAD `0d2f8c168165dce3e629866c76e1a697fae8318c` and historical `d905d525` / `1c901436`. No DebugHelp/FPU code or existing commits changed. These are proposed release-note / follow-up documentation paragraphs for parent review, not amendments to published history.

## DebugHelp affects Win32 as well as x64 — confirmed

`src/engine/shared/library/sharedDebug/src/win32/DebugHelp.cpp`:

- `ScopedDebugHelpLock` at 64–74 is unconditional. `getCallStack` acquires it at 531 and retains it through the loop at 564–572 on both architectures. Previously the critical section covered context capture only.
- `StackWalk64` at 566 now receives `GetCurrentThread()` as hThread on both architectures. The prior call supplied the process handle in both slots. `ReadMemoryRoutine` is NULL, so the documented arbitrary-token exception is inapplicable.
- `loadSymbolsForDll` (505), `lookupAddress` (615), and `writeMiniDump` (662) each hold the same lock for their own operation. This does **not** mean one uninterrupted lock covers `reportCallStack` capture plus every subsequent lookup; those are separate calls/acquisitions.
- x64-specific work remains gated: native system DbgHelp loading, RtlCaptureContext/AMD64 registers, and bypass of the function-table pointer cache. Win32 keeps the bundled DLL, x86 context assembly, IMAGE_FILE_MACHINE_I386, and cached callback path. The `uint64` call-stack element API/storage change also affects Win32 callers, separately from the allocator's preserved Win32 OwnerAddress typedef.

Recommended text:

> The DbgHelp repair intentionally changes both Win32 and x64: stack walking now receives the current thread handle, and complete stack walks, symbol operations, and minidump writes are serialized by the shared critical section. Architecture-specific context capture, DLL selection, and x64 function-table cache bypass remain separately gated. Win32 allocator owner/export compatibility does not imply unchanged Win32 diagnostics behavior.

Recommendation: document the intended shared fix rather than adding an unrequested x64 gate. Microsoft documents DbgHelp as single threaded and requires caller serialization. [StackWalk documentation](https://learn.microsoft.com/en-us/windows/win32/api/dbghelp/nf-dbghelp-stackwalk).

Lock-order limitation: allocator paths acquire the MemoryManager critical section before calling DebugHelp. That is an observed order, **not a global deadlock proof**: callbacks, allocation during symbol/dump work, concurrent shutdown/module unloading, and callers outside this wrapper have not been exhaustively analyzed or tested here. Initialization/removal and pre-lock `library` checks are not a new thread-safe lifetime guarantee. Do not claim “no deadlock” from this bounded review.

## FPU FTZ/DAZ restoration — confirmed with narrower wording

`src/engine/shared/library/sharedFoundation/src/win32/FloatingPointUnit.cpp`:

- x64 `CONTROL_MASK = 0xffc0` (29) includes DAZ bit 6 and FTZ bit 15, masks 7–12, and rounding 13–14; it excludes sticky flags 0–5.
- `install` (67–127) reads incoming control and modifies rounding/exception masks. It preserves incoming DAZ/FTZ; it does not unconditionally enable or disable them.
- `update` (131–143) compares current control with cached `status` and restores the cache on mismatch. `setControlWord` (162–173) merges only the control mask, retaining current sticky flags and upper reserved bits. Raw `setControlWord` does not update cached `status`.
- `Os::update` at Os.cpp:705 calls this update; Game.cpp:1080 invokes Os::update in its main loop. Thus “at each Os update, normally each game frame” is more precise than an unconditional timing guarantee.
- MXCSR belongs to the calling thread. A library/driver change on that thread is undone at the next update (and cached bits may also be reapplied by setters); no all-thread enforcement is established. Cached class state is shared, not newly thread-local policy.
- The Win32 branch still accesses the x87 control word and preserves its legacy precision-setter behavior; it does not newly manage MXCSR FTZ/DAZ.

Recommended text:

> On x64, installation preserves incoming FTZ/DAZ in the saved MXCSR policy. Each Os update restores that saved policy on the calling thread if control bits have changed, so intervening library changes to FTZ/DAZ do not persist across an update. Sticky exception flags are retained. This differs from the legacy Win32 x87-only control path; it does not promise cross-thread policy enforcement or numerical parity.

Existing `allocator-next/fpu-next-plan.md` already describes this control contract; `fpu-cross-review.md` explicitly excludes actual traps. Historical evidence is not rerun or upgraded to new acceptance here.

## Exception-code claim — not established; do not publish as universal fact

The source confirms that x64 exception configuration manipulates SSE MXCSR masks, whereas Win32 manipulates x87 masks. It contains **no mapping** from hardware FP exceptions to Windows SEH codes. The switch to MXCSR alone cannot prove that every unmasked fault changes to `STATUS_FLOAT_MULTIPLE_*` or that all legacy-code filters fail.

Microsoft defines `STATUS_FLOAT_MULTIPLE_FAULTS` (0xC00002B4) and `STATUS_FLOAT_MULTIPLE_TRAPS` (0xC00002B5), but the definitions alone do not establish when the target OS delivers them. [Microsoft NTSTATUS definitions](https://learn.microsoft.com/fr-fr/openspecs/windows_protocols/ms-erref/596a1078-e883-4972-9bbc-49e60bebca55). Preserve this distinction rather than inferring universal dispatch from the names.

The first-party tree search for `EXCEPTION_FLT`, `STATUS_FLOAT`, `_FPE_`, and those two numeric codes in C++/headers found no named-code filter (empty `fp-exception-symbol-search.txt`). `SetupSharedFoundation.cpp:53–152` has a generic unhandled-exception logger/minidump route; its explicit code comparison at 112 handles the breakpoint/fatal case, not an x87-only FP whitelist. `Os.cpp:1359` is the separate debugger thread-naming exception handler. This is not proof about third-party DLL handlers or arbitrary numeric-code filters.

Recommended text:

> x64 exception-enable settings now govern SSE/MXCSR arithmetic. SEH exception classification and compatibility with any external FP-specific filter have not been validated for the target Windows/CRT configuration; do not assume all SIMD exceptions use the MULTIPLE codes or that the old filters necessarily miss every exception. The client's generic crash logger is not restricted to legacy x87 FP codes.

No unmasked FP operation, trap, allocator malformed case, or crash reproduction was executed. Any future exception-dispatch validation is a separately authorized task; it is not part of this candidate's acceptance, and must not reroute the rejected allocator workload.
