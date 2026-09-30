# Allocator, stack, FPU and math checkpoint — 2026-09-30

Published only to the working forks: client [12bb88809](https://github.com/Akilleez-QA/client-tools/commit/12bb888097a567191455f48598a6be9d87d4a257), server Windows counterparts [1b662b4d](https://github.com/Akilleez-QA/src/commit/1b662b4d). No upstream changes, PRs or comments. The client is **not finished**: the full x64 executable has not linked or run.

## Published changes

| Client commit | Scope |
| --- | --- |
| 92b05cbd8 | Build bundled STLport sources against native SDK declarations; retain vendor license/modification notice |
| eb73c7e8f, b8e359f41 | Pointer-sized thread-naming arguments and status-window user data |
| 966365f94 | Five game callbacks match the existing 32-bit archive index contract |
| 032f632a9, edcf5b461 | Select the string insert overload explicitly; retain full string positions and `npos` |
| c08d6c4f7, aa7737363 | Native tag lengths and Debug mesh range-check argument types |
| 1c9014369 | Explicit x64 MXCSR controls; keep Win32 precision behavior |
| 2fdd4639b, b4b4289b2 | Fatal and existing export-template breakpoint intrinsics |
| d905d5254 | Coupled allocator-owner and call-stack width contract, native Windows walking, caller hooks and exported signature |
| 8cdd61ed5, 631c79266, 1a2d514b6 | x64 SSE helpers, affine kernel, collision square root |
| 12bb88809 | Pointer-width ShellExecute status and diagnostic |

Shared changes were committed on `Akilleez-QA/src` first. Its Linux implementations are not replaced by the Windows ports. Client-specific allocator and renderer changes have no equivalent server implementation to copy blindly.

## Native observations

Actual VS2013/v120 on the Windows VM, with real repository dependencies. Each probe records source identity, compiler commands and relevant maps. These are bounded observations, not general migration acceptance.

| Check | Observed result | Boundary |
| --- | --- | --- |
| DebugHelp known caller chain, address bounds, source lookup, four concurrent threads | 257/257 captures in Debug/Release on Win32/x64, for both client and server Windows translation units | Server TU linked against client dependency closure; not a complete Windows server build. Concurrent teardown, unload/reload and minidump lifecycle untested |
| Real allocator with diagnostic `DO_TRACK=1` and `DO_TRACK=5` | 2,568/2,568 each in all four configurations; normal teardown succeeds | Checks owner slot 0, flags, payload, alignment, guard paths and coalescing. Secondary stack slots execute but individual ancestor identities are not asserted |
| Actual five OsNewDel allocation overloads | 20/20 saved owners equal the exact instruction after the caller's call, checked against native disassembly across four configurations | Not merely an address-range or high-bit test; other hook runtime paths remain separate |
| Real DllExport project | Builds all four configurations; both Win32 export sets unchanged, 79 names each | Existing import-library template, not a runtime replacement allocator |
| Direct3d9 allocator-hook object contract | Debug/Release x64 imports match actual MemoryManager definitions and template exports | Final executable exports and runtime delay-load redirection remain open |
| FPU production TU | Win32 candidate and stock 46/46; x64 67/67, each Debug/Release. No-op mutation fails 21 checks; x64 precision API call is rejected at compile time | Control state and sampled rounding; not exception delivery, physics or native Direct3D acceptance |
| Tag conversion | 4,098 actual-header values per ABI equal stock; native Debug consumer compilation passes | Bounded inputs, not giant-string acceptance |
| ShellExecute status | Actual TUs compile all four configurations; source-extracted full-width status/format probes pass and old narrowing controls fail on x64 | No browser launched. Existing trial-launch `<32` boundary is unchanged |

Tracked `reallocate(NULL,16)` still crashes on both architectures. This is a separately reproduced existing tracking-path bug, **not** a passing negative control. Allocation-size arithmetic and aggregate counters also remain unresolved; widening addresses does not make large allocations safe.

## Stack-walk failure and discrimination

The first x64 candidate returned addresses but failed every known-caller check: 0/257. Win32 passed. Four callback combinations isolated the retained function-table pointer cache:

| x64 callback selection | Captures |
| --- | ---: |
| Both original caches | 0/257 |
| Both direct DbgHelp callbacks | 257/257 |
| Direct function-table callback; cached module base | 257/257 |
| Cached function table; direct module base | 0/257 |

The published change bypasses only the function-table pointer cache on x64. RBP initialization was not changed on speculation. The failure and its controls remain in the packet. This establishes the cache's effect in the tested environment; it does not independently prove every detail of native DbgHelp's internal storage lifetime.

## Numerical scope

See [native math results](math-native-results.md) and [register-clobber analysis](ssemath-clobber-analysis.md).

- **SseMath:** native stock Win32 disassembly and a tiny discriminator reveal a pre-existing register clobber between assembly blocks. The production Win32 path stays unchanged. A separately named diagnostic reload control—not stock—agrees with x64 on the finite, subnormal, extreme and discarded-lane categories of 33,280 records per configuration, including recorded MXCSR. Exceptional differences remain. No callers of the four arithmetic helpers were found; no gameplay effect is claimed.
- **Transform:** 1,024 cases per run. Stock and candidate Win32 records match. All 768 finite cases and the tested alias/control cases match x64. Debug is exact throughout. Release's strict comparator remains failed for 136 exceptional records containing 464 NaN-payload differences; it is not reported as universal bit identity.
- **Collision:** all 8,192 sampled values, line-twist classifications and MXCSR words match per Debug/Release run. Separate Win32 x87 status differs from the explicit absent-unit field on x64; this is retained, not compared as though the units were identical.

The FPU port leaves the legacy Win32 setter bug intact. The integration branch continues to carry DPVS C2 with its previously documented sampled PC64 limits. Fixing the Win32 setter requires reassessing that numerical reference. Native Direct3D and representative scenes remain outstanding.

## Product and renderer boundaries

The earlier immutable candidate snapshot, before the last Debug-only fixes and stack-cache repair, builds the Win32 product in both Release and Debug. Its x64 Release reports 54 errors; Debug reports 71 errors, 62 distinct diagnostic lines. These are compiler diagnostics, not root-cause counts or a completion percentage. A new four-configuration checkpoint for exact published head `12bb88809` is running; the earlier results do not establish that final head's full build.

All three real Direct3d9 variants now reach the x64 linker in Debug and Release with zero compiler errors. Each fails on the same 16 unresolved names: five STLport symbols, nine JPEG functions, DirectDrawCreate and DXGetErrorString9A. Their real libraries and SDK selection are being investigated. SwgClient still has separate Miles/Mozilla and skeletal work; dynamic vendor loads also remain outside a static link result. No SDK stubs, allocator stand-ins or feature removals were supplied.

[Wire CI on published client head](https://github.com/Akilleez-QA/client-tools/actions/runs/36678588982) passed. This does not make the native probes hosted CI: they still require the actual v120 environment. The previously merged DPVS tooling likewise has no operating hosted v120 job.

## Reviewers, failures and reproduction

Grok 4.7, Composer 2.5, Codex CLI and complementary local agents reviewed different slices. Their raw reports are provided as **review leads**, not accepted findings. Parent spot checks rejected or narrowed claims such as automatic stack corruption from a narrowed argument, demonstrated visual defects from arbitrary pointer sort keys, and inferred STL ABI mismatch from a forward alias. Composer round 4 found no new root cause in its stated terrain/world/network slice; that is not an exhaustive clean bill.

Failures retained include the original x64 stack walk, missing genuine dependency links, constant-folded rounding fixture, mismatched signaling-NaN probe inputs, and an allocator fixture that incorrectly constructed a second MemoryManager beside the production singleton. The latter completed its allocation checks and then destroyed the heap prematurely; the corrected fixture uses the real OsNewDel singleton lifecycle. None of these earlier runs has been relabeled as successful.

`native-text.zip` contains native text records, commands, maps and results; `reproduction-and-local-text.zip` contains diagnostic recipes, fixtures, local reports and additional native text. They exclude binaries, SDK packages and environment dumps. Recipes contain explicit VM paths and require the earlier native audit metadata plus genuine v120 dependencies. They are not a portable one-command installer. Result JSONs are also exposed separately; hashes are in `artifact-sha256.json`.

Delivery: listed commits pushed to forks. Outcome: listed native checks passed within their boundaries; full x64 build/runtime remains incomplete. Next agent-controlled checks are exact-head product diagnostics, skeletal kernels, allocator sizing and real renderer dependencies. Licensed vendor binaries and native GPU acceptance remain external dependencies.
