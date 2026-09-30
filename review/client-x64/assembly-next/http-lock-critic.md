# VeCritsec candidate and oracle — read-only critic

Reviewed x64 header changes and assembly-next/http-lock-probe.cpp before native
execution. No edits or VM activity.

The candidate uses the documented x86/x64 LOCK BTS intrinsic for acquisition,
with a 32-bit Windows long operand and InterlockedExchange release. Original
Win32 assembly/types are retained behind guards. Normal class alignment is
4 bytes; no packing override was found in HTTPpost or clientGame.vcxproj. The
probe asserts size12/alignment4. This does not independently establish the layout
under arbitrary downstream packing pragmas or user property overrides.

Primary references:
- https://learn.microsoft.com/en-us/cpp/intrinsics/interlockedbittestandset-intrinsic-functions
- https://learn.microsoft.com/en-us/cpp/build/reference/volatile-volatile-keyword-interpretation
- https://learn.microsoft.com/en-us/cpp/cpp/volatile-cpp

The owner-ID read remains volatile outside the lock. Its synchronization model
is MSVC-specific; do not describe it as portable ISO C++ atomic synchronization.
Document observed compiler flags/default /volatile:ms for these Windows builds.

Oracle:
- Expected27 checks is correct:12 ownership checks and15 stress checks.
- Two request/reply phases deterministically require contender trylock failure
  while main owns twice, then once. Premature recursive release should fail.
- Successful joins happen before shared-state/handle destruction. Wait failures
  ExitProcess, so live workers cannot outlive stack objects on a return path.
- Four workers make100000 protected updates; inverse/count checks expose sampled
  loss of exclusion or payload coherence. This is bounded stress, not proof for
  all schedules or fairness.
- Each event/join wait is10s. A deadlock in lock() itself needs the stated outer
  process watchdog. Preserve timeout as failure, never count partial PASS lines.
- enterBlocking is signalled before the worker actually calls lock(). Main may
  release first. Therefore this verifies lock API transfer, not deterministic
  blocked waiting or execution of production yield_thread. Stress makes the
  latter likely but does not prove it. Keep claims bounded accordingly.

No blocking flaw found. Parent should require real VeCritsec.cpp object binding,
exact27/27+zeroexit and outer timeout; run mutations for always-success lock and
premature recursive release. Such negative controls establish discrimination of
this fixture, not broad HTTP stack correctness.
