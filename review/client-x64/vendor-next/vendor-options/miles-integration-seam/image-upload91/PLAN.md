# Explicit-length file_type upload: paired source plan

Scope: source inspection only, based on frozen pipe-composition86/candidate. No implementation, compilation, execution, product edits, SDK redistribution or ownership-retirement claim. Public ClientMiles.h from70 remains unchanged. This first slice covers a running session's nonnull, positive-length readonly file_type input supplied by Audio.cpp:2534–2546. Zero-length/null cases are outside this initial operational scope; do not manufacture an SDK classification for them. WAV_info and both sample-image setters remain excluded (image89/ASSESSMENT.md).

## Existing pieces and actual gaps

Paths below are relative to the seam; selected paths are under pipe-composition86/candidate unless otherwise stated.

* protocol-candidate/miles_wire.h:12,26–30 already defines Buffer identity and BufferBegin/Chunk/Seal/Release. Private Version is 3, not a game/network protocol. protocol-candidate/API-MAP.md in the original protocol candidate specifies opcode9 with resource=sealed Buffer and value0=explicit U32 extent. No wire pointer is needed. Both peers must adopt the same narrowed contract below; do not accept v1/v2.
* transport-candidate/codec.cpp:115–116,153 already bounds each Call frame, including its 136-byte fixed portion. Empty text allows chunk payload at most MaxFrameBytes-136 = 1,048,440 bytes. Use min(remaining, that bound), check all arithmetic before conversion, and do not cap the whole image at one frame.
* backend-boundary24/pipe/Channel.h:17–20 exposes only text. LiveChannel.cpp:52–57 discards the payload possibility, although exchange():68–101 already encodes separate payload/text through the sole command Endpoint and publishes admission before send. Session::request in PipeCore.cpp:175–196 and verifiedResources():239 onward need the same private payload path and a retained local upload identity. Do not introduce another command owner or bypass owner validation/returned ACK join.
* startup-bridge23/reply.h:53 onward lacks BufferBegin resource and file_type return recognition. A successful nonzero file_type would currently fail its shape check. Validation must change before settlement, including owner-specific Buffer identity checks; generic decodeResult alone is insufficient.
* paired-bootstrap59/host.cpp:43–89 already checks monotonic request identity and resolves target/resource through Backend.registry before admission. New Buffer handles must use that registry so existing admission pins work. No new handle registry is justified.
* startup-bridge23/backend.h has no upload owners, budget or Buffer handlers, and no file_type execution case. transport-candidate/resource_registry.h:100–105 does not permit reserving Buffer, though insert can create one. Prefer extending existing reserve's allowed standalone kinds by Buffer so owner allocation/publication uses the established transaction discipline.
* buffer-upload-candidate/buffer_upload.{h,cpp} outside86 is reusable actual source: ordered nonempty append, exact complete seal, immutable after seal, independent copySealed. Its explicit comment delegates aggregate reservation to the session. Its prior tests cover this component, not the proposed pipe integration. It does not expose a vendor view.

Important correction: there is no implemented upload aggregate budget in selected86. startup-metadata-v4 SessionInputs has a cumulative text budget, not an image budget. The older host-candidate/retained_buffers.h is not selected86 and is not a reason to add a second identity system. Selecting a private host upload-byte limit is necessary before authoring a concrete implementation; no numeric limit is inferred here. copySealed duplicates storage, so authorization must cover both upload and classification copy, plus separately bounded frame storage. An authorized image may exceed one frame.

## Minimal paired contract to implement

All operations use normal Request/Reply, lane1, ordinary admission and monotonically increasing request IDs. Each request has zero callback, mask, reserved, unused values and text. Reject surplus fields before allocation/SDK work. Existing codec verifies span boundaries; handlers still enforce exact operation shape.

| Operation | Request | Successful reply |
| --- | --- | --- |
| BufferBegin | null target/resource, value0=N; empty bytes; N positive and authorized | nonnull fresh Buffer resource; every other result field zero |
| BufferChunk | target=that Buffer, value0=current offset, bytes=nonempty bounded chunk; null resource | all result fields zero |
| BufferSeal | target=that Buffer; empty bytes, all values zero | all result fields zero, only after exact coverage |
| file_type | null target, resource=sealed Buffer, value0=N equal to declared size; empty bytes | transport Success and exact SDK S32 return bits, otherwise zero fields |
| BufferRelease | target=that Buffer; empty bytes, all values zero | all result fields zero after identity retirement and storage retirement |

Limit first implementation to one live upload transaction per serialized session/host. This is temporary staging for one synchronous readonly query, not a new global quota or cache. Account N upload bytes plus N independent sealed-copy bytes using overflow-safe wider arithmetic against the selected aggregate limit. Reserve budget and an existing registry reservation before storage allocation; rollback only locally known prepublication failure. Store the upload owner in Backend member state before publishing the handle. Do not leave an escaping registry pointer to a stack object. Keep any unknown published state terminal and retained.

The client keeps the successful Begin handle in a preallocated/member transaction record until confirmed Release; verifiedResources admits only that exact Buffer generation. BufferBegin reply owner validation rejects null/wrong-kind/duplicate identity. Chunk/Seal/Release reply shape is empty success or exact known refusal. The record must remain available if reply handling or later commands throw; destructor cleanup must not send hidden recovery RPCs on an uncertain channel.

For classification, copySealed into Backend-owned storage before the SDK call, retain it through the call and result materialization, and call the genuine AIL_file_type(pointer,N). Preserve any native value, including zero, negative and high-bit S32 values, as transport Success plus unchanged return_bits. There is no boolean-success normalization. A known upload/field/budget refusal is a transport refusal, never a native zero. The client converts with the existing signedValue bit-preserving path.

After a validated classification reply and admission/ACK join, issue BufferRelease and return the cached classification only after a validated release reply. A lost/malformed classification or release reply fails through the existing public failure boundary; it must not return a normal classification or retry the SDK call. This conservative ordering makes cleanup uncertainty visible. It is not evidence of native setter copying or sample quiescence. A received SDK return for this readonly query is the narrow lifetime boundary being selected; this plan does not infer the same boundary for setters.

Partial uploads can be explicitly released after a *known* refusal while the channel remains healthy; however Session::request currently throws immediately for refusals, so the implementation must deliberately preserve that status long enough for the narrowly defined cleanup. Smallest alternative: fail the whole private session on any upload refusal after publication and retain until process destruction; choose this terminal policy for the first slice rather than adding a general recovery API. Do not assume current checkStatus performs cleanup. Pre-Begin known budget refusal has no published image to retire.

Repeated commands with the same request ID are rejected by host.cpp before execution. A fresh request ID does not authorize replay of a consumed/released identity. BufferUpload::seal itself permits a second seal; the new host handler must reject repeated Seal in its state machine if the exact single-transition contract above is selected. Chunk replay/overlap/gap is refused by append. Never retire another generation on a stale release.

## Exact source delta and order

1. Copy buffer-upload-candidate/buffer_upload.h/.cpp unchanged into the new selected candidate; record original hashes. Add the single Buffer allowance to existing ResourceRegistry::reserve. Add private Backend upload owner/state/accounting and the five strict cases in startup-bridge23/backend.h. No additional vendor dispatcher abstraction is needed for the single genuine SDK call.
2. Add payload argument alongside text to Channel::call and its actual LiveChannel implementation; extend Session::request preserving existing callers' empty defaults. Update all selected actual implementers, plus explicitly identified test suppliers only when their gate is authored. Keep runtime publish/send/decode/owner-validation/returned order unchanged.
3. Extend startup-bridge23/reply.h and Session::validateReply/verifiedResources for BufferBegin and file_type. Add the member transaction identity/state in Session.h, including terminal retention. No public opaque Buffer type escapes.
4. Add Core declaration/definition and guarded public file_type definition in PipeCore.h, PipeCore.cpp, ClientMilesPipe.cpp. Use the provided extent only; do not inspect RIFF headers, guess image size, resolve a cache owner, or invent a native output on failure. The caller must keep input accessible and stable throughout synchronous chunking.
5. Freeze paired source, provenance, request/reply contract and budget selection before preparing execution. Native coverage is computed from changed transitive includes against native86's actual selected closure; Backend host TU gains exactly genuine AIL_file_type. Public wrapper gains exactly one Core delegate. No link/runtime/engine claim follows from objects.

## Prospective discriminating checks (not executed)

* Real codec + new host upload state + reply decoder: exact small image and N greater than MaxFrameBytes, split at maximum payload and final remainder; emitted frame sizes never exceed MaxFrameBytes, reconstructed bytes equal input.
* Declared aggregate limit: exact authorized boundary and one byte over; two-copy accounting cannot wrap U32; second active Begin refused without losing first identity; budget restored only after confirmed retirement. No arbitrary cumulative image-count cap.
* Malformed shape: valid envelope with surplus values, nonnull unexpected handle, text, mask, callback; no append/seal/classifier invocation. Decoder rejects wrong resource kind/null Begin success and neighbor return/value fields, leaves caller outputs unchanged.
* Partial coverage, gap, overlap, zero chunk, oversized chunk, duplicate Seal, post-Seal chunk; abandoned partial Buffer can be retired explicitly at host layer; production client terminal policy remains distinct.
* Full request replay rejected before execution; fresh-ID stale generation/released handle refuses. Reuse same registry slot with new generation and prove old release cannot retire it.
* Genuine decoder return oracles use literal 0, -1, INT32_MIN and positive classification, not values computed by the tested conversion. Transport refusal cannot surface as one of these results.
* Inject uncertainty at Begin reply, chunk reply, classification reply and Release reply: no ordinary return, no retry, no hidden destructor RPC, retained transaction state. A classifier test supplier may prove ordering of actual host handler only; label it explicitly as no SDK execution/fidelity evidence.
* Public/Core/Session/real codec composition must verify ordering Begin→Chunks→Seal→file_type→Release and input accessible for each chunk; component-only BufferUpload tests do not establish this composition.

Before implementation: select explicit private aggregate-byte authorization and confirm terminal-on-postpublication-refusal policy. These are concrete missing owner policies, not reasons for a generic upload framework. Normal SessionClose, EOS, setter retention and operational product adoption remain outside this slice.
