# Native HTTP lock checks

Requires Windows, Visual Studio 2013 C++ x86/x64 tools, and Python 3.8 or newer.
From a normal command prompt:

```bat
python tools/test-http-lock/run.py --out C:/http-lock-results
```

The output directory must be new. `--checkout` selects another checkout;
`--vcvarsall` selects another VS2013 installation. To include the baseline
controls, export the upstream header and pass `--stock-header`:

```bat
git show 949451032647e45e42c3aaef3f41b132c8af36e3:src/engine/client/library/clientGame/src/shared/HTTPpost/VeCritsec.hpp > C:/stock-VeCritsec.hpp
python tools/test-http-lock/run.py --out C:/http-lock-controls --stock-header C:/stock-VeCritsec.hpp
```

The fixture compiles the checkout's real header and FoundationTypes in native
Win32/x64 Debug and Release modes. It checks recursion, competing-thread
exclusion through partial release, acquisition after final release, reuse, and
100000 coherent protected updates. Events order the competing attempts; elapsed
time is a deadlock limit, not a performance or exclusion oracle. The fixture's
retry loop uses `SwitchToThread` and intentionally does not call `lock()` or
substitute a definition of `yield_thread()`.

Diagnostic copies with acquisition or final release removed must fail the
specific exclusion or progress check. Stock Win32 must pass; stock x64 must fail
with the exact recorded v120 diagnostic cascade beginning with C4235 at
`VeCritsec.hpp(43)`. Paths, line numbers, messages, order and multiplicity must
match; unrelated or malformed errors/warnings are rejected. Native builds select
English diagnostics (`VSLANG=1033`). Each event wait is bounded to 10 seconds;
compiler wrappers and test processes use 120- and 45-second subprocess timeouts.
The compiler timeout does not guarantee cleanup of descendant compiler/linker
processes. Logs,
commands, source hashes, PE architecture, elapsed times and JSON verdicts remain
in the output directory. A nonzero runner exit means some expected result did
not occur.

This is a header-operation test, not a full client build or HTTP integration
test. It does not execute production `lock()`/`yield_thread()`, prove fairness,
or repair/prove the existing volatile recursive-owner bookkeeping free of data
races. Tests use the existing Microsoft `/volatile:ms` behavior; no portable
C++ memory-model or non-Windows claim is made.

## Portable classifier replay

```sh
python tools/test-http-lock/test_classifier.py
python tools/test-http-lock/test_classifier.py --recorded-results /path/to/http-lock23/results-v2
```

The first command checks the recorded diagnostic fixture and missing, duplicate,
wrong-path, wrong-line, malformed, unrelated-error and invalid-exit controls.
The second also replays the original Debug/Release stock x64 logs. This tests
classification only; it does not compile or execute the native lock fixture.

The diagnostic fixture is transcribed from the [published original logs](https://github.com/Akilleez-QA/client-tools/tree/09fc9dc5d6b1c7636f585778b793dd4143de3154/review/client-x64/pr-ready-next/http-lock23/results-v2).
The prior native results describe the header and probe in commit
`d788e64ced56832894ff77a7d0d5b30fbec1b2ce`, before this runner correction.
Both files remain byte-identical; the native matrix was not rerun for this
classifier-only change. The recorded 27 native checks per configuration are
separate from these portable classifier controls.
