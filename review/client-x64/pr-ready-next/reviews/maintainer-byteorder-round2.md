# ByteOrder maintainer follow-up — round 2

Reviewed 2026-09-30 independently of sibling reviewer reports. The initial blind report is unchanged. This was a source/evidence inspection only; I did not build or execute the candidate or change its files.

**Engineering: 9.5/10. PR readiness: 9/10, conditional on separate prerequisite approval.** The earlier substantive ByteOrder validation concerns are resolved. No production-code revision or broader client build is required on the evidence reviewed. One small metadata correction remains before presenting the packet as final. Unpublished local evidence URLs are not a deduction.

## Reviewed artifact and evidence

- Current HEAD: `110c7b4ba7cf317760119c1b298fabe7d30b61d8` in `client-pr-next-byteorder-stacked`.
- Explicit prerequisite: `9eadbbbebd515a0fffad2133300703dff68bd7ef` (`review-ready/client-imemmove`).
- Production commit: `6bd1e1a275c9405e2e3da324df491d93ad374b97`.
- Relative to the prerequisite: 26 ByteOrder.cpp lines plus 163 lines of runner, oracle, and README. The production implementation is unchanged from round 1.
- Inspected PR-v2.md, stack-v2.json, results/summary/input hashes, archived raw compiler logs and commands, and actual committed test sources.
- All 192 entries in `stacked-v2-input-sha256.json` match the current checkout after normalizing Windows path separators. This includes production source, runner, probe, and headers. Across the four candidate compiler logs, all 36 distinct observed repository header paths are represented by the manifest. Therefore testing before the test files were committed does not itself create an evidence gap: the recorded test-source bytes match the committed ones.
- The current worktree has an untracked `tools/test-byteorder/__pycache__/` directory. It is outside the candidate diff and does not affect the native evidence; avoid including it in any later publication bundle.

## What improved and why it is convincing

The runner builds the real translation unit and public headers directly from its checkout, with explicit architecture/configuration flags and no dependence on old integration audit logs. The narrow standalone link suppression of an unused legacy STLport default-library directive is documented. The actual native headers are intact.

The four candidate matrix entries compile, bind all four byte-order symbols to production.obj, identify the expected object machine, and report exactly 166,631 input cases. The independent oracle retains exhaustive 16-bit coverage and broad 32-bit coverage. All ten outcomes in the control-enabled matrix satisfy their expectations, and the aggregate result verifies unchanged recorded inputs. Unexpected outcomes propagate a nonzero runner exit. Timeouts or setup exceptions also fail rather than silently pass, although they may not leave a completed summary.

The controls have useful, limited meanings:

1. Original Win32 passes with the same current headers, establishing retained byte-order behavior across the production source change.
2. Original x64 fails on C2485/C4235, and the raw log locates these errors in baseline.cpp's naked/assembly implementation. It demonstrates the original architecture incompatibility. The diagnostic test in the runner accepts either code anywhere in the log; the current archived evidence is sufficiently specific even though the generic classifier could be stricter.
3. The x64 no-swap mutation compiles and fails `FAIL long 80000000`, showing that the oracle rejects a plausible incorrect implementation. This mutates one function, not every function; that is adequate discrimination alongside direct checks of all four functions, not an assertion of exhaustive mutation coverage.

The explicit stack is the correct way to handle the discovered common-header dependency. Passing ByteOrder tests over that stack demonstrates the ByteOrder implementation with those prerequisite headers; it does not independently approve imemmove or prove its changed callers correct.

## Required final correction

`stack-v2.json` calls `6bd1e1a275c9405e2e3da324df491d93ad374b97` the `stacked_head`, while the reviewable committed head is now `110c7b4ba7cf317760119c1b298fabe7d30b61d8`. Preserve the earlier value as `production_commit` or `tested_production_commit`, set the final head accurately, and explain that the runner/probe hashes recorded during the run exactly match the final committed tests. PR-v2's wording “on production 6bd1e1a2 and the recorded test-source hashes” is truthful but should also identify the final submission head in the packet. This is a metadata update, not a reason to rerun unchanged code.

## Real reproducibility limits and optional polish

- The runtime prerequisites are explicitly Windows, Python 3, and VS2013/v120. The raw includes show Windows SDK 8.1. Name that SDK in the README/evidence metadata to spare a reviewer toolchain discovery work.
- The probe enforces `_MSC_VER == 1800`; compiler path and include paths are recorded, but exact compiler servicing version, SDK version details, and external toolchain/header binary hashes are not a complete lockfile. This prevents a literal 10 for exact environmental identity, but does not block this scoped fix. A short recorded compiler version would improve provenance without making the runner elaborate.
- The default reproduction command runs four candidate cases. The ten-case claim requires `--baseline`. README explains how to obtain the original bytes and enable controls; putting an exact ready-to-run baseline export command plus the control-enabled invocation next to the evidence would make reviewer reproduction easier.
- The runner's baseline classifier can accept an assembly diagnostic alongside unrelated errors. Candidate success with the same headers plus the inspected baseline logs resolves that ambiguity for this run. If hardening the runner later, bind expected diagnostics to the baseline source instead of expanding into a complex diagnostic framework.
- Source/header manifest coverage is sufficient for the observed run. It enumerates shared-library `.h` files rather than deriving the input set from include traces; a future dependency outside that set would need coverage expansion. This is not a missing input in the current evidence.

None of these points calls for changing the production API, replacing the test harness, testing packets/gameplay, or claiming a full library/client link.

## Describe prerequisite readiness separately

Use a concise dependency statement such as:

> Depends on the imemmove common-header PR at `9eadbbbebd515a0fffad2133300703dff68bd7ef`; review this ByteOrder diff against that prerequisite. This PR's actual-TU tests pass on the stack. The prerequisite requires its own review and must merge first; these results do not validate its other changed callers.

When an upstream prerequisite PR exists, replace the branch-only reference with its link and current revision. Report two distinct statuses: **ByteOrder implementation and scoped validation ready**, and **merge waiting for prerequisite approval/merge**. Do not assign an approval score to imemmove from this review: I inspected its commit scope to understand the dependency, not its full correctness evidence. If the prerequisite changes semantically before merge, rerun the affected ByteOrder matrix on the resulting stack; a metadata-only correction needs no rerun.

After fixing the stale head field, I would regard this as ready to submit as a clearly dependent PR, with merge gated on the separately reviewed prerequisite.
