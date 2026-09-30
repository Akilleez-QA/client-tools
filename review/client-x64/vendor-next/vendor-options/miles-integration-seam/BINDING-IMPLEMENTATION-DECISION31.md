# Binding implementation decision 31

**No complete native-compatible binding patch is supportable from the present lifetime evidence.** The missing part is a vendor reclamation contract, not host allocation machinery. Adding the wire call now with either immediate deletion, permanent history retention or a one-bind limit would encode an unsupported behavior. No production/frozen source changes, runtime, page protection, fault tests or reruns were performed for this decision.

## New evidence used precisely

The one original-DLL binding-probe30 run established same-HSAMPLE A → B → A success, an unsupported-format F returning zero, and successful B recovery afterward. Successful queries returned 1000/2000/1000/2000 ms with current zero. All inputs lived through shutdown. Nothing was queried after F. Therefore this does not determine whether F preserved or cleared A, retained F, or whether any successful replacement stopped referencing older inputs.

F's owned immediate error was `Unsupported wave file format.`; B recovery returned 1 while the same error text remained. The native S32 bind result decides success. A nonempty last_error must not turn that completed B success into an exception, zero, rollback or retry. Transport failure remains distinct from both zero and nonzero native results.

Fresh product scope: actual checkout HEAD49d0eeed4ddaa177d7a93ea396c37c3d9b9942da was verified before probe implementation. Audio.cpp's buffered calls at 5328/5348 reuse the same allocated sample after stop/end and ignore bind return; helper getSampleTime at 4427 uses a fresh allocation. A one-bind restriction or swapping in a fresh native sample would not preserve those calls' semantics.

## Existing components do not close the gap

- `host-candidate/retained_buffers.h` explicitly says commit does not establish that a previous vendor reference ended. `commit` only changes a token; `retire` frees a vector. Neither invokes or observes Miles. Its one active token also is not an image/suffix-pair lifetime.
- `sample-pipe29/prepared_input.h` prepares stable copies of full sealed-upload bytes and suffix. It is a suitable ownership unit, but no sample owns it and no vendor detachment boundary is implemented. Its local byte limit does not account for old/pending owners or transient upload copies.
- `coordinator-candidate/coordinator.cpp:56–73` clears request pins when an admission returns, not when all vendor uses end. `readiness` at 122 onward explicitly returns `vendorTerminationUnproven=true`. No callback registrations in this slice does not prove Miles has no internal retained/asynchronous state.
- `sample-host29` reserves handle registry tracking before native allocation and retires identities after native release/shutdown. Registry identity and generation bookkeeping do not own the image or provide a rebind boundary.
- `protocol-candidate/API-MAP.md:38` already maps opcode32 to Sample target, sealed Buffer resource, suffix text, U32 file_size and S32 block, with an S32 result. Its CONTRACT.md explicitly leaves reassignment/failure lifetime to be established against the original API; conservative storage through destruction was not accepted as a final policy.
- The actual sample-host29 Backend has no BufferBegin/Chunk/Seal/Release handlers. The sample-pipe29 private Channel call carries text but its live call path always supplies an empty binary payload. Therefore a complete binder also needs a small real upload route; merely defining `set_named_sample_file` against an imaginary sealed Buffer is not integration.

## Exact missing ownership contract

For the pinned original DLL, suffix, and each supported format/provider, establish:

1. On a completed **nonzero** bind, does the return guarantee that every reference to all previous image/suffix inputs has ended? This includes any codec state/background work and cleanup hooks, not just the current sample data pointer.
2. On **zero**, can the attempted new image or suffix still be referenced? Can the old image/suffix still be referenced? Failure need not be transactional. Which later native operation, if any, establishes that these references have all ended?
3. On release/shutdown return, what completion/quiescence guarantee permits destruction of every retained input? The current design intends these as lifetime endpoints; the successful probe keeps storage through both, rather than experimentally establishing when it becomes safe to destroy.

The possessed 7.2a Mss.h provides signature and a format-detection prefix-size comment, not these rules. The official history used in review30 is version context, not a lifetime specification. No additional applicable contract was found in the examined host/coordinator sources.

The core contradiction is already present in three calls: after A is current, failed F may reference either/both A and F. To bind B, B must also be owned before entering Miles. Discarding either A or F to keep only two owners guesses lifetime. Repeating this strategy with retained history is unbounded. Even A-success → B-success → C needs success detachment evidence before freeing A. A byte budget prevents an OOM but does not resolve native semantics or justify a one-bind cap.

## Smallest implementation once the contract is established

The actual change should remain within the existing facade and private pipe composition:

1. Add the narrow binary payload parameter to the private Session/Channel/live exchange and implement the existing four Buffer control operations in Backend, with complete ordered sealing, session aggregate budget and generation checks. Use full U32 file lengths; a frame/chunk limit is not a new public file-size restriction. BufferRelease concerns transfer ownership, not permission to free a sample's independent vendor input copy.
2. Add a sample-owned pair (`image`, `suffix`) and a pending pair. Reserve pair storage, container/owner publication and any accounting before `AIL_set_named_sample_file`. Prepare views before the call. Neither post-call publication nor exception unwinding may allocate or destroy potentially retained inputs.
3. Define the public native-shaped facade call with the existing signature; encode U32 byte count and S32 block, return exact signed native bits. Add only opcode32's return_bits allowance to the typed reply decoder; retain rejection of unused fields.
4. Validate sample/upload liveness, sealed exact extent, suffix and reserved fields before invoking Miles. Assign pending ownership into the sample record before entry, so a lost reply or local post-call failure cannot destroy vendor-visible data. A wire refusal leaves native state unchanged; native zero is returned normally.
5. Use a concrete observed/documented retirement rule: on success swap pending/current and retire only inputs proven detached; on zero keep actual native behavior and retire only inputs proven unused. Release/shutdown must invoke native cleanup before clearing pairs. Do not auto-rebind old bytes, retry, translate last_error to failure, or release/reallocate the native handle behind the existing sample identity.

If evidence establishes that success detaches old inputs and failure never retains incoming input, this becomes simple two-pair ownership with constant steady-state memory: current+pending during each call; current only afterward, including unlimited ordinary successful rebinds. If failure can retain both, a different **specific** proven boundary is necessary. “Keep a few previous pairs just in case” is not a solution.

No placeholder patch is supplied: an omitted retirement predicate, unconditional detach assumption or unsupported implementation would be less reviewable than this exact unresolved contract. PreparedInput and reserve-before-vendor support already exist; duplicating those in another disconnected helper would not advance the missing decision.

## Best bounded next investigation

First obtain licensed 7.2a function documentation or a vendor answer for the three contracts above. It is the smallest useful evidence and may avoid another runtime entirely.

If unavailable, the next useful source-only investigation is a **bounded static data-flow inspection of the possessed original DLL's exported bind and release paths**, starting at `_AIL_set_named_sample_file@20` and the PCM / unsupported-tag branches used by probe30. Identify where old codec/source pointers are detached, where incoming image/suffix addresses are stored, which zero-return exits occur before/after state mutation, and how release ends those references. Include all reachable provider/worker references needed for the claimed format; a current-pointer overwrite alone is insufficient. This task was not performed here. It is narrower than another engine/transport experiment and produces a concrete hypothesis for a later measurement.

If that inspection leaves one precise ambiguity, propose a separately reviewed **read-only reference-observation probe**, not a repeat of durations: keep owned A/F/B inputs alive, inspect the identified native ownership fields at successful return and failure/recovery boundaries, and log which input ranges they reference. Observe the export's identified assignments/cleanup path without freeing, poisoning or protecting inputs, and without calling query on a failed sample. Read-only snapshots can distinguish specific stored-pointer/state hypotheses, but absence of a pointer in a selected object cannot prove absence in a provider/thread. The exact offsets, structure identity and observation method must come from the bounded static analysis before writing such a probe; guessed offsets or unstructured memory scans are not acceptable.

There is no honest no-playback, all-buffers-live black-box duration test that alone proves absence of every future buffer reference. Another identical A/F/B run would add no discriminating lifetime evidence. Any future measurement must state the narrow lifetime hypothesis it can falsify and must not be generalized to MP3/Ogg or arbitrary failures. No such execution is authorized by this decision.

## Reviewed local identities

- `host-candidate/retained_buffers.h`: `e62c472f1e46f783a130da8081bb92e958d8e3acaa9010d2fabae6169f329d8e`
- `host-candidate/retained_buffers.cpp`: `263e9ae67ce8f0142758a82f7c85606e56f223125c78eac7199de37c23207091`
- `host-candidate/registry_resolver.h`: `825f78d913ae822545ac12c5621ef2d17ab422270de960339ab0590ecd8b8c2a`
- `host-candidate/host_dispatch.h`: `e8b146c5f493d0a48c0a539494219b5a0e7a19405c9954ec32e84c1cda5b4a66`
- `coordinator-candidate/coordinator.h`: `fb7e2d84697976787f702c1a0af5771d724e8dc17e6899e631858eb7fc709512`
- `coordinator-candidate/coordinator.cpp`: `d434149188ee15bfc51c9a3286c9c5a49ef5d4762e8a7bb95d485cc852ec16b6`
- `protocol-candidate/miles_wire.h`: `8efe3915744250a6aebdc51caa712790f4930c2b32877e9425dcf79c191df0b9`
- `protocol-candidate/API-MAP.md`: `0cdd00ae1686f95d7b9c40c533e432a81fa3083d32e800fd52b5fc3168773b2f`
- `protocol-candidate/CONTRACT.md`: `0824bb1b550b4234cf89cf8fa52c69b5fe12afa0b570cfb14004c5672b44661d`
- `sample-pipe29/prepared_input.h`: `aa2304695b33aca618ba172e9b47a841ec433734898f68897a11d1f52e40c285`
- `sample-host29/prepared/startup-bridge23/backend.h`: `b2dcd7e56cf539fe96a09155dcd0815e0077b47c9c2e91dfd882e22bd153650b`
- `binding-probe30/runtime-recipe-v1/private-run-959d3f4e/results.json`: `0d9911279fb661ae934bfa6a95731d5c599945a2a28acabe1f3bb000f82b7083`
