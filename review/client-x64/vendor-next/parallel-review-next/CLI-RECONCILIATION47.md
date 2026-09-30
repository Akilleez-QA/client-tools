# Callback guard CLI review47

Grok4.7-medium received only the two small authored guard files and a2389-byte prompt. The90-second bounded attempt timed out, exit124, with zero output. Input and empty-output digests are in grok-guard47-identity.json. This is unavailable review, not agreement or clearance. No identical retry was made.

Composer2.5 completed in45.39 seconds, exit0, output digest b67706136ac0b1fe9b36b1111198eba0c68741c02b1d8a700abc58008eef8081. This is source review, not runtime evidence. Parent checked its findings against the complete source:

- Its selected() coverage objection follows from the supplied patch-only context. The actual ClientMiles::startup implementation begins with Session::selected(), before request(); the in-callback startup test therefore does exercise selected's guard. Native47 independently compiled that actual pipe TU, but its runtime behavior is still the portable experiment. No additional direct selected test is needed for this claimed path.
- Direct request/close under a Scope are tested; invoking each again from the read callback would compose already-tested shared guard/sticky handling. That precise combination remains unrun, not a shown defect. Open/close/seek reentry likewise share the wrapper but are not separately executed; keep this narrow limitation.
- The second invoke check intentionally tests one-shot Invocation lifecycle, not guard-based reentry. No false-pass claim follows without mislabeling its oracle. Nested actual Invocation is the separate guard test.
- An admitted nested leaf with an outer Scope cannot occur under this design. Marking it a missing admitted-state scenario would demand contradictory preconditions.
- Exceptions propagating through the SDK are deliberately not an allowed outcome. The client Invocation catches service exceptions; host callback termination remains unimplemented and untested by47.
- Thread isolation and callback-created-thread exclusion agree with the documented limits.

No new blocking implementation defect was established. Keep the specific unrun entrypoint/opcode combinations visible; the next integration work tests operational host/control ownership rather than inflating repeated common-branch cases.
