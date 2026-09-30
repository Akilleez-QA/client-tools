# Preserve Windows socket handles and IOCP keys at pointer width

Windows x64 defines socket handles and IOCP completion keys at pointer width. The network headers used 32-bit SOCKET aliases and Sock stored its handle in int; TcpClient and TcpServer also supplied 32-bit completion-key destinations to GetQueuedCompletionStatus. Use uintptr_t for all three Windows SOCKET declarations, SOCKET for Sock's member, and ULONG_PTR for both completion-key outputs. Socket operation results and transferred-byte counts remain 32-bit.

This PR is stacked on the separate four-file `imemmove` prerequisite awaiting its own review (`9eadbbbebd515a0fffad2133300703dff68bd7ef`). Without that prerequisite, the actual network TUs fail x64 compilation in unchanged Misc.h and STLport with C2668. Merge/review that prerequisite separately; the network diff against it remains five production files.

Reproduction is included in `tools/test-windows-network-widths`. It derives implementation include paths and definitions from the checkout's project, uses real headers without PCH/stubs, records source/header/compiler identity, preserves all raw logs, and fails the overall command on unexpected outcomes. The source-level x64 checks remove Win32's `_USE_32BIT_TIME_T` definition; they do not add an x64 project configuration.

Native v120 result for source head `1092728ace02e74b4a5c9887d9ad505d2d22421b`: all 100 expected compiler outcomes accepted, 60 raw API executions and 1,260 assertions passed. All three actual TUs compile in Win32/x64 Debug/Release. Independently reverting each TCP completion-key declaration produces the expected x64 C2664/PULONG_PTR diagnostic while Win32 still compiles. Source/header binding passed 166 checks against the exact checkout; raw commands, logs, source manifests and original failed attempts are in the revision-2 evidence packet.

The probe runtime uses raw Winsock UDP loopback and IOCP, including a key with nonzero high x64 bits. It does not execute production Sock/TcpClient/TcpServer methods. Actual TU compiles and independent key-reversion controls establish the narrow implementation type check. This is not a full library/client build or product fidelity claim.

The header changes affect x64 class layout and signatures. Rebuild corresponding libraries and consumers consistently; this test does not qualify existing binary providers.

Final review head: `23849687c697520d8934049efc49f62e44fd9b6a`; production remains `1092728a`. The committed runner/probe bytes match the recorded native inputs.

[Native evidence, commands and independent review packet](https://github.com/Akilleez-QA/client-tools/tree/review/client-x64-evidence/review/client-x64/pr-ready-next/socket-widths). Prepared on the working fork; upstream submission and final target branch remain subject to owner approval.
