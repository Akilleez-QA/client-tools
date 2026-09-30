# CLI coverage review, rounds20–21

These are auxiliary search/review reports, not independent runtime acceptance. The parent checked the load-bearing claims against actual source. Raw prompts/results/exit codes are retained.

| Worker | Outcome | Disposition |
| --- | --- | --- |
| Composer surface20 | Exit0, incomplete artifact discovery | Tried guessed nonexistent filenames and reported the seam unreadable. Actual `host-candidate/host_dispatch.cpp` and the other supplied tree files are present/readable. Missing-artifact conclusion rejected; game-side references remain individual search leads. |
| Composer surface21 | Exit0, supplied-source audit | Real dispatcher content supplied directly to remove discovery failure. Useful family inventory, but numerical and mask claims need correction below. |
| Grok file-contract20 | Timed out1500seconds, exit124, no report | No assessment or agreement. A smaller source-contained follow-up21 completed, assessed below. |

## Parent corrections to Composer21

- Actual `supports()` and `dispatchImpl` each contain **39** distinct matching AIL cases, not38. The separate frozen metadata component contributes5 disjoint cases: union44, leaving17 of the61 API-map rows outside **those two TUs**. See CLI-COVERAGE21.json and its input digests. These are lexical implementation counts, not proof of reachability or behavior.
- Several of those17 already have bounded real implementations in the separate live bridge fixture (startup/shutdown, driver/sample allocation/release and named-sample binding). The report did not receive that file; its absence from the supplied two dispatchers must not be generalized to the whole experimental tree. The live fixture is still not a full production backend.
- `MilesStartup::dispatch` calls `validate` before reaching the speaker SDK call. That validator requires output_mask8. The reported “ignores output_mask” defect is false. It supports the actual Audio caller's three-null/spec-only form; broader SDK output forms remain explicitly unsupported.
- The reverb **getter** only accepts OwnedSample. The actual Audio.cpp getter is reached through its3D sample map (lines3924–3928); borrowed stream samples occur in the **setter** at3212, which accepts the borrowed kind. This is no demonstrated caller regression. General API-map wording is broader than the intentionally supported getter shape.
- Rejecting resource/text/callback fields in the scalar dispatcher is its documented boundary. Required buffer/stream/callback implementations must have their own typed handling; weakening that validator would not implement them.
- Dual dispatch entry points need deliberate session routing when integrated. They currently are separate experiments, not a claim of a composed game backend.

The useful result is unchanged: actual callback causality, original TreeFile service/thread ownership, stream/borrowed-sample lifetime, shutdown and the Bink shared driver are still integration work. Listener and scalar steady-state support alone cannot run the game. No upstream action or new production claim follows from these reports.

## Grok file-contract21

The bounded, supplied-source follow-up completed with exit0. Its two central observations match the source: the callback map/counter/file position have no local synchronization; the global `once` flag installs TLS on only its first nonmain entrant. These are useful integration gates, already recorded in the file-seam contracts.

Two qualifications matter. The dormant wrappers do not yet introduce a second runtime caller; saying the patch itself introduces a race would overstate the evidence. The hazard arises when a consumer is added without the stated admission contract. Also the source initializes `s_nextFileHandle` to0 outside the excerpt supplied to Grok; successful handle0 is established by the complete original source and must be preserved. The reviewer correctly said it could not establish the initializer from its excerpt, but that is not a counterexample to the handle contract.

Grok's proposed single-owner thread is a candidate contract, not proof of original scheduling equivalence. A preinitialized worker still has to account for the original non-idempotent `threadInstall` and global guard. No general thread-pool, map-only mutex, callback quiescence or shutdown guarantee was inferred. No model report authorizes removing original registration or changing the thread policy.
