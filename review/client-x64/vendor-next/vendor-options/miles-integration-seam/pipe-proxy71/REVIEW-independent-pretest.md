# Independent pretest review — pipe-proxy71

Reviewed freeze `5ee831bdd9ee006643de994774208e93b462060c2ab63bb2cae7c1ca45416302`; independently recomputed all80 manifest entries with no mismatch. Compared actual candidate bytes with68 and70, read the complete focused diff and affected implementation paths, and traversed selected quoted includes. No compiler, tests, VM, SDK/engine runtime, product edit or source repair was performed. This review is the only authored file.

**No new concrete blocking defect identified in the71 identity conversion.** This is bounded source review, not proof of Windows pointer conversion behavior, SDK type compatibility, a complete callable adapter or safe shutdown. The inherited missing host Reservation API is already recorded under68 and being repaired separately in73. The72 driver argument repair is not included in71 and was not assumed here.

## Actual source and identity path

Only four candidate files differ from68: the public header, PipeCore.cpp, PipeCore.h and Session.h. The public header is byte-identical70 (`952a0d1fe803d02d0c280e2e1c95558cdf5d8dc9bbe9db1d44e330fb4d6452fc`). It forward-declares the three global selected-SDK tags, with plain handle/callback aliases, and introduces no STL, pipe owner or private failure type. I found no selected client definition, instantiation, size query, deletion or dereference of those provider tags. Old excluded native provenance is not selected client code.

`PipeCore.cpp:8–33` owns genuine private DriverProxy/SampleProxy/StreamProxy rows in the existing Session/list containers. Session's unique_ptr now owns the private DriverProxy; it does not own an incomplete SDK object. `driverToken`, `sampleToken` and `streamToken` at42–50 convert only trusted row addresses to opaque public representations. No reverse conversion from a caller token appears in the selected client path.

Driver operations (`driverCall` at109 and speaker query at360) require a live running Session, nonnull selected private row, exact generated token match and that row's Session owner before reading its wire identity. The apparent later `driver->wire` writes are to the locally allocated DriverProxy, not the incoming opaque handle. Verified-resource scanning also reads Session-owned private rows.

Owned-sample lookup at417, borrowed lookup at429 and stream lookup at442 compare the caller token against tokens freshly generated from the authoritative list entries, then use only the matched private pointer. The helper names are distinct from public operation names; the wrappers continue explicitly calling Core operations. No new lookup registry or token-to-object cast was introduced. Borrowed tokens are generated from the embedded SampleProxy, consistently with owned SampleProxy token generation, and owned-only release cannot match the borrowed row through its owned list.

## Publication, invalidation and ordering

Driver storage still exists before the side-effecting request and is published only on accepted nonnull reply. Sample and stream rows are inserted before their requests; genuine null/known refusal removes the unpublished row, while uncertain sample/stream outcomes retain it as before. Private storage addresses remain stable while live. Release erases the already matched owned row after request completion. Close compares generated tokens and erases the matching stream only after completion; the embedded borrowed identity dies with it. These are the inherited native-style lifetimes, not added stale-handle protection: allocator address reuse after release remains outside the valid caller contract.

The64-derived validator is byte-identical68 after replacing just `ClientMiles::OwnedStream` with `ClientMilesPipe::StreamProxy`. Exact request pair masks, alias echo, uniqueness and stable published alias checks are unchanged. LiveChannel is byte-identical68 and still validates before runtime returned/join. Guarded public wrappers, failure containment, one selected Session/runtime and all other production files are unchanged. Driver failure still may discard its unexposed local row while retaining failed runtime state;71 neither improves nor weakens that inherited distinction.

## Limits and future callback identity

Using the selected SDK tag name does not turn a pipe token into a vendor object. The conversion design explicitly relies on the selected Windows object-pointer model; it requires the proposed actual native object probe with tags incomplete, not an ISO portability assertion. Tokens must never enter a real in-process SDK call or survive a switch between implementations.

Future EOS/stream callback dispatch must deliver the same `sampleToken`/`streamToken` derived from the retained client row that ordinary API callers received. That is necessary for Audio's existing stored-handle comparisons. Repeated borrowed lookup already returns the same embedded-row token; there is no implemented EOS dispatcher here to review or certify. No new function-pointer cast or false callback-forwarding implementation was added. Public callback registration remains missing, along with the other17 omissions inherited from68.

The selected quoted include closure matches its manifest exactly, with only the intentional two host `Mss.h` references external. This inventory does not cure the known inherited missing registry API or establish a native link. The explicit source partition must still exclude obsolete native facade files. Successful host stream routing, borrowed control admission, callback TLS adoption, locks, content binding and paired normal shutdown remain absent. Session's terminal destructor and shutdown's local proxy clearing are preserved limitations, not a cleanup proof.

The proposed focused probes are appropriately scoped if they execute the actual lookup/validator bodies and retain these platform/runtime exclusions. No probe pass is claimed by this review.
