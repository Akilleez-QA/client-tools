# Server submission map

This is the server counterpart to the client inventory. It accounts for maintained source already in PR35 and every implemented later Windows/shared counterpart; it does not reopen testing or propose new ports. Public PR metadata was read on 2026-10-01.

**Bases:** `master` = `7d2159a337281184d6a55db30d2bc9a4013c0e80`; `64-bit-types` = `22dd13d4a40014899c547cd370de969ac6ae1fdc`. [PR35](https://github.com/SWG-Source/src/pull/35) targets the latter at `6b998f6fc281a88a50a710d7ae6afd55814b1946`. Its last production change is `8e57911e45ce52be88d6b9199bab82aef67ef1fc`; the tail adds CI/docs. The Windows/shared integration is `731d85cc10326f5f2d656b4b66f09c5feab30635` above PR35.

## What is already submitted

| Package | Correct comparison | Scope/status |
| --- | --- | --- |
| PR35 | `22dd13d4..6b998f6f` | 621 files, +12,264/-4,817; already submitted, do not duplicate |
| [PR37](https://github.com/SWG-Source/src/pull/37) | `7d2159a3..1481143c` | Helper production: 3 files +5/-5; regression evidence and exact local full build exist. Original full-build CI failure is retained. |
| [PR38](https://github.com/SWG-Source/src/pull/38) | `7d2159a3..1c015279` | Workflow only, +45/-19; upstream compile CI green. |
| [Fork draft 1](https://github.com/Akilleez-QA/src/pull/1) | `09932a32..9d44e3a1` | Network: 6 production files +18/-6, including Winsock2 include prerequisite. Tests/docs/CI separate. Exact-head hosted Windows TU compilation green. |

The network draft base already contains both PR37 and PR38. Its next action is upstream publication/base handling, not another source investigation. The old status note saying exact server compilation is pending is historical; [run 36836765096](https://github.com/Akilleez-QA/src/actions/runs/36836765096) passed on the current head.

PR35 source/schema/build/test categories and all originating commits are listed in the JSON. Its [historical production evidence](https://github.com/Akilleez-QA/client-tools/blob/f015ce7abc08d98902c6febdd50df204fe58137b/review/client-x64/followups/server/RESULTS.md) covers both Linux ABIs at `8e57911e`; the current PR also has green upstream [compile](https://github.com/SWG-Source/src/actions/runs/36550589549) and [portable](https://github.com/SWG-Source/src/actions/runs/36550589507) checks. These are existing results, not fresh runs.

## Remaining implemented counterpart packages

The exact `6b998f6f..731d85cc` comparison is **30 files, +533/-128**: 28 production files and two fork workflow selector edits. After helper/network work already submitted, **9 packages, 20 unique production paths, +492/-116 remaining hunks**. `Misc.h` is mixed: the helper hunk is already PR37, string-length hunks remain.

| Package | Production delta | Submission base/dependency | Origin commits |
| --- | --- | --- | --- |
| Windows x64 byte swapping (now [fork draft #2](https://github.com/Akilleez-QA/src/pull/2), excluded from remaining total) | 1 file +26/-0 | joint PR37/38 base; source itself applies to master | `3bb838a2` |
| Windows x64 breakpoint, timestamp counter and address diagnostics | 3 files +19/-1 | PR35; master needs focused hunk transplant | `2a3b1463`, `b6967a02`, `e10e858f` |
| Host-sized duplicate/tag string lengths | 2 files +5/-5 | PR37; retain helper correction | `c98f2a6d`, `c03e4a1a` |
| Thread-name exception arguments and ShellExecute result widths | 1 files +2/-2 | PR35; master needs focused hunk transplant | `51373f7f`, `1b662b4d` |
| Windows x64 SSE floating-point controls | 3 files +55/-2 | PR35; master needs focused hunk transplant | `cc361630` |
| Windows x64 native stack capture | 1 files +49/-5 | PR35; master needs focused hunk transplant | `74287848` |
| Windows x64 scalar/vector/affine SSE math | 4 files +235/-1 | master; identical touched-file baseline | `ad4d5c7f`, `1cc02f6a`, `517d80bd` |
| Checked archive lengths, payloads and ordinary collection counts | 3 files +32/-16 | PR35; master needs focused hunk transplant | `28f43f68`, `5474d3d0`, `2648217a`, `c6cdbe85` |
| ByteStream bounds and exception-safe replacement ownership | 2 files +84/-84 | PR35; master needs focused hunk transplant | `7131fd38`, `731d85cc` |
| Scoped Windows x64 vendor packing diagnostic | 1 files +11/-0 | master; identical touched-file baseline | `78ec0f03` |

Use PR35 as the exact extraction base for shared files with different master contents. This is a packaging/context boundary, not a claim that every Windows fix semantically requires the whole Linux port. Native stack capture, breakpoint/address fixes, API-width fixes and floating controls have master-context differences recorded per path in the JSON. The archive packages actually rely on the maintained fixed-width archive semantics and must not restore final PR35 files over master.

Source grouping preserves the existing implementation: the SSE helpers, affine transform and collision scalar square-root form one math package; floating-point controls stay separate. ByteStream storage includes the final `unique_ptr` repair rather than its intermediate `auto_ptr` state. Archive payload/count preflights remain a separate three-file package. SDK packing is only a scoped wrapper diagnostic; it does not include vendor source history.

**Published/helper divergence:** the old integration helper is +4/-4; PR37 is +5/-5 because it also makes the CRT delegation explicitly `size_t`. Preserve that published correction when applying the remaining `Misc.h` length hunks. The network fork adds the genuine-server header prerequisite and runner absent from the older integration branch. The maintained submission branches are authoritative for those two packages.

## Excluded older upstream history

The `master..64-bit-types` endpoint diff is **619 files, +158163/-6812** across 50 reachable branch commits. This is pre-existing upstream work, dominated by old vendor/ABI changes; it is not our remaining production queue. Comparing PR35 directly with master inflates its scope. PR35 delivery to master still depends on the upstream branch strategy; this task does not split or resubmit that history.

## Next branches

1. Finish the existing network draft’s upstream submission using its joint PR37/38 base metadata and current exact-head CI evidence.
2. ByteOrder is prepared as fork draft #2 at `adb1bc91d2ad0a923a828204410c72d7cab9dbc1`, above the joint PR37/38 base. Its source applies to master, but the selected base retains the native-header helper prerequisite and repaired CI.
3. Assemble the four-file SSE math package on master from `ad4d5c7f`, `1cc02f6a`, `517d80bd`: +235/-1. All touched baseline files match.
4. Queue archive storage and payload/count packages above PR35. Keep published helper/network histories unchanged.

The original inventory ran no builds/tests and made no source changes. A later packaging step prepared and published the exact ByteOrder counterpart as fork draft #2, without another build or runtime test. Client test results must not be described as server Windows qualification. No speculative server allocator/media/UI counterparts are counted as implemented work. [Machine-readable file/hunk accounting](server-package-map.json) includes exact hashes, per-file origins, baseline differences, mixed ownership and separate comparison totals.
