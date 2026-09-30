# Independent opening: the next live slice

2026-09-30. Bounded source-only follow-up. I did not read another worker's new host-live plan. Product source is the supplied `49d0eeed4ddaa177d7a93ea396c37c3d9b9942da` checkout at `/home/akilleez/Work/swg-source/client-build-next`. No runtime, allocator workload, product mutation or descendant agent was used. This is an implementation recommendation, not a passed test.

**Choose an unstarted, memory-backed owned sample:** real x64 controller → checked wire frames → x86 coordinator → existing registry resolver/scalar dispatcher → original Miles 7.2a. Bind one complete, known-valid WAV image in retained host storage; query its duration, change/read volume and playback rate, then release and shut down cleanly. Do not register application callbacks, open a stream, or start playback in this first slice.

This is meaningful while the real-engine fixture's teardown fault remains unresolved. It connects previously separate components to genuine vendor state and resource lifetimes. It cannot establish real Audio/Sound2d integration, audible output, callback affinity, stream IO, Bink, or repair the engine teardown failure. Success means a working, narrowly scoped live component path; full integration remains gated.

## Source basis: there is already a callback-free game operation

[Audio.cpp:4427](../../swg-source/client-build-next/src/engine/client/library/clientAudio/src/win32/Audio.cpp#L4427), `getSampleTime`, allocates a sample at 4437, binds `AIL_set_named_sample_file` at 4449, then on success calls `AIL_sample_ms_position`, `AIL_end_sample`, and `AIL_release_sample_handle` at 4453–4455. It neither starts playback nor registers EOS. This supplies a concrete source-supported prerequisite sequence; a freshly allocated handle alone is a weaker foundation for duration/position assertions.

The ordinary 2D playback path binds the image before volume/rate work ([Audio.cpp:2836](../../swg-source/client-build-next/src/engine/client/library/clientAudio/src/win32/Audio.cpp#L2836)). It reads the original rate before setting the requested one at 2840–2842. Use that state and order for the extra scalar checks. Do not add `AIL_init_sample` merely because the API exists: the inspected game path goes from allocate to named-image bind, and initialization is not among the 61 mapped calls.

Callback-free does not mean Miles has no internal worker threads. It means this deliberately isolated session has no registered application EOS, stream, timer or reverse-file callback whose body must run in x64. Track that fact in coordinator state and exclude registration operations; `Call.callback == 0` in a scalar request does not establish it.

## Smallest useful implementation contract

1. Create one fresh host process/session and one dispatch lane. Bind the channel to that session; correlate monotonically identified requests/replies. Verify the actual loaded original DLL path/hash and record driver parameters and FPU context without inventing a normalization policy. Startup success and a real non-null driver/sample are prerequisites, not successful transport replies alone.
2. Implement only the needed lifecycle/control handlers around the existing scalar dispatcher: handshake, startup, driver open, sample allocation, image upload/seal, named-image bind, sample release and session close. Use existing opcode meanings. Missing handlers must reject explicitly. All actual SDK calls run on the lifecycle object's owning dispatch thread.
3. Transfer a complete known-valid WAV and its exact NUL-terminated suffix. A bounded first fixture can use one chunk, but Begin/Chunk/Seal must still enforce declared size, coverage, immutability and session ownership. Keep file length separate from buffer capacity; pass the correct image length and block zero. A sealed buffer proves transport completeness, not that arbitrary bytes are a valid vendor format.
4. Resolve the real sample locally, associate its retained image with that resource, invoke the genuine bind, and publish the exact vendor return separately from transport status. Do not proceed to duration assertions when bind returns failure. For this one-image experiment, retain all attempted images through sample release and vendor shutdown; that avoids pretending to know an unmeasured replacement-retirement rule.
5. On the bound, unstarted sample, query duration/current position with the real output masks; set/read two ordinary finite volume values and a positive playback rate, then restore or record the changed state. Compare with the identical direct Win32 sequence against the same DLL/input/driver settings. Use the original vendor's returned values as the oracle, rather than assuming volume rounding or duration conversion. Changing rate may change the duration interpretation, so compare each observation at the same point in the sequence.
6. End/release the sample, reject a subsequent stale sample token before any SDK call, drain the single admitted lane, and shut down normally. Retained bytes outlive all vendor users. Record the last completed teardown phase and actual process exit. A timeout/process kill is not a successful cleanup result. No callback-delivery implementation is claimed by this session's deliberate absence of registrations.

The decisive positive evidence is that an x64 request changes the genuine x86 sample state and a separate vendor getter returns it, while the same wire path obtains actual image-derived duration and rejects a retired token. A host-local getter trace alongside the reply makes it harder to mistake an echoed argument or cached answer for a vendor result. No sound output is necessary for this milestone; it must not be advertised as playback validation.

## Concrete prerequisite traps in the present components

| Priority | Observed source | Trap and required resolution |
|---|---|---|
| High | `host_dispatch.cpp:14–54,55–57` | The 39 supported arms omit startup, driver open, allocation, both image binds, release and shutdown. Every supported arm rejects bytes/text/resource/callback fields. Feeding a sealed Buffer token into this dispatcher cannot bind it. Add real coordinator handlers; do not label enum membership or `supports()` as an executable session. |
| High | `host_dispatch.h:13–15`; `host_dispatch.cpp:311–328` | Session/lane/lease admission is external. The file-error, timer-delay and serve arms do not even consult a resource resolver. Routing every decoded opcode straight to dispatch can call Miles before startup or after shutdown. Gate the small allowlist by coordinator state before dispatch, including null-target operations. `AIL_serve` is active servicing, not a harmless scalar getter. |
| High | `session_lifecycle.cpp:26–41,51–60`; `resource_registry.h:103–117` | Lifecycle `Ok` may carry startup failure or a null driver/sample. A token's kind/generation checks do not prove the sample has a valid bound format/image. Require the genuine startup result, non-null resource, successful bind and retained image state separately; never register dummy pointers to satisfy the resolver. |
| High | `miles_wire.h:25–30`; `retained_buffers.cpp:18–52` | BufferBegin/Chunk/Seal are schema only. RetainedBuffers stages complete copies and tracks active tokens; it does not implement chunk coverage, wire Buffer handles, sample ownership or a vendor call. Its local token is not cross-session authority. The glue must supply these missing semantics, without changing the scalar Call layout ad hoc. |
| High | `session_lifecycle.cpp:88–101`; product `Audio.cpp:1430–1437` | Existing lifecycle shutdown explicitly closes each driver before `AIL_shutdown`; the product clears its stored pointer and calls `AIL_shutdown` without that explicit close. The helper path may be a legitimate isolated vendor experiment, but cannot silently become product-equivalent cleanup. State which path is being tested. For a slice intended to establish the future product coordinator, implement the observed product shutdown order; otherwise restrict the result to the alternate standalone lifecycle. Keep Bink absent and make no shared-driver conclusion. |
| Medium | `codec.cpp:135–157`; `miles_wire.h:14–15`; `resource_registry.h:12–13` | Decode validates envelope/fields, not request causality, session identity or admission. Header contains no explicit session incarnation field. A private channel's bound incarnation may supply that missing authority, but a naked Handle cannot. Reject duplicates/mismatched replies and traffic from a prior connection; no ambiguous automatic retry. |
| Medium | `host_dispatch.cpp:143–169,241–274` | Output pointers are selected by `output_mask`; default-zero masks do not fetch volume or duration. Test actual mask 3 and selected single outputs. Setters return void: `Complete` alone does not show that a requested value took effect. A real subsequent getter is essential. |
| Medium | `session_lifecycle.h:11–12`; `host_dispatch.h:5` | Lifecycle and dispatch status enumerations have different meanings (`WrongThread` versus `Unsupported`, for example). Do not cast one directly into the other's wire interpretation. Define a consistent transport-status mapping and preserve a separate genuine vendor result/null resource. |
| Medium | `host_dispatch.cpp:80–85,136–155,290–309`; `registry_resolver.h` | Stream arms require real HSTREAM creation, stream IO and parent-tracked aliases; owned-sample success proves none of them. Volume/rate borrowed aliases are accepted only after real parent resolution. Do not invent a stream by retyping an HSAMPLE or use direct host filesystem streaming as proof of TreeFile equivalence. |

These are integration prerequisites, not newly discovered defects in components that explicitly leave those tasks to their callers. In particular, no-app-callback registration plus serial admission is useful evidence for an empty application callback set; it does not prove vendor memory has stopped being used. Actual release/shutdown boundaries still govern retained data.

## Which operations need callbacks, and which merely can encounter them?

**Legitimate first-slice operations:** real startup/driver/sample creation, complete memory-image bind, volume/rate and image-derived metadata getters, corresponding scalar setters in the bound state, end/release and shutdown. Driver room/listener calls are also plausible without application callbacks, but add little to this minimum and require real driver state and valid parameters. Avoid numerical edge-case fuzzing as a substitute for valid-state coverage.

**Not intrinsically dependent on game EOS:** starting/stopping a memory sample is not universally forbidden without EOS registration. The product's infinite-loop branch intentionally omits registration (`Audio.cpp:2861–2878`), and `playBufferedSound` binds, sets volume and starts without registering EOS (`5328–5344`). A later isolated playback slice can therefore be legitimate with a real bound image and explicitly empty application callback state. It adds mixer progression/output evidence, but is unnecessary for this first scalar milestone and does not validate finite Sound2d completion policy. Do not generalize “no callback required by vendor” into permission to delete the callback from the normal game path.

**Exclude from this slice:** registered EOS/stream callback dispatch; normal finite Sound2d playback policy that expects EOS; TreeFile-backed open/serve/close; borrowed stream samples; original multi-operation `AIL_lock` scopes and cross-lane reentry; Bink. `AIL_serve`, start/stop/end or release can encounter callbacks if earlier session state registered them, even though the current scalar request carries no callback field. A fresh restricted session makes that state explicit; an existing game session does not.

`AIL_set_sample_file` has no input-length parameter (`Mss.h:4485–4487`), and named binding's format inspection expects a complete image or the documented initial header extent (`853–855,4492–4496`). Prefer the known-valid complete image and named bind for the first live slice. Do not pass truncated/fabricated input merely because the wire bounds checker accepts it. A single successful WAV also does not establish other codec/plugin or malformed-file behavior.

## Evidence limits and next gate

The original real-engine teardown failure remains a separate unresolved gate. This isolated vendor session deliberately does not bootstrap DataTable/cache/ExitChain, so its clean exit neither identifies nor fixes that fault. Conversely, waiting for that fault's resolution before testing any genuine component composition is unnecessary: the proposed slice has its own explicit, inspectable lifetime and no dependency on the failing engine teardown path.

If this slice passes, the next expansion should be chosen from evidence, not automatic enablement of all 39 arms. Real-engine baseline cleanup and the callback/TreeFile scheduling contract remain required before claiming the proposed architecture works for actual Audio/Sound2d. Finite scalar/direct comparisons cannot establish universal game fidelity.

## Reviewed candidate identities

All paths below are relative to `vendor-options/miles-integration-seam`. These identify the reviewed source snapshot, not tested binaries.

- `host-candidate/host_dispatch.cpp`: `4810fd0dcad43c769e077f3c2ad8d3ad9ebffec426920ff6f5e0063bd4103595`
- `host-candidate/host_dispatch.h`: `e8b146c5f493d0a48c0a539494219b5a0e7a19405c9954ec32e84c1cda5b4a66`
- `host-candidate/session_lifecycle.cpp`: `58cfefa0177b45d3445faae5cfbc9fa1e902c8e9e6bbd593ad1e0bfc2818f1aa`
- `host-candidate/session_lifecycle.h`: `42e20d84790396676bb35c36cb0acc79fd04e6dd0a0a7fbb039bb257c06f099c`
- `host-candidate/registry_resolver.h`: `2b405ebf56ac51ecc81c8ac919809c5b0f16524c248fc1a932fbc2d7b8fd584a`
- `host-candidate/retained_buffers.cpp`: `9f8fc1f78238b0347e25606fdc1be658414b73aefb021c3ef91577bcd45d7401`
- `host-candidate/retained_buffers.h`: `e62c472f1e46f783a130da8081bb92e958d8e3acaa9010d2fabae6169f329d8e`
- `protocol-candidate/miles_wire.h`: `8efe3915744250a6aebdc51caa712790f4930c2b32877e9425dcf79c191df0b9`
- `transport-candidate/codec.cpp`: `15ab7134eb837fa7c36323d28423ecfa33e8fec69e8a03e4411bef924aade33e`
- `transport-candidate/resource_registry.h`: `f2a4131c73d831a0e407bd67eb1803ec1f8a72ccd0cf36e6af979cae3e8a3768`
