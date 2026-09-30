# Named-sample binding lifetime review 30

2026-09-30. **Decision: prepare a narrow original-x86-DLL lifetime experiment before implementing binder retirement.** Existing evidence establishes the API signature and ordinary same-handle rebinding use, but does not establish whether a failed bind retains incoming storage, preserves the prior binding, clears it, or partially changes it. A correct owner can be prepared now; its reclamation rule cannot honestly be selected from current evidence.

No runtime, VM, native binary, playback or vendor test was executed. No production or frozen candidate files were modified. This document is a proposal for later parent review, not execution authorization. No SDK64 binary is assumed; eventual production architecture remains VS2013 x64 client and x86 original-DLL host.

## What the possessed sources establish

The inspected `candidate/.../miles/include/Mss.h` identifies itself as **7.2a, 20-Dec-07** (lines 31–35). At lines 4492–4496 it declares `AIL_set_named_sample_file(HSAMPLE, C8 const*, void const*, U32 file_size, S32 block)` returning S32 with AILCALL. It does not annotate copying, input lifetime, successful replacement reclamation, failure rollback, or suffix retention. At lines 853–855 its format-detection comment requires the first 8192 bytes or the complete smaller image. That is a format inspection minimum, not permission to upload only a header for later playback. Use full declared images and exact U32 byte counts.

The native `Audio.cpp` call sites imply these requirements:

- `getSampleTime` at lines 4423–4464 creates a fresh HSAMPLE, provides image and a stack SampleCacheEntry suffix, and on nonzero bind result queries milliseconds, ends, then releases before the suffix goes out of scope. Its caller around lines 3702–3730 frees the image afterward. This demonstrates caller lifetime intent, not a vendor lifetime guarantee. **The old helper releases only on successful bind; failed bind or null image leaks its allocated handle.** Do not copy that control flow into a new seam or treat its lack of a crash as proof of failed-bind safety.
- `playBufferedSound` / `playBufferedMusic` at lines 5324–5360 retain one HSAMPLE each. Later calls stop/end the existing allocation, then bind a new image on that same handle and start it. They ignore the bind return. Their stop helpers at lines 5364–5381 do not release. Consequently same-handle repeated binding is ordinary existing use; a one-bind cap changes behavior. Stop/end is not established here as permission to free either input.
- `startSample` at line 2832 binds cached bytes and starts only on success. Cached image storage is external to the Miles call. SampleCacheEntry owns its five-byte extension array but only stores a raw image pointer. None of these call sites prove rollback after failed rebind.

This source snapshot is explicitly identified by hashes below. The separate file-executor29 candidate was checked for corresponding call sites, which retain these patterns at shifted line numbers; no assumption was made that a prior candidate fixed the lifetime problem.

## Documentation search and applicability

Searched local Work, Documents and Imported-Windows paths for Miles/MSS manuals or API pages; no usable version-specific function documentation was located. The found private fixture `miles/index.html` did not provide API documentation. This is a bounded search result, not a claim that no manual exists anywhere.

Official RAD history explicitly dates 7.2a to 20-Dec-2007 and lists `AIL_set_named_sample_file` support for multichannel PCM WAV/Ogg. The same history records later Ogg decoder and asynchronous parsing changes, including background Ogg parsing in 7.2f. It therefore supports matching the **possessed binary and codecs**, not applying a modern SDK or other format's behavior to 7.2a. The public history does not specify bind failure or input-retirement semantics. [RAD Miles development history](https://www.radgametools.com/msshist.htm)

Search results for stubs, reimplementations and third-party header mirrors were not used as semantic evidence. No authoritative public function reference establishing failed-bind lifetime was obtained. A licensed 7.2a manual or an explicit RAD contract applicable to the actual DLL would be stronger evidence than a finite black-box probe.

## Small owner design, conditional on the missing boundary

Use the existing sample identity and same native HSAMPLE. Add one host-owned image/suffix pair per established binding and a prepared pending pair during a bind. Do not add a new public audio engine or replace the native sample on rebind.

1. Before any Miles call, validate the live sample and request fields, resolve a sealed upload, copy the full image and NUL-terminated suffix into stable host storage, and allocate the ownership record and any required container node. Account for both old and pending bytes plus preparation copies. A pre-call refusal or allocation failure leaves sample and existing owner unchanged; this is not a native bind result.
2. Make pending ownership durable in the sample record **before** calling Miles. Fetch/validate stable views first. A local variable destroyed on a post-call error must not free bytes Miles may have retained. All post-call bookkeeping must be scalar/pointer assignments or no-throw ownership swaps. Transmit exact native S32 result bits; zero is a completed native failure, not transport failure.
3. After a nonzero result, make pending the current pair. Retire prior pairs only if the applicable successful-rebind boundary has been established. Do not silently assume `RetainedBuffers::commit` means Miles released the old image.
4. After zero, preserve the actual resulting native state. Do not report the old image as active merely because its C++ owner remains. Keep both possibly referenced pairs until evidence establishes which can be reclaimed. Do not auto-rebind the old image, release/reallocate the handle, or retry: those extra native side effects would change failed-bind semantics and potentially properties or callbacks.
5. Keep potentially referenced input through native release/shutdown return. Clear ownership only after the established native lifetime endpoint. If the call's outcome is unknown, preserve ownership and use existing terminal session handling; do not retry or manufacture success.

`BufferUpload` already provides complete ordered upload/seal and an independent copy. `PreparedInput` already copies image and suffix before use and gives stable views while its owner lives. It is preparation only, and is not attached to a sample. Its per-instance limit does not account for old plus pending pairs or transient copies across a session. `RetainedBuffers` explicitly protects active storage and does not automatically retire a prior commit. Its single active token cannot by itself represent an image/suffix pair or resolve vendor lifetime; an owning pair object is the simpler unit.

**Do not ship indefinite history retention or an arbitrary one-bind limit as the answer.** Once success is proven to detach prior inputs, repeated successful A/B binding should have constant retained storage: one current pair after each call, two during transition. For failure, obtain a concrete rule: incoming unused and reclaimable; prior cleared and reclaimable; or both temporarily referenced with a specific later detachment boundary. If no bounded reclamation rule can be established for repeated failures, the generic native-compatible binder remains unresolved. An aggregate pre-call memory budget is legitimate resource protection, but does not turn that unresolved behavior into a completed implementation.

“Preserve on error” has two meanings: validation/transport errors must preserve client outputs and avoid invented SDK results; a completed zero-return vendor call must preserve **native observed behavior**, which may include changes to the old binding. The facade cannot promise rollback that Miles does not promise.

## Smallest discriminating original-DLL proposal

Start with a tiny VS2013 **x86** console harness using the possessed header/import library and exact original DLL path/hash. No x64 SDK binary, engine, IPC machinery or playback is necessary to distinguish the initial states. Record loaded DLL/version, header/import/DLL hashes and codec module identities. Open the same 22050 Hz/16-bit/stereo driver configuration used by the seam. Register no callbacks; never call start/resume or any playback function. Prepare all records and input buffers before binding.

Generate owned synthetic PCM WAVs, with byte-for-byte reproducible headers and data: A is mono 16-bit 22050 Hz, 22050 frames (1 second); B is the same format, 44100 frames (2 seconds). Use full images, 44144 and 88244 bytes for canonical 44-byte headers, with valid RIFF/data lengths and silent samples. Use distinct allocations and separately owned `.wav` suffixes. Generate F as a complete bounded RIFF/WAVE image with a structurally valid format chunk but an unsupported format tag and consistent lengths; require an observed zero return before labeling it a failed-bind case. Do not use out-of-bounds lengths, freed pointers or tiny truncated buffers. If F is unexpectedly accepted, stop and revise the fixture; do not reinterpret success as failure.

Initial matrix, all buffers kept alive unchanged until release:

| Case | Calls on one allocation | Discriminating observations |
|---|---|---|
| S | bind A; query; end; bind B; query; end; bind A; query; release | Same handle changes 1s → 2s → 1s after nonzero results; end is not release. |
| F0 | bind F; record return/error; query only if permitted by the API contract; release | Fresh failed binding has a baseline distinct from prior-binding preservation. |
| F1 | bind A; query; end; bind F; record result/error; query; release | Zero result followed by A-like, cleared or changed query state separates failure hypotheses. |
| R | bind A; end; bind F; record; bind B; query; end; release | Successful recovery after failed rebind, preserving same native identity. |

Log exact S32 returns, sample status, total/current milliseconds initialized to sentinels before every query, and immediate last-error text. Do not normalize all failures to zero duration or assume query is safe on every failed/unbound state; that portion needs the applicable API documentation or explicit parent acceptance as a characterization probe. A finite small repeat (e.g. 8 A/B transitions) can check repeatability after the initial cases pass. Full stress or playback is a later scope.

**State observations alone cannot prove absence of retained pointers.** Duration can be cached. Add a separately parent-reviewed access-observation variant only after the baseline: place A/B/F images and suffixes on distinct owned page allocations and temporarily protect exactly one obsolete/candidate range after the call returns, keeping allocations owned and addresses unreused. Observe query, next bind, end and release separately. A read/write fault is positive evidence that retirement at that boundary is wrong; record instruction/module, phase and protected range, then terminate that isolated run rather than swallowing a vendor access violation and continuing. Keep all ranges readable during each bind. Use separate processes for old-image, failed-input and suffix probes so attribution is clear. No process-wide allocator replacement, fuzzing, executable patch or broad fault injection is needed.

An absence of faults in those no-playback paths is only evidence for those exact paths/format/binary. It does not prove safety for asynchronous codec reads or the buffered playback callers. Testing successful PCM replacement does not generalize to MP3/Ogg or all failure branches. To admit buffered playback later, require matching contract evidence or a separately reviewed minimal playback/codec experiment. This review authorizes neither.

## Decision outputs required before implementation

The parent-reviewed experiment/report should answer: does successful rebind detach the previous image and suffix on return; what changes after a zero return; may failure retain incoming or prior input; what is the safe later detachment boundary; and which formats/binary versions that answer covers. If evidence supports one-current-pair ownership and failure reclamation, implement that direct rule with no post-vendor allocation. If it does not, keep binder readiness explicitly open instead of concealing the gap with a cap, permanent retention or rollback emulation.

## Exact local source identities

- `/home/akilleez/Work/client-wire-validation/candidate/src/engine/client/library/clientAudio/src/win32/Audio.cpp`: `a6e42b483283c3ff2a1476e48daa4f67312f6a1608ae68b03d988cc1a47dc615`
- `/home/akilleez/Work/client-wire-validation/candidate/src/engine/client/library/clientAudio/src/win32/SampleCacheEntry.h`: `9468221b2b3078b05ed0dabdaf9bc2926c204be591c18580a0644e90cc74c139`
- `/home/akilleez/Work/client-wire-validation/candidate/src/engine/client/library/clientAudio/src/win32/SampleCacheEntry.cpp`: `64e5f3949f4710b7eb6d4852f779316c242b179365e3fc6568ed9ec059ab7d62`
- `/home/akilleez/Work/client-wire-validation/candidate/src/external/3rd/library/miles/include/Mss.h`: `966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e`
- `/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/sample-pipe29/prepared_input.h`: `aa2304695b33aca618ba172e9b47a841ec433734898f68897a11d1f52e40c285`
- `/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/buffer-upload-candidate/buffer_upload.h`: `a3fef35e517a2f3a8d6bc96592f09876eca61ae8241686059160ca1a751d889e`
- `/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/buffer-upload-candidate/buffer_upload.cpp`: `e36e074e1031f4df9366b865131e7575045a0d497c07219b576f3ce419fd9bd5`
- `/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/host-candidate/retained_buffers.h`: `e62c472f1e46f783a130da8081bb92e958d8e3acaa9010d2fabae6169f329d8e`
- `/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/host-candidate/retained_buffers.cpp`: `263e9ae67ce8f0142758a82f7c85606e56f223125c78eac7199de37c23207091`
