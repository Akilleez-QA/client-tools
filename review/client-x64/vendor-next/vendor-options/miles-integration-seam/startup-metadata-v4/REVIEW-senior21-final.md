# Senior21 final targeted review — frozen startup metadata v4

Reviewed 2026-09-30. **All three original findings are closed for their identified failure modes.** Final ratings: **engineering 8.7/10; experimental component readiness 8.3/10**. The component is suitable to retain as a reviewed experimental building block within its documented narrow contract. These ratings do not evaluate a complete backend or client.

No new actionable defect found in this targeted revision. The remaining omitted-call question is a limit on evidence, not a reason to keep the now-tested constant-path counterexample open.

## Final disposition

| Original issue | Final disposition | Evidence |
| --- | --- | --- |
| P2 directory forwarding test admits ignored-input/constant-`miles` implementation | **Closed for the identified counterexample** | host_test.cpp:23–35 obtains distinct copied direct expectations, dispatches both `.` and `miles` after resetting to the other path, and ends at `miles` before startup. The private constant-`miles` mutant fails the dot comparison at :31 in Debug and Release. |
| P2 cleanup exception can skip owned sink unload and result recording | **Closed for the identified ordinary-exception path** | cleanup.py remains byte-identical to the reviewed v3 collector. It independently attempts termination, unload, defaults capture and writing. V3 fresh pure failure-injection results remain applicable to unchanged code; the v4 packet also records those controls. |
| P3 request text limit exceeds wire capacity by eight bytes | **Closed** | metadata.h, metadata_wire.cpp and wire_test.cpp remain byte-identical to reviewed v3: separate request/reply limits, exact-cap encoded request with offset 136, cap+1 rejection. |

Directory evidence is now discriminating in both requested directions. Raw positive logs show dot reply length 1 and miles reply length 7 with **35/35** checks. Raw mutant logs show dot reply length 7, **FAIL line 31**, and **34/35** checks. Both configurations show the same result. The mutant source changes only the redist argument from retained input to literal `miles`. Thus the previously plausible false pass has a concrete failing control.

The oracle still compares same-vendor return text. It does not prove that every possible omitted-call/stale-return implementation would fail, nor does it create a documented non-mutating query for Miles directory state. RESULTS.md describes this ceiling accurately. No additional vendor run is required to close this specific counterexample.

## Retention supplement

The separate startup-retention-supplement/retention_test.cpp exercises the same frozen v4 owner implementation:

- :9–14 retains two small inputs and proves copying by mutating their original buffers.
- :15–23 retains two more entries, fills exactly MaxFrameBytes logical payload bytes, and checks all four retained payloads after insertion.
- :24–27 rejects one additional byte, leaves the total unchanged, and rechecks all earlier payloads.

The arithmetic is substantive: the first two entries total 8 bytes, the large entry is MaxFrameBytes−136, and the final entry therefore fills the remaining 128 bytes. The final one-byte input tests cumulative exhaustion rather than a single-entry size rejection.

I freshly compiled and executed this pure supplement with g++ C++11, `-Wall -Wextra -Werror -fsanitize=address,undefined`: **15/15**, exit 0, no sanitizer diagnostics. Four existing native v120 x86/x64 Debug/Release run logs each show **15/15**. These observations close the previously missing ordinary insertion-stability and exact-budget boundary checks. They do not inject allocation failure, measure allocator overhead/RSS, or test concurrent/asynchronous vendor access. The 15 supplemental checks remain separate from the canonical 39 portable checks and 35 vendor-fixture checks.

## Artifact and observation verification

I inspected actual v4 host and mutant source, positive/mutant raw Debug and Release logs, supplement source and native run logs, and build receipts. I recalculated hashes rather than relying only on summaries.

| Artifact | Verified SHA-256 |
| --- | --- |
| frozen-v4-review.tar | cc4c4c0cb2b9cbee7b23e7ae1c298cd04c39c60e7e8074a97f36387701684261 |
| native-v4/receipt.json | 215e8cd3e725f5d4d6c33978ebbdb710764e4e358607ebb2f49adabf1360f47b |
| native-hardcoded/receipt.json | 03a12d11b54dd3c0905edf1bdc7de1f55003a64b7aa6e7a1ecd13ba1dfe62dc5 |
| supplement native/receipt.json | cdcb86d4920241202bb8ff1e448d3841f6c88265b3f0b90fa41fd1d754ea6ba4 |
| frozen-retention-review.tar | 9ba23599d86b17bfba8a7747d8f2b470a582bd644f7452d711a2e5283ca8269c |

All six v4 matrix PE hashes, both mutant PE hashes and four supplement PE hashes match their receipts; before/after recorded inputs agree. The local component/test sources checked against those receipts also match, with the mutant intentionally mapped to its private source. metadata.h, metadata_wire.cpp, metadata_host.cpp, wire_test.cpp, cleanup.py and cleanup_test.py are byte-identical between v3 and v4.

I did not execute a vendor or engine program. Vendor results are source-bound existing observations, not an independent runtime reproduction by this reviewer. The fresh sanitizer execution was pure portable code. Hashes support artifact attribution, not behavior proof or protection against a hostile concurrent writer.

## Scope limits retained without reopening the closed findings

The component continues to match the inspected caller's preference IDs/values and speaker-output shape, preserves signed host32 bits, copies nullable output text, retains directory request bytes through fixture shutdown, and rejects unsupported fields before dispatch. No new evidence contradicts those prior conclusions.

Still outside this component's demonstrated scope are full serialized request/dispatch/reply integration, client-visible text lifetime, real session/lane and last-error ordering, ownership across actual host shutdown/replacement, expanded stale/wrong-session handle tests, injected allocation failures, arbitrary SDK directory lengths, and complete internal SDK resource teardown. Omitted-call controls would broaden evidence but are not a prerequisite to the present narrow closure. Playback, engine startup, callbacks and whole-backend readiness were not assessed here.

No further source change is required by this targeted review. Preserve the frozen packets and their precise claims when using the component in subsequent integration work.

## POODO continuation record

The inherited frame was sufficiently precise: assess the frozen two-path repair and a separately attributed retention supplement; preserve earlier reviews; make no source changes or vendor runs. The rival was that the new fixture still admitted the named hardcoded-input implementation. The changed test and matching failing mutant discriminate that rival. Source, artifact identity, raw observations and claim scope were checked separately. Fresh test expectation was 15/15 with no ASan/UBSan diagnostics; it passed.

Research context was renewed on 2026-09-30 by opening the primary [C++ draft list modifier specification](https://eel.is/c++draft/list.modifiers) and [Python exception/finally specification](https://docs.python.org/3/reference/compound_stmts.html#finally-clause), following the prior list-stability and exception-cleanup research questions. These language sources support the mechanisms but do not certify v120 or vendor behavior. No new semantic conflict was found. The exact local implementation and tests remain the stronger artifact-specific evidence.

Twenty paths considered before closure: (1) close the constant-path case from the paired control; (2) keep it open if the mutant passes; (3) retain the cleanup closure by byte identity; (4) retain the capacity closure by byte identity; (5) independently verify receipt and PE hashes; (6) repeat the pure supplement under sanitizers; (7) inspect cumulative-budget arithmetic; (8) test allocation failure later; (9) add omitted-call instrumentation later; (10) add stale-return controls later; (11) obtain exact-version SDK ownership documentation; (12) test serialized integration; (13) test client text lifetime; (14) test actual host shutdown ownership; (15) test concurrency/lane ordering; (16) test stale-session resources; (17) compare native Windows and Wine; (18) preserve evidence as separate test families; (19) narrow any whole-backend claim; (20) stop this targeted review when the named counterexample is closed. Selected 1, 3–7, 18–20; the others are future evidence paths, not newly imposed completion gates. Fan-out was considered and omitted: this remains the allocated independent reviewer, with no descendant capacity or new vendor authority.

`delivery_state=checked final targeted report`; `outcome_state=three findings closed for their specified failure modes`; `highest_justified_claim=reviewed narrow experimental component with source-bound two-path mutation discrimination and independently repeated pure retention checks`; `required_runtime_observation=none additional for these three targeted closures; future integration remains unproven`; `who_controls_next_test=primary agent under user-authorized future scope`.
