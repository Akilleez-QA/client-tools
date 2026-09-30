# Runner verdict repair — prospective plan, 2026-09-30

Scope supplied by parent is explicit, so no redundant opening exchange. The reviewer observed a real control-flow defect: both drain23 runners can record a failed build, wrong test exit, or caught timeout and still fall off with process status 0. The archived individual native case counts remain supported; this repair must not be attributed retroactively to those executions. Only runner-verdict24 may be written. No native, private, vendor, audio, product, or push action is authorized or needed.

POODO observation: read REVIEW-startup-drain24.md, both original drain scripts, and startup run-private.py. Only the two drain runners have this reported defect; startup runner already exits on its composed acceptance condition and is outside the change. Topology: declared cases/expected old failures -> build and child return codes -> accumulated records -> persisted evidence -> final process status. Missing/duplicate records and contradictory derived matches metadata are separate failure families. A successful child's status cannot certify a missing matrix; a stored matches=true cannot certify its exit.

Research gate: Python official subprocess and sys.exit documentation, retrieved 2026-09-30; query `site:docs.python.org subprocess run returncode TimeoutExpired sys.exit None zero status`; read https://docs.python.org/3/library/subprocess.html and https://docs.python.org/3/library/sys.html#sys.exit . Both are one specification family. run(check=False) returns nonzero codes without raising; caught timeout plus normal script completion need not signal failure. sys.exit/SystemExit is the explicit runner contract. Challenge: expected negative-control child exits must remain accepted, so global child-exit-zero or check=True is not a valid substitute. Direct Python execution with mocks will provide the separate runtime evidence family. Documentation does not establish this implementation's correctness or native behavior.

20 materially distinct paths considered before selecting:
1. Final strict matrix verdict over raw exits (selected).
2. Check only reported matches booleans (reject: coupled derived evidence).
3. subprocess check=True everywhere (reject: breaks deliberate old failures).
4. Abort immediately at first wrong exit (loses later diagnostics).
5. Aggregate all failures and persist before nonzero exit (selected).
6. Require only two successful builds (insufficient case evidence).
7. Use case count alone (duplicates can hide omissions).
8. Compare exact identity multiplicities (selected).
9. Validate matches and expected metadata against declarations (selected).
10. Remove redundant metadata entirely (unnecessary result-format change).
11. Wrap scripts with an external JSON acceptance gate (leaves direct scripts unsafe).
12. Change only CI caller behavior (caller source outside scope).
13. Replace both runners with a full runner framework (excess scope).
14. Share a small pure verdict function (selected).
15. Unit-test synthetic record mutations (selected).
16. Execute real script bodies with path/subprocess doubles (selected).
17. Rerun native named-pipe matrix (not needed for runner status; excluded).
18. Mock compilation failures only (misses matrix corruption).
19. Preserve originals and create versioned repaired copies (selected).
20. Leave scripts diagnostic-only with explicit warning (fallback, does not satisfy requested fix).

Decision: copy both runners into runner-verdict24, point their default staging path at C:/runner-verdict24, import a shared strict verdict, persist results and verdict diagnostics, and raise SystemExit(1) unless old+candidate each have one successful build and exactly one result per declared case with independently derived expected exit. Reject timeouts, malformed/extra/missing/duplicate records, and contradictory reported matches/expected metadata. Record build timeouts before final verdict as well as already-caught case timeouts. Unhandled launch/filesystem exceptions remain nonzero and cannot falsely report success.

Prospective test oracle v1: pure local actual-script execution via runpy, substitute pathlib.Path root and subprocess.run only, with explicit record-corruption injection at a mock child boundary for missing/duplicate/metadata checks. Test both scripts for complete success, build failures (both variants), wrong old negative-control exit, wrong candidate exit, case timeout, build timeout, missing/duplicate cases, missing/duplicate builds, and reported-matches contradiction. Additional pure verdict inputs cover malformed/unknown records and spoofed expected values. Old original scripts under the same build-failure/wrong-exit/case-timeout doubles should return0, demonstrating reviewer finding without invoking a compiler or native binary.

No acceptance criterion changes after observing results; preserve output then correct failures. Test roots are temporary directories under this packet; no VM call. Repaired source identities and old-tree hash preservation are captured. Stop if mocks attempt a real subprocess or an original path mutation. Fanout considered at each transition: no descendant slot allocated; parent blind review supplies source-correlated criticism, and this small pure runner task has no separable coverage requiring another agent. Final handoff must distinguish repaired runner status evidence from unchanged historical native counts.
