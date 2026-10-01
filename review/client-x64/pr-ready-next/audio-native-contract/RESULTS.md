# Native Audio widths and diagnostic arguments

Base `949451032647e45e42c3aaef3f41b132c8af36e3`, candidate `0699bd3d9b08998cb731d6ac7655681f3d003e6d`: three source-only commits, one Audio.cpp, +28/−24. [Description and original evidence](PR.md) explain the callback handle contract, checked preference conversion and string/count diagnostics. [Source receipt](receipt.json) records exact original-line equivalence and current source identity.

Primary inspection and independent senior-engineer review found no introduced blocker or missing source dependency. Handle bookkeeping and callback registration use the SDK type end to end; read counts and seek offsets retain their existing types. Preference range checks preserve all representable int values. Diagnostic string storage remains alive throughout its full logging expression.

Historical native compilation/callback fixtures are integration-dependent, not a fresh master build. Debug x64 required the separate allocator correction; preference probes exercise SDK-type arithmetic rather than production Fatal/vendor returns. This package does not distribute an SDK, supply an x64 vendor runtime, activate a facade/pipe, or change TLS lifetime. No builds/runtime checks were repeated during packaging.

Submitted: [31](https://github.com/SWG-Source/client-tools/pull/31). The recorded source head, base and GitHub diff counts match the preflight.
