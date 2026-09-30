# HTTP lock candidate 23: decision and prospective evidence ledger

2026-09-30. No native goal is exposed in this worker (`get_goal` returned null); this work is subordinate to the parent's full-client objective. This narrow component cannot complete that objective.

## Frame / Pontificate

The delegated current request establishes unusually specific scope, authority and acceptance, so no redundant user exchange is needed. "Review-ready" means a clean local upstream-based commit, self-contained rationale, and reproducible narrow native evidence; it does not mean a product build or full-client conversion. User-authorized scope is one HTTP lock x64 assembly root cause. No push, PR, integration branch changes, engine/audio/allocator fault workloads, or preexisting owner-field race repair. Strongest rival: the apparent self-contained fix actually needs surrounding integration dependencies. Discriminator: compile/run the real changed header with untouched upstream types and inspect surrounding TU prerequisites.

## Observe

- E1: `949451032647e45e42c3aaef3f41b132c8af36e3` resolves and matches preserved `refs/remotes/origin/master` and origin/HEAD. No remote named upstream exists. The origin URL is the user's fork, so this is a preserved base identity, not a claim of a freshly fetched upstream tip.
- E2: `git diff 94945103 ff3c1742^ -- .../VeCritsec.hpp .../VeCritsec.cpp` is empty. Integration commit `ff3c1742fe5e02b1a84b59afb72867a889776dcf` adds only `_M_X64` branches in the header. No source prerequisite in either file.
- E3: base `clientGame.vcxproj` lists only Win32 configurations; FirstClientGame.h pulls project/STLport/StringId dependencies. This constrains whole-TU/product claims.
- E4: prior assembly-next fixture exercises real header trylock/unlock with event-ordered recursive exclusion and coherent payload updates. It explicitly does not execute production lock()/yield_thread(). Prior results are reported context, not evidence for this new artifact.

Topology: compile syntax -> x64 intrinsic ABI -> 32-bit aligned lock word -> atomic acquire / final release -> recursion ownership -> protected data. Header and type definitions observed; Win32 source branch preserved; production scheduler TU dependency frontier unresolved; C++ owner-field race and non-Windows/ARM paths outside the change. Real HTTP flow and product linking are outside this component acceptance.

## Research gate (retrieved 2026-09-30)

Queries: Microsoft `_interlockedbittestandset` x64 intrinsic long memory barrier; Microsoft inline assembly x64 support / volatile ISO versus MS; Intel BTS LOCK atomic operation. Disconfirmation sought: volatile ordering is not ISO interthread synchronization, and replacing inline assembly does not make the recursive owner bookkeeping race-free.

- Microsoft Learn `_interlockedbittestandset intrinsic functions` (updated 2021-08-03), https://learn.microsoft.com/en-us/cpp/intrinsics/interlockedbittestandset-intrinsic-functions?view=msvc-170 : x64 support and bit-zero old-value semantics. Modern compiler documentation, so native v120 execution still required.
- Intel SDM Vol. 2A (order 253666, supplied PDF revision, BTS pp. 3-136/3-137), https://cdrdv2-public.intel.com/812383/253666-sdm-vol-2a.pdf : independent instruction-family evidence for LOCK BTS atomicity, prior bit in carry, and default 32-bit operation in 64-bit mode. Does not prove compiler lowering or application correctness.
- Microsoft InterlockedExchange, https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-interlockedexchange : atomic exchange and full barrier. Does not eliminate unrelated non-atomic owner accesses.
- Microsoft volatile (updated 2021-09-21), https://learn.microsoft.com/en-us/cpp/cpp/volatile-cpp?view=msvc-170 : MS-specific acquire/release extension; ISO volatile is not interthread synchronization. The fixture retains `/volatile:ms`; no portable/race-free claim.

Sources inspected directly, not only snippets. Semantic additions: bit return value must match jnc success; use 32-bit long on Windows rather than pointer-width widening; explicit final release; retain compiler-mode boundary. Two independent mechanism families (Microsoft compiler/API contract and Intel ISA), neither substitutes for native execution. Gate satisfied for this narrow conversion.

## Orient: exactly 20 materially distinct paths

1. x64-only intrinsic acquisition and exchange release: preserve existing Win32 behavior.
2. Intrinsics on both Windows architectures: simplify branches but expand regression scope.
3. x64 compare-exchange lock word: equivalent state protocol with different instruction.
4. Windows critical section: replace ownership and scheduling architecture.
5. std::recursive_mutex: use library synchronization with toolchain/ABI consequences.
6. External MASM x64 routine: preserve assembly semantics with new build/link dependency.
7. Remove recursive support: change public behavior and simplify concurrency model.
8. Repair owner-field atomicity: broader data-race project beyond assembly compatibility.
9. Header-only native differential test: isolate dependency-free changed runtime surface.
10. Full real-TU linkage: add scheduler execution evidence if upstream dependencies permit.
11. Exact real-TU compile: expose dependency blockers without link workarounds.
12. Instruction disassembly: verify compiler lowering orthogonally to runtime outputs.
13. Stock x64 compile control: show architecture failure rather than assume it.
14. No-acquire mutation: challenge mutual-exclusion oracle deterministically.
15. No-release mutation: challenge progress oracle with a bounded wait.
16. Contended coherent payload test: exercise observable protected-data invariant.
17. Full HTTP integration traffic: larger intended-use surface, outside this chunk.
18. Defer candidate until full project x64 support: trades independent shipment for coupling.
19. Ship documentation-only boundary: justified if clean native fixture impossible.
20. Escalate ownership design for separate review: preserves concern without widening patch.

Select 1, 9, 13-16; inspect 11 source boundary and attempt only if clean. Keep 10 unclaimed unless demonstrable without unrelated shims. 2-8,17-18 widen current scope; 19 fallback; 20 recorded limit. Strongest live rival remains integration dependencies; real-header fixture deliberately avoids claiming their behavior. Bounded saturation: each mapped region is inspected, covered by prospective check, or explicitly out of scope; no full correctness/exhaustiveness claim.

## Transition checks / Decide

All four pre-execution boundaries considered separate subagent spikes. No descendants: parent owns all four slots and has committed to independent blind review later; duplicated source reading here would have less value than the parent's fresh evaluator. Parent review is pending, not evidence. One author owns this checkout. Local worktree creation is reversible setup. Source fix selected only after dependency inspection and research.

## Prospective oracle v1 (before native runs)

Prediction: the actual candidate header compiles/runs with stock upstream FoundationTypes in native VS2013/v120 Win32 and x64, Debug (/Od /MTd) and Release (/O2 /MT), `/volatile:ms`. All 27 public-behavior checks must pass: nested same-thread acquire, competitor excluded through partial unlock, final unlock permits another thread, reuse after transfer, and exactly 100000 coherent protected updates. Stock Win32 passes; stock x64 fails at C4235 inline assembly. Diagnostic no-acquire x64 Release must exit 1 at `other thread excluded while nested`; no-release must exit 1 at `final unlock permits retry acquisition` (not merely any failure).

Sensor: fixture stdout/exit status, compiler logs, PE machine, source hashes and run durations. Oracle derives from lock API exclusion/recursion contract and protected payload invariant, not lock-word internals. Coupling: author-owned fixture, repeated native environment, not independent reproduction or memory-model proof.

Timing precommit: each fixture event wait is 10000 ms; each native process outer deadline 45 s; each compile outer deadline 120 s. Durations are diagnostic only, not performance acceptance. Stop dependent success claims on candidate or control failure; retain logs and diagnose before changing oracle. No-acquire should fail promptly; no-release should reach its 10 s bounded wait. Rollback is discarding this isolated local candidate only. No production runtime or user application touched.

## First run and harness correction

Native v1 met every behavioral/control oracle. Post-run raw-log review found D9002: the optional /MAP argument was ignored because cl response-file /link forwards only the remainder of its line, while the runner wrote one argument per line. No claim about map evidence is made for v1. Correct the response file to one line and repeat the unchanged behavioral oracle as v2; header and probe remain byte-identical. This is harness receipt repair, not an invalidation or reclassification of v1 runtime outcomes. Add map inspection to confirm the documented absence of production yield_thread linkage. New pretest manifest records the runner-only change before v2.

## Outcome and handoff

Final v2 repeats all expected outcomes with the final runner and generates every map. Production header/probe hashes unchanged; runner hash verified against pretest-manifest-v2.json. No production yield_thread symbol is linked. The component acceptance contract passed; broader client outcome remains unobserved. Orchestrate → Loop fan-out was considered; no descendant capacity was allocated, and parent-controlled blind review remains pending. Parent owns synthesis and any later push. See RESULTS.md and capsule.yaml for exact identity and terminal claim contract.
