# Live bridge v2 — independent source/evidence follow-up

2026-09-30. Explicitly nonblind follow-up to the earlier boundary review, but no other review of this new packet was read before this memo. Reviewed authored source and `live-bridge-candidate/evidence-v2` / `evidence-mutation-v1` raw text evidence. No binary, game, allocator or vendor workload was executed; no private vendor asset contents were read. No product adoption, native Windows device fidelity or full-client result is inferred. Only this report was written.

**Conclusion:** The raw evidence supports the stated narrow no-playback result and discrimination of a swapped volume mapping. Four concrete issues need correction before this fixture is reused as coordinator/transport evidence: the claimed payload budget undercounts a copy; an early shutdown request upgrades later ordinary work to cleanup admission; callback-channel faults can be ignored; and one launch failure can orphan a suspended child. None is evidence that the recorded vendor duration/volume/rate values were fabricated or that the completed v2 run suffered a memory overwrite.

Paths below are relative to `/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam`. `B` means `live-bridge-candidate/bridge.cpp`, `C` its `common.h`, `E` means `pipe-transport-candidate/endpoint.cpp`.

## Findings

### 1. Medium — the 32 KiB aggregate payload claim is not enforced by the three-copy formula

**Observed source:** B:48 admits `3*9020+5 <= 32768`. At B:57–58, the upload and the independently published `sealed` vector remain alive while `host-candidate/retained_buffers.cpp:30–36` builds `candidate.bytes`, then copies `candidate` into `make_pair(token,candidate)` for map insertion. That creates at least four simultaneous full logical payload copies: upload, sealed vector, stage candidate and distinct insertion/entry payload. Their logical bytes alone are `4*9020 = 36080`, before vector capacities or allocation overhead. This is a caller accounting/claim defect, not an out-of-bounds write in RetainedBuffers. The arithmetic rejection itself is safe for this fixed size.

**Measured versus inferred:** The positive logs show successful finite allocation/bind/shutdown. They do not measure peak allocations or enforce the asserted aggregate limit. The extra simultaneously live copy is source-derived. The parent has now explicitly retracted the 32 KiB aggregate-budget claim while retaining the finite runtime result; that is appropriate.

**Smallest sound repair:** Keep the staged candidate copy, insert an **empty** map entry first, then swap candidate bytes into the inserted entry, and only afterward publish output token/accounting. Map-node allocation may fail before insertion; candidate destruction then leaves existing entries and output unchanged. After successful insertion, set trivial metadata and use same-default-allocator vector swap, so there is no potentially throwing byte copy after inserting an externally visible entry. This avoids relying on VS2013 implicit move behavior. Check successful insertion before publication. Consuming an otherwise unused unique token on allocation failure is consistent with the existing never-reuse policy.

At this exact call site, that removes the fourth full payload copy. It does **not** establish a 32 KiB RSS bound: vector capacity, map nodes, allocator overhead and endpoint/frame storage are different quantities. State whether the budget limits live logical payload bytes, capacity-backed payload storage, or total allocation, and account accordingly. Merely raising the cap would not validate the previous three-copy prediction.

**Disconfirming check:** A bounded source/build review and ordinary allocation/capacity accounting for this known input must show no fourth payload allocation while retaining the existing strong publication behavior. No allocator-fault reproduction is needed or proposed.

### 2. Medium — a rejected shutdown changes admission state, then every later request is treated as cleanup

**Observed source:** B:90 calls `coordinator.beginDrain` solely from the opcode, before `Backend::execute` checks fields or lifecycle prerequisites. B:91 chooses `admitCleanup` for **every** operation whenever the coordinator is Draining. This defeats the distinction documented at `coordinator-candidate/coordinator.h:34–36` between trusted cleanup admission and ordinary game work.

**Concrete schedule without unsafe vendor input:** after Hello, send a structurally valid, zero-field `AIL_shutdown` before startup. The coordinator becomes Draining. B:45 returns status 4 because `started` is false, so no vendor shutdown occurs. Next send `AIL_startup`: it is admitted as cleanup, and B:43 would call genuine startup. Similarly, shutdown with a live sample returns status 4 while leaving Draining, after which ordinary setters can still enter through cleanup admission. This is a definite source-level state-machine error; the recorded 21-request sequence does not exercise it.

**Repair:** Validate lifecycle/field prerequisites before publishing a drain transition, and let the central owner select cleanup only for explicitly allowed release/close operations. Either reject early shutdown without changing Active, or define it as entering terminal draining and reject new startup/ordinary work. Do not leave the current combination of rejected shutdown and unrestricted cleanup admission. Preserve actual vendor results separately from admission completion.

**Disconfirming check:** A prospective negative fixture can send the valid early shutdown before startup and inspect the state/admission outcome; the rejected operation need not enter Miles at all. A following startup/ordinary operation must follow the explicitly selected contract, not be silently labeled cleanup. No malformed media, playback, callback or allocator fault is required.

### 3. Medium — callback-channel failure does not necessarily fail this two-channel session

**Observed source:** C:24 pumps both endpoints, but C:25 checks only the primary endpoint's state. B:85 and B:107 reject a completed callback frame using `takeFrame`; `Endpoint::takeFrame` returns false when Faulted (E:42–45). Thus a broken callback pipe or invalid callback frame length is not itself rejected. Final `drain()` cancels/collects I/O and changes the endpoint to Closed even if it had faulted (E:102–116); its true return is not a “no prior fault” result. The fixture never checks the callback endpoint's failure reason.

**Consequence/scope:** After handshake, the callback pipe can fail while command traffic continues, and the path can still reach its PASS marker. No callbacks are enabled, so this does not disprove the scalar vendor result. It does mean that keeping the second channel pumped and obtaining a successful drain is insufficient evidence of a healthy two-channel session.

**Repair:** Observe terminal state/reason for both channels during normal operation and explicitly classify expected peer closure during ordered teardown. Do not blanket-reject every peer closure after successful SessionClose—the peer may legitimately close first. Preserve evidence of an unexpected fault rather than allowing drain to erase its significance.

**Disconfirming check:** In a bounded transport-only control, interrupt or fault the callback channel before SessionClose while command traffic remains usable; the session must report the fault instead of a clean pass. Test ordinary ordered-close races separately. This needs no vendor execution and was not performed here.

### 4. Medium — failed job assignment can leave the newly created child suspended

**Observed source:** B:114 creates the child with `CREATE_SUSPENDED`, then requires successful `AssignProcessToJobObject` and `ResumeThread`. The catch block that terminates the child begins only inside the later try at B:115–126. If creation succeeds and assignment fails, the exception bypasses that cleanup. The unassigned child is outside the kill-on-job-close job; closing controller process handles does not implement the explicit child termination path.

**Consequence/scope:** An error can leave a suspended child behind. The successful logs prove none of these launch failures occurred during the recorded runs. This is not an observed vendor crash or allocator failure.

**Repair:** Establish process/thread/job RAII or enter the cleanup guard immediately after successful child creation, before assignment/resume. Cleanup must terminate/wait for the child if assignment fails and close all owned handles exactly once. Do not rely on job termination before assignment has succeeded.

**Disconfirming check:** A bounded launch-only failure control for unsuccessful assignment must leave no live suspended child and report failure. It can use a benign process without Miles or engine bootstrap. No such test was run in this review.

## Field validation, identity and status limits

Codec validation precedes backend payload access (B:85), enforcing complete frames, structural handles and canonical spans. Backend B:35–41 rejects callback IDs, reserved fields, unused scalar slots, disallowed handles/spans and unsupported output-mask bits. Empty spans' offsets are already checked by the codec. The named-image path restricts size, block and suffix, requires a sealed upload and checks the known image hash before vendor binding (B:55–61). I found no reachable raw frame-bound violation on the normal decoded request path. This is not a general validation guarantee for arbitrary SDK arguments: scalar volume/rate values are not constrained to just the two positive values used by the controller, and the host command-line nonce length/hex syntax is assumed from its generating controller.

The controller verifies the **child PID on both pipes** at B:116. The host checks the **server PID only on its command pipe**, and only when `GetNamedPipeServerProcessId` succeeds (B:83); failure prints LIMIT and proceeds. It does not query the callback pipe's server PID. The full 128-bit Hello comparison is separate from the coordinator's shortened incarnation, but it does not turn an unavailable PID query into a successful process-identity check. PLAN states this fallback; RESULTS' opening authentication sentence should name the controller as the party checking child PIDs, then retain the exact conditional host-side caveat. No LIMIT line appears in the reviewed positive host logs; that is consistent with successful command-server querying in these runs, not proof that the fallback path is authenticated. Do not call this unconditional mutual peer authentication.

For this restricted fixture, statuses 0/1/2/3/4/5 are explicitly separated from vendor return bits. Startup, nullable handle creation and bind results are genuine results; the controller checks their prerequisites. The stale released token returns status 2 before dispatch. Status 5 is an oracle mismatch, not a Miles result. Exceptions terminate the experiment rather than synthesize a vendor failure. These are fixture conventions, not a finalized production protocol; the drain-admission defect above remains despite the separate status fields.

## Oracle independence and retained lifetime

The control sample is a separate real HSAMPLE and its getters are called directly (B:59–70), whereas target scalar getters/setters call the existing dispatcher. This is meaningful dispatch-mapping discrimination, not an independent process/engine oracle: both samples share the DLL, driver, retained bytes, decoded values and host environment. The controller also checks literal expected volume/rate values, which supplies an additional check for the selected commands. It does not prove general format, timing or game-state equivalence.

The mutation raw host logs show direct volume `3e800000,3f400000` versus dispatched `3f400000,3e800000`, transport status 5 at request 12, and normal sample release/shutdown through request 21. Controller logs explicitly discriminate that mismatch and exit 1. This supports the negative-control claim. `evidence-mutation-v1/PROVENANCE.json` correctly explains that the original runtime JSON's source field named the unchanged candidate; the mutant build source manifest and binary hashes are the relevant identities.

On both normal and caught-exception vendor paths, I found no early destruction of the retained image: sample/control release precede shutdown; the Backend destructor performs emergency release/shutdown while its retained member still exists (B:27–32). Normal shutdown executes AIL_shutdown before deactivation and eventual member destruction (B:53), with no extra early close-driver. BufferRelease destroys the separate upload, not the vendor-bound retained copy. The success logs explicitly record sample release, shutdown and host exit; they do not repair or exercise the failing real-engine fixture's DataTable/cache/ExitChain lifetime.

## Evidence identity and scope

The reviewed current source hashes matched `evidence-v2/source-manifest.json` for all inspected endpoints, coordinator, codec, registry, dispatcher and stores. Principal identities:

| Source | SHA-256 |
|---|---|
| `live-bridge-candidate/bridge.cpp` | `7f3ae2eeee393d4e6b58a2c58e686b7bb342f17bc093ad66c6442548e06c162c` |
| `live-bridge-candidate/common.h` | `211c99ce1efe32dc59c9a1b36085804d955b7b63a39f790c0444ec93f2ff82ed` |
| `pipe-transport-candidate/endpoint.cpp` | `c8ceb314bc9de684e14887c4687b2d48c50ccd5377294e4ce453d313778209b8` |
| `coordinator-candidate/coordinator.cpp` | `d434149188ee15bfc51c9a3286c9c5a49ef5d4762e8a7bb95d485cc852ec16b6` |
| `host-candidate/host_dispatch.cpp` | `4810fd0dcad43c769e077f3c2ad8d3ad9ebffec426920ff6f5e0063bd4103595` |
| `host-candidate/retained_buffers.cpp` | `9f8fc1f78238b0347e25606fdc1be658414b73aefb021c3ef91577bcd45d7401` |
| `transport-candidate/codec.cpp` | `15ab7134eb837fa7c36323d28423ecfa33e8fec69e8a03e4411bef924aade33e` |
| `transport-candidate/resource_registry.h` | `f2a4131c73d831a0e407bd67eb1803ec1f8a72ccd0cf36e6af979cae3e8a3768` |

`evidence-v2/native-build-results.json` and actual build commands record four v120 x86/amd64 Debug/Release compilations with `/W4 /WX`, exit zero. Debug and Release raw controller/host logs record 21 requests, initial duration 204 ms, changed duration 407 ms, volume 0.25/0.75, rate 11025, stale-token rejection and normal shutdown. Runtime was Wine in the stated private environment; compiler provenance does not convert it to native Windows runtime evidence. The raw input hashes identify the private DLL/image; their contents were not inspected here.

Preserve v2 as this bounded positive observation plus its corrected limits. Fixes and new bounded controls need a new version/manifest; do not retroactively relabel v2 as having passed the missing error-path or memory-budget checks. Playback, callbacks, stream IO, Bink, engine teardown and universal fidelity remain unproved and outside this run.
