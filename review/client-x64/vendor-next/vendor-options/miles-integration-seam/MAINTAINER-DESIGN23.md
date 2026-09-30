# Maintainer design review 23

2026-09-30. Independent source-based maintainer opening. Product HEAD read directly: `49d0eeed4ddaa177d7a93ea396c37c3d9b9942da`. Candidate root: `/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam`. No product adoption, execution of vendor/engine code, allocator-fault workload, commit or push performed.

**Judgment: a defensible boundary, an unfinished runtime, and too many overlapping candidate owners to adopt wholesale.** The separate x86 process is not inherently an obtuse design when the required original library exists only in x86. It preserves a vendor implementation the team does not own. It also converts local calling, threading and pointer-lifetime assumptions into a protocol the team must own indefinitely. The current source has not yet discharged that cost. I would approve another narrowly integrated experimental slice; I would not approve production adoption or claim full fidelity.

Qualitative ratings, restricted to static evidence: boundary rationale **credible**; individual byte/handle mechanisms **reasonably bounded**; integrated lifecycle/progress ownership **incomplete**; production maintainability and behavioral fidelity **unqualified**. Test counts cannot increase the last rating. The maintainer's reported objection is a useful cost hypothesis, not an implementation finding by itself.

## Frame and evidence limits

POODO applied from `/home/akilleez/.agents/skills/poodo/SKILL.md`. A redundant user exchange was waived because the assignment fixes outcome, authority and exclusion precisely. “Full fidelity” means preserving actual reachable audio/video behavior, callbacks, timing, real TreeFile semantics and the original shared Miles/Bink driver relationship. “Small reviewable commits” means one understandable ownership or integration change, not many disconnected components. “Simpler” means fewer independently maintained rules, not fewer source lines or removal of behavior.

This review is the parent's explicitly requested blind maintainer spike. I read architecture and owned source before forming findings; I did not read peer review reports. No descendant capacity was allocated. At each POODO transition I considered additional fan-out; the parent already owns independent roles, and another descendant would duplicate this bounded source review. Independence is limited by the shared architecture, code, parent-provided task facts and model family; agreement would not be runtime corroboration.

Direct observations below are source observations. Architecture claims about previous native successes and the failing engine teardown remain reported evidence here: I did not rerun or independently validate those experiments. This report does not diagnose the old teardown failure.

## Actual maintenance surface

The latest candidate components are not one production implementation. The build recipe `live-bridge-candidate/build-native-v3.py:4-9` compiles codec, pipe endpoint, coordinator, bridge and, for x86, scalar dispatch, retained buffers and upload. It does **not** compile SessionLifecycle, startup metadata v4, SessionVersion22, sound-info handling or the client reverse-file patch into that live slice.

A bounded physical-line inventory of the directly inspected reusable selection is 26 source/header files, 1,947 lines: wire/registry/sound-info 645; host dispatch/resolver/lifecycle/retention/upload 672; coordinator/endpoint 391; metadata v4/version22 239. The live probe's bridge/common/admission add 279 lines in three files. The direct file seam adds a header and Audio patch. These counts exclude tests, build orchestration, archives and old revisions. They are not a size estimate for a finished bridge: several files are densely compressed, and the hard missing scheduling/driver/video responsibilities are not represented.

Excluded from the proposed runtime count: `history/`, `history-v1/`, `transport-baseline-412-v3`, `mutation-source*`, retained mutation directories, tar archives, native staging/snapshot trees, old metadata revisions and SessionVersion21. They are evidence/reproduction assets, not evidence that production would maintain thousands of engine source copies. Retaining frozen evidence is sensible. A build allowlist and a short current-source index are enough to distinguish it; rewriting or deleting the archives is unnecessary.

| Runtime responsibility | Actual owner/candidate | Important boundary |
|---|---|---|
| Fixed-width frame, span and null-handle shape | `miles_wire.h`, `codec.cpp` | Codec does not prove session identity, call semantics or vendor liveness. |
| OS read/write completion and storage lifetime | `Endpoint` | Per-channel state; does not prove session or callback completion. |
| Process/pipe launch, identity, waiting and cancellation | live `common.h`/controller | Currently test infrastructure with throwing `require`, watchdogs and process termination, not product failure policy. |
| Request admission, lock leases, callback pins/frontiers | `Coordinator` plus live `admission.h` | Deterministic model; no real callback scheduler or vendor-termination evidence. |
| Resource generation and stream aliases | `ResourceRegistry`/`RegistryResolver` | Caller supplies quiescence and session binding. Driver-child ownership is not generally encoded here. |
| Original scalar calls | `host_dispatch.cpp` | SDK-bound typed arms; requires initialized/admitted session. |
| Startup, driver and sample lifetime | `SessionLifecycle` **and** live `Backend` | Overlapping alternatives, not both usable as authoritative owner. |
| Immutable sample inputs and uploads | `BufferUpload`, `RetainedBuffers` | Conservative retention; aggregate budget/retirement belongs elsewhere. |
| Startup strings/preferences/speaker metadata | `startup-metadata-v4` | Distinct input retention and status scheme; currently disconnected from live path. |
| Resource version text | `session-version22` | Exact held-module query; module lifetime/admission supplied externally. |
| Real client virtual files | `ClientAudioFileCallbacks.h` plus Audio patch | Reuses the actual callback bodies and single file map. No wire dispatch or scheduling supplied. |
| Idle EOS, close races, permitted reentry | Required architecture, partial coordinator bookkeeping | No actual integrated implementation demonstrated by this source. |
| Bink service/decode/copy with shared driver | Required architecture and original product calls | No Bink resource kind or operational commands in this candidate schema. |

The last two rows are major remaining product work, not optional polish.

## Concrete complexity findings

**1. There are two competing lifecycle policies; choose one before adopting either.** `host-candidate/session_lifecycle.cpp:88-101` releases records, explicitly closes each driver, then calls `AIL_shutdown`. `live-bridge-candidate/bridge.cpp:53` calls shutdown and retires the driver afterward. Product `Audio.cpp:1418-1437` clears its device reference and calls shutdown without that explicit close. This is a static policy difference, not proof that explicit close is invalid. The reusable lifecycle class has useful preallocation/thread checks; the live backend has the exercised slice's ordering. Copying both forward would leave reviewers deciding which one governs behavior.

`SessionLifecycle::releaseSample`/`shutdown` accept `callbacksQuiesced`; registry retirement and retained-buffer destruction also trust caller preconditions. Meanwhile `Coordinator::readiness` at lines121-129 always reports `vendorTerminationUnproven=true`. There is no transition that turns actual vendor termination evidence into a retirement capability. A bool-to-token rename alone would not fix this: one owner must receive the real completion fact, capture the callback frontier, observe acknowledgments and then retire the exact generation.

**2. The live path has not implemented the architecture's progress model.** `bridge.cpp:85` requires lane1, no lease and no causal request; callback traffic is rejected at lines85 and108. Backend vendor calls execute inline on the same host loop. `common.h:44-48` sends while pumping only one endpoint; `receive` pumps both only while waiting. This is acceptable for its declared no-callback probe. It cannot become the full backend by adding callback opcodes to the switch. A vendor call waiting for reverse I/O needs live independent transport progress and an admitted client execution lane. An idle worker callback needs dispatch even with no command waiting. The main design debt is that scheduling contract, not the number of pipe helpers.

The coordinator also has no registration-removal operation. Its default lifetime capacity is64 registrations (`coordinator.h`), checked against a map that is never erased (`coordinator.cpp:73-82`). A long-running implementation registering successive sounds would exhaust this model. Do not “fix” it with an unbounded map or early erase; reuse/retirement must follow actual registration-generation completion.

**3. Wire status values already have incompatible meanings.** Scalar dispatch defines0–3. Startup metadata defines4 as `TextTooLong` and5 as `InputBudgetExceeded` (`metadata.h:9`). The live backend uses4 for lifecycle/admission refusal and5 for direct-control comparison mismatch. `Result.transport_status` has no shared named vocabulary in `miles_wire.h`. Composition will make diagnostics ambiguous unless errors are mapped once at the boundary. Direct-control oracle mismatches should be fixture assertions, not production transport statuses. A small shared status definition is a more valuable cleanup than replacing all switches with a generic RPC framework.

**4. Opcode shape rules are copied in several places.** Scalar `supports()` repeats the dispatch opcode inventory; every arm repeats reserved scalar/output-mask checks. The live backend independently validates a subset (`bridge.cpp:35-41`) before calling scalar dispatch. Metadata has another validator, legitimately narrower for its reachable calls. These can drift as supported shapes change. Keep SDK invocations explicit and typed, but share simple shape descriptors/helpers and route each operation to exactly one semantic validator. Do not combine structural byte validation, opcode validation and resource liveness into one check: they protect different boundaries.

The 48/88/80 and136/128 wire sizes also appear in schema assertions, codec, pipe header storage and metadata limits. Named encoded-size constants would make schema evolution reviewable. This is ordinary bookkeeping reduction, not evidence of a current malformed frame.

**5. Storage policies are fragmented, but not all storage is redundant.** Upload storage, sealed publication and retained vendor input have different trust/lifetime roles. In the live binding path (`bridge.cpp:57-64`), upload is copied to a temporary sealed vector, then copied into retained storage. Eliminating a provably redundant intermediate copy by ownership transfer is possible, but published pointers must remain stable and the ownership move must be explicit. `SessionInputs` separately retains stable path strings until shutdown with a1MiB aggregate bound. Consolidating accounting under the session would improve failure diagnosis; forcing all path strings and sample bindings into one active-token abstraction would make semantics worse. Never retire previous or failed bind inputs simply because a new bind returned success.

**6. The probe mixes mechanism, oracle and policy.** The live backend owns a direct-control sample, hardcodes one9020-byte WAV/hash, restricts driver parameters, compares scalar returns, manages registry/retention and executes vendor calls in a compressed function. Those restrictions bound an experiment; they are not intended production requirements. The next integration should reuse the working channel/admission path while keeping expected-value comparison in the fixture. Extraction should happen only where the next vertical slice needs a reusable owner; a broad new framework would add another untested layer.

## Necessary complexity that should stay

Two independently drained traffic directions, separate causal and unsolicited callback identities, generation-safe aliases, real vendor result bits, actual output-pointer presence, and stable immutable bytes each protect an observed or explicit contract. Endpoint cancellation must preserve operation storage until completion; flattening its state machine into “close handle and free” is not simplification. Source already cleanly separates OS I/O state, resource liveness and semantic call completion in several places; preserve those distinctions.

The real file adapter is a good narrow seam: the patch delegates to `Audio.cpp`'s existing open/close/seek/read bodies instead of duplicating TreeFile precedence. Product `Audio.cpp:3939-4100` shows shared file-map mutation, engine thread initialization and exact signed read/seek conversions. Those are reasons to establish compatible callback execution, not to call the adapter on an arbitrary reactor thread. The Bink driver and frame-service requirements likewise cannot be removed to make an audio-only demonstration appear complete.

## Research and divergence before selection

Queries, retrieved2026-09-30: Microsoft overlapped-pipe operation/cancellation completion; Chromium synchronous IPC reentry/deadlock; Chromium plugin process boundary. Relevant full source content was inspected, not only snippets.

* [Microsoft overlapped pipe I/O](https://learn.microsoft.com/en-us/windows/win32/ipc/synchronous-and-overlapped-input-and-output), updated2021-01-07: separate operations/events permit concurrent I/O. Supports endpoint mechanism, not application deadlock freedom.
* [Microsoft CancelIoEx](https://learn.microsoft.com/en-us/windows/win32/api/ioapiset/nf-ioapiset-cancelioex), updated2021-10-13: cancellation is a request; operation storage remains live until completion and completion can still be normal or another failure. This challenges simplifying shutdown to cancellation success.
* [Chromium IPC design](https://www.chromium.org/developers/design-documents/inter-process-communication/), historical legacy design, current retrieval: distinguishes an I/O thread from the blocked caller and documents synchronous-message deadlocks and ordering effects. This independent engineering evidence supports treating execution affinity separately from channel availability; its browser-specific thread policy is not a Miles prescription.
* [Chromium plugin architecture](https://www.chromium.org/developers/design-documents/plugin-architecture/), historical design, current retrieval: shows out-of-process vendor/plugin adaptation as a real architecture and acknowledges duplicated abstraction layers. It challenges both “separate process is inherently foolish” and “another wrapper is free.” It proves no SWG fidelity claim.

Two evidence families: platform contract and independent project engineering experience. No exact original-Miles callback contract was found or inferred from them. Research gate satisfied for this static maintainability decision; behavioral questions remain open.

Exactly20 materially distinct paths considered before convergence:

1. Acquire a licensed same-version x64 binary: removes the process seam if actually available.
2. Obtain licensed source and port vendor implementation: transfers vendor maintenance burden.
3. Upgrade licensed Miles: reduces ABI mismatch but requires behavioral requalification.
4. Replace with another engine: changes decoder/mixer behavior and acceptance burden.
5. Keep x86 product: useful reference, fails requested x64 objective.
6. Host all clientAudio in x86: reduces vendor-call IPC while expanding game-state/RNG/Object protocol.
7. Introduce a higher-level voice service: fewer messages by moving policy and timing ownership.
8. Use in-process x86 emulation: trades process IPC for a broad execution/ABI compatibility layer.
9. Preserve narrow vendor seam with two pipes: current reversible experiment.
10. Replace pipes with RPC/COM: changes serialization/runtime ownership, not callback semantics.
11. Adopt shared memory with leases: possible copy/latency improvement at a larger lifetime cost.
12. Replicate client files in host: removes reverse callbacks but risks virtual-file divergence.
13. Execute reverse operations through actual TreeFile seam: preserves file semantics; needs engine oracle.
14. Integrate startup metadata/version into existing live path: tests composition with safe bounded surface.
15. Consolidate lifecycle ownership: removes overlapping release policy; needs original-order evidence.
16. Introduce one wire-error/shape vocabulary: removes drift without changing scheduling.
17. Isolate fixture oracles from backend mechanisms: makes intended runtime smaller and reviewable.
18. Repair baseline using existing source/crash evidence: restores prerequisite without repeating prohibited workload.
19. Seek vendor maintainer documentation for callback retirement: may resolve an otherwise unprovable completion assumption.
20. Hold bridge adoption while advancing independent x64 work: preserves product boundary if scheduling remains blocked.

The topology traversed is boundary placement → ownership → execution/progress → bytes/identity → files/driver/video → evidence/authority. Static source covers the first five sufficiently to rank a next authored change. Original-engine affinity, termination guarantees, actual latency and whole-product acceptance remain unresolved; this is bounded saturation for the next decision, not an exhaustive design proof. Strongest architectural rival remains whole-clientAudio hosting; its discriminator is the actual amount and cadence of game state crossing that rival boundary versus measured call/callback overhead here. No static line count decides that contest.

## Smallest next vertical integration

**Select path14, with only the error mapping/routing cleanup required from16: compose startup metadata v4 and SessionVersion22 into the existing real two-process no-playback path.** Reuse its existing startup/driver owner. Do not introduce SessionLifecycle as a second startup authority. Version requests must use the held verified original module, and redist strings must remain owned through actual shutdown. Replies must carry owned text through the existing codec/channel and match the exact pending context. Keep direct-control expectations outside the backend. This is one bounded experimental integration commit or reviewable patch, not a new parallel host harness.

The smallest first sub-slice is SessionVersion end-to-end; the coherent milestone adds the already implemented metadata operations needed by the existing startup path. Stop at this composition boundary; do not append playback/callback machinery to the same review. Product HEAD49d0 stays unadopted.

Prospective gate `startup-composition23-v1`, **not executed here**:

* Bind the exact candidate source manifest, existing native compiler/configurations, original DLL and module handle identity before any separately authorized run.
* Same live x64-client/x86-host session carries version, supported preferences/redist/error text and real-driver speaker output; comparisons use direct original API/resource answers for deterministic fields in matching state. Error-text behavior needs a controlled oracle, not blind equality after different call histories.
* Capture request/reply IDs, accepted admission ordinal and terminal statuses. Request fields rejected before vendor dispatch stay distinguishable from genuine null/negative vendor results. No ambiguous4/5 status reuse.
* Demonstrate owned version/text survives source/reply storage release; existing no-playback bind/release/shutdown path still terminates normally. No second startup, no implicit driver close policy change, no playback, no real-engine fixture.
* A mismatch, ownership defect, unexplained driver/module identity or nonterminal wait fails this narrow gate and stops the experiment. Preserve outputs; do not add retries, fake results or emergency cleanup to the success path. Rollback is removal of the new candidate routing/build inclusion, not a product rollback.

This gate establishes composition of selected adapters, codec, process channel and existing session path. It does **not** establish Audio integration, callback affinity, close-frontier correctness, Bink or full fidelity. Safe native no-playback execution requires the parent's/user's separate authority; this review grants none.

**Why not reverse TreeFile immediately?** It would yield greater architectural information: an actual pending vendor operation causing open/read/seek/close through the real client file map tests the seam that can deadlock. But the current prohibition prevents its real Audio/engine acceptance run. Pure transport tests or a mock filesystem would only qualify another component. Source/compile preparation is possible, but is not presently the better completed vertical milestone. After a clean baseline and explicit authority are available, make the existing Audio/Sound2d path with real TreeFile and original lock scopes the next load-bearing gate; then unsolicited EOS/combined progress and shutdown/Bink must follow. This is a sequencing decision, not permission to omit those requirements or rerun the rejected fixture.

## Handoff contract

- `delivery_state`: static review authored; source inspected; no build/runtime execution.
- `outcome_state`: production behavior unobserved by this reviewer.
- `highest_justified_claim`: concrete duplicate ownership/rule sites and missing integration responsibilities identified; one bounded next composition step selected.
- `required_runtime_observation`: separately authorized startup-composition23-v1 for the next narrow slice; actual engine/TreeFile/callback/driver/Bink acceptance remains required for the product.
- `who_controls_next_test`: parent/user within existing authorization; real-engine and allocator-fault workloads remain prohibited.

Continuity capsule: phase=handoff; source-root as above; product=49d0eeed4ddaa177d7a93ea396c37c3d9b9942da; evidence=direct source plus dated contextual research; external historical results=reported; decision=integrate reviewed metadata into existing live path without new lifecycle owner; unresolved=vendor termination/affinity, combined progress, Bink, aggregate retention, baseline teardown; authority=review/report only; changed-file=MAINTAINER-DESIGN23.md; next-checkpoint=parent synthesis and separately authorized candidate integration. This capsule is metadata, not outcome evidence.
