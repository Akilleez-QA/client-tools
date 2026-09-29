# DPVS branches prepared on upstream

Base: `949451032` (full base recorded by each branch's ancestry). Source branches are published for review; no PR, issue or review comment was created.

| Variant | Local branch | Head | Commits | Diff |
| --- | --- | --- | --- | --- |
| C1 | `x64-dpvs-c1` | `7b5c73da8807ca5a5d12540d9dc4886c4c3e988f` | 4 | 5 files, +74/-27 = 101 lines |
| C2 | `x64-dpvs` | `14005646e8c126b753e3fb2e68b51344ba4e4709` | 5 | 5 files, +85/-27 = 112 lines |

C1 source/header: +24/-4 = 28 lines; C2 source/header: +35/-4 = 39 lines. Both project XML: +50/-23 = 73 lines. No test or diagnostic files are included. Both refs contain only the listed five production paths. The checked-out C2 worktree is clean, and `git diff --check` passes. C1 is an immutable local ref of the first four commits, with no separate mutable worktree.

Commit order:

1. `2985e408b`: distinguish x64 architecture/pointer width and select reciprocal4 algorithm.
2. `346f280aa`: x64 timer and prefetch intrinsics.
3. `8cb0f7548`: keep MatrixCache entries 64 bytes.
4. `7b5c73da8`: isolated x64 Debug/Release project outputs.
5. `14005646e`: optional x64 double-intermediate numerical candidate.

The original five commits cherry-picked without conflicts. Full messages are saved in `commit-messages.txt`; their claims are bounded to architecture/layout changes and the prior numerical evidence. The numerical message explicitly preserves the native Direct3D gap, one-ULP dot difference, signed-zero differences and dependency on the legacy setter bug. No message claims complete x64 gameplay acceptance.

## Independent branch builds

Archived only the committed DPVS subtree from upstream/C1/C2. No wire changes or any of the 67 uncommitted project files entered the build. Extracted each snapshot sequentially into the same `C:\pr-dpvs-review` directory and rebuilt the actual `implementation\msvc8\dpvs.vcxproj` using MSBuild12/v120, `/t:Rebuild /m:2`. Baseline upstream Win32 Release also rebuilt there.

| Variant | Win32 Release | Win32 Debug | x64 Release | x64 Debug |
| --- | --- | --- | --- | --- |
| C1 | 0 errors, 67 warnings | 0 errors, 71 warnings | 0 errors, 168 warnings | 0 errors, 179 warnings |
| C2 | 0 errors, 67 warnings | 0 errors, 71 warnings | 0 errors, 168 warnings | 0 errors, 179 warnings |

Every one of these eight fresh DLLs passed the existing public-interface probe executables: 192 stress queries and 64 fixed-cost occlusion frames. `verify.py` verifies exact sequential record counts, sentinel/callback checks, explicit zero exits, zero failures, first-hidden frame zero, no reappearance and 64 writes. UTF-8 build and probe logs are in `native-text/`; hashes and counts are in `verified-results.json`. Binary DLLs and executables are retained locally, not bundled here. `verify.py` and `compare-dll.py` record the original checks and require the locally generated `native/` binaries; they are not executable from this text-only packet alone. The probes use PC24 for their Win32 integration checks: these are not the separate PC64 assembly numerical experiments or native gameplay.

## Win32 DLL comparison

Both C1 and C2 Win32 Release DLLs have byte-identical `.text`, `.data`, `.rsrc` and `.reloc` sections to upstream. All files are 583,168 bytes. Whole files are identical after explicitly normalizing:

- Parsed PE COFF/export/debug timestamps.
- Parsed CodeView PDB GUID and age (a full rebuild creates new debug identity).
- The CodeView PDB path's `Win32` versus `win32` capitalization.
- The source-defined `DPVS_BUILD_TIME` string (`dpvsVersion.hpp:64`, `__DATE__ " " __TIME__`).

No instruction/data differences were discarded. The embedded build-time string is observable metadata, so this is **not raw byte identity**. The script `compare-dll.py` and `dll-comparison.json` preserve the exact comparison and normalized offsets. This proof applies to Release, not an asserted Debug binary comparison.

## Dependency questions

- C1 and C2 require **none** of the 67 uncommitted build-configuration files. Both build standalone from their upstream-based committed DPVS subtree.
- The project-output commit works atop the first three DPVS commits without wire or full-client configuration changes.
- The project-output commit **alone on stock upstream source does not produce an x64 build**. A negative-control rebuild (`native-text/project-only-x64.log`, exit 1) fails the pointer-size assertion and unsupported Win32 `__asm`, as expected. Its architecture/layout prerequisites are real.
- Full SwgClient builds and broader solution Optimized mappings are outside these DPVS-project runs.

## Limits and review choice

C1 deliberately leaves the known scalar numerical differences unresolved. C2 includes the separately measured double-intermediate candidate: zero sampled caller sign/zero and raster differences against forced-PC64 Win32 assembly, one negative dot differing by one ULP, and 15 min/max signed-zero differences outside the repair. That prior evidence is under [prior-numerical/RESULTS.md](prior-numerical/RESULTS.md); it is not relabelled as a new test here.

Native Direct3D FPU-state tracing remains unverified. Allocation-count narrowing and signed capacity/accounting risks remain open. Neither variant establishes full-client x64 linking or representative gameplay. No stubs or feature removals are included.

No PR template or CONTRIBUTING file is tracked at upstream `94945103` (case-insensitive tree-name search). Local descriptions are `PR-C1.md` and `PR-C2.md`; neither was posted.

## Review follow-up: quantified C1 and unisolated paths

The prior caller-shaped comparison against native Win32 assembly forced to PC64 contains 11,978 rows: 3,584 dot-product rows and 8,394 raster rows. The original scalar path retained by C1 differs in **1,442 of the 3,584 sign/zero classifications**, and in **702 raster rows**, all at scale approximately 7.2. These are sampled numerical differences, not 1,442 demonstrated gameplay failures. See the [original PC64 comparison](https://github.com/Akilleez-QA/client-tools/blob/review/client-x64-evidence/review/client-x64/C-dpvs/prior-pc64/RESULTS.md) and [recorded counts](https://github.com/Akilleez-QA/client-tools/blob/review/client-x64-evidence/review/client-x64/C-dpvs/prior-pc64/comparison.json). This is prior numerical evidence for the retained scalar algorithm, not a new numerical run of C1.

Three additional integer paths switch from hand-written x86 code to C++ on x64: highest-set-bit search (`dpvsBitMath`), the byte-reordering return path (`dpvsFiller.hpp`), and the MMX occlusion-buffer cache filler (`dpvsOcclusionBuffer_CacheFiller.cpp`). They have no isolated differential comparison; the integration probes provide indirect coverage without establishing every branch/input or exact integer equivalence.

Raster overflow/non-finite inputs remain untested: converting a floored value outside the `INT32` range with a C++ cast is undefined, whereas x87 `fistp` has invalid-conversion handling (integer indefinite `0x80000000` when the invalid exception is masked). The current fixtures do not establish caller bounds or equivalent handling outside the tested range.
