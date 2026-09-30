# Allow the HTTP lock header to compile for MSVC x64

The HTTP connection lock uses Win32 inline assembly, which MSVC rejects for x64 with C4235. Add an x64 path that acquires bit zero with `_interlockedbittestandset` and clears the lock word with `_InterlockedExchange` on final release. Use a Windows 32-bit `long` for the intrinsic operand; the tested lock layout remains 12 bytes with 4-byte alignment. Existing recursive ownership behavior and the Win32 assembly path are preserved.

The production change is confined to `VeCritsec.hpp`. A native VS2013 test compiles the real header and unchanged upstream FoundationTypes, checks public lock behavior, and includes deliberately broken acquire/release controls. Run it with `python tools/test-http-lock/run.py --out C:/new-results`; the accompanying README gives the stock-header control command.

Validation on native Windows, MSVC 18.00.40629/v120:

- Candidate Win32 and x64, Debug and Release: 27/27 checks in each configuration, including recursive exclusion, final release and 100000 coherent protected updates.
- Stock Win32 Debug/Release: 27/27; stock x64 Debug/Release: expected C4235 at inline assembly.
- x64 Release with acquisition removed: fails the competing-thread exclusion check. With final release removed: fails the transfer check at its 10-second bound.
- Native executable architecture checked against each target; final runner logs retain commands, inputs, timings and source hashes.

This change is based directly on preserved master `949451032647e45e42c3aaef3f41b132c8af36e3`. Both the original lock header and `VeCritsec.cpp` match the integration parent before `ff3c1742fe5e02b1a84b59afb72867a889776dcf`; no integration prerequisite is included.

The test covers actual `trylock()`/`unlock()` operations. Production `lock()`/`yield_thread()`, full HTTP traffic and the client build remain unverified by this fixture. The base project still only defines Win32 configurations and the production translation unit carries its existing precompiled-header/STLport dependencies. The preexisting non-atomic recursive-owner access remains a separate limitation; these tests use MSVC `/volatile:ms` and do not prove portable race freedom or fairness. This is one independently reviewable x64 blocker, not completion of the client conversion.
