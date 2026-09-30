# Vendor decision investigation

Updated 2026-09-30. Work continues alongside the native x64 client conversion.

## Contract

The user wants a working 64-bit SWG client that preserves the original game experience and fidelity, with no feature removal or placeholder vendor implementations. The user has no licensed x64 Miles, Bink or Vivox SDK. They asked for deep pros, cons and options for every third-party blocker and continuing agent orchestration. Existing context is specific enough to waive a redundant intake exchange under POODO.

The target is the SWG-Source client and its real assets, including the project's documented feature removals (see BASELINE.md). Restoring historical SOE browser/TCG features is outside this conversion. A 64-bit game process with genuine 32-bit supporting processes is an architectural option, not yet the chosen implementation. A complete conversion means a full link, startup and representative functional/runtime acceptance; compiling isolated libraries is insufficient. No finite fixture proves universal equivalence. Differences remain findings to explain and resolve rather than permission to redefine the user's fidelity requirement.

Authorized: source and documentation work, local experiments, native VM builds, agents/CLI workers, commits and pushes to Akilleez-QA forks. No upstream mutations, new PRs, issue comments, vendor contacts, purchases, service-account creation, feature disabling or redistribution of game assets/proprietary binaries.

Latest destination instruction: the finished work should eventually target SWG-Source/client-tools `x64`, not `master`. The user explicitly requires completion and separate approval before any upstream PR. Continue development/evidence on our fork; inspecting upstream is read-only. Do not rebase, merge or change the working baseline merely because the eventual target differs.

Read-only GitHub branch listing on 2026-09-30 did not return an `x64` branch (master remains 94945103). Record `x64` as the user's intended eventual destination; do not invent a present ref or silently redirect a future PR to master. Resolve the actual target when the user approves submission.

## Questions that can change the decision

- Which dependencies are actual link inputs, runtime loads, optional reachable features, inactive source or tool-only dependencies?
- Is the implementation source available, or only headers and wrappers? Can its original algorithms be rebuilt natively?
- Does an authorized x64 provider exist at the required version, and what changed between it and the original?
- Where can an original 32-bit implementation be isolated without moving callbacks, clocks, ownership or presentation semantics?
- Does a replacement preserve actual outputs, not just API names or a feature checklist?
- Which dependencies require a remote service, credentials, hardware or native GPU? A DLL architecture fix cannot supply those.
- What are installation, update, license, portability and maintenance costs? Availability is separate from entitlement.
- What is the smallest experiment that can reject each plausible route before the project commits to it?

## Evidence map and ceilings

| Region | Current evidence | Still required |
| --- | --- | --- |
| Source / ABI | Real client wrappers, headers, call sites and conditional compilation | Native evaluated definitions, full link extraction and runtime load traces |
| Binary availability | Bounded local PE/COFF inventory; user reports no other licensed x64 SDK | Exact provider version/rights for any new SDK |
| Media behavior | Source inventory and callback/service/presentation analysis | Stock traces, output captures and actual cross-process comparisons |
| Services | Vivox/TCG integration code and official migration documents | Working provisioned service and two-client acceptance where relevant |
| Build | Existing native baseline and per-root-cause probes | Full current-snapshot build and link; actual game execution |
| Fidelity | Known Win32 baseline; explicit unresolved DPVS/numerical limits | Same assets/settings/devices, controlled stock variation, per-feature comparisons |

Favored hypothesis to test: retaining original media implementations may preserve more behavior than replacing them. Strongest rival: the new process boundary changes callback scheduling and latency enough that a carefully matched native backend is less disruptive. Reusing the DLL alone does not decide this. Stock event/output traces and a bounded original-runtime helper experiment can discriminate.

## Parallel work and independence

- Native build agent: isolated, source-hashed full builds and real link/root-cause evidence.
- Audio agent: actual Miles calls/assets and Debug x64 fixture failure, plus native/replacement options.
- Secondary-vendor agent: browser, TCG, capture, LCD and other dependencies, with source and current primary research.
- Composer CLI: broad fresh dependency/reachability search, including dynamic plugins.
- Grok CLI: rival architecture critique from source, including helper drawbacks and alternative boundaries.
- Codex CLI: Bink original-runtime/asset experiment. Its separate allocator fault-reproduction request was rejected by the CLI safety filter; that request was not retried.
- Parent: source spot checks, primary research, evidence reconciliation, production commits and publication.

Source-reading agreement is not independent runtime corroboration. Shared context and evidence are disclosed. Each worker owns separate scratch output; only the parent commits production changes. New contradictions reopen the affected claim before further promotion.

## Prospective experiment boundaries

1. Allocator split: after the CLI rejection, use source/layout analysis and candidate-only invariant checks with the real allocator. Validate adequate allocated/free-node size, payload preservation and bounded allocation/free/reallocation on both ABIs. Parent did not execute the previous invalid allocation sequence. This is source repair work independent of choosing a vendor backend.
2. Native full build: freeze all source inputs and evaluate architecture-specific paths before builds; preserve every failure and group by root cause. A zero compile count is not a complete link or runtime claim.
3. Bink: establish original runtime identity and actual asset, decode bounded frames with the original 32-bit DLL; optionally transport results to an x64 driver. Prediction concerns real decoding and architecture communication only. It does not establish sound, timing, TreeFile integration or complete player fidelity. Compare FFmpeg output separately and retain differences.
4. Miles: establish stock callback nesting, service cadence, device/provider and output behavior before selecting a bridge. A compiled callback probe is not audible fidelity evidence.

No production vendor backend is selected by these experiments. Successful experiments narrow uncertainty; failed ones remain part of the decision packet. Work continues on independent conversion paths while external service/SDK questions remain unresolved.
