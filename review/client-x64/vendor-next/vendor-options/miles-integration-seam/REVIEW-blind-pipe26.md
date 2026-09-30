# Blind source/test review: pipe-startup26

Reviewed 2026-09-30. **No confirmed implementation defect found in the seven-operation patch within the inspected source boundary.** This is not runtime acceptance or evidence of production readiness. The new host dispatch branch has no execution coverage in the supplied portable test target.

## Scope and independence

Read the raw patch, staged `private-stage-v2` implementation, `tests/seven_operations.cpp`, and `check-portable.py` before any worker conclusions. Did not read worker RESULTS or other review conclusions. Also followed the staged codec, registry/resolver, reply decoder, session/channel, and signed-value helper; read the existing unstaged `startup-bridge23/bridge.cpp` and `live-bridge-candidate/admission.h` to establish their caller contracts. The parent supplied a later scope clarification that the old 23-request fixture is intentionally unchanged and host work is currently compile-only. That clarification did not replace source inspection.

No vendor DLL, Windows VM, engine, native Miles runtime, or production integration was executed. Safe Linux scripted tests ran only in the new `pipe-startup26/review-scratch-blind-pipe26` directory. Original sources were not edited. The original portable driver was not rerun in place because it creates fixed, already-existing output/stage directories.

Paths below are relative to this seam root unless prefixed by `stage/`; `stage/` means `pipe-startup26/private-stage-v2/`.

## Findings and coverage limitation

**No actionable source defect established.** The following is a proven test-coverage limit, not a claim that host dispatch is broken:

- `pipe-startup26/check-portable.py:43–46` builds the facade, codec, session-version implementation and metadata wire helper. Neither `stage/startup-bridge23/backend.h` nor `stage/host-candidate/host_dispatch.cpp` is compiled into the seven-operation target. `pipe-startup26/tests/seven_operations.cpp:60–110` serializes/decodes the request and supplies an independently scripted reply; it never invokes the host implementation.
- Concrete missed regression: removing the new `Backend::execute` cases at `stage/startup-bridge23/backend.h:48–66`, routing a case to the wrong SDK call, or breaking host-side refusal mapping would leave this portable target unaffected. This was tested more strongly by adding `#error BLIND_REVIEW_HOST_DISPATCH_NOT_COMPILED` at the top of the **scratch copy** of `backend.h`. The seven-operation test still compiled and passed all 1,267 assertions under ASan/UBSan.
- Useful next coverage, before claiming the branch is behaviorally verified: an isolated host harness invoking the actual `Backend::execute` branch and actual dispatcher with SDK-call spies. Exercise all seven success mappings; malformed unused values, output masks, callbacks, byte/text spans and secondary resources; wrong-kind/stale handles; and pre-start/post-shutdown refusal. Assert zero SDK calls on refused requests and exact scalar/float arguments on accepted calls. A v120/x86 compile check alone cannot establish these behaviors. This review does not require vendor runtime execution to close that test gap.

Experiment command lists, exits and outputs are retained in `pipe-startup26/review-scratch-blind-pipe26/experiment.json`. Both normal and host-poisoned runs printed `PASS 1267 scripted-framed checks; no vendor execution`. The number counts assertions, not independent scenarios or host tests.

## Trace results

**Early host dispatch is not an unvalidated bypass.** `stage/startup-bridge23/backend.h:56–60` enforces started/not-shutdown before delegation. The later generic backend field check at line 105 is skipped, but the delegated `stage/host-candidate/host_dispatch.cpp:57` independently rejects reserved fields, callbacks, both span offsets and lengths, and a secondary resource. Per-operation cases reject every unused scalar and all output-mask bits: room getter lines 108–114; rolloff/set-room/listener cases lines 171–205; serve lines 323–328. The six driver cases require a live Driver resource; serve requires a completely null target. `stage/host-candidate/registry_resolver.h:11–17` restricts kind and delegates slot/generation/state matching to `stage/transport-candidate/resource_registry.h:103–117`.

Header/framing validation remains the caller's responsibility, not `Backend::execute`'s. The existing bridge calls `decodeCall`, then checks Request kind, monotonic request identity, lane and zero lease/causal fields (`startup-bridge23/bridge.cpp:99–102`), checks referenced-resource liveness and coordinator admission before execute (lines 117–139). The staged codec checks bounded frame length, envelope kind/opcode, reserved fields, handle shape and canonical complete spans (`stage/transport-candidate/codec.cpp:135–158`). I found no specific malformed request that passes those paths and bypasses the dispatcher's seven-operation field/resource guards. The unchanged fixture's fixed sequence is not evidence that the new runtime sequence has been integrated.

**Pointer identity and lifetime.** The new `driverCall` checks session state, null and exact selected-session pointer identity before reading `driver->owner` or `driver->wire` (`stage/backend-boundary24/pipe/ClientMilesPipe.cpp:72–79`). It therefore avoids dereferencing arbitrary foreign pointers. Calls after shutdown or terminal channel failure stop before dispatch. The driver allocation remains owned by the session; these additions do not transfer or free it. The tests explicitly exercise null/address-1 rejection for all six driver calls and all-seven post-shutdown refusal (`pipe-startup26/tests/seven_operations.cpp:184–195`). They do not test allocator address reuse across destroyed/recreated sessions; no cross-session stale-pointer guarantee is established by these tests, and that is an inherited raw-handle lifetime limitation rather than a demonstrated new patch defect.

**Scalars and return values.** The facade copies F32 representations with `memcpy`, sends the expected 3/3/6/1 scalar counts, and uses zero-initialized calls. The host reverses that representation through `f()` and reconstructs signed room arguments with `s()` (`stage/host-candidate/host_dispatch.cpp:9–12`). Room return bits are explicitly permitted in `stage/startup-bridge23/reply.h:72–76`, decoded as signed 32-bit via `MilesStartup::signedValue`, and returned as `int32_t`. Negative one, minimum signed 32-bit and zero getter/setter values are tested; orientation also carries infinity, a quiet-NaN payload and a subnormal in the framing test (`pipe-startup26/tests/seven_operations.cpp:156–183`). No host ABI/FPU behavior for these values was executed here.

**Exceptions and reply shape.** Known refusal statuses throw distinct facade failures; channel/decode exceptions set a terminal fault in `Session::request` (`stage/backend-boundary24/pipe/ClientMilesPipe.cpp:122–141`). The seven tests cover recoverable InvalidFields refusal, transport throw, correlation corruption, forbidden result fields and no subsequent request after uncertainty (test lines 198–223). The reply decoder rejects unexpected scalars/resources/spans/null flags and allows a room scalar only on Success (`stage/startup-bridge23/reply.h:55–108`). Direct scripted replies that deliberately bypass decoding would rely on the Channel contract; the seven tests do not enable their `bypassDecoder` branch. No new callback implementation is introduced.

## Reviewed fingerprints

All paths in this list are relative to `pipe-startup26/`.

- `patches/01-seven-pipe-operations.patch`: `2f467eefd2faefc71c4f9a6d8e1b4d12b6f9548a33076adb7f83c662b50992c9`
- `check-portable.py`: `f30effec4c7af8fcda960e7d0b389e777c598eb6f3e6ea32ecfa0c170f4b13fa`
- `tests/seven_operations.cpp`: `5052463343209a39ba7e133ce53313ecb38e0cff6784bce02fa2904af9799f7e`
- `private-stage-v2/backend-boundary24/pipe/ClientMilesPipe.cpp`: `b78fec34b28a746d18361758a6a17ab39f5093331dc3805ca6bfecc78b185167`
- `private-stage-v2/startup-bridge23/backend.h`: `473f4f79dd01dd19b8a588b968a82b3fb4b97c40f0a2a84822dc3137c6fc524c`
- `private-stage-v2/startup-bridge23/reply.h`: `99bbe94d1ae635d9040b751da1dbd077df82d4e8ff2027b016c85c7ee36560e5`
- `private-stage-v2/host-candidate/host_dispatch.cpp`: `4810fd0dcad43c769e077f3c2ad8d3ad9ebffec426920ff6f5e0063bd4103595`

Fresh-run compiler and exact compiled-source identities are retained in `pipe-startup26/review-scratch-blind-pipe26/identity.json`. Compiler: `/usr/bin/g++`, `g++ (GCC) 16.2.1 20260810`; binary SHA-256 `f04191f6a7b2cd7d9a62e1745872b8a6088791e5af6955488c69c9b2c4668bc9`. Host path was source-reviewed only in this review. A separately planned native object compilation is not host execution coverage.
