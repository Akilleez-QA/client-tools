# Native game-facing surface gaps 50

Read-only source audit against product `/home/akilleez/Work/swg-source/client-build-next`, whose HEAD was read as `49d0eeed4ddaa177d7a93ea396c37c3d9b9942da`. No compilation, tests, SDK/engine execution, or product edits. No SDK bodies are reproduced. Existing compile receipts were inspected, not rerun. `API-PARTITION.md` is a lexical inventory, not a whole-program reachability proof.

Unless absolute, seam paths below are relative to `/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/`. `Audio.cpp` anchors refer to the actual product's `src/engine/client/library/clientAudio/src/win32/Audio.cpp`. Public headers were taken from **stream-native38/private-source-v1**, including its common Sample identity, plus the plain **native-file-callbacks35** interface. Obsolete top-level27/28 ownership types were not used as the comparator.

## Main adoption gap: the common header is still a modern-STL boundary

The current facade is not ready for direct inclusion in the real engine merely because its native delegates compiled. `stream-native38/private-source-v1/backend-boundary24/ClientMiles.h:4–6` includes cstdint, stdexcept and string; lines14–18 export `OwnedText` containing `std::string`; lines32–42 export `Failure` derived from `std::runtime_error`. Startup text functions at52–56 return that owning object by value. Sample, playback and stream headers all transitively include this same header, so the issue is not confined to callers of text functions.

This was intended as a game-facing source facade: `backend-boundary24/PLAN.md:19` says so explicitly. But the observed38 gate compiled an isolated ordinary call-shape TU and private adapter TUs with the VC standard library. Its real `evidence-native-v1/02/headers.log:2–15` shows the path through ClientMilesStream → ClientMilesSample → ClientMiles.h → VC cstdint/stdexcept; it does not enter FirstSharedFoundation/STLport. The actual build recipe is `stream-native38/private-source-v1/stream-native38/build-native.py:29–30`; its expected translation units are listed in expected.json. The receipt says linked=false and executed=false. That is useful declaration/object evidence, not an in-place Audio source/ABI check.

The engine starts through FirstClientAudio/FirstSharedFoundation and uses STLport. If an engine TU and a modern private TU instantiate the public OwnedText/Failure definitions against different standard-library implementations, the interface no longer has a demonstrated common object layout, destruction/allocator contract or exception base identity. This audit does **not** claim a fresh compiler failure was observed; it identifies an unresolved interface incompatibility that the isolated gate did not test. Swapping a native implementation behind that header is not enough to establish safe engine consumption.

Callback35 is the narrower useful precedent: `native-file-callbacks35/ClientMilesFileCallbacks.h:4–29` exposes integers, pointers and callback types, without STL ownership. Its engine_header_probe.cpp:2–4 includes FirstSharedFoundation before the public callback header. The existing raw results record compiler exit0 and AMD64 object creation, but the overall gate remains failed on its include-boundary oracle; this must not be relabeled an overall pass. It also probes extern callback-shaped declarations, not actual Audio bodies. It demonstrates a materially more appropriate public boundary without proving full replacement.

**Minimal direction:** keep ordinary Miles-shaped functions and opaque handles; put modern STL ownership and transport exceptions behind the adapter. Provide an engine-safe explicit text/nullness/lifetime contract—such as caller-provided storage or a documented retained native-style view—without passing private std::string objects across the boundary. Keep actual SDK null/zero results distinct from adapter failure. Do not expose wire frames, registration IDs, ACKs or scheduler objects to solve this problem. No design or implementation change was made here.

## Functions genuinely absent from the reviewed public declarations

These are omissions in the combined current surface, not requests for a full SDK facade. Existing similarly named private wire opcodes or host helpers do not supply game-facing declarations.

| Missing native operation | Actual source use and required behavior |
| --- | --- |
| `AIL_set_sample_file` | Audio.cpp:2925 binds the 3D sample's retained image. The existing set_named_sample_file declaration is not the same operation and cannot substitute without changing the call. Preserve the native result, image pointer and block semantics. |
| `AIL_register_EOS_callback` | Audio.cpp:2878 and2960 register real 2D/3D completion callbacks; callback bodies at4730 and4751 compare sample identity and invoke sound completion. Need a correctly typed local callback surface, preserving calling convention and native registration semantics, not a wire callback token. |
| `AIL_register_stream_callback` | Audio.cpp:3072, callback body4772. Stream completion likewise needs local stream identity and a native-shaped callback contract. ClientMilesStream.h:28 explicitly disclaims EOS lifetime today. |
| `AIL_file_type` | Audio.cpp:2546 identifies a supplied memory image/length and chooses file-type text. No equivalent public facade declaration exists. |
| `AIL_WAV_info` | Audio.cpp:3710 queries metadata, consumed at3714–3726. A minimal SDK-independent result shape needs the fields actually read: bits, block size, channels, data length, format, rate and sample count, with the original scalar success result. It need not expose the unused vendor data pointer or a serialized SoundInfo structure. |
| `AIL_get_timer_highest_delay` | Audio.cpp:1943 is in the ordinary alter path. Preserve its scalar result; do not substitute a pipe timing metric. |
| `AIL_digital_CPU_percent` | Audio.cpp:3526; called through getDigitalCpuPercent at1946 in the ordinary alter path. |
| `AIL_digital_latency` | Audio.cpp:3539; called through getDigitalLatency at1945 in the ordinary alter path. |
| `AIL_lock` / `AIL_unlock` | Audio.cpp:4922 and4928 are actual Audio method bodies. The public native facade lacks both. These remain separate native operations; pipe lease bookkeeping is not the game-facing replacement. |
| `AIL_active_sample_count` | Audio.cpp:681/683 are under _DEBUG;2900/3005 are diagnostic macro arguments. Missing for that supported diagnostic surface, but not evidence of an unconditional Release gameplay dependency. |
| `AIL_file_error` | Audio.cpp:4547 is real code inside getFileError. A search within clientAudio found only that helper definition, no call to it. It is a lexical/inventory omission, not independently established runtime liveness. Retain that distinction before making it a release-path priority. |

There are twelve absent inventory names, with different usage significance. That count is bookkeeping, not an engineering score or a reason to implement unused SDK functions. Compile/link reachability remains a separate observation.

## Smaller source-compatibility requirements

Audio still gets private SDK declarations transitively from `src/engine/client/library/clientAudio/src/shared/FirstClientAudio.h:18`. Replacing that include also requires the limited values/types actually consumed by engine code. Examples are provider/speaker choices at Audio.cpp:915–955, preferences at1297/5118/5125, sample status at2722/2727, file types at2552–2626, environment values at3788–3813, and the metadata output above. The present public startup header supplies only StereoSpeakerConfiguration; it does not complete this migration. Keep checked game-used scalar constants/plain result types, not private SDK structure bodies or protocol offsets. All provider choices must remain representable: the public open_digital_driver already has sufficient scalar parameters; a native implementation must not inherit the temporary pipe's stereo-only acceptance rule.

`last_errorOwned`, `set_redist_directoryOwned`, `MSS_versionOwned`, and `speaker_configuration_spec` are deliberate adaptations, not missing operations. They still require small caller edits at Audio.cpp:1285/1306/1313/2469/1326. The speaker-spec-only form covers the actual consumed output. The nullness/text ownership contract must survive the STL-boundary correction. Renaming alone is not an in-place binary or unchanged-source substitute.

## Restrictions that are already appropriate or are not native-surface gaps

The latest common Sample type is correct for current call sites. `native-sample27/ClientMilesSample.h:8–11` defines one HSAMPLE; stream_sample_handle returns it; `native-playback28/ClientMilesPlayback.h:5–9` explicitly permits the five borrowed operations used at Audio.cpp:3211,3212,3260,3305,3334. The native stream adapter delegates the query each time (`native-stream28/native_stream28.cpp:70–76`); it does not impose the pipe's stable cached-alias policy on Miles. No new borrowed-only function names or caller casts are needed. Owned-only release/end/binding restrictions do not conflict with the inspected stream call sites.

Callback35 already carries native-width file handles, independent uint32 open status and correctly shaped signed seek/count callbacks. A successful client-local handle value zero is representable. No new game-facing host token, table registration, installation ACK or callback scheduler is needed for a direct native64 adapter.

The startup public header's stereo/preference restrictions at ClientMiles.h:64–66 explicitly describe the **pipe implementation**. The inspected native delegate at `backend-boundary24/native/native_miles64.cpp:63–68,91–93` forwards native-width preferences and all driver arguments. Do not promote those temporary pipe restrictions into the common native contract; their explanatory comments belong with implementation limitations. This is not evidence that the native delegate currently rejects surround choices.

Do not add commented AIL_pause_stream, commented stream_volume_levels, or the filter/capture operations inside Audio.cpp's #if0 blocks at5412 onward just because a lexical search finds their names. No missing public operation was inferred from those disabled paths. Native adapter compiler guards pinned to v120 are evidence-scaffold limits in private implementation files, not game-facing function requirements or proof of compatibility with a future SDK/compiler.

The narrow native objects and plain callback probe provide useful groundwork. Completing the actually used declarations and establishing a plain engine/private-library boundary are the remaining surface work before claiming a straightforward native64 replacement. This document does not claim a linked client, SDK availability, gameplay behavior, or connected pipe composition.
