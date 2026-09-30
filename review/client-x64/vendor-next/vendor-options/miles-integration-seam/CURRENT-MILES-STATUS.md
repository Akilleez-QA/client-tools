# Miles replacement boundary — current checkpoint

The native-shaped API is implemented and compiler-checked as a prototype. The temporary pipe backend remains incomplete. Product stays at `49d0eeed4`; there is no new linked x64 game or fidelity acceptance.

## Replacement design

Game audio policy calls one [ClientMiles header](plain-native70/candidate/ClientMiles.h). The native implementation directly calls the selected SDK. The temporary implementation uses the same signatures and keeps its x86 process, pipe, IDs and ownership machinery private. One implementation is selected for the process. Replacing it must not require pipe-specific changes throughout Audio; there is no hot-swap or general plugin framework.

The possessed Miles 7.2a header contains Win64 declarations, but a matching x64 library is unavailable. Native source retains real unresolved SDK imports. The three opaque handles use the SDK's actual incomplete tags, letting native callback registration pass and return exact callback types without an artificial mapping table. The pipe owns separate proxy objects and treats exposed handles only as lookup tokens. A future SDK upgrade needs fresh compilation and runtime qualification.

## Observed checks

| Artifact | Observation | Limit |
|---|---|---|
| [Native API70](native70/NATIVE-RESULTS-v1.md) | All 62 API functions implemented; 12 new v120 AMD64 objects compile without diagnostics, including both SDK include orders and an engine-header probe | 61 genuine SDK imports remain unresolved; no native library, link or execution |
| [Combined pipe77](native77/NATIVE-RESULTS-v1.md) | 18 x86 host and 17 AMD64 client-side objects compile without diagnostics; 50 of 62 exports defined | No client link or execution; real engine worker remains external |
| [Diagnostic decoder77](portable-diagnostics77/RESULTS-v1.md) | Five scenario groups and 1,241 assertions pass with ASan/UBSan on the actual decoder and codec | Does not execute public/Core delegates, SDK calls or callback scheduling |
| [Earlier reply66](portable-reply66/RESULTS-v1.md) | Five scenario groups and 495 assertions pass with ASan/UBSan | Actual64 core with scripted Channel and unavailable Runtime substitute; no engine/vendor execution |

The earlier combined74 host was also linked once against the possessed x86 Miles import library: linker exit zero and an x86 PE were recorded. Its overall gate failed because the import parser missed underscore-prefixed Win32 names. The failed receipt is preserved under [host-link78](host-link78/RESULTS.md). A separate corrected parser passed its positive/seven negative fixtures and matched all 50 decorated Miles imports in the same saved listing. No helper was executed, and this older host link does not transfer to77.

## Changes and review

77 integrates the private proxy types, native-width driver argument forwarding and the existing reservation-capable registry. An older composed snapshot selected an incompatible registry; that mistake is recorded, and the combined source now compiles. The host also selects its actual file-channel/guard dependencies. Driver forwarding preserves Audio's own null-driven stereo fallback in source; runtime behavior still needs checking.

Five borrowed-sample controls and six existing stream-control dispatcher routes are now reachable through the Backend. Five diagnostic exports preserve signed or unsigned results and validate replies before settling requests. These additions do not create stream handles, install callbacks or complete teardown.

Astra audited source and native records; these are reviews of the same experiments, not independent runtime reproduction. Composer challenged the type design and test coverage. Its two77 source allegations were rejected after checking the actual call chain and five-operation contract; the missing runtime coverage remains open. Grok timed out without output. [Type review](../../parallel-review-next/CLI-RECONCILIATION70.md), [diagnostic review](../../parallel-review-next/CLI-RECONCILIATION77.md).

## Next work

Twelve public definitions remain: three text/version functions, four image functions, lock/unlock and three callback registrations. Complete stream open/borrow/close ownership, content binding, typed EOS delivery, actual Audio TLS integration and normal paired shutdown. The [file callback assessment](file-callback79/ASSESSMENT.md) maps the existing admitted callbacks and worker integration; wrapping an untouched Audio callback would repeat its TLS installation on an already initialized worker.

Native declarations do not establish callback quiescence. Permanent proxy tombstones are not being added solely to strengthen invalid post-close use. Future asynchronous events must respect wire generation and registration lifetime. The rejected real-engine teardown/allocator-fault workload remains held.

After those integration steps, test the actual paired runtime in the approved isolated environment. Full game startup, Bink interaction and representative media/gameplay fidelity remain acceptance requirements. No feature is stubbed or removed to get a green result.

Delivery: authored prototype, observed object builds and a separately recorded host link. Outcome: bounded checks passed; complete backend/client outcome unobserved. Root controls the next tests. All work stays on our fork; no new PR or upstream mutation.
