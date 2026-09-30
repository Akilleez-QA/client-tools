# CLI reconciliation26 — scoped inventory and file-value review

## Runs and retained identities

Composer `composer-2.5` completed `composer-inventory26` with exit **0**. [Prompt](composer-inventory26-prompt.txt), [raw log](composer-inventory26-log.txt), [exit](composer-inventory26-exit.txt), [input/output identity](composer-inventory26-identity.json) and [independent source inventory](composer-inventory26-verification.json) are retained. The 36,530-byte prompt SHA256 is `29f4dc928e6d3fbc62e2574963db94ae9b250e916fa06b93461f495d2afefad4`.

Grok `grok-4.7-high` reached the 300-second cap for `grok-file-channel26`, with exit **124** and no output. Its process group was terminated. [Prompt](grok-file-channel26-prompt.txt), [empty log](grok-file-channel26-log.txt), [exit](grok-file-channel26-exit.txt) and [identity](grok-file-channel26-identity.json) are retained. The prompt SHA256 is `302253eb1ffc7b834ce34c8386ec3eac37f64b320810f7d24adfdc07faba55c9`. **There is no Grok file26 review, finding or approval.** Neither prompt was retried.

Both jobs used read-only ask mode with supplied source only. No private SDK body, credentials or peer opinions were sent. Both had 300-second subprocess limits with process-group cleanup. No vendor/engine/VM runtime or product edits were performed by this review worker.

## Composer inventory: accepted and corrected

The inventory is scoped to actual client-build-next Audio.cpp, Sound2d.cpp and Sound3d.cpp. Audio.cpp SHA256 is `c729174ada8104331702422879ecbfa4986a6c4bba49bc3d763ab62a2e401406`. Mechanical extraction strips comments and string literals and finds **64 distinct direct AIL call names**, including conditional source paths. Fourteen correspond to an existing public facade24/native25 operation; **50 remain absent from that public surface**. This is a source inventory, not a preprocessed call graph or a count of already-migrated production calls. Sound2d.cpp and Sound3d.cpp have no direct AIL calls; their Audio-method calls connect them to the missing sample/stream operations. Exact operations/locations and hashes are in the verification JSON.

Composer's grouped inventory is useful: sample ownership/binding/control; streams and stream-sample aliases; per-sample spatial/mix controls; time/position; metadata/device diagnostics; filters; and lock/unlock. Its raw recommendations are advisory. Two claims need correction:

1. Native25 file callbacks are not merely declared: native_startup25.cpp lines43–45 delegates registration to AIL_set_file_callbacks. The pipe still lacks that implementation.
2. Its proposed roughly fourteen-operation batch would not unblock ordinary cached 2D/3D playback. Audio::startSample also reaches set_sample_reverb_levels through setSampleVolume (Audio.cpp3174/3197), loop/EOS handling (2851–2878 and2947–2960), and 3D position/velocity/distances (2965–2988). Composer defers these operations while claiming cached playback is unblocked. That claim is rejected.

The smaller coherent next source batch is the no-playback duration path at Audio.cpp4437–4455: allocate_sample_handle, set_named_sample_file, sample_ms_position, end_sample and release_sample_handle. It would add an opaque owned sample identity tied to the driver, preserve file-image/extension lifetime through bind/query/release, and verify exact SDK signatures before implementation. Controls should distinguish null allocation, rejected binding, output values, release ordering and handle reuse. This recommendation does not claim vendor execution or runtime fidelity.

The actual duration helper releases its temporary sample only on successful binding. That existing caller cleanup gap is not solved by adding wrappers and must not be hidden in a broader completion claim. Literal gameplay integration, stream aliases, EOS callbacks and image lifetime across asynchronous playback remain separate work.

## Frozen file26 identity and independent source check

The Grok input was frozen file-channel26 manifest `b064bdbf619920c045f1e5f1b3a9327d3141b76e6d886d651566dc1fd9931425`, source-v1.tar `714d75ccbc2356bd059dc85d905333a977a526a250924f6b6aeecf2c121316bb`. Input hashes were checked before launch and again after timeout. No findings from parent or supplemental tests were sent to the running model.

Direct source inspection supports the narrow value/invocation mapping: successful open status is distinct from valid local key0; failed-open identity cannot be published; negative seek result bits are retained; excessive read counts preserve the original return bits and become ReadCountOutsideBuffer instead of EOF; reply bytes are owned; duplicate Invocation entry does not call the service again; callback exceptions become CallThrew without an automatic retry or close. encodeResult builds a temporary frame and swaps only after construction, so the shown post-open encoding-allocation failure retains completion and leaves the caller frame unchanged.

The frozen file_channel.cpp SHA256 `0c5253d7f2a3a7b06ba54af756f170eca6c5f3b84fbbdce952a5700de6a64e27` already allocates one byte for a zero-count read (line133), yielding a nonnull canonical-service buffer (line159). Both frozen archive and current source were independently checked. An earlier in-progress null-buffer observation cannot be attributed to this frozen identity. The separate worker zero-count discrimination supplement is separate evidence, not a Grok finding or a frozen source change.

No new concrete mapping defect was found by this worker's source check. The check is not Grok coverage and is not runtime acceptance. Real executor/TLS admission, serialization with original callbacks, successful-open publication ownership, disconnect/uncertain-completion cleanup and file retirement are explicitly external and remain unresolved. Invocation retention must be supplied by that owner; a shared_ptr pin alone does not prove thread or engine lifetime. All supplied tests are scripted; canonical services were not invoked by this reviewer.
