# Coordinator candidate: admitted-work mechanism only

Current v2: native v120 x86/x64 Debug/Release /W4 /WX **87/87 each**; Linux ASan/UBSan87. Three safe mutants compile and fail: ignore lease owner, advance over acknowledgment hole, drop resource pins on Failed. Exact sources and raw logs are under results; input-v2.tar preserves tested source. Historical v1 passed84 before explicit callbackPins assertions; v1 is preserved, not current evidence. No vendor SDK is linked or executed.

The component centralizes admitted-call ordering, lane/lease recursion, request pins, callback identity/frontier accounting, and Active/Draining/Failed transitions. `admissionOrdinal` is assigned only after scheduler selection. It is **not** a wire correlation ID. No submitted-call queue, fairness proof or transport replay protection is supplied by this ordinal. `admitCleanup` is a trusted coordinator entry point, never an untrusted wire flag. Draining permits cleanup/owner unlock, refuses ordinary game work and new lock acquisitions.

`completeAdmission` means actual observed vendor return; the actual vendor result must be carried separately. It is not semantic success. The void lock/unlock return is the modeled point for lease state change. Failed leaves pending pins, callbacks and last known lease diagnostics intact; no transparent restart or synthetic unlock. A later genuine completion observation can release request pins without restoring the failed session.

Readiness exposes requestPins, callbackPins, close frontier, contiguous acknowledged frontier and vendorTerminationUnproven. The latter **always remains true**. Callback admission records an observation, not game execution. Acknowledgment is a coordinator input whose eventual executor must establish actual effect/completion before sending it. Late callbacks extend the close frontier; no pointer is freed and no vendor quiescence is granted.

## Independent oracle boundary

The peer authored17 schedules without seeing implementation; results/oracle-coverage.json maps them to this slice. It is a coverage interpretation of the87 mechanism checks, **not17 executed end-to-end oracle scenarios**. Wholly unimplemented: post_fence_callback_violation, generation_and_registration_reuse, backpressure_both_channels. Other schedules remain partial except nested-lock ownership mechanics. Mixed causal TreeFile/unsolicited EOS remains UnsupportedContract for actual game callback affinity/reentry.

Registrations never retire/reuse; default64 is a total lifetime cap in this experiment, not production capacity. Callback entries include acknowledged holes until the contiguous frontier advances, preserving bounded accounting. IDs/counters reject exhaustion. Resource handles are structurally checked only: central resource liveness, borrowed-parent expansion and buffer ownership pins must be integrated before this protects real resources. No arbitrary nested vendor call reentry is modeled or declared impossible.

No final Closed state, vendor termination policy, actual driver lifecycle, client terminal-result delivery, source-thread classifier, wire handshake, named pipes, performance result, game-policy dispatch or product integration is present. These are deliberate unresolved boundaries, not passed checks.
