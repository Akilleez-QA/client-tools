# Akilleez-QA client/server x64 work

Verified against GitHub on **2026-10-01**. **58 upstream PRs are open and ready for review: 46 client and 12 server.** All agreed packages have upstream submissions; review and merging remain with SWG Source. This is submission completion, not a claim of complete gameplay or audiovisual equivalence.

Start with the [complete PR index](REVIEW-INDEX.md). It lists every head, scope, diff size and dependency group. The [fork-to-upstream map](package-inventory/fork-preparation-map.md) connects all 36 earlier preparation reviews to their actual upstream PRs. The [JSON ledger](package-inventory/submission-ledger.json) records all 94 URLs without counting preparation PRs as additional packages.

## Where to find the work

| Location | Role |
|---|---|
| [Client integration](https://github.com/Akilleez-QA/client-tools/tree/integration/client-x64-next) / [Miles implementation](https://github.com/Akilleez-QA/client-tools/tree/implementation/client-miles) | Both at `eca74ffa5741f608a1417944b2e2602868936517`; the maintained combined implementation and its recorded runtime evidence. |
| [Server integration](https://github.com/Akilleez-QA/src/tree/integration/windows-shared-compat) | Shared compatibility work at `731d85cc10326f5f2d656b4b66f09c5feab30635`. |
| [Server LP64 branch](https://github.com/Akilleez-QA/src/tree/lp64-fixed-width-boundaries) | Server #35 at `6b998f6fc281a88a50a710d7ae6afd55814b1946`, targeting upstream `64-bit-types`. |
| [Final client regression composition](https://github.com/Akilleez-QA/client-tools/tree/submit/client-regression-ci) | Client #67 at `49ad4dc9da9fb19e0ef761c192a68fe12b83f7be`; separate composed submission/testing tree. |
| Fork `master` branches | Legacy source baselines with fork navigation. They do not contain the combined x64 implementation. |
| `review/client-x64-evidence` | Review packets, historical results and the current submission index; not a game build branch. |

The source inventories and submitted heads have different purposes. Later packaging, CI and TrackIR corrections are recorded in the submitted PRs; do not treat the maintained implementation SHA as the head of every PR. Follow the exact head and reproduction instructions in the package under review.

## Qualification

- **Server:** all reported checks on all 12 submitted upstream heads are successful. Previous failures remain in GitHub and the evidence records. The workflow repair is server #38; affected PRs include it separately from production changes.
- **Client:** no upstream checks are reported. Evidence consists of the scoped native/fork checks linked from each PR. [Final fork run 36903954547](https://github.com/Akilleez-QA/client-tools/actions/runs/36903954547) passed at client #67's submitted head: wire 71/71 Win32 and 78/78 Win64; ByteStream 85 and decoder 34 per ABI; dependency ownership 12; sanitizer assertions 298 EOS, 1,047 Bink protocol and 22 video admission. These are separate suites, not a full-client correctness score.
- **Build/runtime baseline:** the recorded complete VS2013 Release-x64 dependency rebuild had 0 errors and 3,274 warnings. [Bounded mixed-width sessions](https://github.com/Akilleez-QA/client-tools/blob/eca74ffa5741f608a1417944b2e2602868936517/tools/test-wire-compatibility/live-session.md) cover all four Debug client/server architecture pairings, plus a Release x64/64-bit-server follow-up. Recorded original-provider movie replay and ordinary-close behavior are summarized in the [product evidence checkpoint](REVIEW-INDEX-before-final-packaging.md#product-evidence-checkpoint). Each result names its own source and environment; these are not fresh full-game runs of every split PR.

Native Windows GPU behavior, representative gameplay, hardware integrations and complete audiovisual fidelity remain outside these bounded results. Warnings, failed attempts and unobserved helper-exit behavior are retained in the linked reports. A passing package check does not resolve those limits.

## Review and merge order

Review independent source fixes first, then their consumers. The [index](REVIEW-INDEX.md#dependency-batches) describes allocator, build, wire and media chains. Stacked upstream PRs include true prerequisites in their whole-PR diffs and provide incremental comparisons; do not add cumulative PR totals or apply the same prerequisite twice.

Client submissions target upstream `master`. Server #35, #46 and #47 target `64-bit-types`; #46/#47 include #35 as a prerequisite. The other server submissions target `master`. Fork preparation reviews keep their original incremental bases and are historical, even while still open as drafts. No PR has been automatically merged or history rewritten.

## Source accounting and media

The frozen maintained client inventory contains **12,761 changed production lines (+11,965/−796) in 220 files**, including 9,852 Miles/Bink runtime lines under `tools/miles-bridge/src`. Tests, build tooling and documentation are excluded. All 220 production and 83 build/configuration paths are assigned to submission packages. The [accounting record](package-inventory/remaining-units.md) explains the two-line diff-algorithm difference and the separate later TrackIR correction. This is not an equal-scope comparison with the entire PR21 migration.

The [media status](vendor-next/vendor-options/miles-integration-seam/CURRENT-MILES-STATUS.md) describes the temporary original-provider process backend and its replacement boundary. No licensed native x64 Miles runtime is bundled or claimed. The [source index](vendor-next/vendor-options/miles-integration-seam/RUNTIME-SOURCE-INDEX.md) points to maintained code rather than frozen experiments.

Historical reports keep their original evidence and limitations. Their old statements about unlinked clients or unsubmitted PRs describe those snapshots; this page and the PR index are the current navigation points.
