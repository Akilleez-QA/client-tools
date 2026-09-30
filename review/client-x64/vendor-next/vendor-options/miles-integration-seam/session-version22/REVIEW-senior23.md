# Independent senior review — SessionVersion22

Reviewed 2026-09-30. **Accept as a bounded experimental component correction. Engineering: 8.5/10. Narrow experimental readiness: 9/10.** These are judgment ratings, not probabilities or product-readiness scores. No blocking correctness defect was found in the held-handle adapter or portable response handling under their documented preconditions. Two nonblocking evidence-maintenance improvements follow.

The supplied `currentDll` reaches `LoadStringA` directly (`session_version_host.cpp:12`); neither a name lookup nor a compile-time version participates in that path. That is the correct mechanism for the requested handle-to-resource response. The original macro appears only in the controlled single-normal-module reference fixture. This review does not grant product adoption, live transport, Audio, device, playback, or full module-lifetime readiness.

## Findings

### P3 — Runtime verifier identity omits its imported helpers

`run_native.py:5–7` imports `digest`, `machine`, and `exclusive_json` from staged Python modules. Line 18 checks the launcher file against the build receipt, but does not check the currently imported helper files against their recorded build hashes. Comparing `builder_before` with `builder_after` at line 14 checks historical receipt fields; it does not establish that those helpers are unchanged when the runtime launcher executes. An ordinary helper edit after compilation therefore changes the verifier without causing the intended identity refusal.

Before reusing this as a durable launch gate, verify the current imported helper files against their entries in the externally pinned receipt, and record the relevant Python runtime identity for the runtime invocation. Perform that verification with a minimal trusted bootstrap before depending on the staged helpers. The current archive contains the helpers and its hashes agree with the build receipt, and I found no evidence that they changed during the recorded run. This is a gate-completeness issue, not a finding that the recorded native run used incorrect artifacts.

### P3 — Retain per-file identity for the exchange artifacts

`run_native.py:47–51` passes `version-reply.bin` and `macro-oracle.bin` to the consumer and compares `consumer-copy.bin` afterward, but the text results record neither the hashes nor sizes of those three files. `collect_evidence.py` excludes `.bin` files. The local review packet consequently supports the transfer result through the recorded executable checks and logged resource bytes, while providing no immutable identifier for the actual 133-byte reply consumed.

Record pre-consumption size/hash of both inputs, post-consumption size/hash of both inputs and the copied output, and require stable inputs. Preserve these in the final text receipt; preserving vendor binaries is unnecessary. This would make later artifact review more direct and detect accidental exchange-file changes. The current source, logs, and final byte-array record are consistent with the claimed transfer; this limitation does not negate them.

## Correctness and fixture assessment

- The host validates the request before resource access, rejects a null handle, initializes its bounded local buffer, rejects a zero resource result, checks termination at the returned count, and only then constructs the reply. Resource failure leaves the prior frame untouched. Rejecting an empty resource is explicit and compatible with the observed nonempty original version; it is not general preservation of every possible empty-resource behavior.
- The portable decoder requires a canonical result and matching request/causal/lane/lease context before the only destination write. It rejects missing, unterminated, embedded-NUL, oversized, malformed, and unexpected-field responses. Ownership is real: the frame contains bytes, and the destination copies only through the terminator. The source does not expose stack tail or retain a module-owned text pointer.
- The macro comparison is appropriately limited: initial basename absence, exact loaded-path check, and macro/adapter byte equality precede unload. The poisoned build separates the compile-time macro string from the observed resource string. The native reference shares the Windows resource implementation with the adapter; this is useful path comparison, not independent vendor corroboration.
- The two data mappings are distinct and the normal basename namespace is absent. This discriminates the removed basename dependency. **It cannot distinguish choosing the first copy from choosing the second copy because their contents are identical.** A future differential-resource fixture would strengthen runtime discrimination, but the present direct argument forwarding plus API contract already supports the narrow source-level property. `RESULTS.md` accurately states this limitation, so it is not an overclaim finding.
- The valid executable handle with missing resource is a useful failure control, more discriminating than a null-handle check alone. The native logs report unchanged-frame failure followed by successful mapped-resource queries and owned copying after release.
- Module validity, file verification, exclusion of concurrent unload, and session/lane admission remain caller responsibilities. The adapter has no ownership abstraction, integrated failure-response policy, or live transport. These are explicit boundaries, not hidden implementations.

Maintainability is good at this scale: a very small Windows adapter, portable wire logic, and no generalized loader mechanism. The repeated version21 include-guard/test labels in the copied version22 files are minor clarity debt. Do not refactor the frozen experiment merely to remove those labels; fix them if this becomes maintained reusable code.

## Evidence and independence

I formed the source assessment without reading version21's reviewer conclusions or any peer review. Version22's own prospective plan necessarily discloses the intended repair and prior problem framing; this is a limitation on blinding. I inspected the final result report only after the source pass. This reviewer ran no Windows/vendor/Audio/engine executable and inspected no private SDK header body.

Direct observations:

1. All 16 archive entries agree with `source-v1-manifest.json`. The 14 corresponding files available in the local component/dependency tree also agree. The two revision4 helper files are present in the source archive rather than at the archive-relative local paths.
2. All 11 native recorded source identities match the manifest, and archived builder/helper identities agree with the build receipt. Eight builds report success, unchanged before/after inputs, and expected x86/x64 machine types. Twelve launch records agree with their recorded build output hashes and external receipt pin; pre/post executable and DLL hashes agree. These are independently inspected records of the worker's Windows run, not a second native reproduction.
3. Logs report four 600-check wire runs, two 32-check normal host runs, two 33-check poisoned runs, and four 606-check x64 consume runs. The recorded resource bytes are `[55,46,50,97,0]` (`7.2a` plus NUL). The wrong-pin log reports rejection at the external receipt check. Source order confirms that this check precedes output-directory creation and subprocess launch.
4. Independently compiled only the portable suite with `g++ -std=c++11 -Wall -Wextra -Werror -O2 session_version.cpp wire_test.cpp ../transport-candidate/codec.cpp` and ran its temporary binary: **600/600, pointer_bits=64**, exit 0. Prediction before this run was that the unchanged portable logic would pass; failure would have blocked accepting the supplied wire evidence. This is an independent compiler/environment repeat of the same fixture, not an independent oracle.
5. Product checkout remained clean at `49d0eeed4ddaa177d7a93ea396c37c3d9b9942da` when inspected.

Verified SHA-256 identities:

| Artifact | SHA-256 |
| --- | --- |
| `source-v1.tar` | `74edc78ad96434eb6daf44b584a66096c037462370cbba1f4e75059c67e4f01c` |
| `evidence-v1/build-v1/receipt.json` | `b278f8582d5f5d6d4d77d3b8436403668f909a39331470d1f31e15b05c78e30e` |
| `evidence-v1/runtime-v1/results.json` | `fe65820abe560d592c9304967809187b17273f01be8d3e01d7c54f83a82d000d` |
| `evidence-v1.tar` | `e4e736a4c30479534bfd3dbe94c8f72f2453624f1d2246cca4586bedbaa5b1ee` |

## Bounded POODO review record

Opening exchange waived because the assignment specifies the exact correction, artifact, success surface, authority, and exclusions. Decompression: judge explicit held-handle resource selection, preserved bounded owned reply behavior, discrimination of competing explanations, and receipt attribution; do not infer client functionality from component fixtures. The strongest rival is that success comes from a constant, basename resolution, or a previously selected module rather than the supplied handle. Source tracing, poison control, namespace-absent data mappings, and missing-resource failure address different parts of that rival; identical resource contents leave differential module selection unobserved.

Research gate completed before convergence. Queries addressed `LoadStringA` module/length/zero-return semantics and `LoadLibraryEx` data/image mappings versus normal module lookup. Inspected sources retrieved 2026-09-30:

- [Microsoft LoadStringA](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-loadstringa), updated 2024-11-20: supplied module identifies the resource source; ANSI output is bounded and terminated; return count excludes NUL. It does not establish this private DLL's content or caller ownership.
- [Microsoft LoadLibraryExA](https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-loadlibraryexa), updated 2023-02-09: resource mappings and ordinary module loads have different initialization/visibility semantics; mapping handles support resource use. This limits what the duplicate mapping fixture represents.
- [Wine user32 resource implementation](https://raw.githubusercontent.com/wine-mirror/wine/master/dlls/user32/resource.c), moving upstream source inspected on retrieval date: independently shows instance-directed resource lookup and bounded ANSI conversion. This is a second implementation evidence family, not proof of Windows internals or the native fixture's outcome.

Exactly 20 paths were considered before deciding: (1) accept the bounded correction; (2) defer pending peer review; (3) require different-text resource fixtures; (4) add a portable argument-forwarding shim test; (5) independently rerun pure wire controls; (6) independently rerun native resource controls; (7) bind runtime helper identities; (8) retain exchange-file digests; (9) add a real pipe transfer; (10) add caller lifetime ownership; (11) define integration failure policy; (12) enforce a single-basename caller restriction; (13) enumerate and reject duplicate normal modules; (14) retain original macro execution as the implementation; (15) parse PE resources offline; (16) move resource reading into a dedicated process; (17) add locale/ANSI conversion controls; (18) inspect and cross-check the frozen build graph; (19) add resource-boundary fixtures for truncation/empty text; (20) stop if hashes or portable behavior contradict the report. These paths differ in mechanism, evidence family, integration scope, or disposition. Selected 1, 5, and 18, with 7–8 recorded as maintenance recommendations. Native reruns, alternate architectures, integration, and expanded vendor fixtures were outside this review's authority or unnecessary for this narrow verdict.

Topology covered source argument flow, wire bounds/ownership, reference-oracle correlation, duplicate mapping visibility, failure semantics, build/launch attribution, and product boundary. Unresolved frontier is explicitly caller lifetime, different-content selection at runtime, language/code-page variation, exchange-file retention, and real integration. Bounded saturation is sufficient for component disposition, not exhaustive correctness. Fan-out was considered at each transition and omitted: this is already the parent's independent review spike, and no descendant capacity was allocated. No peer agreement was counted as evidence.

`delivery_state`: review authored; portable component independently compiled and checked; native evidence inspected.

`outcome_state`: passed for the independently repeated portable fixture; recorded native bounded probes are internally consistent and support component acceptance.

`highest_justified_claim`: the frozen adapter uses the caller's supplied held module for resource 1 and produces a bounded owned canonical response; the recorded exact-DLL native probes match the restricted macro reference, with the stated evidence limitations.

`required_runtime_observation`: no new native run is required for this review's narrow disposition; actual integration still requires live transport, session/module lifetime, and failure-policy observation. Different-content module selection remains a useful optional stronger discriminator.

`who_controls_next_test`: parent integration owner within user authorization.

Reopen this verdict if any source/receipt identity differs, a valid supplied-handle resource query returns another module's content, or integrated lifetime/failure behavior contradicts the bounded contract. This review writes only this review file; all implementation and evidence artifacts are preserved.
