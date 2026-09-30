# Small client change candidates — blind review and revision

These are fork branches and local PR-body drafts, not new upstream PRs. Existing client PR 22/23/24 are unchanged. Production integration remains 49d0eeed4; the x64 game still does not link because Miles imports are unresolved. The separate media experiments do not establish original-game fidelity.

Two fresh Astra agents received no conversation history or peer reports: one acted as an upstream maintainer, the other as a senior engineer. They inspected the actual diffs, surrounding source, test code and raw historical evidence. Their initial scores were 5–7/10 for submission readiness despite generally sound production changes. The parent then implemented their concrete requests, ran native checks on explicit candidate trees, and returned the revised packets for independent follow-up. Both reviewers use the same model and source evidence: agreement is review opinion, not independent runtime corroboration.

| Candidate | Production delta for this review | Final review head | Dependency |
|---|---:|---|---|
| ByteOrder intrinsics | 26 added lines / 1 file | `110c7b4ba` | imemmove prerequisite |
| Socket/IOCP widths | +9/−6 / 5 files | `23849687c` | imemmove prerequisite |
| PCRE capture count | +1/−2 / 1 file | `1df8947d7` | master 94945103 |
| imemmove prerequisite | +7/−7 / 4 files | `3b00af629` | master 94945103; reviewed separately |

Test tools are separate from those production counts: 163, 363 and 172 lines for the first three candidates, plus 176 for imemmove. No media bridge or build-configuration work is mixed into these three candidates. Exact bases, full hashes and compare links are in [candidates-v2.json](candidates-v2.json).

## What changed after the blind reviews

- **ByteOrder:** a checkout-scoped runner, independent byte oracle, production symbol/machine checks, strict failure propagation and baseline/mutation controls. Fresh native Win32/x64 Debug/Release each pass 166,631 cases. The master-only attempt exposed Misc.h's existing x64 ambiguity; its failure is retained, and the prerequisite is now explicit.
- **Network:** actual Sock/TcpClient/TcpServer TUs compile on both ABIs/configurations. Reverting each real completion-key declaration independently fails x64 SDK type checking; both header copies and include orders are covered. 100 expected compiler outcomes, 60 bounded API programs and 1,260 assertions passed. This does not claim production TCP runtime coverage.
- **PCRE:** the tool binds the actual declaration/call argument structurally and rejects a reverted count before any provider call. Six final native provider/configuration cases pass 25 checks each; a reused-output test fails without changing old results. The actual parser also compiles using explicitly separate development headers/configurations; that is not an independent x64 branch build.

## Reviews and remaining gates

[Initial maintainer review](reviews/maintainer-round1.md) and [initial senior review](reviews/senior-round1.md) are preserved unchanged. Follow-up reports live beside them. Current maintainer ratings: ByteOrder 9.5 engineering/9 readiness, network 9.5/9.5, PCRE 9/9. Senior follow-up ratings: ByteOrder 9.5/9, network 9.3/9, PCRE 9.5/9. See the [review comparison](reviews/SUMMARY.md). Ratings are not merge approvals or a claim of perfection.

Final head metadata now distinguishes the tested production commits from later commits containing byte-identical test tools. The imemmove prerequisite received its own two fresh blind reviews. Both scored it 9/8.5 initially, identified the expected-error classifier weakness, and raised engineering/readiness to 9.5/9.5 after the strict parser, 14 safe controls and fresh eight-case native matrix. These are separate dependency reviews; passing dependent function/TU tests alone did not approve its other callers. Final upstream target/approval and full x64 client acceptance remain separate. No new PR, reviewer request, comment or upstream mutation has been made.

The four narrow production patches total 58 changed lines; the 874 test/tool lines are counted separately. This is a focused batch, not the complete x64 migration.

Use [imemmove PR draft](imemmove/revision2/PR-v2.md), [ByteOrder PR draft](byteorder/PR-v2.md), [network PR draft](socket-widths/revision2/PR-v2.md) and [PCRE PR draft](pcre-count/revision2/PR-v2.md). Evidence is versioned; failed attempts remain visible. Raw evidence is a supplement to the small source/test diffs, not extra code proposed for the product.
