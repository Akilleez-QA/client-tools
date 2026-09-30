# Client x64 integration checkpoint — 2026-09-30

[Client integration branch](https://github.com/Akilleez-QA/client-tools/tree/integration/client-x64-next) at **f102763f701193b72d975a6f6a7822dde4bd1f23** adds eight commits to `332919f25`. It is a stacked integration branch, not a new upstream PR. Existing wire, DPVS and link-cleanup PR histories are unchanged.

[Server counterparts](https://github.com/Akilleez-QA/src/tree/integration/windows-shared-compat) at **a3f496be** are isolated from PR35. Both [portable CI](https://github.com/Akilleez-QA/src/actions/runs/36669295265) and [full Linux build/regressions](https://github.com/Akilleez-QA/src/actions/runs/36669292908) passed. Windows runtime validation below is client-scoped; Linux CI does not validate Windows branches.

## Changes and proof

| Commit | Scope | Observation |
| --- | --- | --- |
| cbfa4dca3 | Deterministic Debug/Release x64 generation and shared settings | 67-project closure; original Win32 XML/settings/mappings preserved; base-derived regeneration detects mutations. 268 native evaluations plus 134 x64 output/link evaluations passed. |
| 3c0535f39 | Rename checked int-length helper to imemmove, preserve five callers | Native x86/x64 overlap/type probe passes 13 checks each; original and body-only variants fail x64 compilation. Full Win32 rebuild passes; common-header overload errors absent from final x64 log. Server ec3acf84. |
| 83f7d2488 | Pointer-width SOCKET declarations and Sock storage | 20 real-header/include-order combinations pass across both ABIs, 21 UDP/IOCP checks each. Stock Win32 passes; stock x64 fails all 10 combinations with incompatible types/width checks. Server a81742ee. |
| 14c1bd30e | Pointer-width IOCP output key | Same probe tests native API high-bit keys; production completion-key change is included in the tested source snapshot. This does not exercise TcpServer accept/close lifecycle. Server a3f496be. |
| 291e70603 | x64 nop intrinsic, retain Win32 assembly | Actual UI project builds Debug/Release on both ABIs. |
| 1ee6a5f4b | Nonnegative parser offset and matching size_t diagnostic format | Actual UI project builds all four configurations. Dedicated stream runtime probe remains blocked by real STLport/custom allocator dependencies; no runtime-format pass claimed. |
| 29289bd8b | Allocation header padding, actual-class compile-time assertion | Actual MemoryManager.cpp compiles Debug/Release on both ABIs. Two x64 old-padding negative controls fail the new assertion. Existing runtime assertion retained. |
| f102763f7 | Pointer-width block-order assertion without unsigned underflow | Same actual-TU compilation; allocator runtime stress remains outstanding. |

The configuration commit adds 7,727 lines including tools and generated XML. The seven source commits change **31 added/17 removed lines across 12 files**. Mechanical configuration growth is not counted as a reduction against another full migration.

## Native environment and final build outcome

Existing Windows 10 VM, VS2013/v120/VC18, native x86/amd64 compilers, June 2010 DirectX SDK selected via DXSDK_DIR. A fresh empty checkout was extracted from the 332919f25 Git archive, then versioned configuration and source overlays were applied. The final guest source matched **all 20,519 tracked-file SHA256 values** at f102763f7, with zero mismatches. No diagnostic source entered the product checkout.

- Clean Win32 Release baseline with new configurations: 0 errors, 170 warnings.
- Win32 after initial memmove/socket/IOCP changes: 0 errors.
- Final Win32 Release build at f102763f7: **0 errors, 30 warnings**, incremental after prior full rebuild; not a claim of a fresh final-head full rebuild or byte equality.
- Final x64 Release attempt: **failed**, 580 compiler diagnostics and 552 warnings reported by MSBuild; 548 distinct project-qualified error records. Counts are not root causes and cannot be compared as equal coverage to the earlier 88-record common-header failure.
- No full x64 executable linked or ran. No live client/server connection occurred.

Compiler/PCH/PDB/resource, linker and renderer-deployment outputs are isolated by architecture. An independent review caught six initial x64 renderer copy commands still targeting dev/win32; these were corrected to dev/x64 before the x64 build. Optimized/IntelCPP x64 mappings are deliberately absent. The original dirty 67-file migration prototype remained byte-identical to its saved patch.

## Remaining blockers

The current log exposes handwritten assembly/naked wrappers in allocation, transforms/SSE math, regex, rendering, HTTP critical sections, byte order, timers, FPU control and stack walking; further pointer/time type errors also remain. No mass type replacement was applied.

Mozilla's bundled mozilla-config.h forces _X86_. Simply removing it exposes NSPR's unsupported x64 architecture and 32-bit pointer-sized types. A compatible implementation and matching headers are required; the diagnostic guard was not applied to production.

Broader local Work/Downloads inventory inspected 1,489 matching binaries: 1,483 x86 and 6 x64. The x64 results are Miles/Mozilla stubs and Vivox wrappers that still need an external SDK. These are not accepted substitutes. This bounded scan does not clear unmounted VM disks or generic archive payloads. Miles is a demonstrated direct import; Bink is attempted at startup; Vivox normally connects through login. Compile guards and extracted library members still govern other features.

STLport's actual UI formatter probe requires its real allocator implementation. Attempting to omit its default library exposes real unresolved symbols; linking the existing Win32 archive then requires MemoryManagerNotALeak allocation support. Failed probes are retained rather than replaced with mocks. A genuine x64 STLport source build remains another dependency task.

Allocation-size overflow, owner/call-stack widths, allocator stress, FPU policy/native Direct3D trace, remaining vendor SDKs, full x64 linking and mixed-width gameplay remain unverified. No stubs, feature removals, toolset upgrades or history rewrites were used.

## Evidence

`native-text.tar.gz` contains text-only build logs, commands, exit statuses, audit metadata, negative controls and result JSON; no EXE/DLL/SDK binaries. `final-x64-errors.txt` is the reviewable compiler-error extract. Scratch probe sources/runners are supplied under `reproduction/` with explicit VM paths; these are diagnostic recipes, not hosted CI or portable installers. Source manifests and original archives remain local; published verification JSON binds the tested head and checked-file count.

Delivery: committed and published integration candidates. Observed outcome: native Win32 build, listed compile/probe checks and server Linux CI passed; full x64 client failed. Next tests are compiler/dependency integration owned by this work, with licensed SDK availability and native GPU acceptance dependent on the project environment.
