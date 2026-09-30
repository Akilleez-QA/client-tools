# Full Audio translation-unit compilation — prepared, not run

This recipe reuses `../reverse-file-seam20/native-v120/run-native.py` and its audited project settings. The new runner differs only in private root (`C:/file-executor29`) and diagnostic guard label (`SEAM29`). It compiles the complete original product Audio.cpp and this complete candidate Audio.cpp in Debug/Release × Win32/x64: eight object compilations. The seam20 compile result is not evidence that this candidate compiles.

After parent scope/source review, prepare local inputs:

```sh
python3 /home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/file-executor29/prepare-native.py
```

That script verifies all old staging manifest hashes, checks every retained snapshot file against the current pinned product checkout, verifies the new source manifest, then copies the existing engine/vendor snapshot and exact audited configuration inputs into a fresh `file-executor29/native-inputs`. It overlays the new candidate sources and runner and creates a new complete input manifest. It refuses an existing destination and invokes neither VM nor compiler. A hash mismatch must be investigated, not skipped.

After separate authorization to use the native compiler, transfer that directory's contents to a fresh `C:/file-executor29` in the established compile environment (never over an existing run). Invoke exactly:

```powershell
& C:/ci-dpvs-review/python/python.exe C:/file-executor29/run-native.py
```

The runner initializes genuine Visual Studio 2013 via `C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat`, selecting x86/amd64. It uses audited Audio.cpp define/include rows from `inputs/clientAudio-{Debug,Release}-{Win32,x64}.audit.log`, preserving Miles, STLport, and original project include order. The x64 DXSDK prefix is the audited `C:/SDKs/DXSDK/Include`. Compilation runs from `snapshot/src/engine/client/library/clientAudio/build/win32` so relative include paths resolve into the snapshot.

Common flags are `/c /EHsc /Y- /Gm- /Zc:wchar_t- /Zc:forScope /GR /Gy /fp:precise /W4 /Zi /FC /showIncludes`, with private `/Fo` and `/Fd` paths and a forced `_MSC_VER == 1800` guard. Debug adds `/MTd /Od /Ob1 /RTC1 /WX`; Release adds `/MT /O2 /Ob1 /Oi /Ot /Oy /GF /WX-`. Candidate public include overlay precedes audited includes. This is isolated full-TU compilation with PCH and incremental compilation disabled, not an MSBuild library build. Optimized|Win32 is outside this inherited matrix.

Collect `results/results.json`, each `command.json`, `compile.log`, and `actual-includes.json`. Require all eight exit codes zero, inspect actual diagnostics, verify source/header hashes against the new manifest, and check correct COFF machine. The inherited runner checks adapter name prefixes in object bytes, not parsed symbol definitions or consumer linking; do not overstate it. No executable, link, DLL invocation, original Audio/ExitChain teardown, worker, transport or runtime test is part of this recipe.

Current status: recipe and runner authored and syntax-parsed only; `prepare-native.py` and `run-native.py` have not been executed for step29.
