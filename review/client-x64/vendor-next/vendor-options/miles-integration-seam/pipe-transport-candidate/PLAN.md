# Private byte-frame pipe transport: prospective plan

Awaiting parent acknowledgment before implementation. Scope is a reusable preconnected Windows endpoint plus private native x64-controller/x86-child fixture. No original vendor DLL, game/product code, RPC exports, scheduler policy or new protocol fields.

## Component API proposal

`Endpoint(HANDLE connectedOverlappedPipe, size_t segmentLimit)` takes ownership of a noninheritable, byte-mode, already-connected duplex pipe handle. Copy/move disabled. Construction must handle event-allocation failure without leaking the adopted handle. The segment limit bounds each requested ReadFile/WriteFile and permits deterministic fragmentation tests; production default is the existing frame cap.

- `send(Bytes)` copies one complete bounded frame into owned storage; refuses a second send while active. Validate supplied length and existing header length field agree; semantic opcode validation remains existing codec's responsibility.
- `pump()` does bounded nonblocking progress for both directions using GetOverlappedResult(FALSE). No vendor/game callback is invoked. An endpoint exposes read/write event handles for a caller reactor, but never waits while holding a global lock. A small fixed completion budget prevents one channel monopolizing the reactor.
- `takeFrame(vector&)` returns exactly one fully assembled frame. No new read starts while a ready frame is unconsumed, giving explicit bounded receive backpressure. Returned bytes are validated by the existing codec.
- `state()/error()/pending()/sendBusy()/bodyCapacity()` provide evidence and caller status without pretending success on disconnect, cancellation or invalid frame.
- `cancel()` transitions away from admissions and uses CancelIoEx for actual pending read/write operations. Already-completed operations are harvested too; ERROR_NOT_FOUND is not evidence a pending buffer may be released.
- `drain(deadlineMs)` waits only up to caller bound for pending completions and harvests every operation, including ERROR_OPERATION_ABORTED, before closing its handles or releasing I/O storage. Timeout leaves endpoint and buffers intact; caller must retain them and continue drain or terminate the owning process. Destructor fallback must cancel and wait for completion before member destruction; this may block, so normal usage must explicitly drain and the fixture has a process watchdog. No forced free-on-timeout path.

Names/signatures may be tightened after review without changing this contract. No transparent reconnect/replay.

## Frame and lifetime invariants

Read the existing48-byte header into fixed storage. Decode its uint32 little-endian bytes field at offset12 manually, never by native packed-struct cast. Reject sizes below48 or above1048576 before allocating body storage. Request only remaining header/body bytes, so coalesced stream data cannot be consumed past a frame. Preserve partial state across IO_PENDING. A zero-byte read/disconnect is failure, not a successful empty frame. Bad magic/version/kind/opcode are additionally rejected by the existing codec; framing bounds are not semantic acceptance.

Read and write have distinct stable OVERLAPPED/event/buffer state. A pending operation's vector is never resized, swapped, destroyed or reused until completion is observed. At most one reader and one writer per channel; one queued send and one completed receive. Total candidate storage is bounded by frame cap plus fixed metadata and vector overhead. Cancellation and peer-close outcomes do not count as frame delivery.

## Private fixture and namespace

Two per-run unpredictable named-pipe names, local machine only, one instance each. Explicit current-user SID ACL; noninheritable pipe/event/process handles. Controller launches an exact private Win32 child executable and passes only these names/test mode. Child opens pipes normally; no anonymous inheritable handle routing. Reject remote clients when platform supports the required flag; fixture requires modern local Windows. The component begins after connection and does not implement production authentication, launched-process verification, version handshake or incarnation binding. Same-user processes may still connect before the expected child; record this limitation instead of claiming names/ACL are authentication.

Use private `C:/miles-pipe-transport-v1` only, no Q/R mappings or active product tree modifications. v120 builds both endpoint configurations; fixture executes actual x64 controller against actual x86 child. Preserve source identities, command lines, result JSON and raw logs; no binaries or private SDK headers published.

## Prospective cases

1. Encode a real existing codec Call and Result, exchange both directions, decode and compare all fields/payload; no invented Hello/payload schema.
2. Limit endpoint segments to small values across header/body boundaries; log completion/byte counts and exact frame equality.
3. Send a48-byte header declaring47 or1048577; prove endpoint rejects before body allocation and never invokes codec/consumer as if a valid frame arrived.
4. Peer closes after a partial header and separately a partial body; frame remains undelivered, disconnect explicit, pending writes/reads drained.
5. Fill command pipe using bounded frame sends while peer deliberately leaves command reads idle. Confirm a command write is pending, then exchange an existing codec reverse request/reply over the other channel before command traffic is resumed. This is actual OS backpressure/progress, not a simulated vendor callback or game-affinity test.
6. Cancel an idle pending read and a backpressured write; observe cancellation completion before buffers go away. Bounded outer watchdog terminates only the fixture child if progress fails; no leaked running process or physical audio/device activity.

Tests advance the independent `backpressure_both_channels` oracle's OS transport part only. They do not establish media fidelity, callback scheduling, queue fairness beyond the fixture reactor, vendor quiescence or full coordinator integration.
