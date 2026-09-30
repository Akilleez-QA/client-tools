# Blind review: sample-pipe29

Reviewed 2026-09-30. Verdict: the four-operation client subset is reasonable as a temporary source candidate; the staged tree is not integration-ready for the actual VS2013 x64 client / x86 original-DLL host.

## Scope and independence

Read the raw patch first, then the staged Session, Channel, LiveChannel and reply decoder, before inspecting client implementation, host routing, registry, native interface and portable test source. Did not read author RESULTS, existing review reports, candidate verdicts, receipts or test logs. The author test source was inspected only after the implementation; its tests were not executed. Compared the native-sample27 forwarding source as interface context, without executing it or assuming a native SDK64 binary exists.

Changes made by this reviewer: this report and files under `review-scratch-sample29/` only. No product/frozen source edits, VM, vendor, native host, game/engine, deployment or audio runtime execution. No descendant agents.

## Findings

### P1 — Actual host composition cannot execute the new client sample operations

Locations: `evidence-v1/stage/startup-bridge23/backend.h:48–68,105–119,152–163`; client request sites `backend-boundary24/pipe/ClientMilesPipe.cpp:346,366,380,388` within the same stage.

A normal `allocate_sample_handle(validDriver)` sends a nonnull Driver target. `Backend::execute` has no sample allocation route; it reaches the generic zero-target check at lines 105–107 and returns **InvalidFields**, before the Unsupported default. Query/end/release likewise supply a nonnull target and are rejected. Although the lower SDK dispatcher has query and end cases, this Backend's routing switch never reaches them. The lower dispatcher has neither allocation nor release cases. There is no creation/publication of OwnedSample registry identities, vendor release plus identity retirement, or sample cleanup bookkeeping at shutdown. The native host composition anchor calls exactly this Backend.

Consequently the client mock's successful sample identities and releases have no actual host counterpart. This is a missing integration blocker, not a defect in the client's refusal behavior. Before accepting an end-to-end sample seam, supply the narrow x86 host allocation/release lifecycle, route query/end, and establish sample registry retirement and confirmed shutdown behavior. Host-side bookkeeping allocation/failure handling must also avoid an unaccounted successful vendor allocation. No new audio engine is needed.

### P1 — The declared named-file step is missing from the usable sample path

Locations: `evidence-v1/stage/backend-boundary24/pipe/ClientMilesPipe.cpp:397–398`; `native-sample27/ClientMilesSample.h:14–15`; `native-sample27/sample_time.cpp:18–19` within the stage; root `prepared_input.h:9–44`.

The shared interface declares `ClientMiles::set_named_sample_file`, and the duration-use excerpt calls it, but the pipe implementation deliberately supplies no definition. A source search of the staged C++ confirms only the declaration, usage and omission comment. The standalone PreparedInput owner copies sealed bytes/suffix but is used only by tests; it is not an upload/bind request or host-owned sample lifetime. Therefore the real usage excerpt cannot link against this pipe subset alone, and no image is installed on a remote sample. This absence is honestly documented in source, but still loadbearing for the intended useful sample operation.

Keep it explicitly partial until a narrow named-file binding path owns the host image/suffix through the actual vendor-required lifetime, including failed bind/rebind and retirement. Do not substitute the unavailable native-x64 forwarding backend to fill this gap.

## Source quality assessment

No additional release-blocking defect found in the implemented client four-operation subset under the existing single selected-session/private-channel model.

- Allocation creates both the proxy and list node before `Session::request`. Local preparation failure cannot cause a remote allocation. Validated null results remove the unpublished proxy; known refusal remains an exception; uncertain outcomes fault the session and prohibit retries.
- Successful release erases storage, so ordinary repeated allocate/release does not accumulate lifetime tombstones. End preserves allocation identity. Release refusal leaves the local allocation available; uncertain release disables further requests. A raw pointer used after successful release is outside the interface lifetime; address reuse is not itself a valid-use bug or a reason to add permanent tombstones.
- `decodeReply` restricts allocation resources to OwnedSample, while the codec validates nonzero slot/generation. It allows only the two millisecond scalar fields for that opcode. The facade additionally rejects nonzero unrequested outputs before touching caller storage.
- Signed conversion goes through the existing signedValue helper; null output pointers become mask bits. Refusal, decode failure and channel failure occur before either output write. Successful confirmed shutdown clears proxies; refusal or unknown outcome does not falsely clear ownership or claim shutdown.
- Namespace placement matches the existing `ClientMiles` public facade and `ClientMilesPipe` private implementation. `SamplePipe28` and its include guard in the preparation-only helper are stale naming, a minor cleanup item rather than an ABI or functional blocker.
- Registry validation/retirement and buffer vendor lifetime are host responsibilities. Neither local proxy deletion nor Session abandonment proves remote release.

The list gives linear lookup/removal in the number of simultaneously live samples. This is simple and adequate for a temporary bounded slice; there is no evidence here requiring a new handle framework. Concurrency/reentrant calls through one Session are not established by this review.

## Independent portable check

Built and executed `review-scratch-sample29/blind_source_test.cpp` against the actual staged ClientMilesPipe.cpp, codec.cpp, metadata_wire.cpp and session_version.cpp using GCC 16.2.1, `-std=c++11 -Wall -Wextra -pedantic`, with the stage root as include directory. Compilation produced no diagnostics and execution exited 0:

```
PASS bounded source-only client/codec check; no native or host execution
```

The checked channel runs actual result encoding and reply decoding. Coverage: vendor-null model, 64 allocate/query/end/release cycles, four output masks, INT32_MIN and -1, query after end, refused release followed by successful release, refusal preserving outputs, lost reply preserving outputs, and no new request after terminal uncertainty. No global allocator overrides or broad fault injection were added. Successful shutdown and malformed replies were reviewed in source; this independent harness does not claim exhaustive test coverage.

These are mocks at the private channel boundary. They establish portable source behavior only, not actual vendor semantics, VS2013 compilation/linking, x64/x86 transport operation, named binding, cleanup ordering or audio behavior. No runtime approval follows.

## Integration readiness

Not ready. The decisive deficiencies are executable host lifecycle/routing and named binding, even before native target validation. The four-operation client patch can remain a separately reviewable temporary partial implementation; presenting it as a working Miles sample integration would exceed the evidence.

## Exact source identities

SHA-256 of the inspected implementation/interface/patch inputs and independently compiled units, plus the reviewer harness, are recorded below and in `review-scratch-sample29/source-hashes.json`. Paths are relative to this report's directory; `../native-sample27/native_sample27.cpp` is explicitly outside the stage and was comparison-only. Hashes identify this review's scope, not approval of every dependency transitively included.

- `patches/01-owned-sample-client.patch`: `337a4922c808ba33576f825ccb0299bcdeed679e9ad793ae0be7458614111247`
- `prepared_input.h`: `aa2304695b33aca618ba172e9b47a841ec433734898f68897a11d1f52e40c285`
- `client_test.cpp`: `2adcfe785d1d63dbdca6af060a335e3011692a1b4dba2455ec8a87121078a604`
- `evidence-v1/stage/backend-boundary24/pipe/Session.h`: `e74fea70bb6f2c2705bc9b1cc59022645eb4fde3ea7ad5cc0aa7de5ffbcea0bd`
- `evidence-v1/stage/backend-boundary24/pipe/Channel.h`: `3b5af2ca31784ce3f9438ad87271963f309980fd6910a190e9ccf9cdc4d9739e`
- `evidence-v1/stage/backend-boundary24/pipe/LiveChannel.h`: `de04d7421ed085f7fe2c0db1919176a64808fde076a31ae57f1e8b858b74aebc`
- `evidence-v1/stage/backend-boundary24/pipe/LiveChannel.cpp`: `84db1ca5753ff29f082c0cc29b1430ef33bbb44e68256fbb067fac9961f622a6`
- `evidence-v1/stage/backend-boundary24/pipe/ClientMilesPipe.cpp`: `3965228efa70458da5e17c0c29b26bfb45dccce961b0af5bebed3c0a10fd1b75`
- `evidence-v1/stage/startup-bridge23/reply.h`: `36b22cd1f74713b6b8ea8bea74c64d2c716ade2212ab9f3a7c9f154f12d69639`
- `evidence-v1/stage/startup-bridge23/backend.h`: `473f4f79dd01dd19b8a588b968a82b3fb4b97c40f0a2a84822dc3137c6fc524c`
- `evidence-v1/stage/host-candidate/host_dispatch.cpp`: `4810fd0dcad43c769e077f3c2ad8d3ad9ebffec426920ff6f5e0063bd4103595`
- `evidence-v1/stage/host-candidate/host_dispatch.h`: `e8b146c5f493d0a48c0a539494219b5a0e7a19405c9954ec32e84c1cda5b4a66`
- `evidence-v1/stage/transport-candidate/resource_registry.h`: `f2a4131c73d831a0e407bd67eb1803ec1f8a72ccd0cf36e6af979cae3e8a3768`
- `evidence-v1/stage/transport-candidate/codec.h`: `d95094b974c053ac4b9e0da1e442c0d7ce5291b22339acc9eafb821e209e60c0`
- `evidence-v1/stage/transport-candidate/codec.cpp`: `15ab7134eb837fa7c36323d28423ecfa33e8fec69e8a03e4411bef924aade33e`
- `evidence-v1/stage/native-sample27/ClientMilesSample.h`: `04f33063e540c3edc1a51e8f1c20cbe70b833128e31813dae0f522b4b3f94732`
- `evidence-v1/stage/native-sample27/sample_time.cpp`: `ce38cfe37ddfc892ead0eaa57aa29d67a99625c74b5a8f8354623b9f5edc7c55`
- `evidence-v1/stage/startup-metadata-v4/metadata.h`: `b9c8bbfb3cff6afbe85db418fa32428d1d649308bdaef1fa78bb0eb4ca40f1e8`
- `evidence-v1/stage/startup-metadata-v4/metadata_wire.cpp`: `14c2466b9a9fdcaadfd94b4dc930913a7268e429b15484eef18634a1afdb6fa2`
- `evidence-v1/stage/session-version22/session_version.cpp`: `eb92d358dfc983ebbfb09f44cff70ca30feaf8a8b5c3cffd85b4ffd47b0d084a`
- `evidence-v1/stage/pipe-native26/native/host_composition.cpp`: `4b690aebbf1901bf57f6669cef036d063b7916eee1c62c0281000e8ab730e573`
- `../native-sample27/native_sample27.cpp`: `d75624aedc9dc80cf79169bb45c8c019206d1f5bb0a8787a78950bef0d3a8304`
- `review-scratch-sample29/blind_source_test.cpp`: `95c0f11da49affa8d77962a98b9af56263e2b04466841e4b87c678aea38537cb`
