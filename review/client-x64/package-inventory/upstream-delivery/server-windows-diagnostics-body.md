Draft pending the existing [server CI repair (#38)](https://github.com/SWG-Source/src/pull/38). The source change applies independently to `master`; this PR does not duplicate that workflow repair. Master’s inherited workflow has a known clone/checkout failure and is not evidence about this candidate. No successful upstream CI run or complete Windows server build is claimed.

Use native-width Windows diagnostics and API results in the shared server code: read the x64 timestamp counter with `__rdtsc`, emit the fatal breakpoint with `__debugbreak`, print exception addresses with `%p`, pass thread-name exception arguments as `ULONG_PTR`, and retain the `ShellExecute` status as `INT_PTR` before comparing it with 32. The existing Win32 assembly paths and non-Windows breakpoint behavior remain unchanged.

Five source commits, four files, +21/−3, directly above upstream `master`. The source delta and blobs are identical to the reviewed fork draft; its CI-only prerequisite is excluded. No PR35 call-stack or directory-search changes, tests, SDKs, build metadata or binaries are added.

Historical evidence is component-specific. The [timer record](https://github.com/Akilleez-QA/src/commit/2a3b1463d7b0bf7db16f0fc84ecee92f1c32125d) describes four native v120 compilation configurations and a source-extracted timestamp helper probe. The packaged timer file matches the client counterpart byte-for-byte. The [breakpoint](https://github.com/Akilleez-QA/src/commit/b6967a0246227501aa14c6c562204afcbc59c159), [address formatting](https://github.com/Akilleez-QA/src/commit/e10e858ff3b431010a1715ce83ba4168c11d46af), and [ShellExecute](https://github.com/Akilleez-QA/src/commit/1b662b4df91ff72e3fed7f2337c1c3b6e71a43d6) records describe existing client or extracted-statement checks, not fresh server-package qualification. Thread naming has source/API-contract coverage only; no isolated runtime result is claimed.

Other complete server files differ from the client: `Fatal.cpp` retains server diagnostic/null-pointer conventions, `SetupSharedFoundation.cpp` lacks client minimum-frame-rate configuration, and `Os.cpp` has substantial server-specific initialization and browser behavior. These source differences prevent treating client TU results as an exact server build. In particular, master already contains `const char *lastSection.clear();` in the Windows menu path; that unrelated syntax defect is retained and prevents claiming this package alone makes the Windows TU buildable.

No new builds or runtime checks were performed during packaging. Full profiler calibration, crash-report lifecycle, browser launch and complete Windows x64 server support are not established by these changes.

[Review packet and exact source identities](https://github.com/Akilleez-QA/client-tools/blob/de951450e45a8caf37cf3b8cea691aad36c75e54/review/client-x64/pr-ready-next/server-windows-diagnostics/RESULTS.md).


Upstream review identity: base `7d2159a337281184d6a55db30d2bc9a4013c0e80`, head `32de00ef89329be87388b8cb4808682206061ac9`. Removing the CI-only prerequisite changed no production blobs or source hunks.
