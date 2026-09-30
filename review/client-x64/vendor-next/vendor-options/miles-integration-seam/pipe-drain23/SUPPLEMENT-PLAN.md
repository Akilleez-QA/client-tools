# Prospective supplement, before fixture changes and run

The first 13-case run passed the candidate and reproduced seven old discriminators. Immutable raw evidence is evidence.zip and evidence/, bound by pre-run-identities.json and remote run-input-manifest.json. Original code snapshots and source.patch will remain unchanged.

Plan precision correction after observing outcomes: PLAN's queued/unissued wording grouped this with session rejection. Actual queued-write checks only the existing Endpoint.sendBusy evidence after direct cleanup, and passes both implementations. It is a regression guard, not an old-versus-candidate discriminator. The partial-write and backpressure cases test actual session rejection for incomplete output. No failed prediction is being relabeled as a pass.

Parent review found a harness cleanup gap: if a timeout assertion throws while cancellation is withheld, Endpoint destruction happens before main's catch clears the switch. Add an RAII reset declared after endpoints so unwinding restores cancellation first. This does not change application source or the acceptance oracle.

Prospective oracle v1 supplement in the same VS2013 v120 amd64 Debug configuration:
1. exchange-session: retain the exact request/reply and codec checks, then call copied drainSession(a,b,true). Both old/candidate must accept consumed, fully sent valid traffic; candidate must retain zero unread bytes.
2. ordered-close-input: collect 13 actual bytes, close peer, then drain with orderedClose=true. Both should retain PeerClosed; old accepts and fails the rejection oracle; candidate rejects due to unread bytes. This discriminates actual first-fault allowance from leftovers, beyond earlier tests that merely enabled the allowance.
3. session-timeout: explicitly withhold cancellation on channel A, invoke copied drainSession, verify rejection and A still pending; candidate B must already be safely Closed despite A's timeout. Release adapter and explicitly drain both before evaluating final assertion. Old short-circuit leaves B Open and fails this oracle.

Rebuild the two test executables for the harness edit. Only run these three supplements; prior cases do not need repeated execution because application source and their paths/oracles are unchanged. A build failure, timeout, or mismatched result interrupts and is retained. The process watchdog remains a last resort, not the primary exception-cleanup mechanism. One parent/source-correlated review supplied this harness criticism; no new descendants or expanded configuration matrix.
