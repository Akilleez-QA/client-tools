# Client x64 review index

This is a submission map, not an approval or a runtime status report. Existing draft bodies and failed evidence remain unchanged. At this audit, the fork has no pull requests (including closed/draft); branch publication is not review approval. No PR creation or upstream mutation is requested by this index.

## Five bounded candidate packages

All links below pin immutable fork commits. `M` means upstream master `949451032647e45e42c3aaef3f41b132c8af36e3`; `P` means the imemmove production prerequisite `9eadbbbebd515a0fffad2133300703dff68bd7ef`. Counts are production `src/` additions/deletions against the stated base; test tooling and evidence are separate.

| Package / fork branch | Exact base → head | Production delta | Root cause |
|---|---|---|---|
| imemmove: `review-ready/client-imemmove` | [949451032647e45e42c3aaef3f41b132c8af36e3](https://github.com/Akilleez-QA/client-tools/tree/949451032647e45e42c3aaef3f41b132c8af36e3) → [3b00af6296e9d3631cd3e068d4a0c31499a9756a](https://github.com/Akilleez-QA/client-tools/tree/3b00af6296e9d3631cd3e068d4a0c31499a9756a) ([diff](https://github.com/Akilleez-QA/client-tools/compare/949451032647e45e42c3aaef3f41b132c8af36e3...3b00af6296e9d3631cd3e068d4a0c31499a9756a)) | 4 files, +7/−7 | The int-length memmove overload conflicts with CRT pointer-width overload resolution. |
| ByteOrder: `review-ready/client-byteorder-x64-stacked` | [9eadbbbebd515a0fffad2133300703dff68bd7ef](https://github.com/Akilleez-QA/client-tools/tree/9eadbbbebd515a0fffad2133300703dff68bd7ef) → [110c7b4ba7cf317760119c1b298fabe7d30b61d8](https://github.com/Akilleez-QA/client-tools/tree/110c7b4ba7cf317760119c1b298fabe7d30b61d8) ([diff](https://github.com/Akilleez-QA/client-tools/compare/9eadbbbebd515a0fffad2133300703dff68bd7ef...110c7b4ba7cf317760119c1b298fabe7d30b61d8)) | 1 file, +26/−0 | MSVC x64 rejects the original inline assembly; use width-specific byte-swap intrinsics. |
| Socket/IOCP: `review-ready/client-socket-widths-stacked` | [9eadbbbebd515a0fffad2133300703dff68bd7ef](https://github.com/Akilleez-QA/client-tools/tree/9eadbbbebd515a0fffad2133300703dff68bd7ef) → [23849687c697520d8934049efc49f62e44fd9b6a](https://github.com/Akilleez-QA/client-tools/tree/23849687c697520d8934049efc49f62e44fd9b6a) ([diff](https://github.com/Akilleez-QA/client-tools/compare/9eadbbbebd515a0fffad2133300703dff68bd7ef...23849687c697520d8934049efc49f62e44fd9b6a)) | 5 files, +9/−6 | Windows socket handles and IOCP completion keys require pointer width. |
| HTTP lock: `review-ready/client-http-lock` | [949451032647e45e42c3aaef3f41b132c8af36e3](https://github.com/Akilleez-QA/client-tools/tree/949451032647e45e42c3aaef3f41b132c8af36e3) → [d788e64ced56832894ff77a7d0d5b30fbec1b2ce](https://github.com/Akilleez-QA/client-tools/tree/d788e64ced56832894ff77a7d0d5b30fbec1b2ce) ([diff](https://github.com/Akilleez-QA/client-tools/compare/949451032647e45e42c3aaef3f41b132c8af36e3...d788e64ced56832894ff77a7d0d5b30fbec1b2ce)) | 1 file, +17/−0 | The lock header uses assembly unsupported by MSVC x64; preserve Win32 and use interlocked x64 operations. |
| PCRE count: `review-ready/client-pcre-count` | [949451032647e45e42c3aaef3f41b132c8af36e3](https://github.com/Akilleez-QA/client-tools/tree/949451032647e45e42c3aaef3f41b132c8af36e3) → [1df8947d7971567c014e8e4815f95ac64b5f9963](https://github.com/Akilleez-QA/client-tools/tree/1df8947d7971567c014e8e4815f95ac64b5f9963) ([diff](https://github.com/Akilleez-QA/client-tools/compare/949451032647e45e42c3aaef3f41b132c8af36e3...1df8947d7971567c014e8e4815f95ac64b5f9963)) | 1 file, +1/−2 | The parser advertises capture-buffer bytes as an element count. |

These five deltas total **75 changed production lines** (+60/−15), excluding the prerequisite from dependent-package counts. ByteOrder and socket branches contain P, not the later imemmove test commits: merge/rebase planning must preserve the production prerequisite and retain its separately reviewed test package. They are separate candidate histories; do not merge overlapping prerequisite copies blindly.

| Package | Existing draft and evidence | Test boundary and remaining gate |
|---|---|---|
| imemmove | [Draft](https://github.com/Akilleez-QA/client-tools/tree/8da5d94466a377606ffbc877ac4d514a3576ee05/review/client-x64/pr-ready-next/imemmove/revision2/PR-v2.md); [evidence/reproduction](https://github.com/Akilleez-QA/client-tools/tree/8da5d94466a377606ffbc877ac4d514a3576ee05/review/client-x64/pr-ready-next/imemmove/revision2/RESULTS.md) | Real foundation-header valid-buffer regression; expected x64 baseline ambiguity and strict error-classifier controls. Based on M. Exact changed caller TUs and full consumers still need native build coverage; valid-buffer checks do not justify invalid-length behavior. |
| ByteOrder | [Draft](https://github.com/Akilleez-QA/client-tools/tree/8da5d94466a377606ffbc877ac4d514a3576ee05/review/client-x64/pr-ready-next/byteorder/PR-v2.md); [evidence/reproduction](https://github.com/Akilleez-QA/client-tools/tree/8da5d94466a377606ffbc877ac4d514a3576ee05/review/client-x64/pr-ready-next/byteorder/REPRODUCTION.md) | Real TU, byte oracle, symbol/architecture checks, Win32/x64 Debug/Release and no-swap mutation. Depends on P. This proves the bounded conversion functions, not a complete library/client build. |
| Socket/IOCP | [Draft](https://github.com/Akilleez-QA/client-tools/tree/8da5d94466a377606ffbc877ac4d514a3576ee05/review/client-x64/pr-ready-next/socket-widths/revision2/PR-v2.md); [evidence/reproduction](https://github.com/Akilleez-QA/client-tools/tree/8da5d94466a377606ffbc877ac4d514a3576ee05/review/client-x64/pr-ready-next/socket-widths/revision2/RESULTS.md) | Actual networking TU compile matrix and deliberate completion-key reversions; bounded Windows API fixtures. Depends on P. Real production TCP lifecycle/traffic and rebuilt consumer ABI remain separate gates. |
| HTTP lock | [Draft](https://github.com/Akilleez-QA/client-tools/tree/8da5d94466a377606ffbc877ac4d514a3576ee05/review/client-x64/pr-ready-next/http-lock23/PR.md); [evidence/reproduction](https://github.com/Akilleez-QA/client-tools/tree/8da5d94466a377606ffbc877ac4d514a3576ee05/review/client-x64/pr-ready-next/http-lock23/RESULTS.md) | Real trylock/unlock, recursion/exclusion/transfer and broken acquire/release controls. Based on M. Production lock/yield_thread, real HTTP traffic, owner-access race assumptions and fairness are not established. |
| PCRE count | [Draft](https://github.com/Akilleez-QA/client-tools/tree/8da5d94466a377606ffbc877ac4d514a3576ee05/review/client-x64/pr-ready-next/pcre-count/revision2/PR-v2.md); [evidence/reproduction](https://github.com/Akilleez-QA/client-tools/tree/8da5d94466a377606ffbc877ac4d514a3576ee05/review/client-x64/pr-ready-next/pcre-count/revision2/RESULTS.md) | Real PCRE providers, safe capture bounds, caller-source binding and reverted-count rejection. Based on M. Caller TU builds used separately identified development headers/configurations; this is not a clean isolated x64 client build or game-command acceptance. |

## Required review standard

- Review the exact proposed base/head and declare every prerequisite. Reproduce an exact-base native build of affected production callers/consumers; do not present a mixed development checkout as the isolated candidate.
- Preserve baseline failures and independently inspect that each deliberately broken control fails for the expected reason. Reject unrelated compiler errors, partial result counts and missing inputs.
- Run SDK-free regressions in portable CI where applicable. Windows ABI, compiler, driver and vendor behavior require the corresponding native or genuine-provider evidence; model agreement and source inspection cannot replace it.
- Record commands, toolchain/configuration, source and provider identities, exclusions and remaining runtime gates. Reviewers must assess the final proposed diff, including tests and build changes. A prior score or a branch named “review-ready” is not an approval.

## Remaining integration queue

The current combined product snapshot is [10fe0da59d63b5e7e0736d0427d100ed72b641e0](https://github.com/Akilleez-QA/client-tools/tree/10fe0da59d63b5e7e0736d0427d100ed72b641e0). Both implementation/client-miles and integration/client-x64-next were clean and remotely verified there. It contains 124 commits after M; the small candidate histories above are not ancestors of this combined branch. Their equivalent production fixes must be reconciled without duplicate application. [Integration CI passed](https://github.com/Akilleez-QA/client-tools/actions/runs/36807127038); this is the workflow's scoped result, not full-game acceptance.

| Committed C/C++ category against M | Files | Added | Deleted |
|---|---:|---:|---:|
| Engine/game client | 38 | 1,115 | 451 |
| Engine/game shared | 51 | 715 | 184 |
| Shared SOE libraries (`src/external/ours`) | 17 | 223 | 152 |
| Third-party/DPVS | 11 | 60 | 9 |
| Miles/Bink product runtime (`tools/miles-bridge/src`) | 103 | 9,846 | 0 |
| **Total** | **220** | **11,959** | **796** |

That is **12,755 changed production source lines**, not 12,755 additions (net +11,163). Reproduce with `git diff --numstat 94945103 10fe0da59`, classifying `.c/.cpp/.cc/.cxx/.h/.hpp/.hxx/.inl` in the listed paths. Tests/harnesses, build/project configuration and documentation are excluded (another 131 files, +13,702/−28). Runtime code counts as product code even when located under `tools/`.

## Product evidence checkpoint

- The source-verified full VS2013 Release x64 client dependency rebuild completed with **0 errors and 3,274 warnings**. Matching Release renderer, DPVS, libxml2 and original-provider host were packaged privately. The source/build files match this head; the final commit changes documentation only. Warnings are retained, not suppressed.
- Earlier Debug development builds under Proton rendered login and local ground/space scenes, responded to bounded ground movement, produced routed original Miles audio, and closed normally. These are artifact-specific observations, not representative gameplay or fidelity acceptance on the current head.
- At a904e489b, the actual Debug client visibly played one original Falcon Bink movie, returned to UI and closed normally. The Video7 admission repair was necessary: the earlier real-game attempt failed despite component checks.
- **Repeated movie playback remains a product failure under investigation.** The second command was visibly received by the console, but a second movie was not shown. The console's success text is unconditional. A private diagnostic build is ready to identify the rejection gate; there is no speculative source repair or repeated-playback claim.
- **Release runtime is not qualified.** One run reached login but its close sensor selected the wrong window title. After that sensor correction, a second run encountered a fatal X11/compositor failure before close. The initiating cause is not established. Neither run demonstrates normal Release shutdown.
- Vivox, native Windows/GPU operation, representative ground/space and mixed-width gameplay, and audiovisual fidelity remain open. Private SDKs, binaries, assets and raw runtime records are not public review artifacts.

Read-only GitHub heads showed upstream SWG-Source/client-tools/master still at M and **no published x64 branch**. Thus the verified upstream-master merge-base equals the original wire base; an alternate upstream x64 target cannot be assumed. Final submission target must be named before rebasing packages.

Remaining packaging work, not already completed packages:

1. Separate the remaining shared/client correctness changes and source-build/configuration work into dependency-ordered diffs, retaining production consumer tests and known limitations.
2. Reconcile the existing wire/DPVS/link candidates with later integrated tests and provider changes; earlier branch evidence does not automatically validate the latest combined tree.
3. Package the Miles process boundary and Bink integration around coherent lifecycle/API/engine integration units. **The 9,846-line bridge is not currently split into small PR packages**; preserve causal callback, ownership and shutdown invariants when choosing boundaries. Vendor binaries, SDK bodies and private media remain outside public source.
4. Keep the new changes separately reviewable: b9d3408f1 enforces the process-owned callback runtime's non-deletion at compile time; 33efad160 enables isolated Release development targets; 10fe0da59 documents the evidence limits. The two host configurations built, and attempted deletion fails with the expected compiler diagnostic. These commits do not establish Release runtime or media fidelity.

This index deliberately makes no 10/10 quality claim. Small diffs, recorded evidence and meaningful review gates make work inspectable; full client, media, voice and mixed-width gameplay acceptance remain distinct from package organization. Historical packet introductions may describe older product states; use their pinned evidence for the stated candidate only.
