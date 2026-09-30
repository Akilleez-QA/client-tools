# pipe-drain23 bounded cancellation-evidence candidate

The isolated candidate passed 16 named native synthetic checks in one configuration: Windows 10 build 19045, VS2013 v120 amd64 Debug, `/MTd /Od /W4 /WX`. The unchanged old source failed nine predeclared discriminating checks and passed seven regression controls. This is component/fixture evidence, not vendor integration or callback quiescence.

## Exact source change

[source.patch](source.patch), SHA-256 `d7a72f047259feb5f058490ae96486614ac69016f8d8d4c4c95f86a6e1b91dea`, changes only three files in the copied `candidate/` tree:

- `pipe-transport-candidate/endpoint.h`: adds `unreadBytes()` and one counter; clarifies that `drain()` is cleanup only.
- `endpoint.cpp`: retains the first meaningful failure independently of lifecycle state; ignores ERROR_OPERATION_ABORTED only after local stopping/fault; accounts all successful completions; counts inbound bytes until takeFrame; after stopping it does not parse/allocate/read again; successful outbound completion updates existing write progress so a completed frame clears sendBusy. No new I/O is issued after stopping.
- `live-bridge-candidate/common.h`: attempts both drains before testing results, then checks first failure, unread bytes, and existing sendBusy separately. Ordered peer close cannot mask traffic evidence.

`drain()` itself and the destructor retain their lifetime contract: successful drain means outstanding operations are collected and the pipe is closed, even when unhealthy traffic evidence remains. Timeout retains ownership. An aborted write may already have delivered a prefix; sendBusy records that the whole frame was not confirmed transmitted.

Original endpoint, fixture, codec/protocol dependencies, and live-bridge common.h remain unchanged against `input-manifest.json`. No original/frozen product source, startup worker inputs, real engine, private SDK, vendor/audio path, allocator faults, commits, or pushes were touched.

## Native observations

| Case | Old | Candidate | Discriminating observation |
|---|---:|---:|---|
| idle | pass | pass | Pending read abort 995 is ordinary cleanup; failure None |
| exchange | pass | pass | Exact encoded/decoded request and reply, full and 3-byte segments |
| late-read | fail | pass | OS completed 13 bytes before collection; candidate unread=13, session rejected |
| late-peer-error | fail | pass | OS error 109 before collection; candidate PeerClosed/109, session rejected |
| buffered-input | fail | pass | Untaken 136-byte frame rejected |
| partial-input | fail | pass | Untaken 13-byte header prefix rejected |
| queued-write | pass | pass | Direct drain preserves sendBusy for unissued frame; regression guard only |
| partial-write | fail | pass | Partially issued segmented frame rejected by session drain |
| backpressure | fail | pass | Read/write cancelled safely; sendBusy still true; session rejected |
| completed-write | fail | pass | Peer received exact 524424-byte frame; native completion wins; candidate clears sendBusy |
| first-fault | pass | pass | InvalidLength/0 retained after later native write error; no overwrite |
| external-abort | pass | pass | Abort 995 while Open retained as WindowsIo |
| timeout | pass | pass | Two real kernel-pending operations, three live handles and same operation/buffer identities after drain(0); later cleanup succeeds |
| exchange-session | pass | pass | Exact framed exchanges accepted through drainSession with ordered close |
| ordered-close-input | fail | pass | Actual PeerClosed/109 plus 13 unread bytes; ordered-close allowance does not hide input |
| session-timeout | fail | pass | First channel retains pending read; second is Closed before releasing first's cancellation gate |

The first 13 cases use archived `input.zip` and `evidence/`; the three prospectively planned supplements use the final fixture and `supplement-evidence/`. Product candidate source is identical in both runs. Raw expected session rejections print `FAIL <reason>` inside the helper; the case succeeds only when the outer explicit oracle prints `PASS <case>` and exits 0. Old discriminator runs exit 1 by design. There were no compiler warnings or runtime watchdog expirations. Initial launcher discovery found `python` was a Microsoft Store alias; no native test ran in that failed launch. The actual existing runtime is `C:/ci-dpvs-review/python/python.exe`.

`SUPPLEMENT-PLAN.md` records two precision updates: queued-write was implemented as unchanged evidence preservation, not session rejection; and a test-only RAII guard restores cancellation before Endpoint destructors if an assertion throws. The three supplemental checks were added before their execution. The first-run fixture remains preserved in input.zip; no historical output was rewritten.

## Reproduction and provenance

Native input identities: `pre-run-identities.json`, `evidence/run-input-manifest.json`, `supplement-pre-run-identities.json`, `supplement-evidence/supplement-input-manifest.json`. All relevant local/remote source hashes matched after normalizing Windows path separators. Collected executable/build/log hashes matched the remote output manifests. Raw archives: `evidence.zip`, `supplement-evidence.zip`; readable results: `evidence/results.json`, `supplement-evidence/supplement-results.json`.

All operations used the allocated `C:/pipe-drain23`; no other worker paths were mutated. Existing executable replay from Linux:

```bash
/home/akilleez/Work/swg-source-vm/winbuild/winps.sh '& C:/pipe-drain23/candidate-amd64-Debug/fixture.exe late-read; exit $LASTEXITCODE'
/home/akilleez/Work/swg-source-vm/winbuild/winps.sh '& C:/pipe-drain23/old-amd64-Debug/fixture.exe late-read; exit $LASTEXITCODE'
/home/akilleez/Work/swg-source-vm/winbuild/winps.sh '& C:/pipe-drain23/candidate-supplement-amd64-Debug/fixture.exe session-timeout; exit $LASTEXITCODE'
```

Replay any table case using its exact name and matching executable group (supplement group for the last three). `run-native.py` and `run-supplement.py` contain exact compiler commands, watchdogs, old/candidate expected exit codes, and manifest generation. For a fresh reconstruction at the same owned path, initial source is input.zip; final source is final-source.zip. Preserve previous evidence before rerunning scripts, since their fixed output filenames are deliberately simple.

The test wrapper affects only endpoint Win32 calls. Real named-pipe operations establish successful and failed terminal results. Cancellation adapters inject a peer write/close/read at the exact cancellation boundary and wait on manual-reset OS completion events; there are no scheduler sleeps masquerading as race proof. GetOverlappedResult results are observed and passed through unchanged. Timeout tests explicitly withhold the cancellation request, returning a test-adapter ERROR_NOT_FOUND while native GetOverlappedResult confirms operations remain incomplete. They prove the endpoint's timeout ownership branch, not that Windows cancellation was naturally slow. The shared self-authored fixture/oracle is not independent validation.

## Advisory review and limits

Parent's Grok review (`client-wire-validation/parallel-review-next/grok-drain23-log.txt`) independently highlighted the Open-state drop but shares source evidence. Its proposed post-stop continuation I/O, taking frames after faults, drain refusal on buffered data, and destructor termination for unread frames were not adopted. Those would change shutdown semantics and conflate storage cleanup with channel health. Its unconditional abort exemption was narrowed to local stop/fault, and its claim that a cancelled writer's peer must observe no payload was rejected because prefix delivery may precede cancellation. Its event-before-collection test idea is consistent with the native deterministic controls used here. ERROR_NOT_FOUND is not used as completion proof.

This candidate retains evidence for bytes actually completed into this endpoint and for queued/incompletely transmitted output. It does not observe bytes still in kernel pipe queues without a submitted read, future peer writes after cancellation, vendor callbacks, or a global callback frontier. It does not establish semantic validity of late frames, acknowledgement by the peer of sent frames, cross-process/cross-bitness behavior for this patch, release-build behavior, allocation-failure behavior, concurrent use of Endpoint, or other drivers. No new test configuration is justified by the current observations.

- delivery_state: built and checked, isolated candidate only
- outcome_state: passed for the named synthetic component acceptance surface
- highest_justified_claim: completion evidence survives local cancellation in the 16 named native cases; session cleanup no longer discards the tested late/leftover evidence
- required_runtime_observation: none for these bounded criteria; intended-use integration remains unobserved and requires a separately authorized later integration test
- who_controls_next_test: parent/user for integration scope; no additional native run needed for this candidate handoff
