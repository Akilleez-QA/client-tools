# Prospective bounded candidate — 2026-09-30

POODO frame: parent assignment supplies unusually specific scope and acceptance, so redundant opening exchange is waived. “Drain” means operation storage is safe to release; “health” additionally requires acceptable completion errors, no untaken inbound bytes, and no incompletely transmitted outbound frame. Parent reports an evidence-loss bug; source inspection independently observes `collect` and `fault` discard results outside Open. No callback-quiescence/frontier claim is authorized. Only this directory and C:/pipe-drain23 may change; no product edit, vendor/audio/allocator fault/real-engine execution, commit, or push.

Evidence inspected: original endpoint.h/.cpp, fixture.cpp, and live-bridge-candidate/common.h (source snapshots and SHA256 manifest will identify inputs). The old fixture checks cancellation safety but not cancellation-time channel health. Its drainSession pre-pumps then cancels, and its ordered-close exception allows PeerClosed. Therefore retained leftovers must be checked independently of first failure.

Topology traversed: queued/issued/completed/collected reads and writes; Open/Faulted/Stopping/Closed; buffered header/body/ready frames; cancellation races; OS buffer lifetime; first fault versus additional traffic evidence; ordered peer closure; single-thread owner; two-channel session cleanup. Native OS ordering is observable with manual-reset events. Exact scheduler race frequency, drivers other than local named pipes, concurrent Endpoint callers, protocol callback quiescence, and vendor integration remain out of scope.

Research gate (retrieved 2026-09-30): queries `site:learn.microsoft.com CancelIoEx normal completion ERROR_OPERATION_ABORTED ERROR_NOT_FOUND` and `site:learn.microsoft.com GetOverlappedResult ERROR_IO_INCOMPLETE buffer cancellation ReadFile`. Inspected official CancelIoEx (updated 2021-01-07): https://learn.microsoft.com/en-us/windows/win32/fileio/cancelioex-func ; GetOverlappedResult (2022-09-23): https://learn.microsoft.com/en-us/windows/win32/api/ioapiset/nf-ioapiset-getoverlappedresult ; ReadFile and WriteFile: https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-readfile and https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-writefile . One specification family: cancel request is not completion; normal success, aborted, or another error remain possible; buffers/OVERLAPPED remain live until completion. Challenge source: Microsoft engineer investigation (2020-11-19) https://learn.microsoft.com/en-us/answers/questions/116109/cancelioex-spuriously-fails-with-error-not-found-w — ERROR_NOT_FOUND does not justify freeing uncollected operations. This separate reported investigation expands the cancellation race model but is not runtime evidence for our artifact. No conflict with endpoint buffer-lifetime rule. These sources do not prove application protocol success or callback quiescence. Research gate satisfied for this bounded decision.

20 distinct paths considered before convergence:
1. Preserve completion evidence in the existing endpoint owner.
2. Add session-only leftovers checks without changing collection (insufficient for lost late bytes).
3. Treat every cancellation as protocol failure (rejects normal idle cleanup).
4. Return protocol health from drain itself (conflates lifetime with health).
5. Continue reads/writes after stop to finish traffic (changes shutdown protocol; rejected).
6. Introduce a protocol shutdown acknowledgement (larger unproven protocol change).
7. Add a callback sequence frontier (invented semantics; excluded).
8. Replace transport with IOCP (large ownership rewrite).
9. Put I/O on a dedicated owner thread (concurrency redesign).
10. Replace named pipes with synchronous socket transport (dependency substitution).
11. Stop using cancellation and block until all traffic ends (unbounded shutdown).
12. Preserve first-failure status plus orthogonal unread/write evidence (selected combination).
13. Record an entire completion journal (more storage/API than needed).
14. Gate native events before collecting to create real completion races (selected experiment).
15. Interpose cancellation only to withhold its request for deterministic timeout (selected limited test adapter).
16. Native random stress repetitions (weak ordering oracle; defer).
17. Static proof/review only (cannot establish OS behavior).
18. Differential old/candidate replay with the same fixture and oracle (selected discriminator).
19. Retain existing code and document inability to certify drain health (fallback).
20. Ask Windows maintainers to resolve uncertain driver behavior (only if native observations contradict specification).

Decision: change copied endpoint to count unread bytes until takeFrame, preserve first non-benign completion failure in any state, collect successful write byte counts even while stopping, and treat ERROR_OPERATION_ABORTED as ordinary cleanup only after local stop/fault. Do not issue new I/O after stop. Copied common.h drains both channels before checking retained failure/leftovers; drain itself remains a storage-safety boolean. Old/candidate snapshots stay side-by-side. Strongest rival: completion count is sufficient but unread data is legitimate shutdown traffic. Discriminator: normal fully consumed framed exchange must pass; an additional frame or partial bytes must fail the explicitly scoped session-health oracle.

Prospective oracle v1, authored before implementation or native execution:
- Idle pending-read cancellation: cleanup succeeds, no channel failure, no unread/write evidence; session health accepted on both old/candidate.
- Valid framed request/reply, including small segments: exact bytes and codec decode unchanged; all consumed and sent; session health accepted.
- Late read: cancellation adapter writes 13 bytes and waits for native read event before forwarding CancelIoEx. OS success wins before endpoint collects. Old session accepts (negative control); candidate rejects with retained unread bytes. No timing-only sleeps.
- Late peer failure: cancellation adapter closes peer and waits for native read event before forwarding. Old session accepts; candidate rejects non-cancellation PeerClosed when ordered close is false.
- Buffered full/partial input: old session accepts untaken data; candidate rejects independently of PeerClosed allowance.
- Queued/unissued and backpressured pending output: old session accepts incomplete send; candidate rejects while cleanup succeeds. No assertion that peer saw zero prefix bytes.
- Completed pending write: peer reads and write event becomes signaled before cancellation/collection; candidate accounts full completion and does not falsely retain sendBusy.
- First meaningful fault: invalid length occurs before later peer I/O failure/cancellation; InvalidLength remains with original Windows error.
- External abort while Open: ERROR_OPERATION_ABORTED is a WindowsIo failure rather than ignored.
- Timeout: explicitly test-only cancellation-withholding adapter leaves real native read/write operations incomplete. drain(0) must return false, retain pending flags, handles and buffer/OVERLAPPED storage; releasing the adapter must permit cleanup. This tests endpoint timeout ownership, not slow Windows cancellation latency.

Build one VS2013 v120 amd64 Debug (/MTd /Od /W4 /WX) configuration; broaden only for concrete failure. Watchdog each run. Before run, freeze fixture/source identities. Failure retracts only the failed scoped claim; preserve raw logs before explanation. Stop on native hangs, ownership anomaly, unexpected source changes, or unavailable environment. Rollback is discard isolated candidate, never modify originals. Fanout checkpoints considered at frame/observe/orient/decide/run: this worker has no allocated descendant capacity; parent runs independent Grok static critique and another isolated task, so no further agents. Grok advice is advisory and source-correlated; omit its post-stop I/O and destructor-health changes.
