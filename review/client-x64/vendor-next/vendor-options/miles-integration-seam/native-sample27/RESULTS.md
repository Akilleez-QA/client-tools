# Native sample27 preparation

Prepared exactly five ordinary ClientMiles functions and direct SDK delegates: allocate_sample_handle, set_named_sample_file, sample_ms_position, end_sample and release_sample_handle. The new opaque OwnedSample identity represents allocated samples only. The header preserves existing pointer-plus-U32-length input, signed32 block/result values and both signed32 millisecond output pointers. It contains no SDK, wire or process types.

The portable header/usage checks compiled two objects on the first attempt with warnings-as-errors. The sample object retains all five unresolved ClientMiles references. All recorded source/compiler inputs remained unchanged. Python sources passed syntax parsing. No executable was linked or run, and the portable check does not compile the native implementation against the SDK.

The example keeps the caller's extension and complete image stable through release. It preserves query→end→release after successful binding and releases the allocation after a normal failed bind, avoiding the original helper's release-only-on-success leak. This is an authored normal-return example, not an observed cleanup result or a future uncertain-transport failure policy. It does not recreate extension selection, source loading or Audio's installation policy.

`build-native.py` is ready but unrun. After explicit parent approval it would compile three AMD64 objects using actual v120 and the pinned private7.2a header, check every SDK signature/scalar type, and inspect exactly five unresolved real AIL imports. It uses no fake import library, vendor link, loader or runtime. No VM staging has occurred.

| Artifact | SHA256 |
|---|---|
| source-v1.tar,15 members | 34dd35b74995f1166d6b4ba68391feaa53e8e367812e0ea7b1a7aab23351eb82 |
| source-manifest.json | ec62d406a40293fc10bc9420707a78d5379b771d9d9289d9298f57a6bc7afdee |
| evidence-portable-v1/receipt.json | da9beebfb82ed64790635f56c2cf734c42679274e29e9965140305c32d7d06b1 |

The source manifest is a flat mapping of seam-relative paths to digest strings. The text packet manifest maps packet-relative paths to `{bytes,sha256}` records, with this native-sample27 directory as path base. Private objects, vendor files, SDK bodies and nested archives are excluded from the text packet.

Delivery state: checked source preparation. Native actual-header outcome: unobserved. The highest justified claim is that the public declaration/example boundary compiles portably and the five direct SDK delegates are authored for review. Parent controls the remaining v120 object gate. No Miles64 executable compatibility, sample ownership/lifetime runtime behavior, playback, callbacks, engine integration, pipe implementation or whole-client fidelity is established. All frozen source and product files remain unchanged.
