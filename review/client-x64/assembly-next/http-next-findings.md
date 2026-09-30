# HTTP critical-section x64 audit

Read-only source review at client `f102763f701193b72d975a6f6a7822dde4bd1f23`. No production edits, builds or VM actions in this audit.

## Root cause

There are **no lock-region macros or actual lambdas** in this implementation. `VeCritsec.hpp:43–48` is Windows x86 assembly using ESI and `lock bts`; the guard is `_WIN32`, which also selects it on x64. The native error list records C4235 at line 43, then undeclared `mov`/`esi`, syntax error at `lock`, and a spurious capture error at line 52. The subsequent C3487/C3493 reports in TCPConnection.cpp and HTTPPoster.cpp are consistent with parser recovery around the unsupported assembler's `[p_i_lock]`, not separate lambda bugs. Only a rebuild after replacing the assembly can establish which diagnostics disappear.

`trylock()` implements a recursive lock: same owner increments a recursion count; other callers atomically test/set bit zero, return false when already set, otherwise publish owner and count=1. `unlock()` decrements count, clears owner and only then clears lock on the final release. `lock()` retries with Sleep(0) after every failure.

## Bounded candidate

Keep Win32 code unchanged. Under `_M_X64`, include `<intrin.h>` and replace only the asm acquisition with `_interlockedbittestandset(&m_iLock, 0)` and the same false/success outcomes. Its zero result means the previous bit was clear and acquisition succeeded. Use `volatile long m_iLock` for that x64 branch (Windows long is 32 bits); this matches the intrinsic's actual operand type without reinterpreting an unsigned-int object as long. Keep the existing unsigned-int member in all other branches. Add compile-time size/alignment checks in the probe; do not widen the lock to 64 bits just because pointers widen.

Use `_InterlockedExchange(&m_iLock, 0)` on x64 final unlock after clearing m_uThreadID, so release does not depend on an implicit volatile policy. Windows thread IDs remain 32-bit, as does recursion count. Do not change SOCKET or thread IDs here. The intrinsic headers and real v120 code generation still need checking; documentation availability alone is not validation of the installed toolchain.

Alternative `_InterlockedCompareExchange(..., 1, 0)` also expresses a flag lock but bit-test-and-set maps more directly to the existing operation. A CRITICAL_SECTION replacement changes object size/lifetime and is unnecessary for this bounded fix.

## Control flow and exceptions

Leave all HTTPPoster/TCPConnection function bodies, return expressions and explicit lock/unlock locations alone. `pumpWrites`, `read`, queue paths and the destructor use explicit early-unlock paths; introducing lambdas changes return destinations/types, and introducing broad RAII regions can change lock duration and recursive behavior.

The existing code is **not exception-safe** around allocation: e.g. TCPConnection::write calls WriteQueue_.Add_Tail between lock/unlock, and read/queueIncoming have similar paths. A C++ allocation exception can bypass explicit unlock today. An assembly-to-intrinsic repair does not fix or worsen that path and must not claim otherwise. If runtime tests inject an exception, retain this as a characterized existing behavior rather than silently changing it in this commit. A separate exception-safe ownership change would need all manual early unlocks audited, nested recursion checked and destruction/lifetime behavior designed.

Legacy caveats remain: wrong-thread unlock/count underflow have no guard; thread-ID sentinel and thread reuse assumptions remain; owner/count volatile accesses rely on Windows/MSVC implementation rather than portable C++ atomics. No claim of general lock redesign or cross-platform memory-model proof.

## Tests before committing

1. Compile the **actual production header**, with real project types, in v120 Win32/x64 Debug and Release. Do not copy the implementation into the test. Check sizeof lock/class stays 12 bytes and 4-byte alignment if that is what the actual compiler confirms.
2. Fresh trylock succeeds; recursive trylock succeeds; after one nested unlock a second thread still cannot acquire; final unlock permits that thread to acquire.
3. Establish ownership before signaling the competing thread with Win32 events, so failed-trylock assertions are deterministic. Require the non-owner failure not to release/change ownership.
4. A bounded multi-thread counter increment test, including nested acquisition, must produce the exact total, and a protected payload publication/consumption test must stay coherent. Use timeouts to fail hangs; joins before destruction. Do not assert scheduler fairness.
5. Exercise blocking lock/yield separately under contention. The real VeCritsec.cpp yield_thread should be linked, rather than a no-op stub.
6. Discrimination: stock Win32 should pass the same runtime tests; stock x64 should fail compilation at unsupported assembly. If a deliberately broken acquisition/release mutation is used, it must reliably fail deterministic ownership checks, not merely hope a stress race appears.
7. Rebuild actual HTTP translation units/clientGame under both ABIs and check the lambda cascade disappears. Then the usual Win32 product build regression. This does not establish HTTP end-to-end network behavior or exception safety.

## Server counterpart

`server-client-compat` contains no VeCritsec, TCPConnection, HTTPPoster or HTTPpost directory. Its HttpGetEncoder is an unrelated shared utility. This bounded clientGame-private change needs no mirrored server edit based on the checked tree.

## Primary references

- Microsoft intrinsic contract/platform/header: https://learn.microsoft.com/en-us/cpp/intrinsics/interlockedbittestandset-intrinsic-functions
- MSVC volatile interpretation (acquire/release differs from ISO; configuration matters): https://learn.microsoft.com/en-us/cpp/build/reference/volatile-volatile-keyword-interpretation
- Windows synchronization/compiler memory ordering: https://learn.microsoft.com/en-us/windows/win32/sync/synchronization-and-multiprocessor-issues

These are current documentation, not proof of every v120 behavior. Native v120 compile/disassembly and runtime checks remain the acceptance evidence.

## POODO worker capsule / additional challenge

This is a bounded source/research worker input to the primary agent's gate, not a primary implementation decision. Frame waiver: user scope, no-PR authority and preserving the current Win32 behavior were supplied in the parent assignment. No descendant agent was spawned: the parent owns the occupied concurrency slots and is already integrating complementary workers. Shared context/model/source means this is not independent corroboration. Candidate selection and native action remain with the primary after its research/20-path gate.

**Alignment and bit preservation:** m_iLock is the first member of VeCritsec, which is embedded normally in TCPConnection. No packing directive appears in these HTTP files. A 32-bit long preserves the expected field size, but confirm real v120 offsets/alignment and enclosing packing with actual-header tests, not just a hand-written mirror. The intrinsic changes only bit 0 on acquisition, matching `lock bts`; failed acquisitions must not clear the bit or owner. No other code writes nonzero bits: constructor and final release write zero, assembly sets bit 0. Therefore clearing the entire word on final release matches existing semantics; it need not preserve unrelated bit flags that do not exist in this implementation. Do not use the 64-bit intrinsic over a four-byte member, which would touch the adjacent owner field.

**Memory-order challenge:** simply replacing the acquisition does not prove release ordering. Windows intrinsic documentation maps bit-test-and-set to atomic `lock bts` on x86/x64. Win32 synchronization documentation says unsuffixed Interlocked operations supply ordering barriers; MSVC volatile documentation distinguishes ISO from MS extensions. Thus using explicit exchange for x64 final release is a bounded way to eliminate dependence on that one volatile store. Owner/count accesses are still the pre-existing recursive-lock design and need contention tests; this is not a portability proof. Check final assembly for locked 32-bit acquisition and release after owner clear. If Win32 must remain exactly untouched, guard both new member spelling and intrinsic paths with `_M_X64`.

**Research record (2026-09-30):** searched Microsoft `_interlockedbittestandset intrinsic x64 long volatile` and `volatile acquire release x64 MSVC /volatile ms`; opened synchronization page (updated 2022-06-09). Learn's two C++ pages failed to open, so read full official MicrosoftDocs raw sources instead: `cpp-docs/main/docs/intrinsics/interlockedbittestandset-intrinsic-functions.md` (metadata 2019-09-02) and `docs/build/reference/volatile-volatile-keyword-interpretation.md` (metadata 2016-11-04). These pages share the same vendor evidence family; runtime v120 artifact validation must supply the separate evidence family. Documentation's displayed pointer declaration differs in volatile qualification across versions, so inspect the installed intrinsic declaration and compile actual header before choosing casts. No cast-away-volatile workaround is authorized by this note.

**Prospective acceptance/stop:** predicted x64 cascade disappears after the header repair; stock Win32 remains runtime oracle for lock recursion/ownership. Run native v120 tests from named commit in both ABIs, four configurations, with exact test totals, bounded timeouts and preserved stock-x64 compile rejection. Any lost count, early second-thread acquisition, release-before-owner-clear observation, changed Win32 path, or remaining actual-header compile failure stops promotion. Rollback is an isolated header commit, not broad HTTP code edits. Allocation exceptions remain an explicit untested/unfixed legacy boundary.

**delivery_state:** source/research findings authored. **outcome_state:** candidate runtime effect unobserved. **highest_justified_claim:** unsupported x86 assembly is a demonstrated compile blocker; lambda diagnostics are a strongly supported cascade interpretation pending native rebuild. **required_runtime_observation:** actual-header recursive/contention/publication tests plus Win32 regression and x64 TU compile. **who_controls_next_test:** primary agent with Windows VM.

## Candidate authored, not validated

At the parent's explicit follow-up, edited only `client-build-next/.../HTTPpost/VeCritsec.hpp`, uncommitted. The patch adds 17 lines guarded by `_M_X64`: actual member type `volatile long`, `<intrin.h>`, atomic bit-test acquisition and exchange release. Win32 statements remain unchanged. `git diff --check` passes for this file. Probe is `assembly-next/http-lock-probe.cpp`, actual production headers with real FoundationTypes and linkage to production VeCritsec.cpp requested; no substitutes. Expected 27 checks; the outcome remains unobserved pending parent-controlled native compile/run. Parent's critic received paths for read-only review. Existing source exceptions remain outside this patch.
