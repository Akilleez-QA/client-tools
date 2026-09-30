# Retained ownership component: bounded mechanics only

Native VS2013/v120 x86 and x64, Debug and Release, /W4 /WX: all four compile/run exit0, **41/41 checks each**. Linux ASan/UBSan passes41. Three discriminating mutants compile then fail normally: permit retiring the active token, retire the previous token during commit, omit byte-cap rejection. Raw text evidence is in retained-results; source identities are in retained-results/source-manifest.json. No original vendor code was loaded or called.

The current v3 dispatcher is unchanged and preserved under history/v3 and input-v3.tar. This component is not connected to it and implements no Miles export.

## Adapter proposal, not enabled

- `AIL_set_named_sample_file` (Audio.cpp2836,4449,5338,5358): copy the explicit fileSize/bufferLength into a Binary entry. Preserve suffix text separately with its exact terminator. Obtain immutable view only after successful stage; pass that local pointer and exact U32 size to the real function.
- `AIL_set_sample_file` (2925): caller adapter must carry the already-known cache entry m_fileSize even though the original vendor API lacks a size. Do not infer extent by parsing or reading beyond supplied bytes.
- Stage before calling the vendor. Failure to stage means no vendor invocation. Vendor return0 must not change active ownership, and neither candidate nor previous storage is freed automatically: it is not established which references a failing vendor call retains. On successful return, commit records the new association but also keeps previous storage.
- `AIL_last_error` and `AIL_set_redist_directory` return text: a separate adapter must establish the readable terminated extent while the vendor result is valid, then stage exact terminated bytes. NullText is distinct from one-byte empty Text. This component never calls unbounded strlen and does not invent a maximum vendor string length. Client shadow-pointer lifetime and concurrent last-error ordering are still unimplemented.
- Explicit retire/deactivate/destruction requires caller proof that no vendor or callback can use the relevant data. Commit success alone is not that proof. Existing tests destroy ordinary stores with no vendor references; they **do not test or enforce vendor quiescence**.

## Boundaries

Tokens are process-local nonpointer IDs shared across stores without reuse. Cross-resource view/commit/retire fail, even when stores both have their first entry. A store remains single-dispatch-thread-owned; the token allocator is atomic only to avoid duplicate IDs across stores. Token exhaustion rejects rather than wraps into reuse. No cross-session/wire authorization is supplied by these IDs.

Caps limit retained payload bytes and entries. Map/vector overhead and transient copying are not included, so this is not a hard process memory limit. Conservative retention can reach a cap; rejection/backpressure is explicit and has not been shown equivalent to the original client's resource capacity. Allocation exceptions propagate with prior active data and accounting unchanged; allocator-failure injection and global token exhaustion were not executed. Span validation assumes the caller's frame pointer/extent actually describes readable memory; it rejects invalid arithmetic before reading. Tests use small real buffers only.

No close/release callback policy, codec decision, host startup behavior, buffer content parser, EOS frontend or product shim is added.
