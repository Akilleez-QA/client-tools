# Retained buffers and SoundInfo — independent source review

2026-09-30. Nonblind component follow-up, bounded to the newly authored retained-buffer and SoundInfo components. SoundInfo review began after the build worker's ready signal. Earlier opening/addendum/teardown reports were not changed. No compilation, tests, vendor code or other workload was executed; only source, hashes and existing result records were read. No product edits. This file is the sole new output.

**Disposition: no actionable implementation defect found in the reviewed snapshot.** That is a bounded source judgment, not a correctness proof or certification of integration. I found no material overclaim in the two results documents. No repeat architecture criticism is added here.

## Exact snapshot

Root **C**: `/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam`.

| File relative to C | SHA-256 |
|---|---|
| `host-candidate/retained_buffers.h` | `e62c472f1e46f783a130da8081bb92e958d8e3acaa9010d2fabae6169f329d8e` |
| `host-candidate/retained_buffers.cpp` | `9f8fc1f78238b0347e25606fdc1be658414b73aefb021c3ef91577bcd45d7401` |
| `host-candidate/retained_buffers_test.cpp` | `2d8bc31b0666d8ec6aab84e2551e2ec67df2872ac0663a0e1f5f8cb1dd15ce86` |
| `host-candidate/RETAINED-RESULTS.md` | `e2e780fecaa8d62acae5c935e6b490fe57e44598a80e92c0474d8d799ed941cc` |
| `transport-candidate/sound-info-codec.h` | `d12fe9d590e53bcbb05b725a5a10bdf2d883e91eb59e7cdffc0dbc7e68f0d112` |
| `transport-candidate/sound-info-codec.cpp` | `39c08092a658627a2069066906e2a795708c4ea51e49f0c897936beec11e44c2` |
| `transport-candidate/sound-info-tests.cpp` | `397e7e33fb1d24dd6ab1d2454e41cb65330602cadbf185e28fe976bfbe046aad` |
| `transport-candidate/sound-info-RESULTS.md` | `1d9af2e8e8e4ed9bbb4e472368f6be9516ccccbcda2fef5ac1253363ca91e8e6` |

These eight identities were unchanged on the closing hash read and match the supplied source manifests where listed. SoundInfo's recorded native-v2 dependency hashes also match the current `codec.h` (`d95094b9…`), `resource_registry.h` (`f2a4131c…`) and `miles_wire.h` (`8efe3915…`). Registry implementation itself is not reviewed afresh here. If a listed source/header changes, this disposition is stale for that file; re-review the delta and bind any subsequent test result to the new dependency identities.

## Retained-buffer assessment

References in this section are to `C/host-candidate/`.

- **Bounds/accounting:** `retained_buffers.cpp:20–29` rejects unknown kinds, out-of-span ranges, lengths beyond U32, capacity excess and invalid terminated text before copying. `limit-used` is safe under the maintained invariant `used <= limit`: construction starts at zero, successful stage adds only an admitted length, and retirement subtracts a resident entry's size (`16–17,23,38,54–59`). No capacity bypass or overflow was identified within a genuinely readable caller frame.
- **Identity:** the shared atomic token source (`7–13`) reserves distinct nonzero IDs across stores using compare/exchange. Unsigned exhaustion advances to zero, at which point future reservations fail instead of returning a reused token. Store lookup cannot resolve another live store's token. This is process-local identity in the component's single-definition deployment, not session/wire authority; the results explicitly say so.
- **Ownership:** stage creates a copied candidate before publication (`30–38`). The map owns that copy; later staging/insertion does not modify previous entry vectors. Commit only changes `activeToken` (`49–52`), preserving old views until explicit retirement. Active retirement is rejected (`56`). The caller's explicit quiescence requirements in the header (`8–10,22–23`) apply to inactive retained entries and destruction as well. I do not classify an explicit misuse of those requirements as a component UAF defect.
- **Failure publication:** invalid input does not change `out`, current active data or accounting. Allocation exceptions may propagate, but publication of the token and incrementing `used` occur only after insertion. An allocation failure after reservation may consume a token; that does not create a published identity or corrupt accounting. The results state exception propagation and correctly disclose absence of allocation-failure injection and exhaustion testing.

The 41-check source exercises retained-copy independence, cross-store rejection, replacement preserving the old address, active-token protection, caps and null/empty text distinction (`retained_buffers_test.cpp:13–53`). These are meaningful behaviors, but 41 checks do not independently prove exception behavior, concurrency or vendor quiescence. The test's “simulated vendor failure” (`28`) means it deliberately does not commit; it invokes no failing vendor function. The results accurately preserve that boundary.

The payload cap is not a process memory cap: candidate/map copies and container overhead add allocations. This is explicitly disclosed, so it is not an overclaim. No recommendation to rewrite the store or add broad new tests follows from this pass.

## SoundInfo assessment

References in this section are to `C/transport-candidate/`.

- **Wire/scalar fidelity:** `sound-info-codec.cpp:52–91` serializes eleven explicit LE32 fields into 44 bytes. Signed fields reconstruct through `memcpy`, and integer conversion into unsigned encoding preserves their 32-bit representation. Genuine `Mss.h:1748–1759` at source commit `49d0eeed…` agrees with the signed/unsigned scalar categories. Native struct layout is not transmitted.
- **Extent rules:** validation (`37–50`) uses checked subtraction for data extent and rejects unknown null bits/noncanonical null offsets. Initial nonnull offsets must designate a byte; data may designate one-past only at zero length. Integer-address mapping (`22–34,93–110`) checks retained-address arithmetic and numeric containment without subtracting unrelated C++ pointers. Resolution (`112–122`) validates before forming pointers and avoids pointer arithmetic on a null base. I found no actionable overflow or premature dereference in these paths under the documented real-allocation precondition.
- **Publication:** encode uses a temporary vector and swaps only after completion; decode/map/resolve construct local results and assign only after validation. Rejected input does not publish a partial result. These functions do not establish allocation identity merely by comparing addresses; identity and lifetime are explicitly supplied by the caller/retained-buffer registry.

The tests include an independently authored golden byte sequence, truncation rejection, boundary values and roundtripping real local addresses (`sound-info-tests.cpp:10–65`). The 44 truncated-prefix checks are useful, but are not 44 distinct semantic contracts. Existing native-v2 records show four successful configurations, with the reported Win32 skip for an unrepresentable size-above-U32 case. I did not rerun them. The mutation result reported as 87/93 is evidence that the tests notice removal of the extent check, not evidence of exhaustive malformed-input coverage.

**Remaining adoption gate, not a discovered bug:** null data requiring zero length, initial pointers rejecting one-past, and all nonnull output pointers requiring containment within the retained file image are deliberately conservative rules. The results explicitly say that genuine valid-format vendor outputs have not yet established those rules. Before enabling the host operation, compare these restrictions with real successful vendor metadata across the intended formats. A legitimate rejected output would disconfirm the proposed semantic restriction and require an explicit compatible representation; it would not justify fabricating a pointer or weakening memory bounds blindly. No vendor behavior was inferred from codec test counts.

## Recommendation

Keep these components as source-reviewed candidates with their documented caller obligations. Preserve the current bounded wording of the result records. The next component-specific evidence worth obtaining is genuine vendor metadata compatibility for SoundInfo and concrete retained-buffer lifecycle use by its caller, when that work is separately permitted. Source reasoning supports the current ordinary failure-publication mechanics; it does not replace allocation-exception/exhaustion evidence if those paths later become acceptance claims. No new blocker or confirmed memory/identity/failure bug is raised in this snapshot.
