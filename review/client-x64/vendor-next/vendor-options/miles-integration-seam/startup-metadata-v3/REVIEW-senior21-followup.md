# Senior21 follow-up — frozen startup metadata v3

Reviewed 2026-09-30. Updated ratings: **engineering 8.3/10**, **experimental component readiness 7.5/10**. These assess this narrow component and its test harness, not a production backend or complete x64 client. Two original findings are closed; directory discrimination is substantially improved but only partially closed at the original finding's breadth.

This review preserves the original v2 review. I read v3 RESULTS.md and verified-results.json as reported claims, then checked actual source, receipts, PE hashes, and raw positive/mutant logs. No vendor or engine workload was executed. Fresh execution was limited to the portable C++ test and pure Python cleanup tests.

## Findings disposition

| Original finding | Disposition | Evidence and remaining boundary |
| --- | --- | --- |
| P2 directory fixture cannot establish requested path forwarding | **Partially closed** | host_test.cpp:23–30 obtains distinct direct results, resets to `.`, and dispatches `miles`. The frozen wrong-path mutation replaces the retained argument with `.`; both raw mutant logs fail line 30. However, the only dispatched path is still `miles`. |
| P2 cleanup exception skips owned sink unload/results | **Closed for the identified exception path** | cleanup.py:4–13 catches each ordinary cleanup-stage exception and continues; both runners invoke it in finally at :31–38. A fresh injected kill-timeout test still reaches unload/write; three injected errors still reach write. |
| P3 request limit eight bytes too large | **Closed** | metadata.h:8 separates MaxFrameBytes−136 request capacity from MaxFrameBytes−128 reply capacity. metadata_wire.cpp:38 uses the request limit. wire_test.cpp:44–52 encodes/decodes the exact limit, verifies offset 136, and rejects limit+1 at encoder and validator. |

### Remaining P2 test gap: only one candidate directory input

The exact original counterexample—an implementation that ignores the request and always invokes `AIL_set_redist_directory("miles")`—still passes. The new control demonstrates that the return-text oracle distinguishes `.` from `miles`, and that replacing the candidate's `miles` call with `.` fails. It does not exercise a candidate request whose expected result differs from a hardcoded `miles` result. This is source-level reasoning; I did not run a new vendor mutation.

Minimal completion: dispatch both valid paths and compare each immediately copied reply with the corresponding direct result; finish with `miles` before startup. Run a constant-`miles` mutant and require the dispatched-`.` check to fail. An omitted-call/stale-return control remains a separate property: results copied from an earlier call can still mimic a correct response without establishing a new vendor call. Instrumented argument/call-count controls can cover this without pretending a returned string is a non-mutating state query.

RESULTS.md accurately limits the current evidence to this specific wrong-path mutation and does not claim all omitted-call/stale-return variants. PLAN.md's opening “repairs the senior review findings” should be narrowed to “repairs cleanup and capacity findings and strengthens directory discrimination” until the second candidate input exists.

## Ownership and lifecycle improvement

metadata_host.cpp:25 retains validated input bytes before calling Miles at :27. SessionInputs::retain (metadata_wire.cpp:5–11) copies into a vector, places that allocation in a stable list entry using swap, and does not modify or remove earlier entries. The cumulative logical-byte check precedes allocation and vendor dispatch. Allocation exceptions before the call cannot have handed Miles a temporary pointer. If output copying later fails, the retained input remains owned.

host_test.cpp:18–19 declares SessionInputs before Session, so Session's shutdown happens before retained inputs are destroyed. This removes dependence on an unproven vendor input-copy guarantee for dispatched directory inputs in this fixture. metadata.h:10 expressly makes the same lifetime obligation the future integrator's responsibility. It does not prove that a future host will satisfy it.

The new ownership tests at wire_test.cpp:53–55 prove source-buffer independence for one entry and empty-input rejection. They do **not** dynamically test stability across multiple retained entries, exact cumulative-budget exhaustion, or allocation-failure behavior. Source supports those mechanisms, but add those pure tests before relying on their runtime coverage. The logical-byte budget is not a claim about allocator overhead or resident memory; RESULTS correctly says so.

## Verification performed

- Fresh strict portable build using g++ C++11, `-Wall -Wextra -Werror`, then execution: **39/39**, exit 0. Inputs: wire_test.cpp, metadata_wire.cpp, sibling transport-candidate/codec.cpp. This is a Linux pure-code result, not original Windows ABI validation.
- Fresh cleanup_test.py with bytecode writes disabled: **2 tests passed**. The injected exceptions cover the original skip-unload path and continuation through multiple stage failures.
- Recomputed every source-manifest.json entry: all match. Recomputed frozen-v3-review.tar against frozen-v3-review.sha256: match.
- Recomputed executed v3b receipt: `8c188c5531f30f6a13e2f256e42707279ce485a62b5f75f22865e0ffbf8263d9`. Checked all six output PE hashes and before/after input equality. Host source hashes match current frozen v3 files.
- Recomputed wrong-path receipt: `90801dc2e5c09723119953f3b024309df258590c278685734a1d5b8befeee768`. Both output PE hashes and input equality match; host source hashes match the private mutant. Its dispatch source differs only by substituting `.` for the retained argument at the redist call.
- Inspected evidence-runtime-v3b/Debug.log and Release.log: distinct direct path responses, **33/33**, mixer 64, fragment readbacks 16/64, speaker 2, and the qualified restore/shutdown call banner.
- Inspected evidence-runtime-wrongpath/Debug.log and Release.log: **FAIL line 30**, one-byte redist response, **32/33**, with the same qualified cleanup-call banner. These are expected mutant failures, not functionality passes.

The raw existing runtime records and receipts support same-vendor Wine observations and artifact attribution. This reviewer did not independently reproduce those vendor outcomes. Before/after hashes and receipts are trusted local provenance, not signatures or a hostile-filesystem defense.

Runner entrypoints reject optimized Python at lines 1–2, before imports and prefix creation. This makes the remaining assertion-based identity checks effective under the permitted interpreter mode. The recorded optimized-mode controls agree with this source ordering; I did not launch those runner entrypoints. cleanup.py makes independent attempts rather than guaranteeing external cleanup succeeds. The new banner accurately reports call invocation, not destruction of all internal SDK resources.

## Remaining unproven integration

1. Encoded request → decode → actual dispatch → encoded reply → client decode for every supported operation. V3 now proves the directory request boundary through validation, but host_test still directly calls dispatch with payload-only Bytes and offset zero.
2. SessionInputs ownership surviving real host shutdown, error unwinding, session replacement and concurrency. Pure stability/budget tests would strengthen the local owner but cannot establish the future lifecycle.
3. Client-visible return-string storage and lifetime, including null versus empty and errors after a failed response construction.
4. Session/lane ordering around global SDK error state and preferences. A same-thread fixture does not establish cross-request causal last-error fidelity.
5. Wrong-kind, retired, stale-generation and cross-session Driver handles with zero-vendor-call observations on rejection.
6. Omitted/wrong-call controls beyond the specific preference-value and directory-path mutants, additional speaker specs where supported, and previous-value-return mutations. The v2 previous-value prediction is correctly retracted in v3 documentation.
7. Real exception cleanup of vendor resources and preference restoration after abnormal paths. Current evidence supports normal call flow and pure runner cleanup control flow. No new claim about full SDK resource destruction is justified.
8. Arbitrary directory lengths accepted by the old SDK. The maximum-size inputs were exercised only in pure code, as intended.

The existing ABI, signed-value conversion, output text ownership and caller-specific whitelist conclusions from v2 remain sound on this inspected revision. None of the new evidence establishes engine startup, playback, callbacks, allocators, complete bridge behavior, or production readiness.

## Compact POODO follow-up record

The existing frame remained sufficient: verify three concrete findings on a frozen new revision, preserve v2, and report component-only readiness. The rival was “new passing tests exercise a narrower property than the closed-finding claim.” The relevant topology was repair → new source → discriminating test → receipt-bound artifact → raw observation → claim scope. Source and portable execution were directly inspected; runtime remained recorded evidence. Fan-out was considered at transitions and omitted because this is a targeted independent worker with no allocated descendant capacity and no separable new runtime authority.

Research gate: queries concerning list insertion/reference stability and Python finally/exception cleanup led to inspected primary [C++ draft list modifiers](https://eel.is/c++draft/list.modifiers) and [Python compound statements](https://docs.python.org/3/reference/compound_stmts.html#finally-clause), retrieved 2026-09-30. The draft supports the list-stability mechanism; Python documentation supports independent catching versus propagation. These separate language evidence families do not corroborate Miles runtime behavior or certify the old v120 library implementation. The disconfirming implication is that correct container lifetime and finally presence alone do not prove caller shutdown ordering or continuation after an unhandled cleanup exception; the actual code and tests must cover them.

Twenty materially distinct paths were considered before closure decisions: (1) close the capacity mismatch from encoded boundary evidence; (2) close cleanup continuation from injected failures; (3) partially close directory discrimination; (4) dispatch a second valid directory; (5) run a constant-`miles` mutant; (6) use call-count instrumentation for omitted calls; (7) test stale returned text; (8) test multiple retained entries; (9) exhaust the cumulative input budget; (10) inject allocation failure; (11) enforce session-owner destruction ordering in the integrated host; (12) exercise a complete serialized dispatch round trip; (13) test client output-string lifetime; (14) test causal last-error ordering; (15) test stale/wrong-session resources; (16) test multiple speaker configurations; (17) compare native Windows and Wine observations; (18) obtain exact-version SDK lifetime documentation; (19) narrow repair wording now; (20) defer production adoption pending integrated evidence. Selected 1–3 and 19 for the present decision; 4–16 remain targeted checks, and 20 preserves the scope boundary. No new vendor experiment was authorized or performed.

Predeclared execution expectation: unchanged portable baseline must report 39/39 and cleanup tests must pass; failure would reopen repair claims. Both passed. No conclusion was drawn from an unexecuted vendor control.

`delivery_state=checked follow-up report`; `outcome_state=two findings closed within tested scope, one partially closed`; `highest_justified_claim=improved experimental component with request-boundary and cleanup-continuation verification plus recorded specific wrong-path discrimination`; `required_runtime_observation=second candidate directory input/constant-path control and integrated transport/lifecycle observations`; `who_controls_next_test=primary agent under user-authorized scope`.
