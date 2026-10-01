# Preserve Windows diagnostic pointers and timestamp reads on x64

Four focused commits remove x64-only assembly and pointer-width failures in existing diagnostic paths:

- Read the profiler timestamp counter with `__rdtsc` on x64; retain Win32 assembly and the existing counter selection/calibration policy.
- Pass `ULONG_PTR` entries and the matching element count to the thread-naming exception API.
- Store and retrieve the status-window object with `SetWindowLongPtr`/`GetWindowLongPtr`, including a `LONG_PTR` result; preserve the existing error check.
- Format the existing exception-address pointer with `%p` instead of the 32-bit `%08x` conversion.

Directly on master, four source files, +14/−4. There are no build changes or unrelated ShellExecute/allocator edits. Each original patch applied without conflict.

Existing native evidence:

- [Profiler results](https://github.com/Akilleez-QA/client-tools/blob/071cb6def2710b13055f330f9b311afda67ed79c/review/client-x64/assembly-next/timer-results.json): the exact candidate source compiled in Win32/x64 Debug/Release. Its extracted counter helper passed 10,000 bracketed samples per configuration; stock Win32 passed, stock x64 assembly failed, and zero-return controls failed. This does not test full profiler initialization, calibration or cross-core synchronization.
- [Crash-format results](https://github.com/Akilleez-QA/client-tools/blob/071cb6def2710b13055f330f9b311afda67ed79c/review/client-x64/vendor-next/warning-fixes-next/crash-format-results.json): the production formatting statement passed 36 checks per configuration with genuine Windows exception-record types, including high-address and buffer-canary checks. No crash was induced; it is not a full exception-handler test.

Thread naming and status-window routing are source-reviewed, without a separate isolated runtime result. Native evidence uses its recorded integrated dependencies, not a new build of this master-based branch. No builds or runtime were repeated during packaging.
