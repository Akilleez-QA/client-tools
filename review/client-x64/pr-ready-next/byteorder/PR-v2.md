# Use byte-swap intrinsics in the Windows x64 ByteOrder implementation

MSVC cannot compile the byte-order functions' x86 inline assembly for x64. Use the corresponding 16-bit and 32-bit intrinsics under `_M_X64`; preserve the Win32 assembly and public signatures.

This change is stacked on `review-ready/client-imemmove`, whose common-header repair is needed to compile the actual translation unit on x64. Relative to that prerequisite, the production change is 26 added lines in ByteOrder.cpp. The included test runner uses real repository headers without local build-metadata files or substitutes.

Native VS2013 Win32/x64 Debug/Release each passed 166,631 input cases in both directions on production 6bd1e1a2 and the recorded test-source hashes. Original Win32 passed against the same headers; original x64 failed on unsupported assembly; the no-swap mutation failed the independent oracle. All ten matrix outcomes matched their expectations. The exact commands, object/symbol binding, raw logs and source manifest are in the evidence packet. This is an actual-TU test, not a full library/client build.

Reproduce with `python tools/test-byteorder/run.py --out <new-directory>`; README documents the optional baseline/mutation controls and toolchain path. Every unexpected build/run result makes the command fail.

The initial master-only candidate passed Win32 but failed x64 in pre-existing Misc.h. That failed attempt is retained; the explicit prerequisite is what resolves that build dependency. No source from unrelated integration work is silently supplied.

[Native evidence, commands and independent review packet](https://github.com/Akilleez-QA/client-tools/tree/review/client-x64-evidence/review/client-x64/pr-ready-next/byteorder). Prepared on the working fork; upstream submission and final target branch remain subject to owner approval.
