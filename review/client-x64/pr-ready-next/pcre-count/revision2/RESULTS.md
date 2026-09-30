# PCRE capture-count revision 2

Candidate production head: `85cd72af93e8d63cdcec5e2ea8a579ea7f2d0b94`, based on `949451032647e45e42c3aaef3f41b132c8af36e3`. Production caller SHA-256: `4b728d8ada8b5b1eac413d817f5bc0c1037dedb246b6d9454089299925675b83`. No production edits in this revision. The worker handed off three test-tool files without changing production. Parent subsequently committed those exact tools at `1df8947d7971567c014e8e4815f95ac64b5f9963`; no PRs or comments were posted.

## Current evidence

| Provider | Win32 Debug | Win32 Release | x64 Debug | x64 Release |
|---|---:|---:|---:|---:|
| Source-built genuine PCRE 4.1 / generated header | 25/25 | 25/25 | 25/25 | 25/25 |
| Original repository library / exact repository header | 25/25 | 25/25 | not available | not available |

Two additional original-library runs with the generated source header also passed 25/25; retained separately, not counted as additional behavior coverage. The version printed by the actual provider must start `4.1 `. All probe builds use native VS2013 `/W4 /WX`, `/MT` or `/MTd`, and pointer-width compile assertions. All six primary builds and executions returned 0. Per-case results include exact compiler command, caller/header/provider/compiler/probe/runner hashes and actual included-header hashes. See `provider-manifest-final.json`, `source-manifest.json`, and `native-text/`.

Original library SHA-256: `c377de21f0b9cebd3f1678810028d9c9908289400e5b3e1fb9f70d28f5663778`; original header: `fc0fe608fab7e65c69456ef455d7e09000463e81d6e18ffb0147fcd5338a99bb`. Generated header: `996b3d2b7b52d4c8609f1e1f08c75af49dd643584c3453889df3516fc980b1be`. Exact source-build library hashes are per-case in the manifest. These identify actual inputs, not a claim that arbitrary supplied libraries have verified provenance or that all linker/CRT toolchain files were hashed.

The probe exercises 0/1/10/11/20 captures through correctly bounded 33-element calls: return count including zero for insufficient capture storage, whole-match offsets, no-match result, and sentinels after both calls. The new five no-match sentinel checks bring the historical 20 to 25. It never executes the previous erroneous 132-element capacity call.

## Production binding and negative control

The runner first requires the reviewed declaration chain, sole `pcre_exec` argument and negative-result guard. This is explicitly a **lexical structural assertion**, not AST or game-command execution. It derives the probe capacity only after validation. An in-memory reverted `sizeof(captureData)` expression must be rejected before compilation/provider execution on every run.

An independently materialized reverted source tree was tested with `--check-only`: runner exit1, `provider_executed:false`; see `negative-control.json` and `safe-reversion/`. No old overflow was run. The first native matrix also demonstrated aggregate failure propagation: all builds failed and the aggregate exited 1 because `/TC` applied to a library argument. Those logs and old runner remain in `native-text/pr-pcre18-revision2/results-v1-failed/` and `run-v1.py`. Fixed by placing the genuine library after `/link`; no failure was converted into a pass. Historical input.tar contains that first runner; current source identities are in source-manifest.json and current native results.

## Commands / reproduction

Run from a matching VS2013 developer prompt (see the checkout's new README):

```
python tools/test-pcre-capture-count/run.py --checkout <checkout> --include-dir <actual-PCRE-4.1-header-directory> --library <actual-static-provider> --bits 32 --configuration Release --out <new-output-directory>
```

Repeat the appropriate bits/configuration/provider combinations. No fixed developer paths occur in the published tool. `native-matrix.py` and `original-header-matrix.py` record this machine's explicit external inputs and vcvars calls as evidence recipes, not portable setup scripts. Native aggregate return was 0 only when every required case returned 0. Inputs must be obtained separately; no provider binary or vendor header is in the publication packet.

## Actual parser compilation, separate boundary

The exact candidate caller compiled successfully in native Win32/x64 Debug/Release using existing project compiler metadata, real dependency headers and `/Y-` to disable PCH reuse. `native-text/pr-pcre18-tu/` retains command responses, include traces, tlog hashes, source hash and logs. The aggregate script exits nonzero for missing metadata or failed compile; all four returned 0 on this rerun. Win32 logs have no compiler warnings; each x64 log has four C4267 warnings (subject length, another parser size, and two existing archive operations). This is not warning-free x64 validation.

Those compiles rely on external complete v1/v2 development checkouts, platform configurations, include paths and SDK/compiler installation. They do **not** establish that the isolated master-based PR branch builds x64 by itself, or that every external input matches its base. No full client link or actual scene command ran. The portable regression tool does not require or claim that translation-unit compilation. The unrelated existing EOF blank-line deletion was left unchanged because production source was outside this revision's ownership.

## Final runner identity and output preservation

Parent review required fresh output directories. Final runner uses `exist_ok=False` before any result writes. An existing-output control returned 1 and every prior file hash was unchanged (`existing-output-negative.json`). The final safe-reversion control also returned 1 before provider execution. The final runner was rerun natively across all six primary cases, all 25/25, build/run exits 0 (`results-final/`, `matrix-final.json` inside native-text/pr-pcre18-revision2). Original-provider cases now use the exact original header. Final run.py SHA-256: `a8b7b3441d47d226c8098cebbb2323b1f6ee5cc5b8deb3927f794f4360743315`. `native-text-final-runner.zip` contains the complete text-only packet; earlier archives are historical snapshots retained unchanged. No provider headers or binaries are packaged.
