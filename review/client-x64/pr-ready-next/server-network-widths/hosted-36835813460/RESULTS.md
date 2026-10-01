# Server Windows networking compile matrix

[Hosted run 36835813460](https://github.com/Akilleez-QA/src/actions/runs/36835813460) passed **20/20** at `7f5182d61454df0b67ff66e6f9d7c6d5b35b73db`: twelve genuine Sock/TcpClient/TcpServer TU compilations, four Win32 key-reversion compilations, and four expected x64 reversion failures. Every x64 failure identifies the real GetQueuedCompletionStatus argument 3/PULONG_PTR C2664 at its actual call location. The 65 local runner checks passed too.

MSVC C++17 with genuine SDK and the server's own CMake include/flag selection was used. The runner explicitly omits _USE_32BIT_TIME_T only on x64, uses /EHsc, and disables PCH. Root inspected all case outcomes and matched all 7,929 tracked input hashes to the tested Git checkout, accounting only for Windows newline conversion. Input hashes also remained unchanged during the run.

The prior [failed 4/20 run](../hosted-36834837153/RESULTS.md) is preserved. Commit 3a07c8c5 selects Winsock 2 in the networking library's common header before legacy Winsock 1.1 can enter through foundation. Commit 7f5182d6 corrects the control's accepted source locations without accepting unrelated paths/API errors.

This is compile-only coverage of those three TUs. There was no link, socket traffic, IOCP lifecycle, full Windows server build or runtime execution. It does not establish the rest of the Windows server dependency closure. [Summary](summary.json), [case results](results.json), [compiler identity](toolchains.json), [raw text logs/commands/input hashes](text-evidence.zip).
