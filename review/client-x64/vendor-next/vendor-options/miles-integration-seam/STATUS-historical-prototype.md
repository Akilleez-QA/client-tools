> **Historical checkpoint.** This report preserves the earlier state and claims. For current source, PRs and qualification, use the [fork status](https://github.com/Akilleez-QA/client-tools/blob/review/client-x64-evidence/review/client-x64/FORK-STATUS.md).

# Miles replacement boundary — current checkpoint

The native-shaped API is implemented and compiler-checked as a prototype. The temporary pipe backend remains incomplete. Product stays at `49d0eeed4`; there is no new linked x64 game or fidelity acceptance.

## Replacement design

Game audio policy calls one [ClientMiles header](plain-native70/candidate/ClientMiles.h). The native implementation directly calls the selected SDK. The temporary implementation uses the same signatures and keeps its x86 process, pipe, IDs and ownership machinery private. One implementation is selected for the process. Replacing it must not require pipe-specific changes throughout Audio; there is no hot-swap or general plugin framework.

The possessed Miles 7.2a header contains Win64 declarations, but a matching x64 library is unavailable. Native source retains real unresolved SDK imports. The three opaque handles use the SDK's actual incomplete tags, letting native callback registration pass and return exact callback types without an artificial mapping table. The pipe owns separate proxy objects and treats exposed handles only as lookup tokens. A future SDK upgrade needs fresh compilation and runtime qualification.

## Observed checks

| Artifact | Observation | Limit |
|---|---|---|
| [Native API70](native70/NATIVE-RESULTS-v1.md) | All 62 API functions implemented; 12 new v120 AMD64 objects compile without diagnostics, including both SDK include orders and an engine-header probe | 61 genuine SDK imports remain unresolved; no native library, link or execution |
| [Combined pipe99](native101/NATIVE-RESULTS-v1.md) | All29 selected objects (15x86/14AMD64) compile without diagnostics;55 of62 public definitions | Seven unchanged units omitted by dependency selection; no link/runtime; engine worker remains external |
| [Version92](version92/RESULTS-v1.md) | Seven process modes,559 assertions pass with ASan/UBSan | Actual90 Core/Session with scripted Channel/Runtime; no actual host resource query |
| [Image98](image98/RESULTS-v2.md) | Five processes, six scenario groups and1,678 assertions pass with ASan/UBSan | Actual93 Core/Session/codec/registry/BufferUpload; counterpart budget and classifier are explicit test models, no Backend/SDK/ACK |
| [Registry85](portable-registry85/RESULTS-v1.md) | Six groups185 assertions pass with ASan/UBSan on actual registry | No vendor effects or callback quiescence |
| [Text87](portable-text87/RESULTS-v1.md) | Five groups308 assertions pass with ASan/UBSan on actual81 Core/Session | Scripted Channel and explicit unavailable Runtime substitute; no LiveChannel/SDK execution |
| [Diagnostic decoder77](portable-diagnostics77/RESULTS-v1.md) | Five scenario groups and 1,241 assertions pass with ASan/UBSan on the actual decoder and codec | Does not execute public/Core delegates, SDK calls or callback scheduling |
| [Earlier reply66](portable-reply66/RESULTS-v1.md) | Five scenario groups and 495 assertions pass with ASan/UBSan | Actual64 core with scripted Channel and unavailable Runtime substitute; no engine/vendor execution |

The earlier combined74 host was also linked once against the possessed x86 Miles import library: linker exit zero and an x86 PE were recorded. Its overall gate failed because the import parser missed underscore-prefixed Win32 names. The failed receipt is preserved under [host-link78](host-link78/RESULTS.md). A separate corrected parser passed its positive/seven negative fixtures and matched all 50 decorated Miles imports in the same saved listing. No helper was executed, and this older host link does not transfer to99.

## Changes and review

77 integrates the private proxy types, native-width driver argument forwarding and the existing reservation-capable registry. An older composed snapshot selected an incompatible registry; that mistake is recorded, and the combined source now compiles. The host also selects its actual file-channel/guard dependencies. Driver forwarding preserves Audio's own null-driven stereo fallback in source; runtime behavior still needs checking.

86 adds the guarded file-table delegate, separate per-function owned text snapshots, and host stream open/borrow/close handling. Stream reservations precede native ownership, Driver retirement invalidates stream descendants and aliases, and closing blocks lookup before SDK entry. These are implemented source paths with object/registry evidence, not observed Audio streaming. File registration remains one-time/non-null; normal paired shutdown and EOS remain missing.

Astra audited source and native records; these are reviews of the same experiments, not independent runtime reproduction. Composer83's suspected lost-handle path was checked: unknown open retains its member-owned pointer/reservation and forbids continued commands. This is intentional failure containment, not complete recovery. The stale inherited stream comment is preserved in frozen86 and corrected in90/99. Backend/SDK runtime coverage remains open. [Stream review](../../parallel-review-next/CLI-RECONCILIATION83.md). Composer96's proposed copy-order defect was checked against LiveChannel: owner validation precedes settlement and copying. Its current host/runtime and mutation gaps remain explicit. Grok96 timed out without output and supplies no clearance. [Version review](../../parallel-review-next/CLI-RECONCILIATION96.md).

The24-case native Windows resource probe84 observed buffer writes for owned ASCII resources at ACP1252. It motivated90's implemented capacity-aware version operation: preserve the counted byte prefix and untouched tail, including empty/interior-NUL results;99 integrates it.92 tests the client path and94/101 compile the genuine Windows resource helper, but its new host path has not run against Miles and the temporary1MiB-minus128 budget remains a documented domain restriction. The24 cases do not establish all locales/capacities. [API observations](version84/resource-probe-v1/RESULTS-v1.md).

## Next work

Seven public definitions remain: WAV_info, set_named_sample_file, set_sample_file, lock/unlock and two EOS registrations.99 adds93's file_type operation using a budgeted exact-length upload, native signed result and validated Release before caller return. It is compiled, not adopted into Audio. Complete content binding, typed EOS delivery, actual Audio TLS integration and normal paired shutdown. Source-level stream lifetime work does not by itself support Audio, which registers EOS before starting a stream. The [file callback assessment](file-callback79/ASSESSMENT.md) maps the existing admitted callbacks and worker integration; wrapping an untouched Audio callback would repeat its TLS installation on an already initialized worker.

Native declarations do not establish callback quiescence. [Bounded original-DLL inspection100](eos-binary100/OBSERVATION-root.md) distinguishes AIL_lock's counter from AIL_lock_mutex's synchronization path; it does not establish universal callback locking or producer termination. EOS97 is an unexecuted diagnostic plan/source. [Sensor103](eos103/evidence-v1/results.json) passed six synthetic classifications and fifteen changed negative log fixtures; that is parser evidence, not vendor behavior. Extra same-thread/registration checks are being added before native use.  sample-live31 did not test EOS; earlier separate generation/EOS diagnostic probes are catalogued with their narrower limits in [EOS88](eos88/ASSESSMENT.md). Permanent proxy tombstones are not being added solely to strengthen invalid post-close use. Future asynchronous events must respect wire generation and registration lifetime. The rejected real-engine teardown/allocator-fault workload remains held.

After those integration steps, test the actual paired runtime in the approved isolated environment. Full game startup, Bink interaction and representative media/gameplay fidelity remain acceptance requirements. No feature is stubbed or removed to get a green result.

Delivery: authored prototype, observed object/portable checks and a separately recorded older host link. Outcome: bounded checks passed; complete backend/client outcome unobserved. Root controls the next tests. All work stays on our fork; no new PR or upstream mutation.
