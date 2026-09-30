# Native network reproduction result

Observed on source head `1092728ace02e74b4a5c9887d9ad505d2d22421b`, native Windows 10.0.19045.6466, Visual Studio 2013 v120 `18.00.40629`, Windows SDK 8.1.

```powershell
C:/ci-dpvs-review/python/python.exe C:/pr-network18-v2-source/tools/test-windows-network-widths/run.py --checkout C:/pr-network18-v2-source --out C:/pr-network18-v2-all --revision 1092728ace02e74b4a5c9887d9ad505d2d22421b
```

Exit 0. Exactly 100 compiler cases accepted: 76 successful compiles and 24 expected negative-control failures. Exactly 60 raw Winsock/IOCP executions passed, with 21 assertions each (1,260 total). All 12 actual-TU compiles passed: Sock.cpp, TcpClient.cpp and TcpServer.cpp × Win32/x64 × Debug/Release. Each of the four x64 reverted-key controls emitted exactly one C2664 diagnostic at the actual GetQueuedCompletionStatus call. Each corresponding Win32 control compiled.

The complete matrix, raw logs and source binding are described in README.md. All 166 native-to-checkout source/header/test identity comparisons passed. identity.json records source and test SHA-256 values; included-files-sha256.json records 333 include identities. candidate-v2.tar.manifest.json records the exported snapshot. SHA256SUMS binds packet files.

This head is stacked on the explicit four-file imemmove prerequisite `9eadbbbebd515a0fffad2133300703dff68bd7ef`. That prerequisite requires its own review and merge. This packet establishes neither its approval nor complete validation of its changed callers. The original isolated network head `a393d1233aada331f99d4edb50f678e8c186fff2` failed actual x64 TU compilation in unchanged Misc.h/STLport; that exit-1 attempt is retained.

No production Sock/TcpClient/TcpServer runtime, complete sharedNetwork/client build, binary-provider compatibility, or game fidelity claim is made. Rebuild all corresponding x64 consumers and libraries because class layout/signatures change. The network source diff remains five files relative to its explicit prerequisite.

Terminal scope: delivery built; bounded outcome passed; highest justified claim is native actual-TU/type-check and raw Windows API behavior in this matrix; no further runtime observation is required for that narrow acceptance contract. Parent/user controls any broader workload. No production edits, commits, pushes, PRs, comments, or vendor-binary publication were performed by this worker.
