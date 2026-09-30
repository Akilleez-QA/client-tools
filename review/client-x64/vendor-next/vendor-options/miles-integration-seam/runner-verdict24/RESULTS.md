# Runner verdict repair

The two original drain23 runners can return 0 falsely after failed builds, wrong child exits, or caught case timeouts. This reviewer finding is now reproduced with pure test doubles. Their archived individual native results still stand: this repair does not generate or retroactively certify those results.

The repaired copies are `run-native.py` and `run-supplement.py`; the shared predicate is `verdict.py`. Exact change: [source.patch](source.patch), SHA-256 `5345571788b7049eba1928fa369c0bb5c9898d2ae4fb18b1dcb09585309e6986`.

Both runners now persist their result/output evidence and a verdict JSON, then explicitly exit 1 unless:

- Old and candidate each have exactly one successful build.
- Every declared variant/case pair has exactly one result; no unknown or ambiguous records exist.
- No timeout exists, and every raw integer exit equals the independently declared expectation. Expected old negative-control exits remain 1; all other expected exits are 0.
- Any stored `expected` and `matches` fields agree with that calculation. Those fields cannot override a wrong exit.

Build timeouts now also produce a recorded timeout before the final failing verdict. The default staging directory is `C:/runner-verdict24`, protecting frozen23 paths. Unexpected launcher/filesystem exceptions still terminate nonzero; this change does not guarantee full evidence persistence after such exceptions.

## Pure verification

Run from any directory:

```bash
python3 /home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/runner-verdict24/test_runners.py
```

Observed: **28 repaired runner executions, 6 original false-zero controls, and 21 verdict controls passed.** Full records, captured runner output, raw exits and diagnostics are in [test-results.json](test-results.json).

For each repaired runner the actual script body was executed with `runpy`, a temporary `pathlib.Path` root and a `subprocess.run` double. A `Popen` tripwire prevents compiler/native launch from the runner body. Tests observed exit 0 only for the complete successful matrix. Exit 1 was observed for failure of either build, wrong old negative-control exits, wrong candidate exit, case/build timeouts, missing/duplicate cases, missing/duplicate builds, contradictory `matches`, spoofed `expected`, and an unknown case. Recording-corruption scenarios explicitly mutate the real runner's accumulated records from the child double at a declared boundary; they do not replace the verdict function or rewrite executed script source.

Additional pure predicate controls cover empty/non-list results, absent or boolean exits, timeout even with exit 0, invalid metadata types, unknown variants, ambiguous records, and malformed case declarations. The six original-script controls reproduce false exit 0 for failed old build, wrong candidate exit and caught case timeout in both original runners.

All frozen23 files—including both scripts, native evidence, and final-manifest.json—were hashed before and after and are unchanged. `frozen23-before.json` captures the exact checked tree. `pre-test-identities.json` matches the source/test identities that generated this result. No VM, native fixture, private SDK, vendor, Wine or product execution occurred. No commits or pushes were made.

For future native use, stage the existing synthetic fixture inputs and these three repaired runner/helper files together under `C:/runner-verdict24`; the helper import is required. This packet does not stage or execute that native run. The observed native counts remain attributed to the frozen23 scripts and raw records, not these repaired runners.

- delivery_state: authored and checked
- outcome_state: passed for pure runner acceptance and exit propagation
- highest_justified_claim: both actual repaired script entry points reject the exercised failed/incomplete matrices and accept complete expected results under explicit test doubles
- required_runtime_observation: none for this pure runner-status repair; a future native execution remains separately attributable
- who_controls_next_test: parent/user for a future native run or combined integration experiment
