# Parent first portable gate review

Reviewed four production sources, actual registry reserve/publish/retire delta, real decoder/copyRead and all proposed tests/runner. Blind source review separately found no blocking defect under serialized producer and owner-lifetime assumptions. These are source reads of common artifacts, not independent runtime evidence.

Authorize the seven positive groups and six bounded authored-only subprocess oracles in PORTABLE-GATE-PLAN-v1.md. Their terminate handler is armed only after assertions, exact exit73/marker required; accidental earlier terminate exits74. Negative subprocesses deliberately skip teardown and leak analysis and cannot establish cleanup, SDK or engine behavior. No live host process, SDK, custom allocator workload or product is touched.

Prediction: successful consumption preserves values/token identities/copy bounds and exposes result only after ACK write observation; malformed/uncertain consumption withholds result and unresolved destruction cannot return. Preserve first failure without automatic retry. Frozen20 inputs checked.
