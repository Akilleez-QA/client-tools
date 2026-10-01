# Allow the HTTP lock header to compile with MSVC x64

MSVC x64 rejects the HTTP connection lock's Win32 inline assembly. Add an x64 intrinsic path for `trylock()` acquisition and final `unlock()` release, preserving the Win32 assembly and recursive ownership behavior. The production diff adds exactly 17 lines to `VeCritsec.hpp`, directly on master `949451032647e45e42c3aaef3f41b132c8af36e3`; no imemmove or integration prerequisite is included.

[Recorded native v120 results](https://github.com/Akilleez-QA/client-tools/blob/09fc9dc5d6b1c7636f585778b793dd4143de3154/review/client-x64/pr-ready-next/http-lock23/results-v2/results.json): 27/27 header-operation checks in each Win32/x64 Debug/Release configuration, stock Win32 passes, stock x64 rejects the unsupported assembly, and deliberately broken acquisition/release controls fail their expected checks. These results belong to the unchanged header and probe at `d788e64ced56832894ff77a7d0d5b30fbec1b2ce`, before the test-only classifier correction.

The corrected runner requires the complete recorded stock x64 diagnostic sequence at the exact header/probe paths and lines. Portable replay passed 77 controls using both original logs, including missing, duplicate, malformed and unrelated failures; this is not a new native matrix run.

The fixture exercises actual `trylock()`/`unlock()` only. It does not execute production `lock()`/`yield_thread()`, establish fairness or portable race freedom, or qualify full HTTP traffic/client builds. A separate genuine-translation-unit extension remains blocked on the existing custom allocator dependency and is not included in this PR; no yield stub is supplied.
