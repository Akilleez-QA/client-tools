# Maintainer follow-up — network and PCRE round 2

Reviewed 2026-09-30, independently of peer reports. Prior reports are unchanged. I inspected committed production diffs, test sources, final PR drafts, identity records, native results and selected raw compiler/runtime logs. I did not run the tests, modify candidate files, or perform GitHub activity.

| Candidate | Reviewed head | Engineering | PR readiness |
| --- | --- | ---: | ---: |
| Network | `23849687c697520d8934049efc49f62e44fd9b6a` | 9.5/10 | 9.5/10, prerequisite-dependent |
| PCRE | `1df8947d7971567c014e8e4815f95ac64b5f9963` | 9/10 | 9/10 |

The round-1 substantive verification gaps are closed. I found no introduced production defect and do not require further production edits or unchanged-code reruns. The remaining limits below are real but proportionate to these small changes. Neither score is an approval of a complete x64 client or of the separate imemmove prerequisite.

## Network

The production diff remains the five-file pointer-width correction reviewed initially. It is explicitly based on `9eadbbbebd515a0fffad2133300703dff68bd7ef`; prerequisite changes are not being smuggled into the advertised five-file diff. The draft now clearly requires consistent rebuilding of affected x64 consumers and libraries.

The new runner supplies the missing implementation evidence: actual Sock.cpp, TcpClient.cpp and TcpServer.cpp compile in both architectures and configurations, 12/12. It derives relevant inputs from the checkout's project and documents the source-level x64 adaptation removing `_USE_32BIT_TIME_T=1`. There is no fabricated x64 project-build claim.

Full-TU controls independently revert each TCP completion-key local. The paired unchanged TU must pass. Inspected raw logs show the actual Windows declaration rejecting argument 3 from `unsigned long *` to `PULONG_PTR` at GetQueuedCompletionStatus in reverted TcpClient and TcpServer copies. This is much stronger and more relevant than raw API runtime evidence alone. The Win32 controls still compile. Header controls cover the three alias/member edits with both include orders and separate UDP variants.

I independently checked that the archived final runner and probe hashes match the committed files, all recorded production/project/prerequisite source hashes match, and all 152 recorded checkout include-file hashes match. Together with the packet's reported 166 binding checks, this resolves the precommit-versus-final-commit identity concern. A commit timestamp later than the run does not invalidate unchanged, hash-bound test bytes.

The native result list contains 100 accepted outcomes, including 12 successful production-TU cases and 60 runtime executions; the aggregate reports 1,260 assertions. Compiler metadata identifies native VS2013 18.00.40629 and SDK 8.1 paths. The 100 outcomes include expected compilation failures, not 100 successful compilations, and the draft describes that correctly. Likewise, 1,260 assertions are repeated checks across the matrix, not 1,260 independent behaviors. The valuable regression evidence is architecture/include-order coverage and each real call-site reversal.

The final runner uses fresh output directories, enforces per-case count and architecture expectations, binds negative cases to passing positives, and exits nonzero on unexpected outcomes. The retained older attempts should stay available but should not be the default evidence links.

**Final metadata housekeeping:** At inspection, `FINAL-IDENTITY.json` contained the correct `production_head` `1092728ace02e74b4a5c9887d9ad505d2d22421b` and tool hashes but omitted the final committed test head. The coordinating author reports that final-head metadata is being updated. Add `final_head: 23849687c697520d8934049efc49f62e44fd9b6a` and identify that head in the PR/evidence index, retaining the production-head field. This is not a stale-source or rerun issue. The score assumes this small announced publication correction is completed.

Remaining limits, not merge-blocking defects in this scoped patch:

- Runtime checks use raw Winsock/IOCP and do not execute production object methods. This is accurately disclosed. The actual TU and reversion checks are sufficient for the narrow declaration changes; no full runtime integration harness is demanded.
- The include manifest parser requires English `Note: including file:` output. README explicitly states that prerequisite. Future convenience improvement: force English output or reject missing include records rather than allowing a successful run with an incomplete manifest on another locale.
- The runner checks unchanged top-level source inputs at the end, but records included headers during compilation rather than taking a full before/after snapshot. For an ordinary stable checkout this is reasonable; it is not a concurrency-proof build-input attestation. No mismatch was found in this packet.
- Tooling is longer than the production patch but earns its scope by reproducing the three distinct surfaces: header compatibility, actual TU compilation, and raw API contract checks. I would not ask for more test infrastructure.

**Disposition:** ready to submit as a dependent PR after final-head metadata is present. State separately: “network change and scoped tests ready; merge blocked until imemmove is independently approved and merged.” Re-review/retest affected inputs if that prerequisite changes semantically. Do not infer its readiness from this network score.

## PCRE

The production fix remains the direct use of the existing array-extent constant. The lexical source assertion now checks the reviewed declaration chain, unique pcre_exec call, and negative-result guard. Its in-memory byte-count reversion is required to fail. A separately recorded reverted-source run also fails before provider execution. This closes the practical regression gap identified in round 1 without invoking an unsafe old call.

The source check is deliberately not a C++ parser, and the documentation says so. It may reject equivalent refactors or fail to reason about arbitrary conditional compilation; that is acceptable for a narrow structural assertion tied to a reviewed caller. Do not relabel it as executing production code.

The bounded runtime probe now verifies adjacent sentinels after both match and nonmatch. In `native-text-final-runner.zip`, the six `pr-pcre18-revision2/results-final/...` records each report 25 checks with successful compile/run status. Their runner and probe hashes match the final committed files. All six runtime logs identify PCRE `4.1 12-Mar-2003`. Current final-identity tool hashes also match the checkout. The archive intentionally includes earlier result directories whose runner hashes differ; these are history, not the final six-case evidence. Link directly to `results-final` when presenting the claims.

The actual caller source hash is consistent in all four additional TU compile results. The raw x64 logs show the disclosed four C4267 warnings per configuration. These compile checks use external development project metadata/headers, with PCH disabled; PR-v2 explicitly states they are not a clean build of the isolated branch. That separation is accurate and sufficient for this one-line, architecture-independent fix. Its merge does not need the broader x64 development stack or a replacement PCRE provider.

The checkout-scoped runner accepts explicit header/library inputs, records hashes and commands, refuses reused output directories, checks the version and pointer width in the runtime probe, requires the exact pass total, and returns nonzero for failures. It establishes the corrected API contract with the supplied provider; it does not authenticate an arbitrary binary merely because its version string says 4.1. README appropriately acknowledges this distinction.

Remaining limits and optional useful polish:

- Exact reproduction of the source-built x64 provider and the supplementary four-way caller compilation still requires separately supplied provider builds and development metadata. The committed runner and draft are honest about this. To reach a stronger reproducibility score, link a precise provider source/build recipe and input manifest, and supply a portable invocation for the optional caller compile. Do not expand the production fix to include vendor binaries or unrelated x64 headers.
- The source/probe/provider hashes identify the inspected inputs, but this runner does not compare all input hashes again after execution. A stable checkout/provider is an assumption, not a full immutable-build guarantee.
- A documented exact invocation using the repository's original Win32 library/header would be easier than placeholders for a first-time reviewer. That is ergonomic polish, since the required arguments and paths' roles are already clear.
- The unrelated final blank-line deletion remains. Restoring it is optional; it has no correctness impact and does not justify withholding this fix.

**Disposition:** ready to submit with the current explicit scope. No additional blocking revision identified. Preserve the separation between structural regression detection, real-provider bounded execution, and supplementary caller compilation; those three together support the change without claiming game-command execution or a clean x64 product build.

## Submission guidance

Keep PR bodies centered on the defect, correction, strongest discriminating tests, and actual dependency/coverage limits. Put extensive counts, historical failures, and manifests behind precise evidence links. Local publication status is not a quality deduction. Network must identify its independent prerequisite; PCRE can stand alone and should not be presented as waiting for unrelated x64 integration work.
