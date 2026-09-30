# Fork checkpoint — 2026-09-30

Client `integration/client-x64-next` at `91dc05e8bebe0881d0540e74d4c53de909feb876`. Server compatibility changes remain on Akilleez-QA/src `integration/windows-shared-compat`. No upstream writes or PRs. Eventual upstream x64 destination requires finished acceptance and the user's explicit PR approval.

## New committed work

| Client commit | Change | Evidence and ceiling |
| --- | --- | --- |
|6776d2054|Native TrackIR provider selection and bounded registry path|Actual TU/layout checks in four configurations;80 path checks per configuration. No hardware/profile6001 acceptance.|
|3550071ed|Bounded LoginClusterStatus fixtures and strict verdict handling|Parent59/59 Win32,66/66 Win64; stock56/56 legacy oracle. Includes multi-galaxy bytes, not a live login.|
|8d9010900|ByteStream read/write arithmetic, growth and ownership|85 checks on each portable ABI and all four native configurations; parent wire59/66. Independent18-check small-buffer review. Server mirror7131fd38; outer-decoder preflight and rollback remain separate.|
|10e684ba7|Reject renderer-dependency outputs without established ownership|12 tests on host and native Windows, no skips; no complete renderer rebuild claimed from this policy-only change.|
|782aed355|TcpClient IOCP completion key at pointer width|SharedNetwork real project all4 builds; Windows high-key completion probe all4. Server mirror4e610ac9. Not a live client connection.|
|78e1f907c|Scope x64 STLport packing diagnostic in Crypto PCH|Real crypto all4 builds; /WX positive4/4 and deliberately unbalanced later-header controls rejected4/4; before/after layouts unchanged4/4. Server guarded wrapper78ec0f03.|
|8fe43cca9|Checked legacy StringStore length|Candidate real-library runtime10checks Win32 and12 x64, both configurations; unchecked-template control fails rejection. Synthetic limit view is never transferred.|
|978a45d81|Explicit attached-message presence test|Same normal attached-queue runtime checks; no cryptographic algorithm change.|
|91dc05e8b|Keep message count in public unsigned range|Ordinary queue lifetime checks pass; UINT_MAX completed-message limit source-reviewed, not billions of entries allocated. Per-message byte counter unchanged.|

[CI at782aed355](https://github.com/Akilleez-QA/client-tools/actions/runs/36687745028) passed the wire/ByteStream/ownership workflow. [CI at91dc05e8b](https://github.com/Akilleez-QA/client-tools/actions/runs/36688620867) also passed; native full-client result remains pending. CI scope is its fixtures, not native game acceptance.

## Native build progression

Historical snapshot `integration-current` has Win32 Release0errors170warnings, Debug0errors219warnings, x64 Release24errors and Debug27errors. It excludes later repairs; do not apply those counts to current HEAD.

Immutable `94a81438c` snapshot `integration-current-v2` is git-archive-derived with20533 tracked source files. Output-path evaluation passes132project/configuration audits. Release x64:1error3874warnings; Debug x64:1error3722warnings. Actual blocking roots are TcpClient's completion-key output type and crypto PCH packing diagnostics. Neither reached final SwgClient link. Logs repeat warnings in summaries; the warning census groups808compiler locations and does not count defects.

Current91dc full build uses an audited commit-bound delta over the frozen private tree, retaining source hashes and earlier outputs/logs. It is incremental, not a clean rebuild. LCD scratch properties are excluded from that run. Native project/probe successes cannot predict the final executable's dependency closure.

## Vendor decisions remain open

Original Miles7.2a plays through a clocked private capture route. Actual x64 controller to identical x86 runtime host works for a single sample/stream command. Original-repeat and direct/controller captured PCM differ; no accepted tolerance, listener equivalence, production helper, callback RPC or TreeFile bridge exists. EOS on this route is a worker-thread event and is not device-drain time. [Full scope](miles-realtime/RESULTS.md).

Genuine legacy Logitech x64 APIs and all-four wrapper links are established, with software layout evidence; hardware/manager behavior is not. TrackIR filename/layout/path checks are established, with provider/profile/device acceptance open. Bink remains a bounded codec/transport probe on a non-SWG sample without audio. Voice preserves the documented disabled baseline, with a saved-setting corner still tracked.

## Active work and completion boundary

The native build owns compiler/link diagnostics. Separate workers review raw decoder preflight, checked AutoArray/AutoList counts, crash formatting and UI allocation limits. Grok/Composer/Codex CLI findings are independently checked; agreement on shared source is not independent runtime evidence. New candidates do not enter this committed snapshot until reviewed and tested.

Delivery state: committed, pushed, and tested within the scopes above. Outcome state: individual fixtures passed; full x64 client incomplete. Highest justified claim: these bounded width/ownership/build repairs have reproducible targeted evidence. Required runtime observation: full link/start, representative ground/space, mixed-width sessions, media and hardware fidelity. Agent controls further builds and available probes; missing native graphics/audio/hardware/services remain explicit test boundaries. Persistent native goal remains active.

## Later fork push and final-link milestone

Code was pushed and the remote verified at `085f77cc73503176931f504a1a2a142640d67240` around 04:27 Eastern. New independent commits:

- `d89b9f49e`: Decoder payload checks and aligned Unicode byte copy. The 34 focused checks pass on both portable ABIs and all four native configurations. The parent also ran 34/34 on the server counterpart on both Linux ABIs. Complete headers remain consumed on rejection; outer rollback is not promised.
- `4d3009851`: AutoArray/AutoList checked counts and 12 ordinary-container legacy-byte checks. The combined parent suite passes 71/71 Win32 and 78/78 Win64; stock Win32 passes 68/68.
- `b1277c963`: Full-pointer exception-address formatting, with 36 extracted-statement checks per native configuration.
- `085f77cc7`: Genuine external x64 Logitech SDK selection and exact archive check. Eight native evaluations establish unchanged Win32 inputs/directories; x64 only prepends the verified SDK directory. Hardware and full-client acceptance remain open.

[CI on085f77cc7](https://github.com/Akilleez-QA/client-tools/actions/runs/36689808371) passed the expanded wire suite, 85 ByteStream checks, 34 decoder checks and output-ownership tests within their matrix scopes.

Both actual x64 incremental builds of **91dc05e8b**, before these newer commits, now reach the SwgClient final linker with no compiler errors. Release stops with 1 error/1,602 warnings; Debug with 1 error/1,633 warnings: `LNK1112` at legacy x86 `stlport_vc71_stldebug_static.lib(locale_impl.obj)`. This is the first encountered link blocker, not a complete vendor inventory. Warning totals from incremental builds are not comparable to clean builds. Selecting genuine source-built x64 STLport is a separate candidate. Its default-library directives, CRT and STL modes are under review.

The original Miles file-callback experiment addresses a missing contract: success return 1 with handle 0 is accepted by the actual 7.2a DLL, just like handle 1. Both produce 14 reads/9,020 bytes, 3 seeks, 1 close and 1 EOS. Failed open for the missing name has no following file callbacks. The parent checked the raw traces and DLL hash. Callback-thread observations apply only to this small probe; they establish no TreeFile, TLS, helper RPC or fidelity result. [Results](miles-file-callbacks/RESULTS.md).

UI pool alignment is a newly confirmed x64 source/layout defect for ordinary object sizes. Native UIButton, UIPage and UIText require eight-byte alignment; the current four-byte stride can misalign second allocations. Independent critic arithmetic corroborates the layout inference. Old misaligned objects were not executed. A minimal candidate preserving Win32 behavior is being tested. This is separate from theoretical huge cache-key aliasing and generic 16-byte allocation contracts.
