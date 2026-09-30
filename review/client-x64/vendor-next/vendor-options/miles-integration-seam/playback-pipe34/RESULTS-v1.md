# Owned playback pipe34 result

Implemented all19 native-playback28 controls in the real private pipe implementation under their existing public names/signatures. Reused the common Sample opaque type, current owned-proxy validation, existing opcodes/framing and real host_dispatch. Reply decoding now permits the three scalar getters and two F32 output-pair getters; output masks are checked before either caller output changes. The host whitelist admits only owned sample targets for this new slice. No native delegates or SDK replacements were added.

The first frozen portable build/run passed strict C++11 warnings and ASan/UBSan. Authored scripted tests passed all19 mappings through actual request encode/decode and typed reply decode, exact value/output-mask fields, signed extrema and U32 values, float special bit patterns, all nullable output masks, aliased outputs, refusal without partial output changes and continued usability, malformed output rejection/unchanged outputs, uncertainty poisoning/no replay, foreign identity/no-channel and borrowed-kind allocation rejection. These scripted results establish client/protocol behavior only; they do not exercise Backend/SDK side effects or establish playback fidelity.

Source archive SHA256: `4dfb895fab817f7a0720b363e52a053d54864bcede06aecd12f03f0021e3e1d0`.
Manifest SHA256: `be276e5b00b586e3a59a78076245b9b7a2321f9de36aecd24cce81d2d893b895`.
Portable receipt SHA256: `00771ac984ef6aecb99e9a9f13a29139fed8ddfde6a2be8e4bbacfcf2246884f`.

No VM/native/vendor/engine execution, binding, playback or product change occurred. Pipe stream_sample_handle and set_named_sample_file remain unimplemented; no fake borrowed or binder success is supplied. Borrowed control support, true vendor state/readback, lifetime/binding, EOS/callback ordering and operational Audio integration remain separate work. All prior snapshots and successful evidence remain unchanged.
