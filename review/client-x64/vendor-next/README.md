# Client x64: vendor decisions and native checkpoint

2026-09-30. **The client is not finished.** The persistent goal is a polished x64 SWG Source client with the existing game experience preserved. Development and evidence stay on Akilleez-QA's forks. The user designated upstream `x64` as the eventual destination, but requires completion and explicit approval before any PR. No upstream changes or new PRs were made.

Start with the [SWG Source baseline correction](vendor-options/BASELINE.md): browser and TCG are documented deprecated features, and normal voice controls are disabled. They must not become speculative restoration projects merely because old wrappers/binaries remain. Then read the [per-vendor options and decision gates](vendor-options/DECISIONS.md).

## Current status and bridge design

Product branch `integration/client-x64-next` is at **49d0eeed4**. Actual source-audited incremental MSBuild results: Win32 Release/Debug link with zero errors; x64 Release/Debug reach the final linker and stop on **60/61 original Miles imports**. No x64 client has launched. [Current build evidence](allocator-next/integration-current-v2/current-head-v2-complete/RESULTS.md).

Read the [bridge architecture proposal](vendor-options/miles-integration-seam/ARCHITECTURE.md): one MediaSession authority, original game audio policy in x64, original Miles and Bink together in x86, explicit callbacks/reverse I/O and resource lifetime. It is under review, not a production backend selection. [Independent Astra architecture opening](blind-astra-miles14/ARCHITECTURE-CRITIC.md) and [original blind review](blind-astra-miles14/ASTRA-BLIND-REVIEW.md) are preserved separately from subsequent nonblind work.

[Candidate component evidence](vendor-options/miles-integration-seam/REVIEW-RECONCILIATION-15.md) includes codec/resource handling, retained bytes, scalar dispatch preflight, and WAV metadata. The original Miles DLL supplied one real WAV metadata result that roundtrips through native x64. These components are not a complete client backend. The [real Audio/Sound2d baseline still fails teardown](vendor-options/miles-engine-fixture/RESULTS.md), and actual callback coordination, Bink integration and representative fidelity remain open.

Native [startup preference observations](vendor-options/miles-runtime-preferences/RESULTS.md) found lock protection off and mutex protection on, with selected x87 precision preserved. No device or playback was involved; it is not a general callback or FPU-equivalence result.

Latest bounded follow-ups:

- [File-callback seam and native compile evidence](vendor-options/miles-integration-seam/reverse-file-seam20/COMPILE-PLAN.md): original callbacks remain unchanged; baseline and proposed full `Audio.cpp` each compile on Win32/x64 Debug/Release. [Maintainer follow-up](vendor-options/miles-integration-seam/reverse-file-seam20/REVIEW-maintainer21-followup.md) rates the dormant source seam 9/10. It is not a reverse-I/O implementation.
- [Startup metadata revision4](vendor-options/miles-integration-seam/startup-metadata-v4/RESULTS.md): five caller-shaped genuine SDK operations, owned directory inputs and returned text, separate request/reply limits, cleanup controls and two-path discrimination. The [final blind review](vendor-options/miles-integration-seam/startup-metadata-v4/REVIEW-senior21-final.md) closes its three findings within their stated scope. Earlier [blind review](vendor-options/miles-integration-seam/startup-metadata-candidate/REVIEW-senior21.md) and [revision3 follow-up](vendor-options/miles-integration-seam/startup-metadata-v3/REVIEW-senior21-followup.md) preserve findings and imperfect earlier tests.
- [Version-resource correction](vendor-options/miles-integration-seam/session-version22/RESULTS.md): reads the supplied held module directly, eliminating the basename lookup identified by the [earlier blind review](vendor-options/miles-integration-seam/session-version21/REVIEW-senior22.md). Native resource controls and file-backed x64 consumption pass; poisoned compile-time text does not replace the actual7.2a resource. The [fresh blind review](vendor-options/miles-integration-seam/session-version22/REVIEW-senior23.md) accepts the bounded correction and records two nonblocking test-attribution gaps. This is not live transport or game acceptance.
- [Build/output receipt tools](vendor-options/miles-integration-seam/live-bridge-candidate/revision4-tools/README.md) bind fresh compile inputs and output hashes; they do not retroactively strengthen old runtime attribution.
- [Teardown source/symbol discriminator](vendor-options/miles-engine-fixture/TEARDOWN-INDEPENDENT20.md) and an unexecuted original-context observer patch preserve the failed engine baseline. No allocator/teardown repair is claimed.
- [Maintainability disposition](vendor-options/miles-integration-seam/MAINTAINABILITY-RESPONSE21.md) and [Composer/Grok reconciliation](vendor-options/miles-integration-seam/CLI-RECONCILIATION21.md) record costs, reviewer errors and open integration obligations.

These experiments are not wired into the product. The actual x64 client still has the 60/61-import link failure above; successful component checks do not reduce that count by themselves.

The [maintainer design review](vendor-options/miles-integration-seam/MAINTAINER-DESIGN23.md) identifies overlapping lifecycle owners, incompatible status meanings, repeated validation and unimplemented callback scheduling. These are integration work, not a claim that the tested components make a production backend.

The [next bounded integration](vendor-options/miles-integration-seam/NEXT23.md) connects those components through the existing two-process path while retaining the no-adoption boundary.

The remaining sections retain earlier commit/build history under their named snapshots. Use the [latest checkpoint](vendor-options/CHECKPOINT-2026-09-30.md) and current build above for present status.

## Earlier committed work and chronological evidence

| Commit | Change | Bounded evidence |
| --- | --- | --- |
| [cf82805a9](https://github.com/Akilleez-QA/client-tools/commit/cf82805a9d13e6082ae96977093d670ea116a82f) | Full-width x64 allocation statistics through consumers | Native statistics 11/11 per configuration; 32/32 caller TU compiles. Viewer/Maya remain source-reviewed only. |
| [5fe9314e0](https://github.com/Akilleez-QA/client-tools/commit/5fe9314e00e36701494c7bc689515661985ecbec) | Real source-built JPEG/STLport and correct native renderer SDK inputs | Six actual x64 renderer project links; cache, mutation and failure checks. No vendor substitutes. |
| [8e6b08fbd](https://github.com/Akilleez-QA/client-tools/commit/8e6b08fbd47775ca48083b102a7d14bc717be4dc) | Allocated blocks and split remainders fit their free-list representation | 1,622/1,622 native checks in each Debug/Release Win32/x64 configuration. Untracked product layout. |
| [d0fea5bc7](https://github.com/Akilleez-QA/client-tools/commit/d0fea5bc7) | Miles file-callback handles use the SDK's pointer-width type end to end | Actual TU compiles on four configurations; real TreeFile callback slices pass 18/18 Release and 20/20 Debug per ABI. Debug x64 requires the preceding allocator fix. |
| [5755f8f3b](https://github.com/Akilleez-QA/client-tools/commit/5755f8f3beee3ddf16d0767c0cf78f1b700327a6) | Reuse checked string length through the payload write | Existing wire matrix 50/57 client and 19/20 server; mirrored server fork commit [28f43f68](https://github.com/Akilleez-QA/src/commit/28f43f686d4ac81338a4b097d2f1726ae20e8f38). |
| [25f7fff28](https://github.com/Akilleez-QA/client-tools/commit/25f7fff28d24c91b932ba95df5a740081b5248e5) | Check Miles preference narrowing and retain diagnostic count width | Actual clientAudio project rebuilds with zero warnings/errors in all four configurations. Arithmetic boundary oracle is separate from vendor/runtime FATAL behavior. |
| [94a81438c](https://github.com/Akilleez-QA/client-tools/commit/94a81438c4c442f21105a58047c82d34e04c9cb4) | Remove unused Mozilla build inputs for Debug/Release client | Win32 whole-executable comparison below; no feature restoration or new feature removal. |

These commits and the later reviewed batch are on `integration/client-x64-next`. **Head at this earlier checkpoint: `085f77cc7`.** The [latest checkpoint](vendor-options/CHECKPOINT-2026-09-30.md) lists TrackIR, LoginClusterStatus fixtures, ByteStream bounds, build-output ownership, TCP completion keys and four isolated crypto commits. External LCD SDK integration remains a separate candidate. The older matrix below retains its original scope.

The next frozen source `94a81438c` reduced x64 blocking errors to one per configuration: Release TcpClient completion-key width, Debug crypto packing diagnostics. Those roots now have separately passing native project/probe results, and both audited incremental builds of91dc now reach the actual client linker. Each stops on the first wrong-architecture input: legacy x86 STLport. This is not a completed client link. [Matrix](allocator-next/integration-current-v2/matrix-summary.json), [warning review](allocator-next/integration-current-v2/WARNING-REVIEW.md). Neither earlier matrix reached a complete x64 client link.

## Native full-build checkpoint

The frozen source snapshot contains the statistics, Audio callback and renderer candidates, but **excludes** the later minimum-block and TrackIR changes. See [snapshot record](allocator-next/integration-current/checkpoint.md) and [matrix JSON](allocator-next/integration-current/matrix-summary.json).

| Configuration | Result |
| --- | --- |
| Win32 Release | 0 errors, 170 warnings |
| Win32 Debug | 0 errors, 219 warnings; existing ForceFileOutput setting retained, no unresolved-symbol/LNK4088 records observed |
| x64 Release | 24 compiler errors, all from the legacy Mozilla SDK architecture/header root |
| x64 Debug | 27 errors, including Mozilla and warnings treated as errors in crypto/clientAudio |

Neither x64 attempt reached a complete client link. Counts are compiler diagnostics, not root-cause counts.

The separate browser omission proof then succeeded on Win32 Release and Debug. Removing only SwgClient's Mozilla scheduling edge and explicit browser inputs produces whole executables identical after normalization of timestamps and PDB age; PDB GUID/path and code remain compared. Other tool dependencies are retained. [Comparison JSON](allocator-next/integration-current/mozilla-link-proof-v2/comparison.json).

## Vendor experiments

- [Miles](vendor-options/miles-options.md): original 7.2a and its actual plugin decode a real game MP3. FFmpeg/miniaudio produce different PCM despite matching frame count/alignment. Native playback lacks a VM output endpoint. A later isolated Wine/PipeWire route captures clocked original playback and a real x64-to-x86 single-command host, but repeat captures differ and establish no accepted fidelity tolerance. [Clocked results](vendor-options/miles-realtime/RESULTS.md).
- [Bink](vendor-options/bink-probe/report.md): original 1.9c decodes a public non-SWG sample; an x64 process receives four nonblack frames through a verified pipe. All four differ from the fixed FFmpeg oracle. This sample has no audio. Game presentation/synchronization remain open.
- [Vivox](vendor-options/vivox-options.md): original 52-entry API resolves and local object/XML lifetime checks pass on Win32. Voice is normally disabled; a saved-preference corner remains source-reachable. No voice service or remote account operation was run.
- [Logitech](vendor-options/logitech-native-route.md): an official signed legacy package provides genuine low-level x64 APIs. All 16 unchanged wrapper translation units compile in four configurations; real wrapper executables link against the original SDK and actual SWG core/allocator libraries in all four. API layout comparisons also pass. Actual hardware/manager behavior is not established.
- [TrackIR](vendor-options/trackir.md): official native provider naming and old/current SDK layout agree with the committed bounded loader; actual TU compilation and80 path cases per configuration pass. Hardware and profile acceptance remain open.
- [Other vendors and conditional reachability](vendor-options/secondary-vendors.md); [reviewer findings and corrections](vendor-options/review-reconciliation.md).

## Reproduction and limits

The packet contains diagnostic source, commands, source hashes, raw counts and text logs. [native-text.zip](native-text.zip) retains native compiler/link/runtime output with its directory layout. Audio historical failures and current successes are retained in its diagnostic ZIPs. They are not all portable one-command tests: scripts refer to the documented v120/SDK checkout and real native core libraries, and proprietary runtime/media inputs must be supplied from the local reference installation. The published wire CI remains independently reproducible.

No game assets, decoded media, proprietary DLLs/libraries, SDK header packages or built client executables are published here. The manifest hashes the published files; it is an integrity record, not an attestation of complete correctness. Actual SDK/package hashes and official retrieval sources are recorded without bundling those artifacts.

Read individual result files for their original candidate-time wording and scope. The commit table above records which candidates have since been committed. Full x64 linking, native graphics execution, representative gameplay, hardware features and mixed-width connection acceptance remain work in progress.
