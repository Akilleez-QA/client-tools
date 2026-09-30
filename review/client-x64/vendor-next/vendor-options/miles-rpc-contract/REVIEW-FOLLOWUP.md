# Independent RPC review reconciliation

Grok reviewed the preserved eight-run probe; the parent checked the dispatch predicate, analyzer, raw events and current game callers. This is source/log review, not another runtime reproduction.

- Getter-vector equality is the supported comparison. EOS command context and delivery differed and must remain separate; empty getter `differences` arrays do not establish event-order equivalence. `event-context-review.json` classifies each callback against the recorded command interval.
- `activeId` retains the most recently dispatched command during idle periods. The original RESULTS already labels this as last/current context, not causal membership. An asynchronous callback between commands is valid. Grok's proposed rule to fail any such event would impose a new, incorrect oracle; it is not adopted.
- The old post-release request simultaneously has a stale generation and no live vendor handle. It proves rejection of that combined state, not that the generation predicate independently protects a reused live slot. A new prospective test recreates the slot, sends the old generation, and uses a generation-disabled diagnostic control with a still-valid vendor handle. Original records remain untouched.
- The returned status is the genuine Miles status, not the game's PlayBackStatus enum. Actual Sound2d/PlayerMusic behavior and 3D playhead conversions are outside this raw-vendor probe. Current game-call-chain notes identify active observers rather than assuming every defined getter has callers.
- Raw callback thread and FPU records are retained; no engine-thread or FPU equivalence is established by the analyzer. The newer immediate/queued/unsolicited observer experiment removes the shared-queue baseline flaw but remains a diagnostic observer model.

No production backend is selected, and neither a successful raw-vendor transaction nor a repaired guard test establishes original game fidelity.
