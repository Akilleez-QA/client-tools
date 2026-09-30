# Miles callback ABI repair: bounded native results

The production candidate is Audio.cpp SHA256 `3e731581ea3b1480c4af0273ada95796c88a2f91c4b65df79dd2c3cf426ddb7f`, +17/−15 lines. It uses the SDK's UINTa for all four file callback handle signatures, the private handle maps/counter and associated diagnostic formatting. U32 byte counts/S32 seek offsets remain unchanged. No SDK, backend, driver, asset or feature change.

Actual whole Audio.cpp compiles with native VS2013 v120 in Debug and Release on Win32 and x64, including direct assignment to all four real SDK callback pointer types without casts. Stock Win32 compiles; stock x64 rejects the mismatched callback types. Evidence: audio-compile-v1-agent.zip.

Runtime probes use exact hashed callback slices, genuine Foundation/File/core/STLport libraries, real TreeFile/SetupSharedFile and disk files. They call through actual SDK-typed function pointers. No Miles implementation is substituted; the vendor audio backend is not involved in these file-callback tests.

| Configuration | Candidate checks | Stock control |
|---|---:|---|
| Win32 Debug | 20/20 | 20/20 |
| Win32 Release | 18/18 | 18/18 |
| x64 Release | 18/18 | Callback type assignments fail compilation as expected |
| x64 Debug, corrected allocator minimum-size rule | 20/20 | Callback type assignments fail compilation as expected |

Checks cover distinct handles 7 and 0x100000007 on x64, separate read contents/positions, all three seek origins, EOF, independent close, absent-file failure clearing the full handle and output canaries. Debug adds handle-diagnostic map checks.

The original Debug x64 setup crash remains recorded. A diagnostic observer that never handles exceptions located it before callbacks: SetupSharedFoundation → MemoryManager::registerDebugFlags → DebugFlags vector reallocation → operator delete → MemoryManager::free. The allocator's minimum-block correction lets the same real setup and callbacks complete. The passing private relink uses candidate allocator SHA256 `172dcd8958b78af24ef4b08f1f0a2409e89ae81665fb2ef6717b9a24d161467f` and matching InstallTimer object. See debug-startup-investigation.md and audio-debug-investigation.zip. This requirement is explicit: the earlier Debug x64 allocator is not claimed to pass.

Original v1 lacked SetupSharedThread/Debug prerequisites; that failure is retained. Later fixtures use real ClientMain setup order. No initialization was bypassed or replaced. Failed logs remain evidence, not passes. Binaries stay in private VM directories; ZIPs preserve source, commands, maps, logs and results without binaries.

The SDK bound by the actual project is Miles 7.2a. A separate source inventory has 62 lexical AIL API names; 61 are real exports in the original 7.2a DLL and AIL_MSS_version is a resource-query macro. This runtime/export inventory is distinct from callback validation.

Limits: no full Audio::install, callback threading stress, handle exhaustion, x64 Miles binary, full client runtime or fidelity claim. The original-runtime decoder/playback exploration is documented separately in ../vendor-options/miles-probe/RESULTS.md. Parent owns the source commit; no production backend replacement was made.
