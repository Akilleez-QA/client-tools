# Exact proposed native object gate

Do not invoke before parent reviews source, driver and input manifest. Transfer the prepared `native-inputs` contents to a new `C:/file-executor31`; refuse any existing destination/results. The eventual single invocation is:

```powershell
& C:/ci-dpvs-review/python/python.exe C:/file-executor31/run-native.py
```

The driver verifies every manifest-pinned input before creating results. Compiler setup uses `C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat` with x86/amd64 and forces `_MSC_VER == 1800`. The environment is kept private, never logged. Working directory is `snapshot/src/engine/client/library/clientAudio/build/win32` to resolve inherited engine include paths.

For each Debug/Release × Win32/x64 combination, compile these exact private sources once:

| Unit | Source under VM root | Standard library |
|---|---|---|
| engine-worker | seam/file-executor31/EngineFileWorker.cpp | Original engine STLport4.5.3 |
| invocation-job | seam/file-executor31/FileInvocationJob.cpp | Native MSVC v120 STL |
| file-channel | seam/file-channel26/file_channel.cpp | Native MSVC v120 STL |
| canonical-services | seam/file-channel26/canonical_services.cpp | Native MSVC v120 STL |
| codec | seam/transport-candidate/codec.cpp | Native MSVC v120 STL |

Common flags: `/nologo /c /EHsc /Y- /Gm- /Zc:wchar_t- /Zc:forScope /GR /Gy /fp:precise /W4 /Zi /FC /showIncludes`, plus private `/FI` compiler guard, `/Fd` PDB and `/Fo` object destinations. Debug adds `/MTd /Od /Ob1 /RTC1 /WX`; Release adds `/MT /O2 /Ob1 /Oi /Ot /Oy /GF /WX-`.

All units receive the exact audited Audio.cpp `/D` set from `inputs/clientAudio-{Debug,Release}-{Win32,x64}.audit.log`. Win32 keeps `_USE_32BIT_TIME_T=1`; x64 does not. **Only engine-worker receives the audited engine `/I` list**, including STLport and existing x64 `C:/SDKs/DXSDK/Include` prefix. Modern adapter units receive no engine/STLport `/I` flags and no engine First header. Their quoted local includes resolve from their source directories; platform/compiler headers come from vcvars. The engine header crossing that boundary contains no STL or Windows types.

Inspect actual include traces: engine-worker must consume STLport and no file26/transport header; all modern units must consume no STLport or snapshot header. Record raw `command.json`, `compile.log`, `actual-includes.json`, source/compiler hashes, diagnostics, and actual object COFF machine (0x14c Win32, 0x8664 x64). Preserve the first failure and stop without repairs/retries. Correct objects do not establish SDK64 runtime compatibility or successful linkage.

File26's relative seam20 declaration header is pinned unchanged; those ordinary declarations match step29. This gate does not link canonicalServices to Audio, register callbacks, create an engine thread, install TLS, call TreeFile/Miles, run Audio/ExitChain or execute generated code. Final allocation/module ABI, owner/admission and lifecycle integration remain future work.
