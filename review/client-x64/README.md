# Client x64 review packet

Latest commits-only checkpoint: [native build, dependency and fidelity work](vendor-next/vendor-options/CHECKPOINT-2026-09-30.md).

Current working code: [integration/client-x64-next](https://github.com/Akilleez-QA/client-tools/tree/integration/client-x64-next). The x64 client is not complete: full link/start and intended gameplay/media acceptance remain open.

At `49d0eeed4`, actual Win32 Release/Debug builds finish with zero errors; x64 Release/Debug reach the final linker with only 60/61 Miles imports unresolved. [Commit-bound native results](vendor-next/allocator-next/integration-current-v2/current-head-v2-complete/RESULTS.md). This was an audited incremental build, not a clean rebuild. [Private runtime staging](vendor-next/allocator-next/runtime-readiness/private-staging-evidence/RESULTS.md) establishes basic loader prerequisites, not client startup.

Miles remains an experimental original-engine process boundary. [The real Win32 Audio/Sound2d baseline](vendor-next/vendor-options/miles-engine-fixture/RESULTS.md) completed two sample lifetimes but failed during teardown, so it is not a passing reference. [Candidate interface plan](vendor-next/vendor-options/miles-integration-seam/PLAN.md) and [exact API signature checks](vendor-next/vendor-options/miles-integration-seam/protocol-candidate/README.md) do not establish a complete adapter or game fidelity.

Previous commits-only checkpoint: [integer assembly and HTTP lock](assembly-next/RESULTS.md).

Previous commits-only checkpoint: [client x64 configuration and compiler fixes](next-build/RESULTS.md).

Previous follow-up: [CI, reproducibility and final-head server validation](followups/README.md).
The original tables and manifests below record the **initial submission baselines**;
client #23 and #24 now also contain separately tested CI/reproducibility commits.

These are separate review branches on `Akilleez-QA/client-tools`, based on upstream `949451032647e45e42c3aaef3f41b132c8af36e3`. They are published so cloud reviewers can inspect the source and evidence. No pull requests or issue comments were opened.

| Review | Branch | Head | Scope |
| --- | --- | --- | --- |
| A | [x64-link-cleanup](https://github.com/Akilleez-QA/client-tools/tree/x64-link-cleanup) | `46a56f6a5` | One Release link-list replacement, +1/-1 XML lines |
| B | [x64-fixed-width-wire](https://github.com/Akilleez-QA/client-tools/tree/x64-fixed-width-wire) | `b5bb8792f` | 260 production/project lines changed; 828 harness lines added |
| C1 | [x64-dpvs-c1](https://github.com/Akilleez-QA/client-tools/tree/x64-dpvs-c1) | `7b5c73da8` | Four DPVS commits; 28 source/header + 73 XML lines changed |
| C2 | [x64-dpvs](https://github.com/Akilleez-QA/client-tools/tree/x64-dpvs) | `14005646e` | C1 plus isolated numerical candidate; 39 source/header + 73 XML lines changed |

The combined A+B+C2 diff is 1,202 changed lines, including 828 wire-harness lines. A+B+C1 is 1,191. These are measured branch diffs, not an estimate of the remaining full-client migration.

Exact SHAs, commit lists, file lists and counts: [branches.json](branches.json). C1 and C2 were the initial comparison alternatives, not two changes to merge independently. The later integration branch carries C2; its bounded numerical evidence and native Direct3D limitations remain in the subsequent checkpoints.

## Draft descriptions and evidence

- A: [draft](A-link/PR-A.md), [validation](A-link/RESULTS.md), including all 74 removed entries grouped for review.
- B: [draft](B-wire/PR-B.md), [validation](B-wire/RESULTS.md), [historical commit-message corrections](B-wire/COMMIT-REVIEW.md).
- C: [C1 draft](C-dpvs/PR-C1.md), [C2 draft](C-dpvs/PR-C2.md), [validation and DLL comparison](C-dpvs/RESULTS.md).
- [Bink/Vivox loading and PR-template source audit](loader-and-template.md).

Source branches contain their intended commits only. All reports and probe artifacts in this packet are on this separate evidence branch. The original migration checkout's 67 uncommitted configuration files were not included. Source worktrees were checked clean before publication.

## Review limits

The wire matrix preserves the listed legacy bytes for representable values. Checked rejection of oversized counts intentionally changes failure behavior even on Win32; it is not a claim that all Win32 behavior is unchanged. The published historical wire commits are retained; their overbroad wording is corrected in the commit-message review.

Both DPVS variants build independently of the 67 pending full-client configuration files. The output-path commit requires the preceding DPVS source fixes for x64: applying it alone to stock source fails. Every freshly built variant/configuration passed 192 stress queries and 64 fixed-cost occlusion frames. This is bounded project/probe evidence, not full-client or gameplay acceptance.

C2's previous PC64 numerical measurements remain separate from this branch-validation run. Native Direct3D FPU-state tracing, representative gameplay, allocation-size narrowing, vendor SDK availability and a successful full x64 client link remain open. No stubs or feature removals were introduced.

Bink is attempted at graphics startup with a nonfatal missing-DLL path in the inspected code. Vivox's wrapper initializes at startup, while vendor SDK loading is lazy and can be triggered by connection or feature operations. These source findings do not prove that an x64 client works without those vendors.

No PR template is tracked in the requested upstream base; the organization `.github` repository lookup returned HTTP 404, so no organization-level template was available to inspect. The draft headings are proposed structure.

## Artifact use

Text logs and JSON results are included; built executables, DLLs, SDKs and game assets are not. Original comparison scripts record how the local binary artifacts were checked and require those artifacts to rerun. Native logs retain build paths as evidence.

The portable runner wrapper in `B-wire/run-portable.py` takes its Wine prefix from `SWG_TEST_WINEPREFIX` for distribution, replacing the original local absolute prefix; its test logic is otherwise unchanged. Use an initialized WoW64 Wine prefix. Historical numerical scripts retain their original build-directory assumptions and need a matching local fixture layout; they are evidence, not a standalone SDK installer.
