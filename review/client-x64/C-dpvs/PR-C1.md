# DPVS: add x64 architecture support and isolated project builds

DPVS currently treats Windows as x86, enabling unsupported inline assembly and using a 32-bit pointer integer in x64 builds. This four-commit series selects the existing portable paths on x64, uses pointer-width storage, supplies timer/prefetch intrinsics and preserves the matrix cache's required 64-byte entry size. Its project gains isolated Debug/Release x64 outputs. Win32's assembly and layout stay intact.

The branch is based directly on upstream `94945103`, with no wire changes or full-client configuration prototype. Review size: 28 changed C++/header lines and 73 project XML lines, five files.

Validation: native VS2013 DPVS project rebuilds pass for Win32/x64 Debug/Release. Each DLL passes 192 stress queries and 64 fixed-cost occlusion frames. Win32 Release code, data, resources and relocations are byte-identical to upstream; the whole DLL matches after normalizing PE/debug timestamps, PDB identity/path case and the embedded compile-time string. The build emits existing/port warnings; this is not a warning-free claim.

Known limits: numerical scalar differences remain open in this variant, as do allocation-size narrowing, native Direct3D FPU verification, full-client linkage and gameplay validation. The broader solution's Optimized mapping is not addressed. No stubs or feature removals.

Evidence: [validation report](RESULTS.md), [parsed build/runtime results](verified-results.json), [DLL comparison](dll-comparison.json), and [native logs](native-text/).
