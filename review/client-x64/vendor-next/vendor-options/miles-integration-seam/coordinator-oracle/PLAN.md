# Independent coordinator oracle — prospective only

2026-09-30. Read ARCHITECTURE.md and actual Audio.cpp (start-sound lock scope2320–2337; file callbacks3951–4098; EOS4730–4791; lock forwarding4920–4929). Did not read coordinator-candidate implementation. No tests, VM operations, source changes, or runtime outcome claims. cases.json defines adversarial traces before implementation-specific tests.

Source facts: startSample calls occur inside a vendor AIL_lock scope. TreeFile callbacks may perform open/seek/read/close and use a process-global file map; their `once`/PerThreadData code is not proof a new arbitrary dispatcher thread is safe. EOS searches actual sample maps, sets PS_done and immediately calls Sound2::endOfSample. Therefore delivery, execution, game-state effect and acknowledgement are distinct observations. Transport queue progress cannot substitute for game callback completion or correct affinity.

Model invariants are testable with abstract transitions: exact session/resource/registration identities; lock owner progression without admitting unrelated work; causal attribution from explicit source context; pending calls have one terminal result; callback pins remain until completion; per-registration close frontier requires contiguous completion, not maximum seen sequence; no retirement until an externally established no-new-callback condition plus all required work completes; host loss does not invent a vendor return or retry an ambiguous action.

Real-vendor gates remain unproven by these traces: which thread may run actual game callbacks; legal reentry during vendor locks; whether close produces callbacks; the real SDK no-new-callback guarantee; source callback timing, performance, FPU context and actual shutdown order. A test may inject an explicit vendor-quiescence fact to exercise mechanism, but cannot claim to establish it. Unknown callback-affinity/reentry contracts must produce an explicit integration blocker rather than silently defer, drop, or execute on an arbitrary lane.

Fairness is expressed as finite enabled-transition progress under a fair scheduler, not a guessed millisecond bound. A test fixture chooses a finite scheduling budget and reports that artificial bound; it cannot prove real audio latency. Independent channels may reorder arbitrarily while preserving each channel's own order. All cases must retain exact event records, including rejected/deferred input and reasons, not only the final state.

Required observables/API surface (names are concepts, not dictated implementation names):
- Session state, connection-bound identity, handshake version and terminal failure reason.
- Request identity, resource generation, source lane, causal identity, lock lease, admission disposition/reason, dispatch start/end and exactly-one terminal outcome (real vendor result vs NotExecuted vs ExecutionUnknown).
- Lock owner lane+lease+depth; runnable/blocked queue views; chosen next eligible work; causal waiting stack separate from active-request coincidence.
- Callback identity and registration/resource generations; source thread-role/context; receive/admit/dispatch/complete/ack separately; assigned affinity or explicit UnsupportedContract; outstanding pins.
- Reverse-I/O request/reply association and completion; channel drain counters; no transport mutex held across game/vendor calls (instrument actual implementation later).
- Resource Closing/retired state, in-flight request count, callback pins, captured close frontier per registration, contiguous ack frontier and holes, actual vendor-release completion, separate no-new-callback evidence.
- Host-death notification, pending terminal classification, no automatic retry/restart and stale-session rejection after a new session.

The combined locked reverse-I/O + foreign EOS schedule is mandatory. Passing its separated components is insufficient. If real callback affinity is not yet known, the combined model can check message classification, pin retention and progress of reverse I/O while recording unresolved execution policy; it must not be scored a full semantic pass.
