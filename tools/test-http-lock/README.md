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
with C4235 at the inline assembly. Each event wait is bounded to 10 seconds;
compiles and test processes have 120- and 45-second outer deadlines. Logs,
commands, source hashes, PE architecture, elapsed times and JSON verdicts remain
in the output directory. A nonzero runner exit means some expected result did
not occur.

This is a header-operation test, not a full client build or HTTP integration
test. It does not execute production `lock()`/`yield_thread()`, prove fairness,
or repair/prove the existing volatile recursive-owner bookkeeping free of data
races. Tests use the existing Microsoft `/volatile:ms` behavior; no portable
C++ memory-model or non-Windows claim is made.
