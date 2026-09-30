# Bounded compile plan and results

Completed on 2026-09-30, in this candidate directory:

```sh
i686-w64-mingw32-g++ -std=c++11 -Wall -Wextra -Werror -pedantic -fsyntax-only compile_types.cpp
x86_64-w64-mingw32-g++ -std=c++11 -Wall -Wextra -Werror -pedantic -fsyntax-only compile_types.cpp
g++ -std=c++11 -Wall -Wextra -Werror -pedantic -fsyntax-only compile_types.cpp
```

All three returned exit status 0 with no diagnostics. This compiles only the
new SDK-independent header, standard type traits/limits, and type assertions.
There are no callback definitions, vendor headers, engine headers, allocations,
entry point, linked library, executable, or runtime invocation in this probe.
Checks establish API signatures, fixed signed/unsigned widths, pointer-sized
local handle storage, no implicit bool/pointer handle conversion, and the
ability to represent open success with a zero handle. They do not establish
SDK ABI agreement or functioning file I/O.

Read-only patch check, run from the pinned product checkout:

```sh
git apply --check /home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/reverse-file-seam20/Audio-file-callbacks.patch
git diff --exit-code -- src/engine/client/library/clientAudio/src/win32/Audio.cpp
git rev-parse HEAD
```

All returned exit status 0. HEAD remains
`49d0eeed4ddaa177d7a93ea396c37c3d9b9942da`. The patch was generated from bytes
matched against that commit, inserts one include and the adapter block, and adds
the two header paths. The four original callbacks are unchanged. No patch was
applied and no product source was edited.

## Native full-translation-unit gate, completed

The user's existing authorization for native source work covers this compile
gate; no additional permission was required. On 2026-09-30 the full baseline
and candidate Audio.cpp each compiled with genuine Windows Visual C++ 2013
v120, `_MSC_FULL_VER=180040629`, using `/c` only:

| Configuration | Current 49d0 baseline | Patched candidate | Diagnostics |
|---|---:|---:|---|
| Win32 Debug | exit 0, x86 COFF | exit 0, x86 COFF | none |
| Win32 Release | exit 0, x86 COFF | exit 0, x86 COFF | none |
| x64 Debug | exit 0, AMD64 COFF | exit 0, AMD64 COFF | none |
| x64 Release | exit 0, AMD64 COFF | exit 0, AMD64 COFF | none |

No candidate source correction was needed. The exact reviewed patch and header
remain unchanged. Candidate objects contain all four decorated namespace symbol
prefixes (`open`, `close`, `seek`, `read`); their machine fields are `0x14c` on
Win32 and `0x8664` on x64. This compiles the adapter's width/origin assertions and
its direct calls to the actual original static callbacks in the complete TU.

The disposable VM root is `C:/file-seam21`. The local evidence directory is
[`native-v120`](native-v120/). Only that VM root was written. The product
checkout, `C:/client-next-build`, and other workers' paths were not changed.
Each configuration/mode has a separate object and PDB directory under
`C:/file-seam21/results`; objects/PDBs remain there and were not executed.

### Exact source and configuration

- Product commit: `49d0eeed4ddaa177d7a93ea396c37c3d9b9942da`.
- Baseline full Audio.cpp SHA-256:
  `c729174ada8104331702422879ecbfa4986a6c4bba49bc3d763ab62a2e401406`.
- Candidate full Audio.cpp SHA-256:
  `e99b66dffd1224766b46d3ba7d64a9cc2a13b4595e7c28271322764c3bdb7563`.
- A disposable snapshot contains current tracked engine/library source and
  include files. The unapplied patch was applied only to a separate candidate
  copy inside that snapshot's staging area. The VM checked all 9,538 input
  hashes before compiling; [input-manifest.json](native-v120/input-manifest.json)
  records the source, candidate headers, audit settings, and compile script.
- Audited define sets and include order were checked against the current
  `clientAudio.vcxproj`, including the existing x64 DXSDK include prefix from
  `tools/configure-client-x64/client-x64.props`. The exact properties and check
  results are in
  [configuration-verification.json](native-v120/configuration-verification.json).
  Win32 retains `_USE_32BIT_TIME_T=1`; x64 does not define it. Debug retains
  `DEBUG_LEVEL=2` and `_DEBUG`; Release retains `DEBUG_LEVEL=0` and `NDEBUG`.
- Common flags: `/c /EHsc /Y- /Gm- /Zc:wchar_t- /Zc:forScope /GR /Gy
  /fp:precise /W4 /Zi /FC /showIncludes`, plus the exact audited `/D` and `/I`
  settings, a forced `_MSC_VER==1800` guard, and private `/Fo`/`/Fd` destinations.
  Debug uses `/MTd /Od /Ob1 /RTC1 /WX`; Release uses
  `/MT /O2 /Ob1 /Oi /Ot /Oy /GF /WX-`, matching the project's configuration
  distinctions. `/Y-` and `/Gm-` deliberately remove shared PCH/incremental-build
  state for independent full-source compilation. The candidate's public header
  overlay is added before the original project include directories.

The native compile invocation was:

```powershell
& C:/ci-dpvs-review/python/python.exe C:/file-seam21/run-native.py
```

[`run-native.py`](native-v120/run-native.py) invokes only `vcvarsall.bat` and
`cl.exe /c` for compilation. It does not call a linker or generated executable.
Each of the eight subdirectories under
[`results`](native-v120/results/) preserves `command.json`, `compile.log`, and
`actual-includes.json` with the actual absolute compiler/header paths and hashes.
[`results.json`](native-v120/results/results.json) records compiler binary hash,
source hash, exact argv, working directory, exit status, diagnostics, object hash,
COFF machine, and candidate symbol-prefix checks. Environment values were kept
in memory and never saved or printed.

### Header identity and limits

Every baseline build consumed 370 unique files through `/showIncludes`: 245
pinned project/vendor headers, 124 native compiler/Windows SDK headers, and the
v120 guard. Each candidate consumed 372, adding exactly the two new adapter
headers. [include-verification.json](native-v120/include-verification.json)
records the comparison. All project/vendor header bytes match the pinned local
snapshot or the reviewed candidate header; all native toolchain/SDK header
hashes are recorded. None came from the shared `C:/client-next-build` checkout.
The actual Miles header remains SHA-256
`966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e`.

The current baseline has no compile failure in this matrix. Earlier stock x64
ABI-rejection and engine/allocator/teardown failures remain their original
separate evidence; this baseline is current 49d0, not the earlier stock source.
No runtime failure was reproduced, erased, relabeled, or claimed fixed.

**Test ceiling:** native object compilation of full source with real headers,
plus source/header identity and object inspection. No link, DLL load, callback
execution, TreeFile I/O test, engine startup/shutdown, allocator/vendor workload,
fault experiment, or fidelity measurement occurred. The thread/TLS,
serialization/reentry, lifecycle, byte-transfer and close contracts in README.md
remain unresolved. Native compilation closes the compiler-integration gap only.
