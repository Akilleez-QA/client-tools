# Integer assembly checkpoint — 2026-09-30

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
