# HTTP lock local candidate 23

- Branch: `review-ready/client-http-lock-local23`
- Commit: `283f6bffb9b5db76e4fd15bca922b8bedeedf8c8`
- Preserved base: `949451032647e45e42c3aaef3f41b132c8af36e3` (matches locally preserved origin/master and origin/HEAD; no fresh upstream fetch claim)
- Checkout: `/home/akilleez/Work/swg-source/client-http-candidate23`
- Production diff: 17 insertions in one header; full candidate adds a 3-file native test (318 total insertions, 4 files).
- No PR, push, reviewer assignment, labels, comments, integration-branch edits or VM workload outside this lock fixture.

## Native evidence

`results-v2/` is the authoritative final run. Windows VM, Python 3.12.10, MSVC 18.00.40629/v120. Command:

```powershell
& C:/ci-dpvs-review/python/python.exe C:/http-candidate23/source/tools/test-http-lock/run.py --out C:/http-candidate23/results-v2 --stock-header C:/http-candidate23/source/stock-VeCritsec.hpp
```

| Lane | Compile | Run | Wall seconds | Verdict |
|---|---:|---:|---:|---|
| Debug-Win32-candidate | 0 | 0 | 0.219 | expected outcome observed |
| Debug-Win32-stock | 0 | 0 | 0.203 | expected outcome observed |
| Debug-x64-candidate | 0 | 0 | 0.203 | expected outcome observed |
| Debug-x64-stock | 2 | None | — | expected outcome observed |
| Release-Win32-candidate | 0 | 0 | 0.172 | expected outcome observed |
| Release-Win32-stock | 0 | 0 | 0.172 | expected outcome observed |
| Release-x64-candidate | 0 | 0 | 0.141 | expected outcome observed |
| Release-x64-stock | 2 | None | — | expected outcome observed |
| Release-x64-broken-acquire | 0 | 1 | 0.047 | expected outcome observed |
| Release-x64-broken-release | 0 | 1 | 10.094 | expected outcome observed |

Six passing candidate/stock-Win32 processes each report 27/27 checks. Both stock-x64 compile logs contain C4235 at VeCritsec.hpp inline assembly. Broken-acquire exits 1 at `other thread excluded while nested`; broken-release exits 1 at `final unlock permits retry acquisition`. No outer subprocess timeout fired. PE machine values are 0x14c for Win32 and 0x8664 for x64.

The initial v1 run also met the runtime/control oracle, but its optional map output was absent because response-file `/link` and `/MAP` were on different lines. The runner was corrected to put all arguments on one line. The unchanged behavioral oracle was repeated in v2; no D9002 remains and each linked map exists with no production `yield_thread` symbol. v1 is retained as history, not represented as the final runner's evidence.

`pretest-manifest.json` and `pretest-manifest-v2.json` were written before their corresponding test executions. The final source hashes equal the v2 pretest manifest and native inputs. Raw logs, build response files, command scripts, source copies, binaries and maps are retained. Timings are observations only, not a benchmark.

## Scope and dependency boundary

The base lock header and VeCritsec.cpp are byte-identical to the integration parent before ff3c1742. The standalone header needs only real upstream FoundationTypes and Windows compiler/SDK facilities; those exact headers are in the source packet. No replacement uint32 definition, yield implementation, PCH shim, stock-source rewrite or allocation shim enters the fixture. Diagnostic acquire/release mutations affect disposable header copies only.

The upstream clientGame project defines Win32 configurations only. Its real VeCritsec.cpp includes FirstClientGame.h, which brings FirstSharedFoundation, _precompile.h and StringId.h plus the project's STLport/custom allocation environment. This candidate does not compile/link that translation unit or claim its scheduler behavior. TCPConnection.h calls production lock()/unlock(), so full HTTP/client use remains a broader integration acceptance surface.

The existing owner-thread/recursion fields are not converted to atomics. That preexisting portable C++ data-race concern remains a documented limitation; `/volatile:ms` observations are not a race-freedom proof. No fairness, non-Windows, ARM, full HTTP or completed-client claim follows.

## Handoff contract

- delivery_state: committed and built (header fixture), local only.
- outcome_state: passed for the predeclared native header-operation matrix.
- highest_justified_claim: actual candidate trylock/unlock compiled and passed the bounded recursion/exclusion/release/payload observations in native v120 Win32/x64 Debug/Release, with discriminating stock and broken controls.
- required_runtime_observation: none for this component matrix; production lock()/yield_thread, full HTTP flow and full client remain outside it.
- who_controls_next_test: parent agent controls blind review and any later integration tests.
