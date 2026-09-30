# Maintainer review: startup23 plus drain23

Reviewed 2026-09-30. Implementation read before receipts/results. No prior agent review files were read. This review used source inspection, local SHA-256 comparisons, and archived raw logs; it did not execute a native binary, Wine, Miles, or a vendor test. Only this review file was written.

**Decision:** the evidence supports two separate bounded results. The drain candidate is suitable for the next isolated replacement experiment in the startup fixture. It is not yet a tested combined bridge. I found no Endpoint implementation defect that blocks that bounded experiment. The bridge is **TEMPORARY**, replaceable behind a backend boundary; neither these fixtures nor their wire types establish the product-facing backend contract.

## Must fix / acceptance gates

### P2 — Drain runner process status does not report failed acceptance

`pipe-drain23/run-native.py:18-34` and `run-supplement.py:18-34` record failed compilation, mismatched case exits, and caught case timeouts, then reach the end normally. A compiler returning nonzero takes the `break` at line 19; an unexpected test result merely prints at line 27; a timeout records data and breaks at line 29. All three paths can therefore return Python exit 0. A parent using only the runner exit code can report a failed or incomplete matrix as successful.

Fix before these scripts become an automated acceptance gate: after persisting evidence, require both successful builds, the complete exact variant/case matrix, no timeouts, and every expected exit match, and exit nonzero otherwise. Preserve the old variant's deliberately expected failures. This is a static control-flow finding, not an observed failure of the archived run. It does **not** overturn the current result: I inspected the individual exit records and raw logs, including the outer `PASS <case>` or failing oracle.

### Required gate — Do not transfer the two separate passes to the new composition

`startup-bridge23/bridge.cpp:1-2,87,261` imports the old common/Endpoint stack; `startup-bridge23/build.py:32` names the old Endpoint translation unit. Local hashes confirm that all three startup dependencies equal `pipe-drain23/old/` byte for byte. The drain changes are confined to the candidate copies. The startup runtime therefore did not exercise cancellation evidence retention.

For the next experiment, substitute **all three** candidate files (`endpoint.h`, `endpoint.cpp`, `common.h`) in a new isolated source snapshot. Endpoint alone preserves evidence but the old helper never checks unread bytes/incomplete output; new common.h alone requires the new accessor. Keep the completed packets immutable. Build and attribute a fresh x86-host/x64-controller Release pair, then observe the same 23-request no-sample run and both drain outcomes before claiming the combined slice passes. The existing native amd64 Debug component result cannot establish x86/Release/Wine behavior of this patch. This is an evidence gate, not a demand for broad callback or playback work before the small experiment.

## Nonblocking findings and limits

- **Temporary boundary still leaks transport concepts.** `startup-bridge23/backend.h:40-42` accepts `MilesWire::Header`, `MilesWire::Call`, and a raw encoded frame. `reply.h:43-50` exposes `MilesWire::Result` as the owned reply. `bridge.cpp:190-215` makes the caller manipulate Endpoint and wire encoding directly. Owned text is an improvement, but this is a transport-facing experimental adapter, not a backend-neutral product interface. Keep those details private to the temporary bridge when introducing a replaceable backend; do not let product Audio consumers acquire wire opcodes, lane/correlation fields, pipe state, or transport-status dependencies. No architecture was authored in this review.
- **Three-second drain is not a total destruction bound.** `candidate/pipe-transport-candidate/endpoint.cpp:25,107-121` retains pending ownership on timeout, then the destructor waits indefinitely for cancellation completion. That is an intentional storage-safety contract, not bounded recovery. The timeout fixture eventually releases its withheld cancellation (`drain-fixture.cpp:134-141`), so it does not prove shutdown under permanently noncompleting OS I/O. Nonblocking for the existing supervised fixture; do not export the helper's timeout as a product shutdown guarantee.
- **Two drains attempted is narrower than exception-safe cleanup of both.** `candidate/live-bridge-candidate/common.h:39-42` first pumps each endpoint, then drains sequentially. Allocation failure in an initial pump can still bypass both explicit drains; destructors retain lifetime safety. The supplemental timeout case validates boolean timeout behavior, not throwing/allocation-failure behavior. The result documentation excludes allocation faults, which is appropriate.
- **Test policy remains visible.** `backend.h:118-122` permits only the fixture's exact driver shape. `fixture.h` contains request-number-specific side effects and restoration. This is acceptable for the explicit no-sample experiment, but it is not evidence that arbitrary startup configurations or uninstrumented production sequencing work.

## What the evidence actually establishes

| Component | Observed in archived evidence | Not observed |
|---|---|---|
| Startup23 | One Release x64 controller / x86 original-DLL run under private Wine; 23 ordered replies; startup return 1; owned version/directory/error text; positive preference set/readback/restoration; real driver and speaker spec 2; five intended refusals; shutdown before registry retirement and retained directory storage through close | New drain implementation; native-Windows device behavior; negative vendor preference returns; arbitrary configurations; sample/playback fidelity; callbacks, reentry, retirement frontier, product integration |
| Drain23 | 16 native Windows amd64 Debug synthetic cases; candidate all pass; old has nine intended discriminator failures and seven regression passes; successful late read retains 13 bytes; real peer error retains 109; complete late write clears sendBusy; incomplete output remains; second channel drains when first times out | Cross-bitness or Release behavior; vendor callbacks; remote/process lifecycle integration; peer acknowledgement of transmitted frames; unseen kernel-queued or future bytes; natural slow Windows cancellation |

The cancellation wrappers do use real overlapped named-pipe completion results. In `drain-fixture.cpp:49-66`, boundary actions deliberately establish a native read/write/error completion before Endpoint collects it. In the timeout branch, the wrapper deliberately withholds CancelIoEx and returns test-adapter ERROR_NOT_FOUND; actual GetOverlappedResult confirms operations remain pending. This supports deterministic branch coverage, not a measured incidence of races or naturally slow cancellation.

The implementation change matches that evidence: successful read bytes are counted before the Open-state guard (`endpoint.cpp:48-62`); successful writes update progress after stopping (`64-67`); terminal errors preserve the first failure and only local-stop aborts are exempt (`31-36,69-81`); session health checks happen after both drain attempts and inspect unread/sendBusy (`common.h:37-46`). Read bytes are reset only when the consumer takes the frame (`endpoint.cpp:43-46`). These are coherent changes for the named contract.

## Receipt checks performed

- Recomputed startup native-v2 receipt SHA-256: `94d2e537b1b85e49a505cb6d9bddc04c001ecaedce75ad62f9d472b0de8755e5`. Receipt reports stable inputs and successful x86/amd64 builds with distinct PE machine IDs and output hashes matching the runtime record.
- Rehashed all 31 startup source-manifest members against their local source locations, resolving `revision4-tools/*` to the existing `live-bridge-candidate/revision4-tools/`: all matched.
- Read both startup raw logs and runtime result/postcheck JSON. The reported 23 replies, rejection statuses, loaded DLL path, ordered shutdown, and clean exit agree. The logs preserve ALSA warnings. Full raw frames are not archived, so hashes cannot independently reconstruct or re-decode them; the running client performed that decode.
- Verified all 32 locally collected first-run drain output-manifest entries and all 12 supplement-specific entries available in the supplement directory: hashes matched. The supplement manifest also lists the 32 earlier outputs; those were checked in the first evidence directory, not represented as absent supplemental artifacts.
- Read all 32 old/candidate case logs across the two drain batches and their result records. Expected helper `FAIL` text inside a successfully rejecting candidate case is followed by the explicit successful case oracle; it is not a hidden case failure.

The next justified step is the small, newly attributed combined startup fixture. Successful completion would establish that combined no-callback slice only. Product behavior remains unchanged and full bridge/fidelity work remains open.
