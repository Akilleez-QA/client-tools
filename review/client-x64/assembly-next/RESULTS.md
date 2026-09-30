# Integer assembly checkpoint — 2026-09-30

**Later checkpoint:** [allocator, stack, FPU and math work at client 12bb88809](../allocator-math-next/RESULTS.md). The sections below describe the earlier integer batch and retain its original limits.

Commits only; no PRs opened or edited for this batch. Client integration head: [ff3c1742f](https://github.com/Akilleez-QA/client-tools/commit/ff3c1742fe5e02b1a84b59afb72867a889776dcf). Server Windows counterpart: [3bb838a2](https://github.com/Akilleez-QA/src/commit/3bb838a2). These continue the [prior integration checkpoint](../next-build/RESULTS.md).

## Changes

- **98388ee37:** Windows x64 ByteOrder uses 16/32-bit CRT byte swaps. Existing Win32 assembly and public signatures remain unchanged. Identical Windows source was committed server-first as 3bb838a2; Linux byte-order code is untouched.
- **ff3c1742f:** client-private HTTP recursive lock uses 32-bit interlocked bit-test/set and final-release exchange on x64. Existing Win32 assembly, caller control flow and exception policy remain unchanged. No server counterpart exists for this HTTP implementation.

The two client commits add 43 lines across two files. No FPU changes, allocator substitutes, SDK stubs or feature removals.

## Native results

VS2013/v120 on the existing Windows VM; Debug and Release, Win32 and x64. Probe compilation enforces `_MSC_VER == 1800`; object machine types are checked. Final guest source matches all 20,519 tracked files at ff3c1742f, with zero mismatches.

| Test | Candidate | Stock/control |
| --- | --- | --- |
| ByteOrder actual production translation unit | 166,631 input cases per configuration, both directions; all four configurations pass | Stock Win32 passes both configurations; stock x64 fails on naked/assembly; identity-swap mutants fail at `80000000` |
| HTTP actual-header `trylock`/`unlock` | 27/27 each configuration, including recursive exclusion, final release and 100,000 protected updates across four threads | Stock Win32 passes; stock x64 fails compilation; no-acquire and no-release mutants fail their expected runtime checks |
| Actual VeCritsec.cpp compilation | All four configurations compile | Standalone full-TU runtime link fails on real STLport allocator dependencies; preserved below |
| Product Win32 Release | 0 errors, incremental build (18.5 seconds) | Not a fresh full rebuild or binary-identity claim |
| Product x64 Release | Still fails: 438 MSBuild errors, 238 warnings; 429 distinct project-qualified error records | No ByteOrder or HTTPpost errors remain in this log; counts are not root-cause counts |

ByteOrder checks every 16-bit input and structured/deterministic 32-bit samples against independent byte expectations, not only round trips. Link maps bind all four functions to the production object. Its standalone link suppresses an inherited **unused** STLport default-library directive; no implementation is substituted. This does not establish complete serializer or network compatibility.

HTTP runtime coverage is narrower than the first proposed test. FirstClientGame's static Unicode string requires the real STLport node allocator; that allocator calls SWG's custom allocation operator, whose x64 assembly/owner-width migration is unresolved. The initial full-TU runtime probe therefore **failed to link**. We did not substitute an allocator. The passing fixture includes the actual VeCritsec header and drives retry loops itself; actual VeCritsec.cpp separately compiles. It does **not** establish runtime execution of production `lock()`/`yield_thread()`, a complete HTTP request, fairness, exception safety or portable C++ memory-model correctness. Tests explicitly use MSVC `/volatile:ms`. Existing allocation exceptions can still bypass callers' manual unlocks.

## POODO record and remaining work

Prospective criteria, 20 paths and decisions are recorded in the local continuation ledger. Three complementary workers audited byte order, HTTP locking and allocation/timers; a second pass challenged test counts, compiler identity, symbol binding, layout and timeout behavior. Shared source/context/model means their agreement is not independent empirical corroboration. The native runs and mutation controls are the separate observations.

Failed experiments retained: initial ByteOrder runner used the wrong metadata directory; corrected run compiled but hit the unused STLport directive. HTTP full-TU link failed due to genuine allocator dependencies. Scope was narrowed before reporting success; those failures were not recast as passing controls.

The next coupled task is allocation-owner and call-stack address width through MemoryManager, exported allocator hooks and Windows stack walking, before replacing OsNewDel assembly. Merely casting `_ReturnAddress()` into the existing uint32 API would retain truncation. The server Windows DebugHelp's wider storage is not an x64 stack walker: its implementation still uses x86 context fields/assembly. ProfilerTimer has a smaller separate intrinsic candidate, not implemented here. FPU/native Direct3D, vendor SDKs, full x64 linking and live gameplay remain open.

Delivery: commits published. Outcome: listed native integer/lock primitive checks and Win32 build passed; full x64 build failed. Required next observations: allocator/call-stack integration, production HTTP lifecycle and full client runtime. Agent controls compiler work; licensed SDK and GPU availability remain environment dependencies.

## Reproduction and artifacts

`native-text.tar.gz` contains 212 text logs, commands, maps and result files, including failed runs; no binaries or SDKs. JSON summaries and the normalized compiler-error extract are also visible separately. Scripts in `reproduction/` retain explicit VM paths and use the effective project metadata from the prior checkpoint; they are diagnostic recipes, not hosted CI or a portable installation.

`http-lock-full-probe.cpp` and `run-http-lock-full.py` describe the **failed** full-TU attempt. The other HTTP pair is the narrower passing actual-header test. Stock source inputs came from client f102763f7. Run only in fresh output directories. The archived prior metadata and an actual v120 installation, original repository dependencies and correct native checkout are required.

Primary contextual references: [Microsoft byte swaps](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/byteswap-uint64-byteswap-ulong-byteswap-ushort), [x64 ABI](https://learn.microsoft.com/en-us/cpp/build/x64-software-conventions), [bit-test/set intrinsic](https://learn.microsoft.com/en-us/cpp/intrinsics/interlockedbittestandset-intrinsic-functions), [Windows synchronization ordering](https://learn.microsoft.com/en-us/windows/win32/sync/synchronization-and-multiprocessor-issues). Modern documentation alone does not establish v120 behavior; the native tests provide the version-specific evidence above.

## Integration follow-up (2026-09-30)

Published only to the Akilleez-QA forks: client `b00ebf3df`, server `2a3b1463`. The client includes merge commits for `ci/client-wire` and `ci/client-dpvs`, plus the integration push trigger. [First integration wire CI run](https://github.com/Akilleez-QA/client-tools/actions/runs/36674511571) passed: 50/50 Win32 and 57/57 Win64 checks on exact head `b00ebf3dfe8198c02a2ff4ed6513469ad10c47e6`. The DPVS branch provides a native v120 runner, not an operating GitHub job; merging it does not supply hosted v120 coverage. The DLL comparator's eight synthetic tests passed locally.

Integration retains the existing C2 numerical candidate. This is a selection for integration testing, not proof of full-client equivalence: sampled PC64 comparison permits one negative dot difference of one ULP and 15 signed-zero min/max differences. Native Direct3D validation remains outstanding. The pending FPU port retains the Win32 precision-setter behavior; any future correction of that behavior requires reassessing C2. C1 remains a historical review alternative, not the current integration tree.

Client `9dc0e340f` and server `2a3b1463` replace only the x64 ProfilerTimer timestamp helper with `__rdtsc`, retaining the Win32 assembly and existing calibration/selection. The actual translation unit compiled in all four native v120 configurations. The source-extracted helper passed 10,000 bracketed TSC samples per configuration; stock Win32 passed, stock x64 failed compilation, and zero-return mutants failed. See `timer-results.json` and diagnostic recipes. This does not establish full profiler calibration, cross-core synchronization or production lifecycle behavior.

Allocator/stack/FPU/SSE candidates remain uncommitted. An immutable earlier allocator/stack snapshot passed the Win32 Release product build and failed x64 with 194 reported errors (185 normalized project-qualified records). It excludes later FPU/SSE/caller edits. Counts are diagnostics, not root causes or a completion percentage. The full client is not yet built or accepted.
