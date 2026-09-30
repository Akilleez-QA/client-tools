# Independent senior engineering review — startup metadata component

Reviewed 2026-09-30. Engineering **7.5/10**; readiness **6.5/10** for this experimental component and its validation harness, not the complete client. No P0/P1 implementation defect found in the supported caller-shaped operations. Keep it experimental until the discriminating controls and envelope integration checks below exist.

## Scope and evidence boundary

The assignment established the objective and authority sufficiently to waive another intake exchange: independently assess semantic fidelity, ownership, signed values, original SDK ABI, test discrimination, cleanup, unsupported inputs, and claims; write only this report. I inferred acceptance as a trustworthy narrow component experiment, not a replacement Miles implementation. I did not read parent summaries or other reviews, change source, run vendor/engine programs, commit, or publish anything. I inspected recorded raw logs and receipts; those are existing evidence, not a fresh independent reproduction.

The strongest rival to “the fixture establishes forwarding” is “the fixture observes already-established state or constants while a relevant forwarding behavior is broken.” Different valid directory inputs and omit/wrong-call mutations discriminate that rival.

Core source identities (SHA-256):

| File | Digest |
| --- | --- |
| metadata.h | ef46e5a6edf8d22c3efe13d01c5f91d53aecff16d3872cfd0967f5c0d01fc503 |
| metadata_host.cpp | e1257ffa2a035b1b53d36e407225409d23ddb94663f35d8ed6b0a16353389f44 |
| metadata_wire.cpp | 0d30548423bde3cf8000f02c0a828dafe5cf0fa18717740af289b8ba457dd3e5 |
| host_test.cpp | b43b1bb7e40d5da88cb4b00bf0034bb6f8177917c22347c5855b8f8a7f5c3366 |
| wire_test.cpp | 741c8a8d293ee6af854e5446f8d4afcdb082fe29bc7101b285027d64883623c6 |

These host sources match entries in native-v2/receipt.json. Its SHA-256 is d7826e5c760214ebe251bd000b3b561ba610b21cf8780092e92bfeac7d45b016; mutation receipt is 1dc1db6fcdc560b17e38331c35d73c5a83a6c174c25fafc616219a34e95528ba. Receipt identity supports attribution, not semantic correctness.

## Findings

### P2 — Directory fixture cannot establish that the requested path is forwarded

Evidence: host_test.cpp:21–24 establishes `miles` with a direct call, calls it directly again, then dispatches exactly the same path. The test compares only returned text/nullness. A regression that always passes literal `miles` instead of the input satisfies the fixture. The directory is already configured before dispatch, so this is also a weak sensor for whether dispatch changes vendor state. This is a test discrimination defect, not evidence that metadata_host.cpp:25 currently forwards the wrong path.

Minimal improvement: use two distinct valid private directory paths, obtain their direct-call results, reset to the first, dispatch the second, and check the resulting state through an independently justified observation. Add an ignored-input mutation and an omitted-call mutation with separately predicted failures. Keep path changes pre-startup as the caller does. If the SDK provides no non-mutating observation of the configured path, use an instrumented call-count/argument test for that property and label the vendor comparison as return-text evidence only.

### P2 — Cleanup exceptions can strand the owned null sink and erase results

Evidence: run-private.py:28–31 and run-mutation.py:28–31 execute `wineserver -k` with a timeout before unloading the owned PulseAudio module. A TimeoutExpired or process-launch exception at line 29 skips line 30 and all receipt writing. An unload exception similarly skips recording defaults and results. This defeats the harness's cleanup/accountability precisely on an off-nominal run. The normal logs do not exercise this path.

Minimal improvement: independently attempt Wine termination, owned-module unload, defaults capture, and receipt writing in nested `try/finally` or an error-collecting cleanup routine. Preserve the original failure and record each cleanup result. Test this using injected subprocess failures; no vendor run is needed to verify control flow.

### P3 — Request text limit is eight bytes larger than its encodable envelope

Evidence: metadata.h:7 defines `TextLimit = MaxFrameBytes - 48 - 80`, the reply payload capacity. metadata_wire.cpp:30 reuses it for directory request input. protocol-candidate/miles_wire.h:95–97 defines 48-byte Header, 88-byte Call, and 80-byte Result. transport-candidate/codec.cpp:117 plans calls with fixed 136 bytes. Thus validation accepts a text span of MaxFrameBytes−128 bytes, while encodeCall permits at most MaxFrameBytes−136 bytes. This does not bypass a correctly applied decodeCall, but the advertised component acceptance surface and wire surface disagree at the boundary.

Minimal improvement: define separate request and reply capacities, use MaxFrameBytes−136 for the request, and add exact-cap and cap+1 cases through encodeCall/decodeCall followed by validate. Also document that dispatch receives a previously validated envelope; its current tests deliberately use payload-only Bytes with offset zero and do not exercise the protocol's frame-relative offset contract.

## What is sound, and what the evidence establishes

- **Caller shape:** Audio.cpp:1285 immediately consumes the directory return as a string, :1297 reads mixer preference, :1306/:1313 consume error text, :1326 requests only channel spec. Audio.cpp:5118/:5125 writes fragment counts 64 and 16; the latter constant is at :152. The narrow whitelist is intentional and appropriate. It is not a generic preference implementation. The subsequent AIL_serve calls remain outside this component.
- **Original ABI:** the actual client-build-next original Mss.h declares signed SINTa returns/argument at :4149/:4155, char-pointer returns at :4158/:4410, and the five-argument speaker query returning a vector pointer at :4427–4434. metadata_host.cpp uses those declarations directly, requires v120 x86, and asserts signed 32-bit SINTa. It correctly ignores the speaker return pointer and supplies only the requested spec output. This is stronger than redeclaring a guessed signature. No claim about direct x64 DLL compatibility follows.
- **Signed values:** metadata_wire.cpp:6–10 range-checks before narrowing and transfers bit representations with memcpy. The host reconstitutes a signed value before SDK dispatch and preserves signed result bits. Tests cover −1, INT32_MIN/MAX, and out-of-range rejection without changing the destination. Those are helper/codec tests; the allowed real SDK setter writes are positive 16/64.
- **Text ownership:** copyText makes an owned copy before later SDK calls, distinguishes null from nonnull empty, bounds the scan, and leaves its destination unchanged on the explicit length failure. host_test.cpp:32–37 checks a captured error after changing vendor error state. This is meaningful ownership evidence. The contract explicitly trusts a valid vendor C string; no arbitrary-pointer safety is implied. Allocation failure remains an exception, as PLAN.md states.
- **Validation:** rejected fields return before the switch executes. Speaker dispatch resolves the Driver kind through RegistryResolver and rejects a null native address. The exact whitelist, absent outputs, and zeroed reply candidate reduce accidental capability expansion. Generic transport status interpretation remains a caller obligation.
- **Discrimination:** setter readback and distinct speaker sentinels are useful controls. Existing raw mutation logs show `FAIL line 44`, requested 16/actual 64, and 30/31 checks for both Debug and Release. The mutation demonstrates wrong-set-value detection. It does not demonstrate all missing/no-op/wrong-call variants.
- **Cleanup:** Session restores the saved preference and calls shutdown on normal returns and C++ exceptions after successful startup. The fixture relies on SDK shutdown for the open digital driver; it does not explicitly close/retire the registry entry. That is not established here as a resource leak, but neither the banner nor process exit proves per-resource cleanup. A cleanup banner is a control-flow sensor, not a shutdown-effect sensor.

Fresh reviewer execution: compiled only wire_test.cpp, metadata_wire.cpp, and transport-candidate/codec.cpp using g++ C++11 with `-Wall -Wextra -Werror`; the pure binary returned 0 and printed **30/30 metadata wire checks**. This is a Linux portable-code check, not a Windows ABI or vendor test. The existing native receipt records x86/x64 Debug/Release wire success and x86 host builds. Existing private-startup logs record 31/31 host checks and cleanup banners. Those source-bound recorded runs remain same-vendor Wine evidence.

One claim correction: PLAN.md:13 says readback and previous-value expectations must fail under the 16→64 mutation. The recorded logs show only readback failing. Both calls can return the same previous value regardless of the new value written; host_test.cpp:40 also recomputes later expectations from current state. Amend the prediction to the exact expected readback failure. Do not retrospectively claim a return-value mutation was tested.

## Missing intended-use checks

1. Real encoded request → decodeCall → dispatch → encodeResult → decodeResult for every supported operation, including nonzero frame-relative text offset, exact limits, and null/empty distinction. The current host path calls dispatch directly.
2. Independent omit-call/wrong-opcode/wrong-output tests for get preference, error text, directory path, and speaker query. Include changing error messages and multiple supported driver specs where the environment supports them. Constant 64 and stereo are insufficient to detect every constant-result implementation.
3. Wrong-kind, stale-generation, retired and cross-session driver handles, plus counters proving rejected inputs make zero vendor calls. Existing null-driver and field tests are useful but incomplete.
4. Exception/failure cleanup tests and explicit evidence of preference restoration on the failed path. Normal scope cleanup is structurally present; a banner alone does not measure restoration after an exception.
5. Input path buffer lifetime after dispatch: establish the vendor's retention/copy contract with exact-version documentation or a controlled test before a future receive buffer is recycled. Output ownership is directly implemented; SDK input retention is not established by a `const char*` declaration.
6. Integration-owned session/lane ordering, same-session last-error capture, and client-side returned-text lifetime. These are explicit future seam obligations, not reasons to broaden this component today. No engine startup, playback, allocator, callback or complete x64-client readiness claim is supported.

## POODO research and decision record

Observed topology: caller requirements → request/schema → validation → resolver → original SDK call → copied result → encoding → client consumption; lifecycle spans startup ordering, driver ownership, SDK global error/preference state, C++ exception cleanup and subprocess cleanup. Source/ABI regions were inspected; portable behavior was executed; native execution was assessed only from raw existing records; client transport integration and vendor input retention remain unresolved. This is bounded coverage, not exhaustive validation.

Research gate completed before final orientation. Queries: “site.learn.microsoft.com x64 calling convention pointer size long 32 bit” and “site.radgametools.com Miles AIL_set_redist_directory AIL_speaker_configuration”. Opened official [Microsoft x64 ABI conventions](https://learn.microsoft.com/en-us/cpp/build/x64-software-conventions?view=msvc-170) and [RAD Miles development history](https://www.radgametools.com/msshist.htm), retrieved 2026-09-30. Microsoft documents 32-bit long versus 64-bit pointers and the x64 calling model; RAD history supplies independent vendor context that redist setup precedes startup and Miles behavior evolves by version. These are two primary evidence families, not two independent validations of this binary. Public pages do not establish exact old-SDK ownership or this Wine run's correctness. That uncertainty changes the next test: verify retention and frame lifetime instead of assuming a pointer declaration proves copying. Exact local header/caller evidence remains controlling. Public history has entries of varying dates rather than one applicable release date; Microsoft page's displayed freshness is not a v120 compatibility guarantee.

Twenty distinct paths considered before convergence:

1. Retain the current narrow whitelist to contain the experiment.
2. Split request/reply capacities to align accepted payloads with envelopes.
3. Add changing-directory differential controls to expose ignored input.
4. Omit vendor calls in private mutants to measure no-op sensitivity.
5. Substitute wrong opcodes to measure dispatch identity sensitivity.
6. Add call-count/argument instrumentation to prove rejection-before-call.
7. Exercise serialized round trips to cover offset and reply ownership handoffs.
8. Add stale-handle lifecycle cases to test resolver admission.
9. Inject allocation failures to test exception-state behavior.
10. Inject cleanup subprocess failures to verify independent cleanup attempts.
11. Explicitly close the fixture driver to make resource cleanup observable.
12. Test multiple speaker configurations to distinguish constants from query results.
13. Test SDK input-buffer retention before buffer reuse.
14. Compare a native Windows run with Wine to expose environment dependence.
15. Obtain exact-version vendor guidance for ambiguous pointer lifetime.
16. Add client returned-string storage integration to preserve caller lifetime.
17. Audit lane/session ordering around last_error to preserve causal error text.
18. Narrow the mutation prediction to the observed readback property.
19. Defer client integration pending transport and lifetime checks.
20. Stop at a documented source-review result if runtime authority remains absent.

Selected minimal actions: 2, 3, 6, 7, 10 and 18; retain 1 and defer product claims under 19. Other experiments can follow when their uncertainty becomes load-bearing. Runtime actions were not authorized for this reviewer. Fan-out considered at each transition and not used: this is already the primary's blind independent worker, no descendant capacity was allocated, and extra same-source reviewers would not supply independent runtime evidence. Independence is in prompt/conclusion isolation and fresh source examination, not model family or artifact.

Precommitment for this review's sole execution was a strict portable build and existing 30-check pure test; nonzero exit or failed check would disconfirm that narrow baseline. It passed. No intended-use vendor validation prediction was executed here.

Terminal state: `delivery_state=checked report`; `outcome_state=passed for portable baseline, inconclusive for full forwarding discrimination`; `highest_justified_claim=source-aligned narrow metadata component with portable tests and source-bound recorded same-vendor controls`; `required_runtime_observation=changing-input/omitted-call controls and serialized intended-use handoffs`; `who_controls_next_test=primary agent within user-authorized runtime scope`.
