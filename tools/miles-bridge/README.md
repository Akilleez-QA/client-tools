# Miles component development

This package contains the private paired-process Miles bridge and a direct native
facade. The default game retains direct Miles. Explicit `ClientMilesDevelopment=true`
selects the pipe facade for a development Debug-x64 game; the separate `audio-dev`
target remains a compile-only check. Native and pipe adapters implement the same public names; choose one,
never link both.

## Build prerequisites and commands

Run from this directory on native Windows with Python 3, Visual Studio 2013
(v120), and the genuine Miles SDK. No SDK headers, import libraries, DLLs or game
assets are bundled. Paths below are examples of existing local inputs.

```powershell
python build.py --target host --sdk C:/SDK/Miles/include --sdk-lib C:/SDK/Miles/lib/win/Mss32.lib --out C:/build/miles
python build.py --target pipe --sdk C:/SDK/Miles/include --out C:/build/miles
python build.py --target native --sdk C:/SDK/Miles/include --out C:/build/miles
python build.py --target engine-worker --engine-root C:/source/client-tools --out C:/build/miles
python build.py --target pipe-probe --sdk C:/SDK/Miles/include --engine-root C:/source/client-tools --out C:/build/miles
python build.py --target audio-dev --sdk C:/SDK/Miles/include --engine-root C:/source/client-tools --out C:/build/miles
```

`--vcvars` selects a VS2013 `vcvarsall.bat`. Each invocation creates a fresh
output directory under target/architecture and records commands, logs, failures
and artifact hashes in `receipt.json`. The script builds but does not run binaries.

| Target | Output and boundary |
| --- | --- |
| `host` | x86 executable linked with genuine `Mss32.lib`; runtime needs the matching original DLL/providers. |
| `pipe` | x64 client archive; archive creation does not resolve a complete application link. |
| `native` | x64 direct-call archive; linking requires a matching genuine native vendor library. |
| `engine-worker` | x64 archive using actual engine headers and legacy STLport settings. |
| `pipe-probe` | x64 probe linked with the pipe adapter, engine worker and genuine engine archives. |
| `audio-dev` | Real Audio object compiled with explicit `CLIENT_MILES_DEV_FACADE`; no game link. |

These component targets use the debug static CRT (`/MTd`); there is no Release
configuration switch here. Engine translation units retain the engine's STLport
and `wchar_t` settings, separately from modern component translation units.
Application CRT/configuration compatibility remains an integration prerequisite.

The three engine-dependent targets require an external maintained engine checkout
whose `clientAudio.vcxproj` contains explicit `Debug|x64` definitions and include
paths, with no unresolved MSBuild substitutions. Its include paths must contain
real `src/external/3rd/library/stlport453/stlport` headers. This package's inherited
project has only Win32 configurations; it does not supply that x64 conversion.

`pipe-probe` also requires Debug-x64 archives under `src/compile/x64/<name>/Debug`:
`sharedThread`, `sharedSynchronization`, `sharedFoundation`, `sharedMemoryManager`,
`sharedDebug`, `sharedMath`, `sharedRandom`, `unicode`, `sharedFile`,
`sharedCompression`, `fileInterface`, `archive`, and `zlib`, plus
`src/compile/deps/v120/x64/Debug/stlport.lib`. The runner records selected libraries
and copies their available compiler PDBs from `obj` directories for linking.

## Source and ownership boundaries

- `api/`: SDK-header-free public declarations, SDK-coupled native adapters and
  the pipe facade; selected nominal SDK handle types remain part of the contract.
- `host/`, `backend/`, `dispatch/`: process entry, resource resolution and genuine
  SDK calls. `wire/`, `protocol/`, `transport/`: explicit byte encoding and pipes.
- `admission/`, `file-*`, `host-runtime/`, `client-runtime/`, `eos/`: engine-worker
  admission, reverse callbacks, ownership and completion/consumption acknowledgments.
- `buffer/`, `image/`, `upload/`, `metadata/`, `version/`: bounded transfers,
  retained sample images, owned outputs and version queries.

`sources.json` lists the target translation units. Missing private includes must
not be bypassed by adding every source directory to the include path.

The command session belongs to its creating thread. SDK lock/unlock are counter
operations, not proof of callback quiescence. Nested locks retain their lease;
refusals leave depth unchanged, and causal callback acknowledgments must join
before command settlement. Background file callbacks remain serviceable. SDK
shutdown while locked is refused.

File and typed EOS callbacks share a reverse transport/request sequence. EOS runs
on the real engine worker with its TLS installed and waits for completion plus
consumption acknowledgment before native return. Callback-driven forward Miles
calls are refused before command mutation. Stable typed thunks support at most
64 distinct functions per callback type per session, for owned samples and
streams; borrowed-sample EOS is unsupported. Previous callback returns come from
the SDK, including its reset behavior. Retirement reasoning is specific to the
selected original DLL's inspected mutex-protected paths, not arbitrary versions.

Paired close requires SDK shutdown, an exact final reply, helper exit zero,
callback drain and engine/control-thread joins before client owner release.
Disconnect alone is not success. Uncertain roots remain retained on failure.
The host runtime and vendor module remain process-owned; paired stop does not
permit runtime destruction or synthetic DLL unload. The opt-in Audio bootstrap binds admitted callbacks and pairs shutdown while
retaining template/cache paths until their consumers are released.

## Portable checks and evidence

These commands use existing tests and real component logic, without a vendor SDK:

```sh
c++ -std=c++11 -Wall -Wextra -Werror tests/lock_admission.cpp src/admission/coordinator.cpp -o lock-admission
./lock-admission
c++ -std=c++11 -Wall -Wextra -Werror -fsanitize=address,undefined tests/eos_protocol.cpp src/eos/eos_protocol.cpp src/wire/codec.cpp -o eos-protocol
./eos-protocol
```

They cover admission state and EOS protocol validation, not SDK execution, worker
TLS, live transport or full-game behavior. **This package has no CI workflow.**
No build, test or runtime was rerun for this split package.

The [historical checkpoint README](https://github.com/Akilleez-QA/client-tools/blob/d1c5903de35586dc8cfb0939a5da1756cca43179/tools/miles-bridge/README.md)
preserves original commands, artifact identities, observations and failures,
including strict stderr failures and the corrected mixed file/EOS sequence bug.
Those integrated results apply to their recorded source/configuration snapshots;
they do not establish that this split branch builds standalone, enables game
audio, or proves callback fidelity, device behavior or heap safety.

## Opt-in game selection

The x64 property sheet imports `client-miles-dev.props` only when
`ClientMilesDevelopment=true`. It requires Debug|x64/v120 and explicit existing
`ClientMilesPipeLibrary` and `ClientMilesWorkerLibrary` archive paths. Build
clientAudio with the same property before SwgClient; its isolated archive path
prevents fallback to an old direct-Miles archive. Outputs are under
`src/compile/miles-dev/x64`; ordinary Win32/default selection is unchanged.

This source package is not the full client correctness/build closure. In
particular, obsolete browser/capture inputs and the other separately packaged
x64 source fixes must be composed before claiming a working full client build.
`link-client-dev.py` is a development relink tool using existing real libraries
and pinned build receipts, not a fresh whole-source rebuild or runtime qualifier.
Release selection and movie integration remain later packages.

The host is windowless; original module paths are normalized and compared as
absolute Windows paths. Forward traffic uses normal-size I/O segments. These
changes preserve diagnostics and terminal transport failure behavior.
Historical game-integration observations remain at the
[original checkpoint](https://github.com/Akilleez-QA/client-tools/blob/a68ceb4280ca59af5317f3ad5c6de8a3e0a87314/tools/miles-bridge/README.md),
not fresh acceptance of this split branch. No CI workflow is present here.
