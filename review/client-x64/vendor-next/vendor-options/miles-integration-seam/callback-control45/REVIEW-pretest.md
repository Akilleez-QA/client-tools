# Source review before portable execution

Reviewed PLAN.md and complete host_association_mapper.h/.cpp against this candidate's actual Coordinator34 and SessionFileOwner implementation. No compiler, tests, SDK/vendor/engine execution, VM contact or product changes performed.

The ordinary-command correlation/return join is internally consistent under the stated single-control-thread, authenticated-endpoint and fully validated ACK/forward-result preconditions. One action-scope issue should be resolved or explicitly excluded before broader use.

## Finding: lock-action settlement lacks outcome distinction

`host_association_mapper.cpp:18–20` accepts AcquireLock and ReleaseLock via the general Action parameter. `observeForwardReturn` at34–40 receives only session/request, and `settle` at28–32 unconditionally calls Coordinator::completeAdmission. That coordinator applies lock acquire/release transitions whenever it is not Failed, without a vendor-executed/success flag.

A caller can publish AcquireLock, receive a correctly correlated but known Backend refusal (for example unsupported operation), then report that validated forward return. The mapper settles and the coordinator fabricates a held lease although no vendor lock occurred. ReleaseLock has the symmetric hazard. “Fully validated” is not synonymous with success: known refusal frames are valid results elsewhere in this bridge.

For this minimal ordinary file-callback slice, rejecting actions other than Ordinary is sufficient. Alternatively the header must explicitly require the outer result owner to mark the session Failed before reporting any unsuccessful lock action, and that contract needs a negative test; a future outcome-aware action settlement can be separate. This finding does not contradict the planned ordinary-command ACK-race prediction. No source repair was made by this reviewer.

## Correlation and replay

- Forward publication refuses reuse/nonmonotonic IDs, retains wire ID distinct from local admission, and performs no fallible mapper work after successful coordinator admission. Next publication is blocked until explicit Settled consumption.
- Reverse requests require the authenticated session, real decoded ReverseRequest, nonzero monotonically increasing reverse ID and available mapping capacity. Gaps are allowed, duplicates/backtracking are not; this should be the documented sequence policy, not described as contiguous numbering.
- Causal reverse requests match the retained wire cause, lane and lease before mapping to local admission. The reverse peer never chooses the local intake ordinal. Unsolicited requests require the separate background lane, zero cause and zero lease even while a command is active.
- Mapper records correlation storage before owner.receive. An owner refusal leaves that record retained and fails the coordinator. It does not free an uncertain operation or replay it. If rejection happened before owner's lastIntake advanced, later requests can remain rejected; that is terminal failure behavior, not recovery. Do not claim continued late-observation coverage for every malformed/capacity-failure history.
- Authentication and proving host TLS provenance are outside this object. An authenticated but dishonest host could label a background request causal; the mapper validates consistency with an admitted command, not independently that a vendor callback occurred on its thread. Hostcontext41 plus trusted host binding must supply that guarantee.

## ACK and forward return ordering

- ACK before forward return: acknowledgeConsumed resolves reverse→local intake, requires queued reply and owner readiness, then clears only that reverse record. Since command is still Executing, settle does nothing; the later actual forward observation completes admission.
- Forward return before causal ACK: ReturnedWaiting is retained while Coordinator::causalPending is true. ACK invokes settle again. Neither path waits on the control thread.
- Additional causal traffic while ReturnedWaiting is accepted only while its command remains retained. This is appropriate for already in-flight reverse traffic; after Settled or consumption it is rejected rather than attached to a later command.
- Unknown/early/duplicate ACK fails before a second owner acknowledgement. markReplyQueued means complete-frame acceptance by Endpoint.send, not peer consumption. The endpoint owner must call it before it can dispatch an ACK event on the same control thread. Full ACK opcode/envelope/payload validation remains an outer precondition; a bare integer from unvalidated bytes is insufficient.
- Unsolicited callback pins do not keep an unrelated ordinary command Executing. They stay retained in owner/coordinator until their own ACK; that is distinct from session/file teardown readiness.

## Failure retention and boundary obligations

`fail()` only marks Coordinator Failed. Existing mapper/owner records remain; it does not cancel jobs, fabricate replies, join the worker or certify termination. Owner refuses new worker dispatch in Failed but can finish/record work already accepted. A real forward-return observation and real consumption ACK may still release their respective pins in Failed, as Coordinator explicitly permits; the session does not become healthy again.

Constructor capacity allocation and coordinator admission allocation can throw outside the callback ABI. Outer control-thread exception handling must fail and retain the actual owner; this helper is not a noexcept SDK thunk. Destruction still depends on the outer owner retaining engine/jobs/context through a valid shutdown or failure protocol. Coordinator zero pins alone does not prove vendor quiescence.

## Suggested pretest assertions

Exercise both ACK/return orders, out-of-order ACKs among multiple causal callbacks, background callbacks during/after a command, stale session/cause/lane/lease, reverse-ID replay after record reclamation, early/duplicate ACK, capacity exhaustion and malformed owner rejection. Confirm rejected/uncertain records remain and no subsequent worker invocation occurs in Failed. Include the chosen lock-action exclusion or refusal contract explicitly; ordinary-only scenarios cannot establish it.

Disposition: no concrete defect found in the stated ordinary-command join. The accepted Action surface currently permits an unsafe interpretation for known refused lock operations; narrow or document it before expanding scope. This review supplies no execution or operational-host evidence.
