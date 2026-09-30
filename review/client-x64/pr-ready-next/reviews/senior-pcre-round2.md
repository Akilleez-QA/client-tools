# PCRE revision 2 — independent senior engineering reassessment

Reviewed clean candidate HEAD `1df8947d7971567c014e8e4815f95ac64b5f9963`, against production-only head `85cd72af93e8d63cdcec5e2ea8a579ea7f2d0b94` and the previously reviewed base. Revision 2 adds exactly three test-tool files, 172 lines; production is unchanged. I inspected the committed tool, revision-2 draft and packet, raw final results, negative controls, compiler responses/logs and source identities. I did not read the maintainer's reports, modify the initial review, execute the runner, build code, or run provider/runtime tests. This report is the only output written.

| Assessment | Round 1 | Revision 2 |
|---|---:|---:|
| Engineering | 9.0/10 | **9.5/10** |
| PR readiness | 6.5/10 | **9.0/10** |

The original required engineering/test remedies are substantially addressed. I would submit this narrowly scoped fix after the pending identity/publication bookkeeping below. No new production defect or merge-blocking test defect was found. A 10 would overstate the remaining reproducibility and lexical-binding limits; those limits do not justify another broad runtime campaign.

## What is now demonstrated

**The production regression now has a discriminating check.** `run.py::assert_caller` requires the reviewed constant declarations, array extent, sole pcre_exec call with subscriptCount, and immediately following negative-result guard. A literal reversion of the argument can no longer leave the complete test tool passing. The runner checks its in-memory reversion before compilation/provider execution, and an independently materialized reverted checkout differs from the candidate at exactly the capacity argument. Its retained final result is `passed:false`, `provider_executed:false` with the structural-mismatch error; the control summary records exit 1. I verified that source diff directly. No unsafe old call is compiled or executed by this control.

This is a lexical contract check, as the README and draft say. It is not an AST, preprocessor or game-flow check. The reviewed source satisfies the intended declaration chain, and returning 33 after verifying that exact chain is defensible for this focused test. The assertion would not protect arbitrary future source restructuring, inactive preprocessor regions, or all possible changes to match-handling behavior. Those are limitations, not evidence that this candidate's check accepts the actual reversion. Requiring a compiler frontend or extracting production code into a new abstraction would be disproportionate here.

**The provider probe is bounded and independently checks relevant behavior.** Its generated CAPTURE_SLOTS is 33 after caller validation. All calls use that true capacity. Cases cover 0, 1, 10, 11 and 20 captures, expected return values, whole-match offsets and no-match behavior. The missing no-match sentinel checks from round 1 are now present. The expected zero return for too many captures remains a successful match in the production caller. There is no production ABI or provider change. The 25 checks are five assertions over five patterns, not 25 distinct regex grammars.

The final six primary native cases each record build exit 0, run exit 0, 25 checks, provider execution, and successful safe-reversion discrimination. Their run logs print `PROVIDER 4.1 12-Mar-2003` and exactly one `PASS 25 bounded correct-count checks`. Recorded commands use the actual static library after `/link`, `/W4 /WX`, and the selected static CRT. The probe has a pointer-width compile assertion. Four cases use source-built providers for Win32/x64 Debug/Release, and two use the original Win32 provider with the repository header. The original provider's Debug/Release cases use the same library; these are two probe configurations, not two independently built original providers.

**The final source identity is traceable.** My own hashes of the committed files match the source manifest and recorded native inputs:

| Input | SHA-256 |
|---|---|
| Production caller | `4b728d8ada8b5b1eac413d817f5bc0c1037dedb246b6d9454089299925675b83` |
| run.py | `a8b7b3441d47d226c8098cebbb2323b1f6ee5cc5b8deb3927f794f4360743315` |
| probe.c | `80e31ad6fd1207a923306de378d760b692fe4986af5fc045fe224d021621990f` |
| README.md | `13ac2a0f94f07375e16a1fafbbd92325fa1b0b086c085abe2ecbf3d08b7f6fb3` |
| Repository PCRE header | `fc0fe608fab7e65c69456ef455d7e09000463e81d6e18ffb0147fcd5338a99bb` |

All six final manifest entries agree with their raw result files for caller, inputs and checks. Included-header records identify the expected PCRE header and generated capacity header. The final ZIP has 117 unique entry names, its runner is byte-identical to the committed runner, and I found no difference between ZIP entries and their corresponding existing local native-text files. I did not independently rehash the remote provider/compiler binaries; their digests are execution records, not independently reauthenticated binaries in this review. Runtime version text and hashes are useful identification, not proof of source provenance for arbitrary supplied libraries. The revised README acknowledges that boundary.

**Existing results are protected.** The committed runner creates the output directory with `exist_ok=False` before any result write. The existing-output control records exit 1 and an unchanged results.json hash, `c4cc1f898cb7bcafec92d63af2184692a27191448b6c47ed47558011ae128cb3`; that also matches my hash of the retained structural-final result. Rejection occurs outside the reporting try block, so it produces a nonzero exception rather than rewriting results.json. That is acceptable for preserving prior evidence.

**Actual-caller compilation is now accurately scoped.** All four TU records report exit 0 and the same caller hash I computed. Each response file names the candidate caller and includes `/Y-` and `/showIncludes`. Win32 logs contain no compiler warnings; each x64 log has the disclosed four C4267 warnings, including the bounded subject-length conversion at the modified call. Unlike round 1, x64 Release has actual compile evidence. These are compilations against external v1/v2 development headers and configurations. They do not establish a clean or independently buildable x64 master-based branch. The draft makes that distinction clearly, and the standalone regression tool does not depend on these historical tlogs.

## Remaining actions

1. **Required publication bookkeeping, already identified as parent work:** finalize the candidate identity consistently. `source-manifest.json` still calls `85cd72...` the candidate head, and RESULTS.md says the tools are uncommitted. That was true when the runs were collected, but it is stale for the committed submission `1df8947...`. Preserve raw records; add a clear final identity record naming the tested production commit, final submission commit and matching file hashes, and mark the preparation-time prose as historical or update it. This is not evidence of mismatched tested source: the file hashes match. It is a reviewer-facing ambiguity to remove before publication.
2. **Required when actually submitting:** make the referenced evidence packet reachable from the PR. PR-v2 currently says hashes and logs are in “the evidence packet” without a concrete link. Link the final packet/manifest and committed README when the publication destination exists. No need to copy the full evidence narrative into the PR description.
3. **Optional reproducibility improvement:** add or reference the precise source-provider build recipe and source provenance corresponding to the four supplied library digests. The new runner itself is checkout-scoped and accepts explicit dependencies, which closes the previous hard-coded-path defect. Rebuilding those exact source providers still requires more than the README's “authentic source build” direction; the source archive digest alone is not a complete build recipe. Original-provider reproduction and check-only validation are already narrower practical routes.
4. **Optional diagnostic improvement:** on TimeoutExpired, retain any partial compiler/probe output and record a timeout stage. The current catch correctly returns failure, but build.log/run.log are written only after subprocess.run returns normally, so a timeout can leave less diagnostic evidence than the README's general retention wording suggests. This cannot produce a false pass.
5. **Optional only:** remove the inherited final blank-line deletion if production ownership permits. It remains harmless and should not trigger another provider matrix by itself. Broader regex grammar, command execution, warning cleanup elsewhere in the parser, and x64 project enablement remain outside this fix.

## Recommendation

Proceed toward submission after the final identity/link cleanup. The substantive improvement is regression discrimination tied to the actual caller plus reproducible, bounded provider testing—not merely a larger assertion count. The retained external TU evidence adds confidence without disguising its dependencies. No further production rewrite, vendor runtime workload, full-client link, or game command test is required for my approval of this capacity correction.
