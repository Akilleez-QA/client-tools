# Independent senior review — HTTP lock candidate 23

Reviewed commit `283f6bffb9b5db76e4fd15bca922b8bedeedf8c8` against `949451032647e45e42c3aaef3f41b132c8af36e3` in the actual candidate checkout. Read the actual diff and fixture implementation before the v2 evidence and PR description. No peer REVIEW files were read. No native runtime was launched and no production file was edited.

**Verdict: ready for a narrowly scoped maintainer review, with a timeout-documentation nit; no introduced production correctness blocker found.** Engineering: **8.5/10**. Readiness for this header-only x64 blocker: **9/10**. These scores do not rate the readiness of the HTTP subsystem or client x64 conversion.

## Correctness and scope

The 17-line production addition preserves the original Win32 assembly path and recursive bookkeeping, substitutes an atomic bit-zero test-and-set for x64 acquisition, and clears the same 32-bit lock word atomically on final release. The Windows `long` operand matches the intrinsic type without pointer casts. Source ordering leaves owner reset before release. Fixture static assertions verify the 12-byte size and 4-byte alignment in the tested Windows configurations. I found no production change outside the intended header.

The legacy recursive-owner read/write is still non-atomic; neither a passing stress test nor the new lock-word intrinsics prove portable C++ race freedom. That limitation predates this change and is stated explicitly. Keeping it outside this small compile-enablement patch is reasonable. The source's inherited comment asserting that the owner comparison is not a race should not be repeated as a new guarantee.

## Test discrimination and evidence

The ownership test establishes nested ownership before requesting each competing attempt and waits for the reply before partial/final unlock. Exclusion is checked from the actual trylock result rather than a sleep or throughput threshold. Final transfer, worker termination, reuse, and protected counter/complement updates are checked. The stress run supplements these deterministic checks; it does not prove fairness or establish all possible interleavings.

The deliberate no-acquire copy fails exactly at `other thread excluded while nested`; the no-release copy fails exactly at `final unlock permits retry acquisition` after about 10.094 seconds. Both compile successfully as x64. Stock x64 fails with C4235 at the expected assembly site, while stock Win32 passes. These are useful controls that rule out a fixture which merely compiles or always reports success.

I inspected all ten v2 build logs and all eight runtime logs. Four candidate lanes and two stock Win32 lanes each contain 27 PASS records and SUMMARY 27/27; stock x64 lanes fail compilation as described. I independently matched current header/probe/runner/FoundationTypes hashes against native inputs, matched copied probes and lane header hashes, parsed retained PE machine fields, and checked maps for absence of yield_thread. Values and outcomes agree with results.json and PR.md. The checkout is clean with a single commit over the stated base; diff whitespace checks and a pure Python syntax compilation pass.

The retry helper uses SwitchToThread and never calls production lock(). VeCritsec.cpp defines yield_thread using Sleep(0), and the fixture does not link that translation unit. Accordingly this supports actual trylock/unlock operation on native v120, not production scheduler behavior, HTTP traffic, or the client build. PR.md describes this boundary accurately. The suite's 27 checks include handle/thread administrative checks; they should remain described as checks rather than 27 independent concurrency scenarios.

## Nonblocking timeout qualification

`tools/test-http-lock/run.py:20-29` passes a timeout to subprocess.run. The compilation command launches cmd.exe, which launches compiler/linker descendants. This is not process-tree containment: termination of cmd.exe does not guarantee termination of those descendants, and inherited output handles can delay cleanup. The direct probe executable does not create child processes, so this concern is chiefly about build invocations.

README.md's statement that compiles have a 120-second outer deadline is acceptable as the configured timeout value, but too strong if interpreted as a guaranteed wall-clock cap or compiler-tree cleanup. Prefer “120-second subprocess timeout for the build command; compiler/linker process-tree cleanup is not guaranteed.” A Windows job/process-tree implementation would require its own timeout-path verification and is optional hardening for this small patch, not a reason to expand the production change.

RESULTS.md says “No deadline had to terminate a process.” More precise wording is “No outer subprocess timeout fired.” The broken-release lane intentionally reached its 10-second event-wait limit and called ExitProcess(1). The observed failure is valid and expected, but the unqualified sentence can obscure that distinction. No v2 evidence exercises the runner's outer-timeout cleanup path.

## Rating rationale

Engineering 8.5 reflects a small understandable intrinsic substitution, preservation of the legacy path, discriminating tests, and unusually traceable evidence. It stops short of 10 because the timeout cleanup contract is weaker than a reader might infer and the test intentionally leaves the real lock()/yield_thread() path unexecuted; no general concurrency correctness claim is justified.

Readiness 9 reflects the clean single-commit delivery, reproducible fixture instructions, matched source/evidence identity, accurate principal limitations, and reviewable production scope. I would submit this small fork commit for review after the minor wording clarification rather than add unrelated synchronization redesign or client integration changes. Production HTTP and full-client acceptance remain later, separate work.
