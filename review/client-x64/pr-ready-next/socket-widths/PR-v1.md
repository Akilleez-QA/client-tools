# Preserve Windows socket handles and completion keys at pointer width

The network headers declare SOCKET as a 32-bit integer and Sock stores it in int. On x64 that disagrees with Winsock's pointer-sized handle contract. Use uintptr_t in all three Windows declarations and SOCKET in the member. Keep socket operation status values unchanged.

TcpClient and TcpServer pass a 32-bit completion-key destination to GetQueuedCompletionStatus. Use ULONG_PTR at both sites; the transferred-byte count remains 32-bit.

Production diff: five files, nine added and six removed lines, in three focused commits. No platform configurations or unrelated network behavior changes.

## Validation

Existing native probes cover the actual headers in both include orders, Winsock UDP loopback, and IOCP keys with nonzero high bits. They do not execute the production Sock or TcpClient/TcpServer implementations. The later integration tree compiled the affected network library; this isolated master-based branch has not yet reproduced that build. Local test runners and raw results exist outside this candidate and must be packaged before submission.
