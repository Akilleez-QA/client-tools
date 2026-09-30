# Proposed object-only native gate (not run)

Two v120 amd64 objects, fresh `C:/native-file-callbacks35`, no link or execution, stop at first unexpected failure. Before approval, stage and hash these three authored source files, `file-executor29/ClientAudioFileCallbacks.h`, the frozen33 snapshot and `inputs/clientAudio-Debug-x64.audit.log`; preserve their relative paths under `seam/`. Record a new whole-input manifest and runner identity for review. This proposal is not authorization to stage or run a native compiler.

Use `C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat amd64`. Native SDK must be the actual private `snapshot/src/external/3rd/library/miles/include/Mss.h`, SHA-256 `966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e`. Do not generate SDK declarations or use substitute headers.

Forwarder command, from fresh `results/native` (resolve `cl.exe` from the captured environment):

```
cl.exe /nologo /c /W4 /WX /EHsc /MT /O2 /Y- /DWIN32 /D_WIN32_WINNT=0x0601 /showIncludes /I C:/native-file-callbacks35/snapshot/src/external/3rd/library/miles/include C:/native-file-callbacks35/seam/native-file-callbacks35/native_file_callbacks.cpp /FoC:/native-file-callbacks35/results/native/native_file_callbacks.obj
```

Engine header probe command is the exact frozen33 Debug/x64 engine compile recipe, with only the source/output and root replaced. Run from `snapshot/src/engine/client/library/clientAudio/build/win32`. Parse the `CL|` audit row whose second field ends `/Audio.cpp`; append `/D` for every semicolon-delimited field6 entry, then `/I` for every field7 entry, in order. Never rewrite relative engine include order or replace STLport. Flags before those definitions/includes are exactly:

```
/nologo /c /EHsc /Y- /Gm- /Zc:wchar_t- /Zc:forScope /GR /Gy /fp:precise /W4 /Zi /FC /showIncludes /FI<output>/require-v120.h /Fd<output>/engine_header_probe.pdb /MTd /Od /Ob1 /RTC1 /WX
```

The forced guard rejects `_MSC_VER != 1800` and non-`_WIN64`. Append the absolute `seam/native-file-callbacks35/engine_header_probe.cpp` and `/Fo<output>/engine_header_probe.obj`. The engine probe includes no Mss.h or modern adapter header; verify actual includes show original STLport and no MSVC C++ standard library headers. The forwarder includes Mss.h and MSVC `<type_traits>`, with no engine/STLport headers.

Retain exact expanded commands, raw logs, observed include paths/hashes, compiler identity and actual COFF machine (`0x8664`) for both objects. `dumpbin /symbols native_file_callbacks.obj` must show exactly one undefined Miles import, `__imp_AIL_set_file_callbacks`. Hash all staged sources/inputs before and after. Header hashes collected during compile alone must be described as single-time observations, not before/after attestations. Keep SDK snapshot, objects and PDB private. No retry, warning suppression, full Audio/ExitChain workload, DLL load or native execution.

Passing establishes these declarations, pointer assignments and engine header compatibility on Win64. It does not establish Win32 ABI (where calling conventions differ), linkage, runtime behavior, callback lifetime or worker routing.
