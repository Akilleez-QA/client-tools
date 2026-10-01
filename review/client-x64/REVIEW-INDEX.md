# SWG client/server submission index

The completed x64 implementation is packaged into focused source and build changes. Independent source/evidence reviews found no remaining introduced blockers in the submitted packages. This is a review map, not merge approval or a claim of full gameplay/fidelity acceptance.

All **220 production paths and 83 build/configuration paths** in the maintained client inventory are assigned to package closures. [Finite accounting](package-inventory/remaining-units.md) separates assignment coverage from a fresh composed-tree build. [Client map](package-inventory/remaining-package-map.json) and [server map](package-inventory/server-package-map.json) retain source identities and dependency details. No histories were force-pushed or automatically merged.

## Review order

Review independent master-based fixes first. For fork drafts, use the displayed base branch: its prerequisite changes are intentionally excluded from the diff. Joint bases preserve already-published dependencies. Follow allocator layout → addresses → sizes → statistics, and Miles contracts → facade → transport/callbacks → host/session → build/Audio → game selection → Bink host → renderer → Release configuration. Shared server counterparts have separate bases and explicitly scoped evidence.

The latest [submission hygiene check](package-inventory/final-submission-hygiene.md) verified 24 selected PRs and 86 pinned evidence links. No checks were reported on that selected set; absent CI is not a pass. The later exact-head [composed regression run](https://github.com/Akilleez-QA/client-tools/actions/runs/36850510021) passed both ABI jobs; [results and raw log](pr-ready-next/regression-ci/RESULTS.md). Other earlier checks and failures remain in the individual packets and [historical index](REVIEW-INDEX-before-final-packaging.md).

## Upstream submissions

The table counts the **entire PR delta**, including any tests/configuration/docs. Individual PR bodies separate production counts. Head SHAs were queried on 2026-10-01. Source branches live on our forks; no upstream branch pushes occurred.

| Repository / PR | Scope | Head | Files; +/− | State |
|---|---|---|---|---|
| [SWG-Source/client-tools #22](https://github.com/SWG-Source/client-tools/pull/22) | Remove unused explicit Win32 Release link inputs | `46a56f6a52` | 1; +1/−1 | open |
| [SWG-Source/client-tools #23](https://github.com/SWG-Source/client-tools/pull/23) | Preserve legacy wire widths on 64-bit clients | `e6738a9f5b` | 38; +1083/−95 | open |
| [SWG-Source/client-tools #24](https://github.com/SWG-Source/client-tools/pull/24) | DPVS: add x64 support with a bounded legacy numerical compatibility repair | `ebce07521e` | 15; +908/−27 | open |
| [SWG-Source/client-tools #25](https://github.com/SWG-Source/client-tools/pull/25) | Separate the checked int-length move helper from CRT memmove | `a7954b5e78` | 9; +265/−7 | open |
| [SWG-Source/client-tools #26](https://github.com/SWG-Source/client-tools/pull/26) | Pass the PCRE capture-vector capacity in elements | `123cce87b7` | 5; +207/−1 | open |
| [SWG-Source/client-tools #27](https://github.com/SWG-Source/client-tools/pull/27) | Preserve natural alignment in the UI pool stride | `5ff93941c3` | 1; +1/−1 | open |
| [SWG-Source/client-tools #28](https://github.com/SWG-Source/client-tools/pull/28) | Retain pointer-width ShellExecute results | `6d73ef869f` | 2; +3/−3 | open |
| [SWG-Source/client-tools #29](https://github.com/SWG-Source/client-tools/pull/29) | Preserve allocator header size and full-width block-order checks | `2af9f19b50` | 1; +6/−3 | open |
| [SWG-Source/client-tools #30](https://github.com/SWG-Source/client-tools/pull/30) | Support the HTTP lock on MSVC x64 | `003f8757c7` | 6; +456/−0 | open |
| [SWG-Source/client-tools #31](https://github.com/SWG-Source/client-tools/pull/31) | Preserve native Miles widths and Audio diagnostic arguments | `0699bd3d9b` | 1; +28/−24 | open |
| [SWG-Source/client-tools #32](https://github.com/SWG-Source/client-tools/pull/32) | foundation: support Windows x64 floating point controls | `16dbf07a4e` | 3; +55/−2 | open |
| [SWG-Source/client-tools #33](https://github.com/SWG-Source/client-tools/pull/33) | Preserve Windows diagnostic pointers and timestamp reads on x64 | `855b299004` | 4; +14/−4 | open |
| [SWG-Source/client-tools #34](https://github.com/SWG-Source/client-tools/pull/34) | math: add Windows x64 SSE kernels | `3c8c9099dc` | 4; +235/−1 | open |
| [SWG-Source/client-tools #35](https://github.com/SWG-Source/client-tools/pull/35) | Fix x64 UI, tag and mesh native-size mismatches | `9396a51814` | 7; +19/−11 | open |
| [SWG-Source/client-tools #36](https://github.com/SWG-Source/client-tools/pull/36) | Match game archive callback indices on x64 | `e26bdd9b2f` | 4; +12/−10 | open |
| [SWG-Source/client-tools #37](https://github.com/SWG-Source/client-tools/pull/37) | Retain inserted FileManifest entries until removal | `514498397a` | 1; +2/−2 | open |
| [SWG-Source/client-tools #38](https://github.com/SWG-Source/client-tools/pull/38) | Use native SDK declarations when building bundled STLport sources | `de5e89d01c` | 2; +13/−0 | open |
| [SWG-Source/client-tools #39](https://github.com/SWG-Source/client-tools/pull/39) | Check legacy crypto length and message-count boundaries on x64 | `19eb22639f` | 4; +28/−5 | open |
| [SWG-Source/client-tools #40](https://github.com/SWG-Source/client-tools/pull/40) | Select the native TrackIR provider with bounded paths | `12e1a62160` | 1; +14/−4 | open |
| [SWG-Source/src #35](https://github.com/SWG-Source/src/pull/35) | Complete Linux server LP64 compatibility, database boundaries and shutdown fixes | `6b998f6fc2` | 621; +12247/−4800 | open |
| [SWG-Source/src #37](https://github.com/SWG-Source/src/pull/37) | Separate the checked int-length move helper from CRT memmove | `1481143ca4` | 9; +338/−5 | open |
| [SWG-Source/src #38](https://github.com/SWG-Source/src/pull/38) | Build the submitted server revision in legacy CI | `1c0152794e` | 1; +45/−19 | open |

Server #35 targets `64-bit-types`, not master. Its upstream dependency history is not part of the other focused PRs. The maintained client master remains `94945103`; no upstream x64 target was available at the recorded target check.

## Dependent fork drafts

These are reviewable incremental packages, not independently qualified full-client/server builds. Remaining dependencies are explicit. No private SDKs, provider binaries or game media are included.

| Fork / PR | Scope | Head | Base | Files; +/− |
|---|---|---|---|---|
| [Akilleez-QA/client-tools #1](https://github.com/Akilleez-QA/client-tools/pull/1) | Support Windows x64 byte-order conversions | `b0a977f8df` | `client-imemmove` | 6; +307/−0 |
| [Akilleez-QA/client-tools #2](https://github.com/Akilleez-QA/client-tools/pull/2) | Preserve Windows socket handles and IOCP keys at pointer width | `dbcd4d7d95` | `client-imemmove` | 11; +545/−6 |
| [Akilleez-QA/client-tools #3](https://github.com/Akilleez-QA/client-tools/pull/3) | Preserve allocator owner and diagnostic stack addresses on Windows x64 | `fc667f38ea` | `client-allocator-layout` | 15; +346/−149 |
| [Akilleez-QA/client-tools #4](https://github.com/Akilleez-QA/client-tools/pull/4) | Check allocator sizes and preserve the minimum free-block representation | `1f8f341aab` | `client-allocator-address-stack` | 1; +70/−29 |
| [Akilleez-QA/client-tools #5](https://github.com/Akilleez-QA/client-tools/pull/5) | Introduce the private Miles contracts and codec | `8ebfbe2c8b` | `master` | 18; +1359/−0 |
| [Akilleez-QA/client-tools #6](https://github.com/Akilleez-QA/client-tools/pull/6) | Add native Miles facade adapters | `0fb8da90bd` | `client-miles-contracts` | 15; +945/−0 |
| [Akilleez-QA/client-tools #7](https://github.com/Akilleez-QA/client-tools/pull/7) | Add Miles file transport and reply transactions | `9ef7a2c7dd` | `client-miles-native-facade` | 20; +1331/−0 |
| [Akilleez-QA/client-tools #8](https://github.com/Akilleez-QA/client-tools/pull/8) | Add Miles engine-worker admission and client callback ownership | `97dc8c1f92` | `client-miles-file-transport` | 17; +1798/−0 |
| [Akilleez-QA/client-tools #9](https://github.com/Akilleez-QA/client-tools/pull/9) | Add the Miles host backend and callback runtime | `7bedd5e2f9` | `client-miles-client-callbacks` | 15; +1773/−0 |
| [Akilleez-QA/client-tools #10](https://github.com/Akilleez-QA/client-tools/pull/10) | Add the Miles pipe facade and session composition | `3430934ced` | `client-miles-host-runtime` | 12; +2158/−0 |
| [Akilleez-QA/client-tools #11](https://github.com/Akilleez-QA/client-tools/pull/11) | Add Miles component build entry points and guarded Audio handoff | `afe844818e` | `client-miles-audio-prerequisites` | 6; +564/−40 |
| [Akilleez-QA/client-tools #12](https://github.com/Akilleez-QA/client-tools/pull/12) | Generate isolated v120 Debug/Release x64 client configurations | `5b558625c0` | `client-x64-config-prerequisites` | 71; +7727/−0 |
| [Akilleez-QA/client-tools #13](https://github.com/Akilleez-QA/client-tools/pull/13) | Archive: bound payload reads and preserve ByteStream storage | `085a62e335` | `ci/client-wire` | 5; +117/−100 |
| [Akilleez-QA/client-tools #14](https://github.com/Akilleez-QA/client-tools/pull/14) | Preserve allocator byte statistics and null reallocation metadata | `0c09740e0c` | `client-allocator-size-invariants` | 15; +85/−65 |
| [Akilleez-QA/client-tools #15](https://github.com/Akilleez-QA/client-tools/pull/15) | Implement x64 hard-skinning kernels with SSE intrinsics | `4f44852113` | `client-skeletal-prerequisites` | 1; +97/−0 |
| [Akilleez-QA/client-tools #16](https://github.com/Akilleez-QA/client-tools/pull/16) | Build and select genuine x64 client dependencies | `ba1dd44324` | `client-native-provider-prerequisites` | 19; +912/−13 |
| [Akilleez-QA/client-tools #17](https://github.com/Akilleez-QA/client-tools/pull/17) | Require a resolved x64 client link and reserve two MiB of stack | `5292d6fd8d` | `client-native-providers` | 1; +4/−0 |
| [Akilleez-QA/client-tools #18](https://github.com/Akilleez-QA/client-tools/pull/18) | Opt in to the development x64 Miles process boundary | `78428d8c3f` | `client-miles-game-prerequisites` | 15; +493/−33 |
| [Akilleez-QA/client-tools #19](https://github.com/Akilleez-QA/client-tools/pull/19) | Carry original Bink decoding through the existing media host | `16942c5fc6` | `client-miles-game-selection` | 27; +1616/−24 |
| [Akilleez-QA/client-tools #20](https://github.com/Akilleez-QA/client-tools/pull/20) | Select the original Bink host through the development video adapter | `abe067bcc7` | `client-bink-host-session` | 9; +511/−225 |
| [Akilleez-QA/client-tools #21](https://github.com/Akilleez-QA/client-tools/pull/21) | Build matching Release Miles and Bink development components | `91d70a54b6` | `client-bink-game-selection` | 4; +57/−28 |
| [Akilleez-QA/client-tools #22](https://github.com/Akilleez-QA/client-tools/pull/22) | Remove unused browser build inputs and disabled capture polling | `f5c3f27851` | `client-x64-projects` | 3; +5/−11 |
| [Akilleez-QA/client-tools #23](https://github.com/Akilleez-QA/client-tools/pull/23) | Add bounded Archive storage and decoder regression runners | `6ebf897912` | `client-archive-storage` | 6; +424/−0 |
| [Akilleez-QA/client-tools #24](https://github.com/Akilleez-QA/client-tools/pull/24) | Cover galaxy-list and ordinary-container wire encodings | `d8cb69a4b5` | `client-archive-storage` | 5; +256/−35 |
| [Akilleez-QA/client-tools #25](https://github.com/Akilleez-QA/client-tools/pull/25) | Preserve the native UI pool alignment regression harness | `fdaa82180f` | `prerequisite/client-ui-memory-tests` | 3; +157/−0 |
| [Akilleez-QA/client-tools #26](https://github.com/Akilleez-QA/client-tools/pull/26) | Record bounded mixed-width sessions and paired media shutdown | `926eda724a` | `client-wire-regressions` | 1; +171/−0 |
| [Akilleez-QA/client-tools #27](https://github.com/Akilleez-QA/client-tools/pull/27) | Compose the archive and media protocol regressions in CI | `505795c7dd` | `prerequisite/client-regression-ci` | 1; +26/−1 |
| [Akilleez-QA/src #1](https://github.com/Akilleez-QA/src/pull/1) | Preserve Windows socket handles and IOCP keys at pointer width | `9d44e3a1da` | `server-network-prerequisites` | 10; +352/−6 |
| [Akilleez-QA/src #2](https://github.com/Akilleez-QA/src/pull/2) | Support the Windows byte-order functions on x64 | `adb1bc91d2` | `server-network-prerequisites` | 1; +26/−0 |
| [Akilleez-QA/src #3](https://github.com/Akilleez-QA/src/pull/3) | foundation: support Windows x64 floating point controls | `01755444ed` | `server-build-workflow` | 3; +55/−2 |
| [Akilleez-QA/src #4](https://github.com/Akilleez-QA/src/pull/4) | math: add Windows x64 SSE kernels | `9aa3e319be` | `server-build-workflow` | 4; +235/−1 |
| [Akilleez-QA/src #5](https://github.com/Akilleez-QA/src/pull/5) | Bound archive payload reads and preserve storage ownership | `0b45f5e726` | `lp64-fixed-width-boundaries` | 5; +116/−100 |
| [Akilleez-QA/src #6](https://github.com/Akilleez-QA/src/pull/6) | Capture native Windows stacks with complete DbgHelp locking | `b17b06f87a` | `lp64-fixed-width-boundaries` | 1; +49/−5 |
| [Akilleez-QA/src #7](https://github.com/Akilleez-QA/src/pull/7) | Use native-width Windows diagnostics and API results | `fc300fe802` | `server-build-workflow` | 4; +21/−3 |
| [Akilleez-QA/src #8](https://github.com/Akilleez-QA/src/pull/8) | Preserve host-sized string lengths in shared helpers | `7dc8ef9194` | `server-network-prerequisites` | 2; +5/−5 |
| [Akilleez-QA/src #9](https://github.com/Akilleez-QA/src/pull/9) | Scope the native crypto PCH packing diagnostic | `485331412c` | `server-build-workflow` | 1; +11/−0 |

## Source size and evidence boundaries

The maintained implementation is `eca74ffa5741f608a1417944b2e2602868936517`, with last production change `da9c56054`. Its frozen count is **12,761 changed production lines: +11,965/−796 in 220 files**. This includes 9,852 Miles/Bink runtime lines under `tools/miles-bridge/src`; it excludes tests, build tools and docs. Explicit Myers counting gives 12,759 because of hunk alignment in two files; [the accounting record](package-inventory/remaining-units.md) explains the difference. Do not add dependent PR totals together or compare this focused work with PR21's entire migration as an equal-scope ratio. The later TrackIR registry correction is separate from that frozen snapshot.

The recorded full VS2013 Release-x64 dependency rebuild had 0 errors and 3,274 warnings. Original-provider movie replay, bounded mixed-width sessions and Release/Proton observations are preserved in the [historical evidence summary](REVIEW-INDEX-before-final-packaging.md#product-evidence-checkpoint). These records do not establish a new full build of every split branch, native-Windows GPU behavior, representative gameplay or complete audiovisual fidelity.

[TrackIR's new registry boundary check](pr-ready-next/trackir-provider/RESULTS.md) is separately scoped: 16 cases / 32 queries per native ABI, with original failing-capacity controls. It executes the extracted real WinAPI contract, not the production loader or hardware. The original runner and hardened reproduction runner remain distinct.

## Packaging disposition

All planned production/build packages and identified auxiliary follow-ups are now reviewed and published: **22 upstream PRs and 36 dependent fork drafts**, including the earlier wire/DPVS/link submissions. [Final accounting](package-inventory/final-packaging-disposition.json) records the completed auxiliary queue. The last five drafts deliver archive tests, galaxy/container wire regressions, native UI tests, scoped live-session notes and the portable CI composition.

At CI head `505795c7d`, wire checks passed 71/71 Win32 and 78/78 Win64; ByteStream passed 85 and decoder checks 34 per ABI. Dependency ownership passed 12 tests; Linux sanitizer checks passed 298 EOS, 1,047 Bink protocol and 22 video-admission assertions. These counts are separate suites, not a full-client correctness metric. Native UI retains its scoped historical four-configuration records and manual genuine-provider requirements.

Maintainers control merges and upstream prerequisite decisions. Dependent diffs must be reconciled without duplicate application; no automatic merge or history rewrite was performed. Historical baseline failures, consumer dependencies, numerical limitations and incomplete runtime acceptance remain in each packet. The completed deliverable is PR packaging, not a new claim of universal gameplay/fidelity equivalence. No numerical review score substitutes for that assessment.
