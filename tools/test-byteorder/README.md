# Native ByteOrder check

Requires Windows, Python3 and MSVC 2013 or newer (both x86 and x64 compilers). The default toolchain remains VS2013/v120; pass `--vcvars` explicitly for another installation. This standalone check builds the checkout's actual ByteOrder.cpp and headers; it does not build the entire sharedFoundation library or client. It creates only the new output directory you name.

```bat
python tools/test-byteorder/run.py --out C:\temp\byteorder-check
```

Use `--vcvars C:\path\VC\vcvarsall.bat` if VS2013 is installed elsewhere. Each Win32/x64 Debug/Release program must report exactly 166,631 input cases, testing both byte-order directions. All 16-bit values and 100,000 generated 32-bit values plus boundary patterns use an independent byte oracle. Production symbol binding and object machine type must match. Commands, raw compiler/run output, source/header hashes and aggregate summary are saved. Unexpected build/run failures return nonzero.

To add baseline and mutation controls, save the original upstream ByteOrder.cpp byte-for-byte, then pass `--baseline C:\temp\original-ByteOrder.cpp`. For example Python's `subprocess.check_output(['git','show','949451032647e45e42c3aaef3f41b132c8af36e3:src/engine/shared/library/sharedFoundation/src/win32/ByteOrder.cpp'])` returns the original bytes. The baseline and copied no-swap mutant use the candidate's same headers. Expected controls: original Win32 passes; original x64 fails specifically on unsupported assembly; x64 no-swap mutant builds and fails the long-value oracle. These controls do not change the checkout. Ten matrix entries must satisfy their expected outcomes when controls are enabled; four otherwise.

The standalone link suppresses the unused legacy STLport default-library directive; no STL container implementation or engine allocator is replaced. The real headers remain intact. This check requires the common-header imemmove fix first: the original Misc.h memmove overload is independently ambiguous on x64. This branch is stacked on review-ready/client-imemmove. A missing prerequisite must fail compilation, not be hidden by a test header substitute.

No claim about packet serialization, full client startup, or gameplay follows from this function test.

The Windows-2022 workflow discovers its compiler with vswhere and passes the exact vcvarsall path. Hosted modern-MSVC results are separate from saved VS2013 evidence. Baseline failures must contain C2485 and C4235 and only the recorded assembly-body diagnostic code/location combinations; missing headers, tool/link failures and unrecognized diagnostic cascades fail the check. Raw logs remain available for inspection.
