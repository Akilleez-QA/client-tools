# CLI review reconciliation51

Composer2.5 completed three bounded source passes; raw prompts, exact hashes, outputs and timings remain beside this note. Grok4.7medium timed out after90seconds with no output on the separate plain-header question. Grok provides no finding or clearance; no retry of that query occurred. These are source-review inputs, not independent runtime observations.

## Parent decisions

The first Composer pass called retained reverse rows and failed host reservations leaks/stuck-state defects. The supplied contract already required terminal host failure and client retention of unknown work. Root checked actual mapper/owner/coordinator behavior: no healthy-session restoration or fabricated consumption is implied. Releasing these rows merely to improve a count would erase unknown side effects. The second pass accepted this distinction. Final runtime callers must still implement the promised failure/retention policy; incomplete53 explicitly does not provide normal teardown.

The first pass suggested close failure bits were ignored. Root inspected actual callback declaration and invocation: close returns void; decodeReply rejects nonzero close bits and any nonzero transport status, while CallThrew cannot encode a normal reply. Composer's second pass corrected that finding. This preserves the observable void callback return; it does not prove that a underlying filesystem close succeeded.

The second pass alleged ClosedAwaitingAck could become misleading when encoding failed. Root traced the actual fixed writer: normal returned close has zero result fields, empty payload, null published handle, valid retained header and exactly128 preallocated output bytes. The encoder accepts those conditions; validHandle explicitly accepts all-zero handles. The third pass found no reachable corruption-free close-encoding defect from these inputs and no premature normal close release. No speculative production change was made. Conditional failure retention remains defensive behavior, not proof of a successful ACK.

The split intake counters deliberately cannot resume normal service after pre-admission failure. The runtime must observe Failed and stop executing new callbacks.53 now checks coordinator failure after polling and rejects control errors; its unresolved teardown is kept explicit. Causal callbacks block command settlement; unsolicited callbacks remain session-owned and need not block an unrelated command. Existing positive/uncertain-order tests cover these distinctions within their scripted scope.

ACK queue/write/receive ordering is a real integration obligation.50 host's new owner consumes before sending ACK and waits for write completion before SDK return;53 client marks reply queued before another control dispatch. Those new loops have separate source reviews, not native execution evidence. Exact host write completion cannot be inferred from protocol encoding alone.

The last bounded Composer pass returned no new demonstrated defect on the challenged normal close path. This is bounded saturation of that question, not exhaustive bridge clearance.
