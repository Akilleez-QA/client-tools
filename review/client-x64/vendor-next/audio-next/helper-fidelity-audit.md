# Original-Miles helper under the100%fidelity requirement

User requirement: preserve the original game experience and fidelity100%.
This makes the unchanged32-bit Miles runtime,original plugins and original assets
the fidelity-first prototype,not permission to substitute equivalent-sounding DSP.
No helper is implemented or selected here. Keeping the original algorithm does
not establish unchanged timing or complete game experience.

## Keep the reference exact

Record original mss32.dll and every loaded .asi/.flt plugin hash,actual version,
driver settings,speaker layout,mix frequency22050,bits16,buffer fragments and
asset bytes. Do not assume the7.2a header means the runtime DLL has that version.
The host's existing binaries are the candidate reference,not a modern Miles SDK.
The helper should own the original output driver,mixer,decoders,reverb and loops.
Sending its already-mixed PCM through another resampler/device stack would add
another semantic change and needs separate proof; direct helper output avoids
that particular extra change.

## Synchronous coupling that cannot be hidden by batching

| Call family | Actual SWG dependency | Cross-process consequence |
|---|---|---|
| AIL_open_digital_driver/startup/error | Audio.cpp1299–1315 chooses stereo fallback or shuts audio down on immediate result | Initialization needs real completion/error reply,not optimistic success |
| allocate_sample_handle/open_stream/set_named_sample_file/set_sample_file | createSampleId/startSample installs maps and handles failures immediately | IDs can be proxy tokens,but backend acceptance/failure must be observed before SWG assumes playback;pointer handles cannot cross |
| sample_playback_rate/volume_levels/stream_sample_handle | Audio.cppstartSample reads default rate then changes it;other getters feed fades and engine state | A stale cached value may change following commands;need ordered barrier or proven immutable/configured-value mirror |
| sample_status/stream_status | Audio.cpp2690–2735 combines vendor status with callback-maintained PS state | Snapshot must be consistent with all preceding commands/events;one-frame-old state is a behavior change |
| sample/stream_ms_position,sample_position | Audio.cpp4222–4451 and Sound2d.cpp883 use real playhead/duration,including byte position conversion | Cannot silently replace with client-clock estimate;decoder delay,pauses,seeks and rate changes matter |
| file callback open/read/seek/close | Audio.cpp3937–4100 executes TreeFile on first audio-thread use and real AbstractFile methods | Helper decoder may synchronously request data while client waits for a Miles command;blocking single IPC loop risks deadlock |
| AIL_lock/unlock | Audio.cpp2318–2335 encloses starting all queued sounds | A protocol transaction may preserve order/exclusion,but lock ownership and callbacks must not deadlock across process waits |
| EOS callbacks | Audio.cpp4728–4790 → Sound2d::endOfSample845ff | Callback increments loop,makes user callback,resets fade/current-time,defers sample release to next alter;late delivery can alter game policy |
| Shutdown | Audio.cpp1377–1440 stops sounds,clears maps,thenAIL_shutdown | Drain/cancel stale completions before objects disappear;no helper callbacks into destroyed tokens |

The Sound2d source explicitly warns that certain Miles functions cannot be
called inside endOfSample,and release occurs on the next alter. This is a real
callback-reentrancy contract. Replaying every completion indiscriminately on a
new thread would not preserve it. The exact original callback thread/call order
must be measured; source alone cannot establish it.

## High-frequency updates and clocks

- Game.cpp1200 calls Audio::alter per frame. PlayerMusicManager also calls it with
  delta0 outside the ordinary frame path;Audio::stopAllSounds invokes alter0 too.
  Therefore one batch per rendered frame is not an equivalent scheduling boundary.
- Audio::alter1939ff updates listener position/orientation each invocation.
  Sound3d::alter122 updates each source position before Sound2d::alter.
- Audio::serve4941ff checks main-thread/driver/sounds and callsAIL_serve after an
  accumulated interval over50ms. This is an explicit maintenance point,not evidence
  the mixer only runs every50ms;Miles has its own timers/audio callbacks.
- Premix fragment changes at5116/5123 forceAIL_serve immediately. A helper cannot
  defer those arbitrarily without testing loading-screen underruns.
- Native Miles execution occurs after IPC dispatch,new process scheduling and
  queueing. Command timestamps record when the client wanted a change;they cannot
  make a command arrive before it did. The used AIL_start_sample/start_stream calls
  have no client-supplied scheduled-start timestamp argument.
- A shared high-resolution monotonic clock plus sequence/generation IDs can
  measure/order intent,delivery,andcompletion. It does not erase extra latency or
  guarantee which audio quantum observes a moving source or newly started voice.
- Pre-buffering can reduce deadline misses but may increase onset latency and
  change response to pauses/seeks. Increasing lookahead is not fidelity-neutral.

## A bounded batching candidate,not a guarantee

Keep high-level SWG Sound/template/prioritization logic in the client. Maintain
explicit local proxy IDs;helper retains real32-bit handles and decoder buffers.
Serialize commands in observed order;group only commands between semantic barriers
(no pending getter,completion processing,immediate serve,or externally observable
state transition). The existing start-queue lock scope is one candidate batch,
subject to measuring callback interactions. Apply its commands in order under the
same original Miles lock in the helper,then return acceptance/results.

Position updates may be coalesced only if evidence proves intermediate positions
were never mixer-observable. Until then preserve each update;last-value-wins
coalescing is a potential audible/spatial change. Do not batch across EOS-delivery
or playhead-query boundaries by assumption.

For I/O,compare two actual prototypes rather than defaulting to callback RPC:
1. Helper reads identical archives/config directly using a real32-bit TreeFile
   module,with explicit parity for client search/cache/patch order.
2. Client owns TreeFile and serves shared-memory byte blocks via a dedicated I/O
   worker,with bounded prefetch/backpressure and reentrant command/event channels.
The first duplicates file-state coordination;the second introduces I/O latency.
Neither is automatically equivalent. Copying raw AbstractFile pointers is invalid.

## Discriminating evidence required before claiming fidelity

1. Instrument original Win32: monotonic time,thread ID,voice ID/generation,command
   ordering,callback entry/exit,playhead/status results,file I/O and output device
   buffer/underrun counters. Include representative real gameplay and stress.
2. Replay a captured deterministic command/asset sequence with original DLLs
   in-process and helper. Compare emitted PCM where capture is available without
   changing DSP,plus loop boundaries,voice completion order and reported positions.
3. Run live-input onset measurement: gameplay event→command→Miles execution→audio
   output. Compare distributions and worst-case delay under CPU/disk pressure,
   source movement,many simultaneous voices,player music and UI bursts.
4. Detect exactly the coupling above: paused/seeking streams,EOS creating another
   sound,stop during callback,scene transition,loading premix,driver loss and crash.
5. Repeat stock baseline runs to characterize existing scheduler/device variation.
   Do not label that variation permission for new audible regressions;record any
   added queueing/changed event ordering separately and return it to the user.
6. Preserve original assets,decoders,room presets and rendering settings. Any
   substitute codec/reverb/spatial engine is a new explicit fidelity decision.

Highest justified claim now: the helper architecture can retain original vendor
DSP/codec implementation and existingSWG policy in principle. Whole-experience
100%fidelity,including timing,has not been demonstrated. A replacement built on
JUCE would need much broader acoustic equivalence evidence; feature-list coverage
alone cannot meet this requirement. No promise of exact fidelity is made by this
source audit. Next test is an instrumented original Win32 baseline,not a rewrite.
