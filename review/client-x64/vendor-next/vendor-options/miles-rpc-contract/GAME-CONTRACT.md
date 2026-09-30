# Game-facing Miles bridge contract: source audit

2026-09-30. Read-only source audit at client integration HEAD
`a21af16302efa17cf1d889cd4b246fcc493c8248`. Paths below are relative to
`src/engine/client/library/` unless otherwise stated. No production bridge is
selected or implemented. This supplements, and narrows, the existing RPC result.

## Decisive gap in the existing experiment

The direct and controlled arms both queued EOS until their next dispatcher
boundary. Their equal getter results establish that finite dispatcher experiment,
not preservation of SWG's immediate callback policy. In the stream runs even the
direct arm waited about 20 ms to dispatch EOS. That delay is not a stock-game
baseline or an accepted latency allowance.

## Actual completion call chain and observers

`clientAudio/src/win32/Audio.cpp:4729,4750,4771`: each real sample/3D/stream EOS
callback finds its sample-map entry by vendor handle, sets `m_status=PS_done`,
and immediately calls `Sound2::endOfSample()`. There is no application lock in
these functions. Source alone does not establish thread ownership; the existing
original-runtime probes observed callback execution on both caller and worker
threads. A new main-thread event pump would be a scheduling change, not a
transparent replacement.

`Sound2d.cpp:845–874` performs these side effects in this exact order:

1. Set `m_endOfSample=true`.
2. Increment `m_currentLoop`.
3. Invoke the installed game callback, if any.
4. Set `m_fadeOutTimer=0`.
5. Set `m_currentSoundTime=0`.

The source explicitly defers sample release because some Miles functions cannot
be called in this callback context. The callback is therefore not permission to
reenter arbitrary Miles operations.

The observed non-null callback registrations in this checkout are
`clientGame/src/shared/scene/PlayerMusicManager.cpp:177,231`:
`sampleFinished()` at 103 immediately sets `s_sampleFinished=true` and starts a
`PerformanceTimer`. At 590 the music update consumes that flag, clears callback
registrations at 603, and advances band/performance policy. The timer is also
observed by the 5/20-second fallback checks at 697–702. Deferring the callback
changes both the first eligible music update and the timer origin.

`Sound2d::alter`, line 349 onward, checks `m_endOfSample` before normal updates.
`reset()` at 807 releases an auto-delete sample, clears state and prepares the
next sample when still looping. Late EOS can therefore change release/start and
loop/fade policy on the next alter. `Sound2d::startSample` also calls
`endOfSample()` locally on queue failure (936): the bridge must distinguish that
local engine transition from a vendor completion and avoid duplicate delivery.

**Correction to the older broad audit:** `Audio::getSamplePlayBackStatus`
(2691 onward) combines vendor status with callback-maintained map status, but a
source-wide search found only its definition/declaration, no call site. It is
not the strongest evidence of active game coupling. The EOS observers above and
the playhead consumers below are live call chains.

## Synchronous observations are part of the policy

`Sound2d.cpp:589` uses real sample time to detect an infinite-loop wrap
(current time less than previous time), increments the loop and updates fades.
`getVolume()` at 650 uses current/total time for fades. `getSampleTime()` at 877
calls Audio's real getter and clamps current to total. `Sound2d::getCurrentTime`
at 1235 also calls `Audio::getSampleCurrentTime`, not the separate cached
`m_currentSoundTime` accessor at 901.

`Audio.cpp:4146,4166` -> `Sound2d::getCurrentTime` ->
`Audio::getSampleCurrentTime:4291` reaches actual `AIL_sample_ms_position`,
`AIL_stream_ms_position`, or 3D byte position plus cached duration/file size.
Thus PlayerMusicManager_Musician's `Audio::getCurrentSoundTime` is a vendor-backed
playhead query despite its name. `isSampleAtEnd:4209` independently reads stream
position. Total-time queries likewise use real vendor results except the cached
3D duration. A client-clock estimate or previous-frame snapshot changes these
contracts.

Minimal request/reply rule: a getter must execute after preceding accepted
commands for that voice and return the actual vendor observation. Preserve the
causal order of any callback delivered synchronously during that command.
For asynchronous worker callbacks there is no demonstrated total order with
concurrent commands: record the vendor callback entry and establish an explicit
transport linearization, without claiming that this reproduces all baseline
races. Do not forcibly reorder callbacks to precede commands merely because they
share a request number.

## Command epochs and permitted batching candidate

`Audio.cpp:2318–2340` encloses starting queued sounds in `AIL_lock`, ordered
`startSample` calls, then `AIL_unlock`. This existing lock scope is a candidate
ordered batch; it is not evidence that all of `Audio::alter` is atomic.
Keep each operation and its error result. Never hold a client lock while waiting
for a reverse callback that needs that same lock/thread.

`Audio::alter:1935` updates listener state each invocation; `SoundObject3d.cpp:32`
sets position, zero velocity and orientation in order. `Sound3d::alter:122` sets
source position before `Sound2d::alter`. The latter updates volume then playback
rate before smoothing obstruction/occlusion. Preserve these intermediate calls
until measurement establishes that coalescing is unobservable to the mixer.

PlayerMusicManager explicitly invokes `Audio::alter(0)` around band starts
(lines 162,181,216,236); stop-all also uses alter(0). A rendered-frame boundary
is not an adequate transaction boundary, and a zero delta is not a no-op.

`Audio::serve:4943` is gated on main thread, live driver, playing sounds and a
timer. It calls `AIL_serve` after accumulated time exceeds 0.05 seconds.
`setLargePreMixBuffer`/normal at 5116/5123 change fragment preference and serve
immediately. Do not convert these into an unrelated helper timer cadence.
`AbstractFile::readEntireFileAndClose:52` invokes the registered audio-serve
callback before seeking/reading. That creates an additional real maintenance
entry point; ordinary `AbstractFile::read` is not shown to invoke it universally.

Commands may be packed for transport without being collapsed. Do not delay an
EOS event until a getter, `serve`, or the next command arrives. Flush/getter
barriers alone cannot preserve a callback that the game observes while the
command channel is idle. Conversely an arbitrary callback receiver thread is
not established equivalent to the original callback context.

## TreeFile and ownership/reentrancy

`Audio.cpp:3937–4100` implements the registered file callbacks using real
`TreeFile::open(...PriorityAudioVideo,true)`, an owned `AbstractFile*` map,
seek/tell/read and close/delete. The vendor's output buffer is filled directly
in its owning process. The callback's `once` flag initializes PerThreadData on
the first foreign-thread call; it is global, not proof of initialization for
all possible service threads.

Opaque generation handles can represent these resources across a boundary;
raw AbstractFile pointers, Miles sample pointers, file buffers and cached sample
buffers cannot. Sample memory must remain alive until the corresponding real
vendor release, not merely until the command has been sent.

A synchronous vendor open/decode command can request file bytes while the client
waits for its reply. A single blocking request loop which requires that same
client thread to service TreeFile is a deadlock design. A pumpable reverse-I/O
path or separately owned file service is required and must preserve TreeFile
search/patch/cache semantics. A helper opening a filename relative to its own
working directory is not an equivalent substitute. Worker-thread TreeFile
access and initialization must be established; source does not license adding
arbitrary concurrent reads to this unsynchronized callback map.

Lifecycle also needs a real quiescence barrier: cancel/drain vendor callbacks
and I/O before destroying local Sound/sample/file mappings. Generation checks
reject stale transport events, but cannot substitute for the original vendor
release/driver shutdown completion. Do not silently apply an old completion to
a reused game sample ID.

## Bink driver seam

`src/game/client/application/SwgClient/src/win32/ClientMain.cpp:314` passes
`Audio::getMilesDigitalDriver()` to `VideoList::install`, which reaches
`clientGraphics/src/Bink/BinkVideo.cpp:115–117` and `BinkSoundUseMiles(driver)`.
This is a genuine in-process driver pointer, not an abstract service token.
The unchanged original 32-bit Bink audio path must therefore share the original
Miles driver process, unless an independently validated alternative is chosen.
Co-hosting preserves that pointer seam but does not solve video surface/frame
transport, presentation timing or device lifecycle. Silent Bink or a substituted
mixer is not justified by this audit.

## One bounded next discriminator (prospective, not run)

**Highest-risk question:** does delivering EOS only at a request boundary delay
the first application observer epoch relative to immediate original callbacks?

Use the existing short owned sample and stream, original DLL, private clocked
sink, native x86 host and x64 controller. Three explicitly named arms:

- Original in-process callback immediately records completion into a small
  interlocked diagnostic observer state; no Miles call from inside callback.
- Existing queued dispatcher control (preserved, not called stock).
- Independent unsolicited event channel to the controller; receiver records
  completion as soon as it arrives, without waiting for command dispatch.

Run an explicit 1 ms observer schedule in each arm with the command channel
idle across expected EOS; keep necessary service calls on a separately recorded,
identical cadence. Record callback entry/exit, thread, event-send/receive,
observer timestamps/sequence numbers and first observer seeing completion. Also
record command completion and status/position at the next natural query. Repeat
with a documented phase offset between observer epochs and expected completion;
report every run, not only matching epochs.

The observer is **a diagnostic model**, not actual Sound2d/PlayerMusicManager.
It isolates the event-delivery architecture without inventing a production API
or calling unsupported vendor functions from callbacks. It must not be cited as
a full engine integration or audio-output fidelity test. The direct arm must
mutate the observer at callback entry rather than reuse the queued helper.

Expected discriminator: queued control can miss observer epochs while the
channel is idle; unsolicited delivery removes request-cadence dependence but
still adds transport/scheduler delay. Record added delay and changed first-epoch
counts; no accepted tolerance or 100% fidelity claim. Even matching finite runs
would leave actual engine callback-thread affinity, races with alter/release,
player-music synchronization, TreeFile reverse I/O and Bink co-hosting unproven.
A failure is evidence to redesign the boundary, not permission to weaken the
user's experience requirement.
