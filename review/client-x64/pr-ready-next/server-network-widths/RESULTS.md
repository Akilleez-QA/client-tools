# Server Windows network width package

Fork branch `review-ready/server-network-widths` at `43249ae00b0599a4560191917256b9cbb259ce0f`, based on submitted helper PR37 `1481143ca4f033ef979faff52a4d03bb8d636292`. Three source-only commits, five files, +9/−6:

- `a4ea7a1923312cb8c1710578acd1a76669f85362`: Windows socket declarations and member storage.
- `48569551fb4633328b6deeb2c20512218d6c60ad`: TCP server completion-key output.
- `43249ae00b0599a4560191917256b9cbb259ce0f`: TCP client completion-key output.

The diff matches the three corresponding client fixes and omits unrelated integration-branch clock changes. Root and an independent source reviewer checked that `INVALID_SOCKET` remains the full-width handle sentinel, `SOCK_ERROR` remains an operation-result constant, completion keys use `ULONG_PTR`, and transferred-byte counts stay 32-bit. Shared `Sock.h` matches the client; other implementation files have pre-existing differences. Linux branches, wire formats and LP64 PR35 are outside this delta.

**Publication state: fork source branch; no upstream PR.** This exact server candidate has no Windows compile/runtime result. Client results support the API-width rationale but do not establish that these server TUs compile. The server uses CMake and has no client `sharedNetwork.vcxproj`; copying the client runner would be incorrect. The next qualification is a bounded compile of real server Sock/TcpClient/TcpServer TUs with their own public headers/build definitions, plus deliberate key-reversion controls. It does not require another full-game acceptance run.

The inherited server full-build workflow has a known clone-path defect addressed separately by upstream PR38. Opening this draft on the old workflow would produce a known unrelated CI failure; keep it as a fork review branch until the workflow/dependency and exact Windows qualification are reconciled. Existing published helper history is unchanged.

[Proposed description](PR.md), [exact source identities](source-receipt.json), [source diff](https://github.com/Akilleez-QA/src/compare/1481143ca4f033ef979faff52a4d03bb8d636292...43249ae00b0599a4560191917256b9cbb259ce0f).
