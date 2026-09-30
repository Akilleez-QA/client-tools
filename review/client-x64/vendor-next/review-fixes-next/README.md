# Bounded review repairs — candidate for parent review

Completed in a **new detached worktree**, left uncommitted:
`/home/akilleez/Work/client-wire-validation/review-fixes-next/source`

Base captured from `/home/akilleez/Work/swg-source/client-build-next` current HEAD at start:
`0d2f8c168165dce3e629866c76e1a697fae8318c`.
Review input: `/home/akilleez/.codex/attachments/d8a2badb-3dc6-4099-822e-eb9214890d0b/Pasted text.txt`.

## Candidate

[Combined patch](candidate.patch) changes exactly two lines in two source files:

1. `MemoryManager.cpp:1721`: both free-pattern diagnostic addresses use `%p` with explicit `void *` arguments; remove the manually added `0x` prefix because `%p` spelling is implementation-defined. Pointer arithmetic, dereference, loop, allocation, locking, corruption detection, and fatal behavior are unchanged. Only text formatting/type conversion changes.
2. `SwgClient.vcxproj:233`: Optimized|Win32 removes all ten occurrences of six obsolete names: `libMozilla.lib`, `nspr4.lib`, `plc4.lib`, `profdirserviceprovider_s.lib`, `xpcom.lib`, `xul.lib`. Non-browser inputs, including their existing duplicates and order, and every other XML value/attribute are preserved. Search/include paths are deliberately unchanged, matching prior cleanup scope.

Prior `94a81438` removed five of these names in Debug and all six in Release; Debug already lacked explicit libMozilla. Its commit explicitly left Optimized settings unchanged while removing the SwgClient solution dependency. This candidate closes that mismatch. No new browser feature disabling or solution edits occur. See `prior-cleanup.json`.

## Verification and evidence

- `git diff --check` passes. `static-validation.json` records exact changed-file scope, one diagnostic line, ten removed input entries, and candidate hashes. Candidate changes no allocation semantics.
- Native VS2013/MSBuild 12.0 evaluation, no Build/Link targets: before/after Debug, Optimized, Release all exit 0. Evaluated inputs are Debug 233→233, Release 155→155, Optimized 191→181. The exact ten browser entries are absent afterward; every other input retains order. See `native-evaluation-comparison.json` and `native-results/review-fixes-next-0d2f8c168/*inputs.txt` / `*audit.log`.
- MSBuild wrapper imports the unchanged before/candidate vcxproj snapshots and reads the native Link item-definition metadata on a dummy, never-linked item. This includes installed Microsoft/user property imports, using private relocated scratch project files. It is not a full solution build, library availability check, object default-library audit, or final linker command; no source, object, post-build, or deployment target is invoked. x64 props are not imported in these Win32 evaluations.
- Native diagnostic-only extracted expression compiled `/c /W4 /WX` for x86 and amd64; both old/new compiled. COFF headers confirm 0x14c / 0x8664. With C4311 explicitly enabled (`/w14311 /WX`), the old amd64 expression fails with C4311/C2220 and the candidate passes. Thus the pointer truncation is confirmed, but the review's default `/WX` failure claim needs that warning enabled on this v120 toolchain. No executable is built or run.
- Browser references: all 19 inventoried engine/game C++ implementation occurrences are under existing `#if DEBUG=0` directives; three additional unguarded header occurrences are the libMozilla include and pointer/method declarations in SwgCuiWebBrowserWidget.h, which do not themselves request library linkage (`browser-guard-inventory.json`). This legacy spelling is nonstandard; native MSVC issues C4067 and skips it when `DEBUG` is undefined (both `_DEBUG` and `NDEBUG` probes). Deliberately defining `DEBUG=1` selects the branch and triggers the compile-only negative control. Current relevant project definitions use `_DEBUG`/`NDEBUG` and `DEBUG_LEVEL`, not `DEBUG`; first-party definition search found no `#define DEBUG`. Do not generalize the disabled-browser claim to arbitrary external `/DDEBUG` builds. These guards are not edited.
- Existing pointer diagnostics reviewed across allocate/free, owner/caller fallback formatting, map output, block reports, report-to-file, and verify. Native-width PRI[xX]PTR formats and existing `%p` sites already preserve addresses. `%02x` values are byte contents, not pointers. The companion remote-channel free-pattern message has no address to truncate. `Report.h:49–65` forwards variadic arguments to `Report::printf`; `Report.cpp:205` uses `vsnprintf`, so no intermediate 32-bit pointer conversion exists. See `memory-diagnostic-inventory.txt`.
- `verify-callers.txt` records Os::update, Game::run path, command parser memoryVerify, and the CuiManager→SetupUi→UiReport callback route; two DynamicMesh mentions are commented out. No signatures or call sites require changes. None were executed.

Native scripts and exact extracted inputs are in `native-input/`. Native artifacts/logs are in `native-results/`. Initial PowerShell file invocation was rejected by default script execution policy; the existing wrapper then supplied reviewed script text on stdin. A first batch-file construction mistake produced an `x86` command error; the corrected runner is `run-compile.ps1`. Both failed wrapper logs are retained. No host execution policy was changed. C4311 follow-up is `run-c4311.ps1`; no old allocator test script was used.

## Read-only conclusions and handoff

[Documentation recommendations](documentation-recommendations.md) provides precise proposed text: DebugHelp's thread handle and broader locking affect Win32 as well as x64; x64 FPU updates restore saved FTZ/DAZ on the calling thread; universal MULTIPLE exception-code dispatch is unproven. DebugHelp/FPU source and published history remain unchanged.

[Durable build_config_next handoff](build_config_next-handoff.md) is the coordination artifact for the parent/config owner. No message or external post was sent and no receipt is implied. Parent should review/apply the patch against its current base; source candidate is not integrated. Existing parent changes after the captured HEAD, if any, belong to the parent.

No commits, pushes, posts, Q/R mapping changes, parent source edits, malformed allocator cases, runtime fault reproduction, or full-client success claims. Native scratch is `C:\review-fixes-next-0d2f8c168`; only private files there were created. Full Optimized linking remains unvalidated and can still encounter unrelated legacy inputs. Source worktree registration necessarily adds Git worktree metadata to the shared repository; parent checkout/index/ref were not edited by this task.

Final observation: parent advanced independently to `d36090a8cec01785b25bcb9608473a8b1b770c18` and is clean. Candidate remains detached at the captured starting HEAD. Read-only `git apply --check` against that parent FAILED for both files; nothing was applied. Both parent files now match the candidate byte-for-byte, indicating the repairs have independently arrived in the parent. Do not apply this patch again; verify current parent history before integration.
