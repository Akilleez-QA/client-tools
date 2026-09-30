# Miles replacement boundary — current checkpoint

The native-shaped API is implemented and compiler-checked as a prototype. The temporary pipe backend remains incomplete. Product stays at `49d0eeed4`; there is no new linked x64 game or fidelity acceptance.

## Replacement design

Game audio policy calls one [ClientMiles header](plain-native70/candidate/ClientMiles.h). The native implementation directly calls the selected SDK. The temporary implementation uses the same signatures and keeps its x86 process, pipe, IDs and ownership machinery private. One implementation is selected for the process. Replacing it must not require pipe-specific changes throughout Audio; there is no hot-swap or general plugin framework.

The possessed Miles 7.2a header contains Win64 declarations, but a matching x64 library is unavailable. Native source retains real unresolved SDK imports. The three opaque handles use the SDK's actual incomplete tags, letting native callback registration pass and return exact callback types without an artificial mapping table. The pipe owns separate proxy objects and treats exposed handles only as lookup tokens. A future SDK upgrade needs fresh compilation and runtime qualification.

## Observed checks

| Artifact | Observation | Limit |
|---|---|---|
| [Native API70](native70/NATIVE-RESULTS-v1.md) | All 62 API functions implemented; 12 new v120 AMD64 objects compile without diagnostics, including both SDK include orders and an engine-header probe | 61 genuine SDK imports remain unresolved; no native library, link or execution |
| [Combined pipe86](native86/NATIVE-RESULTS-v1.md) | All28 affected objects (14x86/14AMD64) compile without diagnostics;53 of62 public definitions | Seven unchanged units retain only their earlier77 object evidence; no new link/runtime; engine worker remains external |
| [Registry85](portable-registry85/RESULTS-v1.md) | Six groups185 assertions pass with ASan/UBSan on actual registry | No vendor effects or callback quiescence |
| [Text87](portable-text87/RESULTS-v1.md) | Five groups308 assertions pass with ASan/UBSan on actual81 Core/Session | Scripted Channel and explicit unavailable Runtime substitute; no LiveChannel/SDK execution |
| [Diagnostic decoder77](portable-diagnostics77/RESULTS-v1.md) | Five scenario groups and 1,241 assertions pass with ASan/UBSan on the actual decoder and codec | Does not execute public/Core delegates, SDK calls or callback scheduling |
| [Earlier reply66](portable-reply66/RESULTS-v1.md) | Five scenario groups and 495 assertions pass with ASan/UBSan | Actual64 core with scripted Channel and unavailable Runtime substitute; no engine/vendor execution |

The earlier combined74 host was also linked once against the possessed x86 Miles import library: linker exit zero and an x86 PE were recorded. Its overall gate failed because the import parser missed underscore-prefixed Win32 names. The failed receipt is preserved under [host-link78](host-link78/RESULTS.md). A separate corrected parser passed its positive/seven negative fixtures and matched all 50 decorated Miles imports in the same saved listing. No helper was executed, and this older host link does not transfer to86.

## Changes and review

77 integrates the private proxy types, native-width driver argument forwarding and the existing reservation-capable registry. An older composed snapshot selected an incompatible registry; that mistake is recorded, and the combined source now compiles. The host also selects its actual file-channel/guard dependencies. Driver forwarding preserves Audio's own null-driven stereo fallback in source; runtime behavior still needs checking.

86 adds the guarded file-table delegate, separate per-function owned text snapshots, and host stream open/borrow/close handling. Stream reservations precede native ownership, Driver retirement invalidates stream descendants and aliases, and closing blocks lookup before SDK entry. These are implemented source paths with object/registry evidence, not observed Audio streaming. File registration remains one-time/non-null; normal paired shutdown and EOS remain missing.

Astra audited source and native records; these are reviews of the same experiments, not independent runtime reproduction. Composer83's suspected lost-handle path was checked: unknown open retains its member-owned pointer/reservation and forbids continued commands. This is intentional failure containment, not complete recovery. One stale inherited source comment is preserved in frozen86 and scheduled for correction. Backend/SDK runtime coverage remains open. [Stream review](../../parallel-review-next/CLI-RECONCILIATION83.md). Grok's last attempt timed out without output, which supplies no clearance.

The24-case native Windows resource probe84 observed buffer writes for owned ASCII resources at ACP1252. It explains why version22's nonempty requirement is incorrect, but does not yet implement a native-equivalent version operation or establish all locales/capacities. [API observations](version84/resource-probe-v1/RESULTS-v1.md).

## Next work

Nine public definitions remain: version, four image functions, lock/unlock and two EOS registrations. Complete content binding, typed EOS delivery, actual Audio TLS integration and normal paired shutdown. Source-level stream lifetime work does not by itself support Audio, which registers EOS before starting a stream. The [file callback assessment](file-callback79/ASSESSMENT.md) maps the existing admitted callbacks and worker integration; wrapping an untouched Audio callback would repeat its TLS installation on an already initialized worker.

Native declarations do not establish callback quiescence. sample-live31 did not test EOS; earlier separate generation/EOS diagnostic probes are catalogued with their narrower limits in [EOS88](eos88/ASSESSMENT.md). Permanent proxy tombstones are not being added solely to strengthen invalid post-close use. Future asynchronous events must respect wire generation and registration lifetime. The rejected real-engine teardown/allocator-fault workload remains held.

After those integration steps, test the actual paired runtime in the approved isolated environment. Full game startup, Bink interaction and representative media/gameplay fidelity remain acceptance requirements. No feature is stubbed or removed to get a green result.

Delivery: authored prototype, observed object builds and a separately recorded host link. Outcome: bounded checks passed; complete backend/client outcome unobserved. Root controls the next tests. All work stays on our fork; no new PR or upstream mutation.
