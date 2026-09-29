# DPVS: add x64 support with a bounded legacy numerical compatibility repair

DPVS currently treats Windows as x86, enabling unsupported inline assembly and using a 32-bit pointer integer in x64 builds. The first four commits select existing portable paths on x64, use pointer-width storage, supply timer/prefetch intrinsics, preserve 64-byte matrix-cache entries and isolate Debug/Release project outputs. The fifth independently reviewable commit uses double intermediates for x64 plane dots and exact-product raster flooring. Win32 assembly stays unchanged.

The branch is based directly on upstream `94945103`, with no wire changes or full-client configuration prototype. Review size: 39 changed C++/header lines and 73 project XML lines, five files.

Validation: native VS2013 DPVS project rebuilds pass for Win32/x64 Debug/Release. Each fresh DLL passes 192 stress queries and 64 fixed-cost occlusion frames. Win32 Release code/data/resources/relocations are byte-identical to upstream; whole-DLL equality requires normalizing PE/debug timestamps, PDB identity/path case and embedded compile time.

The separate numerical fixtures compare real Win32 assembly forced to PC64 against the final candidate. They found zero sampled caller classification/raster differences, one negative dot differing by one ULP, and 15 min/max signed-zero differences outside the repair. This is bounded evidence, not general numerical equivalence. The source trace under Proton associates PC64 with SWG's existing FPU setter/collision bug; native Direct3D could still change the state. Reassess this repair together with any setter-bug fix.

Open: native Direct3D tracing, allocation-size narrowing, broader Optimized mappings, full-client x64 linking and representative gameplay. Warnings remain. No stubs or feature removals.

Three additional integer paths switch from hand-written x86 code to C++ on x64: highest-set-bit search (`dpvsBitMath`), the byte-reordering return path (`dpvsFiller.hpp`), and the MMX occlusion-buffer cache filler (`dpvsOcclusionBuffer_CacheFiller.cpp`). They have no isolated differential comparison; the integration probes provide indirect coverage without establishing every branch/input or exact integer equivalence.

Raster overflow/non-finite inputs remain untested: converting a floored value outside the `INT32` range with a C++ cast is undefined, whereas x87 `fistp` has invalid-conversion handling (integer indefinite `0x80000000` when the invalid exception is masked). The current fixtures do not establish caller bounds or equivalent handling outside the tested range.

Evidence: [validation report](https://github.com/Akilleez-QA/client-tools/blob/review/client-x64-evidence/review/client-x64/C-dpvs/RESULTS.md), [parsed build/runtime results](https://github.com/Akilleez-QA/client-tools/blob/review/client-x64-evidence/review/client-x64/C-dpvs/verified-results.json), [DLL comparison](https://github.com/Akilleez-QA/client-tools/blob/review/client-x64-evidence/review/client-x64/C-dpvs/dll-comparison.json), and [native logs](https://github.com/Akilleez-QA/client-tools/tree/review/client-x64-evidence/review/client-x64/C-dpvs/native-text).
