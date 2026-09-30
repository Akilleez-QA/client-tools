# Coverage review 23: parent disposition

Composer integration23 exited0 after reading supplied owned source. Its useful observations are that the existing reply encoder supplies empty text spans, the controller drops decoded frame storage, metadata is absent from the existing21requests, and startup/shutdown must stay with one owner. These were checked directly in live-bridge-candidate/bridge.cpp and metadata-v4.

Corrections and limits:

- Scalar dispatch acts on the framed request's target sample through RegistryResolver. The separate control sample receives direct fixture calls. Composer's statement that dispatch runs on the control sample is incorrect.
- Calling existing paths playback operations is loose wording: the old fixture binds a known image and manipulates parameters but never plays a sample. Its21request count is not metadata coverage.
- Absence of a started guard in metadata_host.cpp does not prove the vendor accepts every preference call before startup. The new plan uses the observed game's pre-start directory setup, then preference calls after actual startup.
- Composer noted status alignment0–3 but missed the4/5 collision. The blind maintainer identified it; the new plan maps metadata failure4/5 to explicit unique codes and keeps oracle failure outside the transport status vocabulary.
- The routing suggestion is a sketch, not a tested patch. Owning Reply/text must survive encoding and subsequent client use. A Bytes view or function-local reply that expires before encoding is not an acceptable implementation.

The selected implementation is a new startup-only23request experiment, not a claim that metadata is present in the old21request evidence. Its only lifecycle owner is the existing Backend concept; it excludes samples/playback. The worker must bind actual source/build/run identities and preserve the first outcome.

Grok drain23 exited0 after the supplied-source review. Its diagnosis matches direct source inspection: drain sets Stopping, collect ignores completed bytes and non-incomplete errors, and fault cannot record a new result outside Open. Its event-before-collection tests are useful deterministic controls and were sent to the implementation worker.

The proposed patch is not accepted wholesale. Automatically issuing more reads/writes after cancellation changes shutdown semantics and can require unavailable peer progress. Making destruction terminate merely because a completed frame is unread confuses protocol acceptance with storage cleanup. A deliberately canceled operation can complete normally, and a canceled write may already have delivered a prefix; Grok's condition that the peer must observe no payload is not generally justified. ERROR_OPERATION_ABORTED is ordinary cleanup only with the relevant local cancellation state, not an unconditional success classification. The new candidate instead separates safe operation-storage cleanup from retained late-data/incomplete-output/first-error evidence. This is a parent design decision to be tested, not a passed result.

No vendor callback retirement claim follows from correcting OS completion handling. These CLI reviews share supplied source and root framing; they are coverage assistance, not independent vendor observations.
