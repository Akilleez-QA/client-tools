# Callback composition 46 — review before first execution

This is a new portable composition gate. Existing 44/45 snapshots and product sources remain unchanged. No gate has run. Production dependencies are copied byte-for-byte from frozen selected-file-services44/candidate; mapper .h/.cpp are copied byte-for-byte from callback-control45/candidate. This carries native39's one-token nondependent-typename correction already present in44. Exact baseline/output SHA256 and transformation descriptions are in provenance-v1.json. The change from the selected composite baseline is in source.patch.

The production path under review is selected native-shaped callback pointers → real44 retain → const FileSessionContext services → real45 HostAssociationMapper → real owner → portable FileInvocationJob plumbing → real Invocation → selected adapter → supplied test callback. The actual Windows FileInvocationJob.cpp is retained unchanged from44 for later native compilation; it is not compiled or replaced on disk. The gate links a separately named, explicitly portable worker/job translation unit instead.

The portable plumbing change only accepts/forwards the provided FileServices. It no longer constructs an implicit canonical/Script36 table. Native-shaped fixture A wraps existing Script36 callback counters; fixture B uses distinct functions/counters, returns a different status, validates a local handle above UINT32_MAX, produces different read bytes and signed seek output. Both are passed through real retain. No global/TLS active-table selector, scheduler, production authentication, registration transaction, or pipe loop is introduced. Ordinary-only action restriction is unchanged.

## Initial frozen gate

Reuse the 11 meaningful45 scenario groups against the selected-service path: both return/ACK orders; unsolicited during a command and idle; causal/session/lane/lease rejection; unsupported lock actions; reverse replay; invalid/duplicate ACK; uncertain dispatch; capacity refusal; malformed frame. Add:

- Two sessions/tables using the same wire request numbers independently, interleaved open/read/seek/close, exact A/B statuses and bytes, high local B handle checks, and callback lifetime retained before/after ACK until session ownership ends.
- A selected callback exception with no fabricated reply; callback table remains retained after external references are dropped, forward settlement is blocked, and rejected ACK cannot release it.
- Multiple causal callbacks with ACKs out of order, plus a second causal arrival while ReturnedWaiting.
- Wrong-session, wrong-wire, duplicate forward-return observations cannot release request or callback pins.
- Valid mapper envelopes rejected by owner for unknown close target or invalid open fields: terminal failure, no file call, retained mapper row. Later fresh requests remain FailedUnanswered and cannot execute engine callbacks. Retaining the failed row is intentional; no rollback/recovery API is assumed.
- Zero-callback forward settlement, duplicate reply-queue observation, and post-Settled causal refusal.

Freeze all candidate, test, compatibility, runner, manifest and plan inputs before a single strict C++11 ASan/UBSan/leak-detection build/run. Do not execute until parent source review. The runner refuses to overwrite an evidence directory, preserves first failures, and verifies frozen inputs before building. No silent retry or in-place repair follows a failed gate.

## Scope and limitations

The compatibility wrapper is copied unchanged from44: system stdint first, temporary Windows/MSVC/empty calling-convention macros scoped around the exact native35 header, then undef before standard C++ headers. This gives no MSVC/x86 ABI evidence. Test callback functions use the resulting portable types only.

Real owner/mapper code runs, but worker/job scheduling is scripted. Its pending queue uses weak job references and does not establish the actual Windows queue ownership or event publication contract. Destruction in these fake-file tests is not proof of legal production cleanup; uncertain real files must remain owned through the eventual explicit failure protocol. Lifetime observations prove retained shared ownership in this composition, not vendor quiescence. This gate has no real EngineFileWorker, TLS, allocator workload, Endpoint, native DLL, VM, or product runtime. Native41's existing five-object result and reused native39 owner result do not compile44's changed job/owner/services path; that native work remains separate. No native64 API library exists or is implied.
