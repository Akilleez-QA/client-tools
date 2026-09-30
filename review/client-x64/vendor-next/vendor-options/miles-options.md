# Miles: options under the unchanged-experience requirement

Research date: 2026-09-30. Decision dossier, not a selected backend or a fidelity claim. User requires preserving the original experience and fidelity completely. No vendor contacted and no backend implementation changed.

## What is actually being replaced

The real client project includes **Miles 7.2a**, not the adjacent 7.2e directory. Header version is not runtime identity: hash the DLL and loaded ASI/FLT plugins before establishing an oracle. Existing first-party source has **62 distinct live AIL function names at 151 lexical sites** in Audio.cpp and SoundObject3d.cpp; comments, strings and literal `#if 0` removed, other build conditionals retained. There are no live RIB calls in that scan. These are source counts, not execution coverage.

[All function names and exact source links](../audio-next/miles-function-table.md), [machine-readable inventory](../audio-next/miles-live-source-inventory.json), [capability audit](../audio-next/backend-capability-audit.md), [synchronous coupling analysis](../audio-next/helper-fidelity-audit.md).

The wrapper opens a 22,050-Hz, 16-bit driver, uses cached sample and streaming paths, byte-based music loop boundaries, 26 environment presets, multichannel speaker choices, per-voice playback rates/gains, listener/source positions, obstruction/occlusion and EOS callbacks. It reads immediate status/playhead/volume/rate results. Listener/source velocities are explicitly zero in the inspected paths: do not invent a Doppler requirement. High-level SWG voice selection, music timing and fades should stay in place whatever backend is evaluated.

## Actual assets, rather than inferred codec support

A read-only parser based on `TreeFile_SearchNode.h:174–198` and `.cpp:274–345` read every top-level TRE in `swg-source-vm/client/SWGSource Client v3.0`. All TOCs/name blocks decompressed to their declared sizes. Across archives, including patch duplicates, there are **5,908 WAV entries and 373 MP3 entries**, 5,637 distinct media names. No BIK/OGG/FLAC/AIFF entries were found in this bounded root. This is not an effective mounted filesystem census: patch order, tombstones and loose overrides are not resolved.

All **5,900 nonempty WAV entries** parsed successfully; 8 other entries are empty. There are 5,786 format-tag-1 PCM entries and 114 WAVEFORMATEXTENSIBLE entries with the PCM subtype GUID. Most are mono 22,050-Hz 16-bit (5,045), but 44.1/48-kHz, stereo, 8/24-bit and unusual 22,255/11,050-Hz sources exist. Thus resampling/rounding is material even without ADPCM. No compressed WAV codec was observed here. A first real MP3 has now been decoded through the original runtime and compared with two open decoders; see the direct-evidence section. This is not a complete MP3 corpus validation. Empty entries are recorded, not automatically declared corrupt or tombstones.

Reproduce with [TRE scanner](tre-media-scan.py) and [WAV scanner](wav-format-scan.py); [entry metadata](tre-media-inventory.json) and [format counts/examples](wav-format-inventory.json) contain no redistributed audio. The scanners are diagnostic readers, not production replacements; source compatibility and data-size checks are their oracle.

## Options and decisive tradeoffs

| Option | What it preserves / gains | What remains different or unavailable | Effort and decisive experiment |
|---|---|---|---|
| Exact original SDK/source rebuilt for x64, if legitimately available | Closest in-process route to original algorithms, no IPC | Source and build rights not established; assembly, pointer width and plugins still need porting; x64 arithmetic may differ | Potentially best fidelity architecture, but presently blocked. Inventory licensed source and compare original/rebuilt decoder, mixer, reverb and timing |
| Matching-era official x64 Miles runtime/SDK | Original vendor/API family, avoids new process | Exact version/build availability and rights not established; nearby release is not identical DSP | Acquire only through authorized channels; test exact asset/command corpus against original DLL before preferring it |
| Current licensed Miles | Maintained vendor path, integrated game audio tools | Modern event/data model and DSP changes; not a drop-in proof of 7.2a sound | API migration + asset/behavior comparison. Public marketing does not establish older low-level compatibility |
| Original 32-bit Miles in helper process | Retains original decoder, mixer, reverb, loop implementation and plugins, with original output driver | IPC, scheduling, callback delivery, blocking getters, file I/O and lifecycle change; helper remains 32-bit; crashes/restart/state resync and packaging add work | Prototype a narrow original-DLL replay and measure output/timing first; significant integration effort, not a cheap shim |
| OpenAL Soft + decoder layer | Mature spatial audio, streaming buffers, environmental effects and loopback capture | New attenuation, resampling, panning/reverb; no automatic Miles decoder/byte-loop/EOS equivalence | Medium-to-large adapter plus decoder and exact SWG semantics. Compare wet/dry impulses, position curves, loops and callback timelines |
| miniaudio | Compact C backend, custom I/O, decode/resource/engine facilities; convenient reproducible capture/prototyping | Different spatialization/mixer; Miles room behavior and byte/MP3 loop semantics must be supplied; format support is not decoded-sample identity | Useful bounded decoder/output experiment. Full faithful backend substantial beyond initial playback |
| XAudio2 (+ explicit decoder/spatial/effect layer) | Native Windows mixing and voice graph, filters and sample-accurate operations | Lower-level API; MP3 decoder, file parser, 3D policy and Miles effects are separate; new resampler/quantum | Good Windows integration substrate, high semantic reconstruction effort; decoder + mixer oracle required |
| FMOD Core | Broad mature game-audio facilities, streaming and effects | Proprietary dependency remains; new DSP, callbacks, scheduling, resource policy and licensing | Functional migration likely easier than bespoke engine; still an extensive fidelity validation task |
| JUCE | Device I/O, file readers, processing framework and tooling | Not a Miles game-audio compatibility layer. Its stock FreeVerb-style reverb is not the 26 Miles environments; spatial/voice/loop policy must be built | Good analysis/capture tool or foundation, high backend reconstruction effort. No evidence it is a fidelity shortcut |
| Clean-room Miles-compatible reimplementation | Long-term source ownership and deliberate API compatibility | Reconstructing codecs, mix rounding, effects, edge cases and scheduling is a research project; matching names is insufficient | Highest uncertainty. Start only from measured behavior and explicit scope, not a guessed line estimate |
| Keep original Win32 client while x64 alternatives are evaluated | Exact existing integration remains available as oracle and supported experience | Does not complete x64 client | Honest fallback if no candidate meets the requirement; not a stub or removed feature |

Effort bands are comparative engineering judgments, not schedules or measured implementation sizes. A maintained replacement may be easier to operate than the helper once mature; an original licensed source rebuild could be better than both. Therefore **“helper strongest” only means strongest currently accessible experiment for retaining the exact legacy DSP**, not an established final architecture.

## Why the helper can still lose

Moving commands across a process boundary cannot preserve their exact arrival time automatically. The used start calls accept no future sample timestamp. Synchronous getters feed SWG decisions; stale mirrors can change fading, looping or eviction. EOS calls `Sound2d::endOfSample`, which changes loop/current-time state, calls a user callback and deliberately defers release. Callback thread identity and reentrancy must be observed, not guessed.

`Audio::alter(0)` occurs outside the regular frame update. `AIL_serve` is explicitly invoked on loading/premix paths. Coalescing all updates into one frame batch can therefore change behavior. A narrow transaction around the existing `AIL_lock`/start-queue/`AIL_unlock` sequence is a candidate only; getter, callback and serve boundaries are barriers.

A synchronous file-read callback can deadlock if the client waits for a helper call while the helper waits for client TreeFile I/O. A genuine 32-bit TreeFile implementation in the helper duplicates mount state; a dedicated I/O channel adds latency and lifetime complexity. Both require tests. Shared pointers, callbacks and STL objects cannot cross the process boundary. Handle generations, bounded queues and orderly shutdown are necessary but not proof of fidelity.

Direct helper output avoids adding a second resampler; alternatively transporting mixed PCM to the client introduces another buffer/device path. Neither removes OS scheduler variability. Measure repeated legacy baselines and incremental latency, under load, without declaring any new difference acceptable on the user's behalf.

## Decisive experiments in order

1. Fingerprint original DLL/plugins and establish a reproducible **Win32** baseline: same assets, driver/speaker settings, gain/rate, file search order and room presets. Trace command/EOS/status/playhead timing and thread IDs.
2. Use actual asset representatives: mono/stereo PCM at every observed rate/bit depth, extensible PCM, MP3 and music-loop table entries. Compare decoder sample counts, exact PCM, start/end trim, seek offsets and looping seams. A null render confirms mechanics only, not output fidelity.
3. Compare dry mix impulses, rate sweeps, gain/clipping, channel routing and all room/obstruction/occlusion settings. Separate decoded-sample identity from resampled/effected mix identity. Compare repeated stock runs first.
4. Original-runtime helper replay: same commands/assets, ordered results, EOS and loop boundaries. Then live game-event-to-output latency, CPU/disk pressure, moving sources, many voices and player music. A good offline replay cannot establish live timing.
5. Scene transition, stop-in-callback, shutdown, device loss and helper failure. Original audible behavior must remain the acceptance target; do not silently mute on failure.
6. Only then compare replacement engines with the same corpus. Exact differences remain evidence for a user decision; perceptual similarity alone does not satisfy the stated 100% requirement.

## Primary research and limits

Queries on 2026-09-30 included `site.radgametools.com Miles Sound System source code 64 bit licensing`, `site.openal-soft.org HRTF EFX resampler`, `site.miniaud.io decoding formats mp3 flac wav spatialization`, `site.fmod.com docs Core API reverb audio formats`, `site.learn.microsoft.com XAudio2 supported audio formats ADPCM PCM xWMA`, and `site.juce.com get juce licence AGPL commercial`. Primary pages below were read; search snippets were not treated as SDK compatibility proof.

- [RAD Miles overview](https://www.radgametools.com/miles.htm), [licensing](https://www.radgametools.com/sales.htm), [development history](https://www.radgametools.com/msshist.htm): vendor offers evaluation/licensing; history documents Windows-64 work, source rebuild scripts and later mixer/decoder behavior changes. This establishes that “Miles has no x64 ever” is false, not that a matching authorized SDK is available here. 7.2d changed mono multichannel placement and SIMD mixing; a neighboring version cannot be presumed identical. No license entitlement or source completeness established.
- [OpenAL Soft](https://openal-soft.org/): 1.25.2 offers Win32/Win64 binaries, spatial audio/EFX and loopback; current source requires C++20. A C ABI module can separate modern compilation from v120; DLL loading and exact artifact license still need review.
- [miniaudio manual](https://miniaud.io/docs/manual/): decoding/custom backends and spatial engine are documented. Their presence is not a promise of Miles-compatible output.
- [XAudio2 introduction](https://learn.microsoft.com/en-us/windows/win32/xaudio2/xaudio2-introduction), [Microsoft Wave Formats](https://github.com/microsoft/DirectXTK/wiki/Wave-Formats): low-level mixing/effects and supported input formats; MP3 needs a decoding layer. XAudio2 ADPCM support is not generic IMA-ADPCM support.
- [FMOD Core concepts](https://www.fmod.com/docs/2.03/api/core-api-concepts.html), [loading sounds](https://www.fmod.com/docs/2.03/api/loading-and-playing-sounds-in-the-core-api.html): file/stream/decompression facilities; no Miles bit-equivalence claim. Commercial terms and project eligibility not determined.
- [JUCE source README](https://github.com/juce-framework/JUCE), [AudioDeviceManager](https://docs.juce.com/master/classjuce_1_1AudioDeviceManager.html), [AudioFormatManager](https://docs.juce.com/master/classjuce_1_1AudioFormatManager.html), [Reverb](https://docs.juce.com/master/classjuce_1_1Reverb.html): modern toolchain/framework with device/decoder facilities and a simple FreeVerb-style reverb. Current README states AGPLv3/commercial licensing; exact selected modules/version terms must be assessed before distribution. It does not establish reuse permission for this project.

No new vendor SDK installed, no vendor contact, no replacement chosen. Existing callback width repair remains separate from this decision.

## New direct evidence: original decoder versus replacements

[The disposable native baseline](miles-probe/RESULTS.md) now establishes original DLL resource version7.2a, successful startup and original-plugin MP3 decode. VM output-driver creation is blocked by zero audio devices; it is not a playback success. On one real38,998-byte music asset, Miles, FFmpeg and miniaudio return the same frame count/rate/channels and best alignment0, but both open decoders differ on roughly23.7k of214,272 PCM channel samples (maximum502 signed16-bit units). This is concrete evidence against assuming drop-in decoder identity. Audibility and whole-game effects remain unassessed.
