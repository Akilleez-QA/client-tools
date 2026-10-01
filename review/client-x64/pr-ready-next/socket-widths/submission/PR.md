# Preserve Windows socket handles and IOCP keys at pointer width

Three local Windows `SOCKET` declarations and `Sock::handle` use 32-bit integers on x64. Both TCP completion loops also pass a 32-bit output address to `GetQueuedCompletionStatus`, which writes a pointer-width key. Use `uintptr_t`/`SOCKET` for handles and `ULONG_PTR` for completion keys. Byte counts and operation-result types remain unchanged.

Five production files change (+9/−6), in three source commits; tests and CI are separate. This draft is based on `review-ready/client-imemmove` at `a7954b5e7`, the prerequisite submitted as [upstream PR25](https://github.com/SWG-Source/client-tools/pull/25). Its displayed diff contains only the network package. Rebuild affected x64 libraries and consumers together because their layouts/signatures change.

Validation:

- Recorded VS2013 checks cover all 12 real Sock/TcpClient/TcpServer TU compilations across Win32/x64 Debug/Release, high-bit completion keys, both Winsock include orders, and reversed-width controls. Production and API-probe bytes are unchanged.
- [Hosted header/API CI](https://github.com/Akilleez-QA/client-tools/actions/runs/36832580060) passes 80/80 expected compiler outcomes, 60 executions/1,260 assertions, and 45 classifier checks on `dbcd4d7d9`.
- Hosted CI deliberately covers headers/APIs only. Legacy STLport expects VS2013 CRT headers absent from the modern toolchain; actual production-TU checks remain in the default 100-case v120 runner. The failed hosted full-matrix run and corrected diagnostic-classifier cases are retained in the [evidence packet](https://github.com/Akilleez-QA/client-tools/tree/140eb58dac199440cf3f3eb47e852a1fbe038163/review/client-x64/pr-ready-next/socket-widths/submission).

The native x64 TU check explicitly removes `_USE_32BIT_TIME_T` from genuine Win32 project settings; it adds no x64 project configuration. The runtime fixtures exercise Windows APIs, not production TCP lifecycle/traffic or a full library/client link. The [server source counterpart](https://github.com/Akilleez-QA/src/compare/1481143ca4f033ef979faff52a4d03bb8d636292...43249ae00b0599a4560191917256b9cbb259ce0f) requires its own Windows qualification.
