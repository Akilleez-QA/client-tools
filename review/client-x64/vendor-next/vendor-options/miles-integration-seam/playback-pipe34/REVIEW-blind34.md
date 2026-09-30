# Independent blind source review — playback-pipe34

Reviewed authored patches, composed sources, SDK declarations in the read-only product checkout, the real `host_dispatch.cpp`, reply validation and ownership paths before reading test code. Did not read other reviews, RESULTS, or evidence narratives. No SDK build, PE, vendor, or engine execution. Independently verified all 61 manifest entries against both disk and `source-v1.tar`; all matched. Frozen inputs were unchanged.

**Highest justified conclusion:** coherent source implementation of the 19 owned-sample controls, with real SDK dispatch targets; no demonstrated scalar-mapping, opcode, lifecycle, or ownership defect in this added slice. This is not a proven native-equivalent playback backend or a runnable host delivery.

## Findings and limits

1. **Aliased getter fidelity remains unproved (concrete topology loss, not an established vendor behavior bug).** `private-source-v1/backend-boundary24/pipe/ClientMilesPipe.cpp:400–415` encodes only output presence and writes first output then second. `host-candidate/host_dispatch.cpp:162,169` always supplies distinct host locals when both outputs are requested. Native wrappers pass original pointers through. Therefore `sample_volume_levels(s,&v,&v)` and the equivalent reverb call are not represented faithfully at the SDK-call boundary. The scripted alias assertion establishes only that the pipe chooses the second result; it cannot establish the vendor's write order or whether aliasing is supported. Resolve via an authoritative alias contract or explicit alias topology forwarding; do not label the current assertion native parity. SDK declarations alone establish neither write order nor alias preconditions.

2. **Host execution/build coverage is absent from this candidate's check and source closure.** `check.py:10` compiles the facade, codec and metadata/version helpers, not the modified `Backend`, `LiveChannel`, or real SDK dispatcher. The frozen archive has no host executable entry point invoking the modified backend. This is acceptable as a source-only addition but blocks a claim that these 19 controls are already backed by a delivered, integrated x86 host. Merely having dispatch cases does not show that a launched host executable contains them.

## Checked details

- All 19 new facade entry points map to corresponding real `::AIL_*` calls. Host calls reject unwanted fields, resolve resource identity, and preserve byte versus millisecond units.
- Signed setters convert to unsigned wire bits; host reconstructs `S32` by memcpy. Playback-rate getter uses explicit signed reconstruction. Status and byte position remain unsigned. No observed signedness defect.
- Float transport uses memcpy bit representations with no new clamps or arithmetic. Portable test bit patterns do not establish x86 floating-point ABI behavior or vendor handling of NaNs, infinities, denormals or out-of-domain parameters.
- Nullable outputs produce matching null host pointers. This preserves null shape without proving SDK null validity. On valid refusal, no caller outputs change and the session remains usable. Malformed/lost replies poison the session before copyout, with no replay or fabricated SDK result.
- Owned sample checks occur in both facade and backend; dispatcher resource resolution checks current registry identity. Controls do not introduce resource allocation or ownership transfer. Reusing a released raw HSAMPLE violates lifetime preconditions; address reuse is not itself a new bug here.
- Borrowed samples are deliberately excluded from this pipe slice despite their presence in the common facade declarations and broader SDK dispatcher. Missing binding/upload work (`set_named_sample_file`) prevents useful end-to-end playback but is stated unfinished scope, not a hidden implementation of a successful stub.

No portable scripted test was rerun: it cannot resolve the principal vendor semantics or host-delivery limits above.
