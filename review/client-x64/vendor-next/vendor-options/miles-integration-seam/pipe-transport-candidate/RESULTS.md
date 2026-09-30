# Private pipe endpoint: native cross-architecture transport evidence

Current v5 compiles with native VS2013/v120 /W4 /WX on Win32 and x64, Debug and Release. An actual x64 controller launches actual Win32 children: **seven cases pass in each configuration**, each child exit0. PE machine IDs0x8664/0x14c and binary hashes are recorded; binaries are not in this packet. Exact input hashes and per-case summaries are under results. No vendor imports, media playback, product changes or new protocol fields.

| Case | Debug/Release observation |
|---|---|
| Existing codec call/reply | Exact bytes and real codec decode; controller reads2/writes1 |
| Fragmented header/body | Controller reads32/writes20, child reads46; exact codec bytes preserved |
| Declared frame47 | Rejected before body allocation; child capacity0 |
| Declared frame1048577 | Rejected before body allocation; child capacity0 |
| Close after13 header bytes | PeerClosed; no completed frame delivered |
| Close after60 total bytes | Partial body PeerClosed; no completed frame delivered |
| Command backpressure + reverse progress | 524288-byte payload write stays pending while reverse request/reply completes; child never reads command; pending read/write then explicitly canceled and drained |

The reverse exchange uses existing codec Request/Result layouts; its chosen return bits are synthetic transport fixture data, never presented as a vendor result. There is no SDK invocation. This advances the OS-transport part of `backpressure_both_channels`, not game callback affinity or media fidelity.

## Pending-storage contract

Separate stable read/write OVERLAPPED, manual-reset events and owned buffers. pump bounds its work and does not hold a shared mutex. At most one write frame and one completed read frame are retained. Header length is decoded manually little-endian before body resize; allocations cap at the existing1MiB frame limit. The original output vector is released during takeFrame rather than retaining arbitrary caller capacity.

CancelIoEx only requests cancellation: ERROR_NOT_FOUND is treated as a completion race, and GetOverlappedResult still harvests the operation. Explicit drain timeout leaves buffers/object alive. Destructor fallback waits for completion; if an OS wait fails and completion cannot be established, it terminates rather than freeing pending storage. Normal tested paths all use successful bounded drain. This fail-stop branch and allocation-failure branch are source-reviewed, not fault-injected. Allocation failure marks a distinct Storage fault, cancels other pending I/O and rethrows, preventing a later pump from using absent body storage.

## Fixture isolation and limits

Random128-bit names under local `\\.\pipe\swg-media-private-*`, one instance, current-user-only explicit DACL, PIPE_REJECT_REMOTE_CLIENTS, noninheritable handles, exact child executable path and CreateProcess inheritFALSE. A private kill-on-job-close job cleans up child processes if the controller is killed by its outer90-second watchdog. Per-operation watchdogs are10seconds, drain3seconds, child-exit15seconds. These are test failure bounds, not latency measurements. No observation timeout is silently retried with reconstructed endpoints.

Current-user access is not peer authentication: another same-user process/session could race to connect. Production launched-process/channel binding, incarnation handshake and authorization are absent. Endpoint is preconnected and assumes correctly owned overlapped byte-mode handles. No reconnect, replay, complete session coordinator, semantic opcode admission, vendor callback contract or production failure UX is established. Only x64-controller→x86-child topology is executed; both endpoints exchange bytes in both directions.

## Preserved iterations

v1 stopped on fixture sprintf deprecation under /WX; bounded hex encoding replaced it. v2 passed but concurrent stdout interleaved; v3 separates child logs and clears transferred storage. v4 adds destructor/allocation exception handling. v5 distinguishes Storage failure from genuine Windows errors. All raw logs and input archives remain preserved. Current evidence is v5, not an aggregate pass count across revisions.

Primary documentation checked2026-09-30: [CancelIoEx](https://learn.microsoft.com/en-us/windows/win32/api/ioapiset/nf-ioapiset-cancelioex) requires waiting for operation completion before releasing OVERLAPPED storage; cancellation can race normal completion. [ReadFile](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-readfile) requires live buffers until completion. [Named-pipe security](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-security-and-access-rights) explains explicit DACL access and the distinction between user SID and logon/session isolation. The fixture uses user SID, so it makes no stronger session-authentication claim.
