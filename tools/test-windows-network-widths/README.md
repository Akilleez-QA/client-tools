# Windows network width checks

Run from a native Windows checkout with Python 3 and Visual Studio 2013 (v120, including the x64 compiler and Windows SDK):

```powershell
python tools/test-windows-network-widths/run.py --checkout . --out C:/network-widths-results-1 --revision (git rev-parse HEAD)
```

The output directory must not exist. If Visual Studio is installed elsewhere, pass `--vcvars 'D:/VS12/VC/vcvarsall.bat'`. The reported revision is a label; SHA-256 hashes bind the actual source, project, test, and included-header bytes. `identity.json`, `included-files-sha256.json`, per-case commands/logs and `summary.json` are the reproduction record. The command exits nonzero for any unexpected compilation, runtime, count, architecture, or control outcome. Failed runs remain intact. The Windows compiler output must use English `Note: including file:` lines for the complete include-file manifest.

The default matrix contains 100 compiler cases:

- 40 candidate header cases: x86/x64, Debug/Release, both Winsock include orders, and five combinations of Sock and the two UDP headers. Each successful executable performs exactly 21 assertions (UDP loopback, two IOCP keys including nonzero high x64 bits, and count assertion).
- 40 reverted-header cases: the three typedef/member edits are reversed in private output copies. Twenty Win32 cases compile and run 21 assertions each. Twenty x64 cases must fail on the header type/layout checks. UDP copies are tested separately because they define the same library classes.
- 12 actual production TU compiles: Sock.cpp, TcpClient.cpp and TcpServer.cpp in the four architecture/configuration combinations. These use the real repository headers and source without a PCH or replacement declarations.
- Eight full-TU key controls: each TCP source is copied and only its completionKey declaration reverted. Four Win32 controls compile; four x64 controls must fail with C2664 at the real GetQueuedCompletionStatus API's PULONG_PTR parameter, and their corresponding unchanged TU must compile successfully.

Expected total: 100 accepted compiler outcomes, 60 successful runtime executions, 1,260 runtime assertions. `--only headers` and `--only implementation` isolate the 80-case or 20-case subsets for diagnosis; they cannot establish the omitted surface.

The implementation compiler inputs are derived from the checkout's sharedNetwork.vcxproj Win32 Debug/Release include directories and definitions. The bounded x64 adaptation removes `_USE_32BIT_TIME_T=1`; no x64 project configuration is added. Debug uses `/MTd /Od /RTC1`, Release `/MT /O2`; both use `/EHsc /W4 /Zc:wchar_t- /GR /Gy`. Compiler commands and native COFF machine values are recorded. The project contains a stale sharedMemoryBlockManager include-directory entry; it is passed unchanged to cl, which diagnoses any genuinely missing required header.

A clean original master-based network patch is insufficient for these real x64 TUs: Misc.h's global int-length memmove overload conflicts with the CRT size_t overload and causes C2668, including in STLport. Apply the separate four-file `imemmove` prerequisite awaiting its own review as an explicit preceding branch/commit; this runner never applies it or substitutes headers. Hashes of all four prerequisite files are included in `identity.json`.

The raw API runtime checks do not instantiate Sock or execute TcpClient/TcpServer. Real allocated socket handles need not have high bits set; header layout assertions detect narrowing. The completion-key controls are compile-only evidence bound to each actual TCP implementation. This is not a production network workload, complete sharedNetwork library build, client link, or fidelity result.

Widening Sock::handle and the UDP socket members changes x64 class layout and affected signatures. Rebuild the corresponding x64 libraries and consumers consistently; these checks do not qualify prebuilt binary providers.

Hosted Windows CI passes `--modern-msvc` and an explicit vswhere-discovered `--vcvars` path. Without that opt-in the runner still requires v120 (18.00); the opt-in requires MSVC 19.x. Actual compiler versions and raw toolchain logs are recorded separately. Both modes set `VSLANG=1033` because include tracing and negative diagnostics use English text. Negative controls require every error to match the expected source, location and SOCKET-layout or completion-key cause, and require their paired positive case to pass. Run `python tools/test-windows-network-widths/test_diagnostics.py` for rejection checks. Hosted results do not replace historical VS2013 evidence.
