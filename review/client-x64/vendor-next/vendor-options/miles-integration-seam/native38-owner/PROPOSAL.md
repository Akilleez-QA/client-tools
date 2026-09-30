# Native38 owner object gate proposal; prepared locally only

Six v120 AMD64 Debug objects, in order: SessionFileOwner37, actual FileInvocationJob33, changed file26 adapter, changed codec, Coordinator34, host-context41. The TLS helper is compiled independently; it is not yet an integrated trusted mapper. The portable job and replacement allocator TUs are excluded. EngineFileWorker33 source/header are unchanged; reuse its prior compiler evidence and leave the real worker submit reference unresolved. No SDK header or engine STLport include is needed in these six modern-STL TUs.

Fresh proposed destination `C:/native38-owner`. Exact inputs are frozen in the19-entry private input manifest SHA256 `4647bf4ad00dcdc1e80c082ac454eeba491e2d459710726ec8b87659f2a007c4`. Runner SHA256 `0e9e60ef8af2b4308130d07999cf13f65bcfd535633591514ccd941d8898b95b`. Local preparation verified every frozen37 input and clean product49d0; actual job/worker header hashes equal33. Engine worker CPP SHA256 `2cbad198b35b98013ef5a2d92153566599776704ea033132ad21fbf3194e5216`; no recompile of that TU is proposed.

After root review and explicit authorization, stage the packet in the fresh destination, refuse existing output/active compiler, then invoke exactly once:

```
C:/ci-dpvs-review/python/python.exe C:/native38-owner/run-native.py --approved-compile-only
```

Environment comes from VS12.0 `vcvarsall.bat amd64`. Common exact flags are in private-inputs-v1/flags.json:

```
/nologo /c /EHsc /Y- /Gm- /Zc:wchar_t- /Zc:forScope /GR /Gy /fp:precise /W4 /Zi /FC /showIncludes /MTd /Od /Ob1 /RTC1 /WX /DWIN32 /D_DEBUG /D_MBCS /DDEBUG_LEVEL=2 /D_CRT_SECURE_NO_DEPRECATE=1 /D_LIB
```

Append `/FI<root>/require-v120.h`, unique `/Fd`, source and `/Fo` per TU. No `/I` overrides or vendor SDK input. Guard requires actual v120 and Win64. Each compile must exit0; `/WX` preserves warning failures. Stop first compile/header/COFF/import failure, retain logs and do not retry. Actual includes must exclude engine source, STLport, snapshots and Mss.h; MSVC C++/CRT and Windows SDK headers are expected. Each COFF machine must be0x8664. Dump symbols on each successful object: no AIL reference; owner must reference actual FileInvocationJob::enqueueAdmitted; job must reference actual EngineFileWorker::submit and canonicalServices. This deliberately leaves canonicalServices/engine operations unresolved, with no linked program or runtime claim.

Capture commands/raw logs/actual include paths+hashes/object hashes/symbol observations. Validate all staged input hashes before and after; system headers are single-time observations during compilation. Objects/PDB and raw possessed-header contents stay private. Curated proof can record the previously read type_traits hash and declaration location without republishing its text. No custom allocator execution, Audio/ExitChain workload, native DLL load, engine runtime or product adoption.

The canonicalServices binding is the current mechanism, not the final public callback-table design. Retaining and honoring the actual supplied public callback table is a separate source change. A passing object gate will establish compilation and dependency references only; it will not resolve trusted mapping, receiver scheduling, worker lifetime, callback fidelity or external termination proof.
