# Server Windows network width package

[Fork draft PR #1](https://github.com/Akilleez-QA/src/pull/1) contains the networking changes above the combined prerequisites from submitted upstream helper PR #37 and workflow PR #38. Base `09932a32c9949bd40e8e4dbb22e1a7027944eb21`; head `9d44e3a1da7b96de41ff864c121dbc60d0c45c5e`. Six production files, +18/−6; four test/workflow files, +334. The displayed diff excludes both prerequisites. No upstream network PR has been opened.

The socket/key repairs retain full-width Windows handles and IOCP keys while keeping status and byte counts at their existing widths. A separate +9-line common-header fix selects Winsock 2 in the networking library before foundation can import Winsock 1.1. Root inspected this sequence against Microsoft's documented Windows/Winsock include convention. Linux, wire formats and LP64 PR #35 are outside these source edits.

[Windows compilation passed 20/20](hosted-36835813460/RESULTS.md) at the source/test head `7f5182d6`. Merging the already-qualified workflow prerequisite changed only compile-src.yml. The [exact submission head rerun](https://github.com/Akilleez-QA/src/actions/runs/36836351608) also passed 20/20; root checked all outcomes and matched all 7,929 tracked input hashes, allowing only Git Windows newline conversion. [Exact-head summary and raw logs](hosted-36836351608/RESULTS.md).

The [initial failed 4/20 run](hosted-36834837153/RESULTS.md) remains preserved. The subsequent header and classifier fixes are separate commits. These tests compile genuine Sock/TcpClient/TcpServer TUs and reverted-key controls using the server's CMake-derived settings and SDK. They do not link or run a Windows server, exercise traffic or verify IOCP lifecycle.

[PR description](PR.md), [GitHub submission receipt](submission.json). The earlier source-only receipt remains historical evidence for commit `43249ae0`.
