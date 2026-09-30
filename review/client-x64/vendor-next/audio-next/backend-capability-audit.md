# SWG audio backend decision evidence

Read-only inventory,2026-09-30. No JUCE backend implemented or selected.

Updated authority: the user now requires original experience/fidelity100%.
See helper-fidelity-audit.md; original32-bit Miles preservation is the preferred
investigation. Feature parity alone cannot authorize a replacement.

The useful replacement boundary is **clientAudio**, not a reimplementation of the
entire Miles SDK. The first-party scan found **62 distinct AIL functions at151
source call sites in two .cpp files**, Audio.cpp and SoundObject3d.cpp. No RIB calls.
These are lexical source counts after removing comments,string literals,literal
#if0 blocks; other build-conditionals remain. They are not observed runtime-call
counts. The raw scan71functions/167sites overcounts disabled audio capture and
comments. Every call site/source hash is in miles-live-source-inventory.json;
all62functions with line links are in miles-function-table.md.

## Existing boundary and concrete behaviors

| Surface | Source evidence | Replacement obligation |
|---|---|---|
| Device lifecycle | Audio.cpp1285–1335: redist path,startup,file callbacks,22050Hz16-bit driver,stereo retry | Device selection/error reporting,real output,start/stop sequencing,default-device failure behavior |
| Cached 2D voices | createSampleId566ff; startSample2796ff; HSAMPLE in Sample2d.h29 | Allocate/release voices; decode memory image selected by extension; volume,rate,status,position,loops,completion |
| 3D voices | Audio.cpp2907ff; Sample3d.h28; SoundObject3d.cpp32–34 | Listener transform and per-source position; rolloff and min/max distances; obstruction/occlusion; dry/wet reverb; orientation and channel mapping |
| Streams | Audio.cpp599–619,3030ff; SampleStream.h27 | File-backed decode/buffering; pause/resume/seek; loop blocks/counts; completion; expose equivalent underlying voice controls used by stream_sample_handle |
| Event lifecycle | Audio.cpp4728–4790 EOS callbacks mutate maps/status and call Sound2::endOfSample | Exactly-once/reentrant completion,object lifetime and correct thread dispatch; cannot call SWG game objects from arbitrary real-time callback |
| File system | Audio.cpp3937–4100 callbacks → TreeFile/AbstractFile | TRE/cache lookup,read/seek/tell/close behavior and thread setup; raw OS filename loading is insufficient |
| Voice prioritization | Audio.cppcreateSampleId/alter/startSound paths, start queue lock2318–2335 | Keep existing SWG sound/template selection,limits,priority eviction,delays and category fades outside backend |
| Musical loops | datatables/music/music.iff at1343; getLoopOffsets4690ff; loop_block at2848/3033 | Preserve exact byte-based loop offsets and loop counts when converting to decoder sample positions; seek/decoder delay matter |
| Timing and service | Audio::serve4939ff, rate-limited main-thread AIL_serve; setLargePreMixBuffer5114ff | Stable timing/position query semantics,buffer starvation handling,loading-screen premix behavior and observability |
| Spatial environments | Audio.h87–115 exposes26room presets; Audio.cpp3780ff maps to Miles | Map or deliberately reauthor each preset; a generic reverb knob is not demonstrated acoustic parity |
| Buffered sound/music | Audio.cpp5200ff start/stopBuffered* | Memory-buffer playback and distinct category/mute/fade behavior must remain |

The public Audio.h API is largely SWG types, not Miles handles; internal
Sample2d/Sample3d/SampleStream hold HSAMPLE/HSTREAM and SoundObject3d holds
HDIGDRIVER. FirstClientAudio.h18 includes mss.h for this library. SOUNDINFO is
consumed by getSampleInformation3691ff: bits,block_size,channels,data_len,format,
rate,samples. A replacement needs equivalent metadata, not a copied vendor struct.
HPROVIDER/HDRIVERSTATE globals remain, but the actual filter calls are inside
#if0 capture code5410–5474. Treat that as pre-existing disabled functionality;
do not remove it or charge it as currently executing playback requirements.

## Formats and assets: established versus still unknown

Actual SDK include selected by clientAudio.vcxproj is miles/include/Mss.h **7.2a**;
a second7.2e tree exists but is not the observed project include. PCM_WAV,
ADPCM_WAV,ASI and MPEG classes in Audio::getSampleType are a diagnostic classifier,
not proof those assets exist or all are playable. Cached samples use actual
extension + memory image;3D samples use AIL_set_sample_file. File images come from
TreeFile,including packed TRE content. The client data directory has TRE archives;
this pass has **not enumerated/decompressed their audio entries**. Therefore
codec completeness is unresolved until a real asset inventory records format
headers,compression tags,channels,rates,loop metadata and corrupt cases. Do not
assume 'JUCE reads WAV' entails legacy IMA ADPCM/ASI compatibility.

ConfigClientAudio.cpp36–38 defaults cached2D cutoff64KiB (bounded512KiB),
obstruction0.6,occlusion0.95. Audio.cpp1264–1273 preserves master/category volumes,
max samples,enabled flag,provider and fade factor. Speaker options include system,
headphones,stereo,4.0,5.1,6.1,7.1,8.1 and Dolby-surround mappings. These UI choices
need honest new-backend mappings, not silently ignored settings. Listener/sample
velocity is explicitly zero in the inspected path; do not invent a currently
active Doppler requirement, but preserve positional/orientation semantics.

## JUCE and a32-bit helper: what is actually being compared

JUCE provides useful building blocks: device management and audio callbacks,
format readers from files or custom InputStreams,and mono/stereo FreeVerb-style
reverb. These are documented capabilities,not evidence of a drop-in spatial
Miles replacement. Sources inspected2026-09-30:

- https://docs.juce.com/master/classjuce_1_1AudioDeviceManager.html
- https://docs.juce.com/master/classjuce_1_1AudioFormatManager.html
- https://docs.juce.com/master/classjuce_1_1Reverb.html
- https://github.com/juce-framework/JUCE#minimum-system-requirements

Current JUCE requires C++17 and Visual Studio2019 or later,whereas this client
uses v120/VS2013. A modern-toolchain audio DLL with an explicit C ABI is a viable
architecture to investigate without moving every SWG project, but keep allocation
ownership/exceptions/STL types inside each module. Do not link its C++ objects
straight into a VS2013/STLport executable and assume ABI compatibility. No JUCE
version,license or deployment baseline is chosen in this audit.

| Option | What it preserves | What must be built/measured | Main uncertainty |
|---|---|---|---|
| Modern native audio backend,JUCE as components | Existing SWG high-level sound selection/templates/categories can remain | Mixer/voice lifecycle,3D panning and attenuation,occlusion,26reverbs,codec/loop/seek behavior,TreeFile stream adapter,thread-safe completion,ABI boundary | Audible/gameplay parity and maintenance burden; substantial semantic implementation |
|32-bit Miles helper process | Existing licensed/runtime-compatible32-bit DSP,codecs,room behavior may remain | Real32-bit host,versioned IPC with opaque IDs/generations,buffer transfer/backpressure,file I/O strategy,event ordering,latency,crash/restart/shutdown recovery | End-to-end command/audio latency and callback deadlock;helper still32-bit memory-limited |

A helper should host the digital driver and stream decoder and output sound
itself. A synchronous cross-process call for every tiny audio/file callback would
risk deadline misses/deadlock. Investigate preloaded/shared-memory data or an
explicit asynchronous TreeFile service. HSAMPLE,HSTREAM,function pointers,STL
containers and engine object addresses must never cross IPC. Completion becomes
an event carrying a stable generation-tagged sound ID,not a copied callback
address. This preserves vendor algorithms only; latency/order differences still
need tests. Runtime redistribution rights remain a separate project constraint.

## Mandatory acceptance probes before selecting/merging a backend

1. Asset census plus actual decode of every observed format class,including
   TRE reads;compare sample count,duration,channel order and corrupt-file failure.
2. Stock32-bit baseline capture for deterministic PCM impulses/tones and real
   assets;observe gain,pitch,position,loop seam and seek offsets. Predeclare numeric
   tolerances separately from listening acceptance;do not require arbitrary
   compressed-decoder bit identity.
3. Cached2D,3D and long streamed voices across cutoff;pause/resume/rate change,
   finite/infinite loops and byte-loop blocks,including block boundaries.
4. Listener yaw/pitch/translation with fixed sources;front/back/left/right and
   distance curves;each output layout that UI exposes;no silent channel drop.
5. All26room presets plus dry/wet,obstruction/occlusion sweeps and transitions;
   compare audible tails and continuity,not just API return codes.
6. Exactly-once EOS under natural end,looping,stop,eviction,destruction,restart;
   record thread identity and no callback into destroyed Sound2/map entries.
7. Stream/file concurrency and main-thread stalls;no allocator/file/IPC blocking
   on real-time callback;measure underruns and worst-case callback latency.
8. Voice exhaustion and prioritization with realistic combat/ambient crowds;
   keep existing category/mute/ducking/user preferences and loading premix behavior.
9. Native Win32 regression with original backend and native x64 with candidate;
   no feature removal or success from silent rendering.
10. Device unavailable/hotplug/config-invalid/repeated install/remove;for helper,
    crash/hang/disconnect and restart without hung client or stale callbacks.
11. Budget CPU,memory and measured input-to-output latency before test;measure
    helper transport separately from decoder/device latency. No guessed penalty.
12. Representative ground/space gameplay recording and project maintainer
    listening review,including music,UI,ambient,combat and voiceover categories.

## Decision boundary

This inventory supports a bounded prototype decision,not backend adoption. The
actual SDK surface is concentrated,but reproducing acoustic semantics is larger
than replacing62function names. Strongest rival to a rewrite is preserving the
vendor behavior behind a32-bit helper; strongest rival to that helper is avoiding
its scheduling/IPC failure modes with a native backend. Choose after asset census
and one comparable3D+looping-stream prototype on both architectures. No JUCE,
helper or vendor replacement source was authored in this audit.
