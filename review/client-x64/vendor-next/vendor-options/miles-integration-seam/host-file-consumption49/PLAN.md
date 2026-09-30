# Host file tokens and reply consumption 49 — source-only first slice

No compilation, tests, Endpoint, SDK, VM, engine or product execution. This is a concrete part of HOST-INTEGRATION-PLAN.md, separable from its dedicated I/O-owner threading. Existing38/46/48 sources remain unchanged.

## Reuse and identity separation

Reuse the actual stream-native38 ResourceRegistry with reserve/publish/beginClose/retire. Its reserve API currently accepts only Driver/OwnedSample; the sole change permits File as well, with the existing null-parent condition. This avoids reimplementing slot generation, reservation cancellation and publication. The older46 registry has no reserve API and is not silently substituted.

The SDK callback has only a 32-bit opaque host UINTa value. It cannot carry the registry's three-field Handle. FileTokens therefore adds a bounded record array and monotonic uint32 token, mapping **SDK token → host registry identity → record containing client wire File identity**. These are deliberately distinct: the host registry handle never appears in a reverse request, and the client's wire identity is never passed to ResourceRegistry.resolve/retire. Records' stable addresses, not client handles, are the registry's private void* values. Client native uintptr/zero handles never enter this host layer at all.

Capacity is a configured simultaneous-file bound allocated before callbacks. Tokens never repeat, including after failed opens or close/reuse; UINT32_MAX exhaustion is explicitly rejected before sending another open. There is no invented smaller cumulative call cap. Registry generations remain reused normally underneath; an old SDK token cannot reach a newly opened record even if its array slot is reused. Empty/live/closing record scanning is bounded by the configured live capacity.

## Transaction and call order

Construct ReplyTransaction with the genuine validated outstanding Request, retained registration, existing host token for nonopen operations, and original vendor read destination/capacity for read. It copies/validates the request, preencodes the exact protocol48 ACK into fixed136-byte storage (not yet exposed), validates buffer shape and existing-token/remote-target equality, then reserves open ownership as the last fallible preparation. Constructor failure occurs before request send; reserve storage may allocate only at this stage.

`beginSend` must precede any transport exposure; for close it marks registry/record Closing. From then on no cancel/rollback is permitted. `consume` sets a sticky Failed state before invoking the real file26 decodeReply, so malformed context/status/payload or allocation exception cannot be retried. On a fully valid reply it performs precisely one operation:

- open success: allocation-free publication of the reserved host record against the full client File identity; reject duplicate live remote File identities. Keep exact uint32 status separately from nonzero opaque host token. The client service's valid zero local handle was already preserved by46 and is not inferred from wire bits.
- open ordinary failure: cancel the unused reservation, preserve exact zero result, publish no token. Consumed token numbers remain unavailable forever.
- read: real decodeReply validates source frame/payload and returned count; real copyRead rechecks destination nullness/capacity, count and vector extent before memcpy. No clamp/chunk/EOF substitution.
- seek: preserve decoded uint32 return bits for the actual thunk to reconstruct the signed result using the established bit-preserving convention.
- close: only after a validated normal close reply, retire the host registry entry and invalidate its SDK token. No retirement on an uncertain result.

Only success changes state to Consumed and exposes `ack()`. The eventual sole Endpoint owner sends those exact bytes after consumption and calls `observeAckWriteComplete` only after actual write completion. `result` exposes return bits/open token only in Acked. It does not equate local ACK write completion with client-side settlement; the peer mapper must independently receive, validate and consume the ACK.

Before any send, explicit cancellation or Prepared destruction releases an open reservation. Issued, Consumed or Failed destruction calls std::terminate: there must be retained transaction ownership or the prescribed nonreturning host failure boundary, never stack unwinding that cancels unknown effects. FileTokens must outlive all transactions; destroying it supplies no remote closes or quiescence proof. ACK-send uncertainty leaves Consumed ownership retained and requires the terminal host path. No API retries, resends or claims recovery after uncertainty.

## Files and boundaries

New `file_tokens.h/.cpp` and `reply_transaction.h/.cpp` under candidate/host-file-consumption49. Protocol48/file-channel/codec dependencies are pinned copies; ResourceRegistry comes from stream-native38 with the single File reservation extension. provenance-v1.json and source.patch describe exact parents and deltas.

This is not yet an x86 SDK thunk implementation. A later Mss.h unit must statically check exact callback typedefs/UINTa width, map the transaction's returned bits to the original signatures, and use a guaranteed nonreturning catch-all failure routine. It must serialize producer access, capture host TLS origin before waiting, prepare the original Request/ACK expectation before send, and provide actual Endpoint events. This source introduces no alternate filesystem, generic scheduler, authentication, callback-installation state, or public API change.

## Proposed source-review checks before any gate

Verify reserved/live/closing identities and no token reuse; exhaustion check before reserve/send; reserve File parent constraints; no allocation after successful open publication; strict target match; exact reply decoder/copyRead use; ACK visibility ordering; sticky failure/no retry; and destructor retention contract. Portable test authoring/execution comes only after review. Later tests should include different host/client slot/generation values, stale token after record reuse, failed open preserving status, successful remote File with zero originating client handle, malformed read/status/context, short/null destination, signed seek bits, ACK-before-consumption refusal, result-before-ACK refusal, and retained failure paths without invoking a real SDK or allocator workload.
