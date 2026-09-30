# Experimental original-Miles integration seam

2026-09-30. Read-only audit at client HEAD `49d0eeed4ddaa177d7a93ea396c37c3d9b9942da`.
No production backend is selected. Main checkout is untouched. This plan builds
on GAME-CONTRACT.md and the completed EOS discriminator, not a new options survey.
`partition.py` produces API-PARTITION.md/api-partition.json from the existing
reviewed inventory and current source locations/hashes. It covers 62 names:
61 function names plus a header macro. Actual product links previously reported
60 Release/61 Debug imports; conditional reachability and imports, not lexical
counts, are authoritative for any particular configuration.

## Exact representations and lifetimes

Use a separate private protocol, not serialized Mss.h structs. Explicit version,
message kind, bounded payload length, sequence/request ID, resource type, slot
and generation; no raw process pointers, bool, size_t or native struct dumps.
U32/S32 are unsigned/signed 32-bit. F32 arguments/results retain their IEEE float
bits, with no decimal conversion, promotion/reassociation or NaN canonicalizing.
SINTa is 64-bit at the client header and 32-bit at the original host: only actual
used preference IDs and range-valid scalar arguments can cross by checked signed
conversion. Do not generically transport SINTa as a pointer or silently truncate.

| Object/data | Client representation | Original host ownership and release |
|---|---|---|
| HDIGDRIVER | typed local proxy with slot/generation | real driver from open; stays valid through samples/streams/Bink and shutdown |
| allocated HSAMPLE | typed proxy, never cast token into dereferenceable SDK struct | own actual handle; release only after real release completes and callback quiescence is resolved |
| HSTREAM | typed proxy with generation | real stream and decoder; close destroys it and invalidates borrowed sample alias |
| stream_sample_handle result | stable borrowed sample proxy tied to stream generation | actual returned handle; no independent release; same alias for repeated queries while valid |
| sample byte buffer | client cache remains unchanged; transfer bounded length/bytes | copy owned until vendor no longer references it, not until RPC send completes; reassignment/end/release policy needs actual API lifecycle proof |
| filename/extension/redist path | bounded byte string preserving original encoding/NUL semantics | host-owned copy with documented operation lifetime; TreeFile filename retains virtual path semantics |
| last_error/set_redist_directory return | client-owned copied string storage | snapshot original return while valid; never expose host address; lifetime/thread policy must match observed callers |
| speaker_configuration | explicit channel spec and other requested scalar outputs | returned MSSVECTOR3D array remains host-owned; current caller ignores return pointer and requests only channel spec; do not invent valid client pointer if future caller uses it |
| AILSOUNDINFO | marshal scalar fields plus checked offsets into uploaded image | data_ptr/initial_ptr point into file image; translate only if proven in bounds, never copy host pointers; current Audio consumer only uses scalars |
| EOS callback | registered client function pointer held only locally | real host callback maps vendor handle to stable generation; async event carries identity, not callback address |
| file callback handle | client TreeFile-owned handle map + separate protocol identity | vendor gets host-side handle; reverse open/read/seek/close resolves to client resource; no AbstractFile pointer crosses |

The ordinary getter category includes real out-parameters (position, volume,
reverb). Preserve all outputs and the vendor return/error semantics; category
names are not permission to treat startup or setters as void. `set_preference`
also returns the previous SINTa value. `stream_sample_handle` is used for stream
volume/rate/reverb, so stream support requires real sample-alias behavior.

`AIL_set_sample_file` and `AIL_WAV_info` have no input byte count in their SDK
signatures. A shim cannot recover a safe cross-process image size from an
arbitrary pointer. The actual Audio call sites already know the cache/file size:
carry that explicit size through an experimental adapter at those exact sites,
or use a validated registered-buffer span. Do not infer full payload size from
an unbounded header read. The size-aware `set_named_sample_file` is simpler and
is why the first runtime slice should use a cached 2D sample.

The `AIL_MSS_version` Windows macro is another hidden seam: it calls
LoadLibrary(MSSDLLNAME)/LoadString/FreeLibrary locally. The header selects
MSS32.DLL for Win32 and MSS64.DLL for x64; no genuine MSS64 provider is available
here. There is no function export to forward, and forwarding AIL calls under
another DLL name does not satisfy that local version-resource lookup. An explicit diagnostic version-query adapter must ask the original host;
leaving an empty version string is not a faithful implementation.

## Full reachable surface, without placeholder success

API-PARTITION.md lists every reviewed name and current call sites:
29 scalar/control commands, 15 scalar/out-parameter getters, 4 memory APIs,
3 callback registrations, 6 resource creation/release/alias APIs,
4 pointer-return/preference APIs and 1 macro.

The forwarding layer must provide genuine behavior for every linked/reachable
entry. No empty exports, fake handles, fixed getter returns or silently ignored
setters. An unimplemented path remains a linker failure, not a runnable client.
Protocol rejection may report a real transport error, but is not an acceptable
implementation of an ordinary requested vendor operation. Do not ship a shim
that happens to satisfy the linker while aborting on all untested APIs.

Provider selection here is the existing numeric MSS_MC_SPEC plus real plugin
redist directory, original files and device choice; there are no live first-party
RIB provider-handle calls in the reviewed inventory. That does not prove plugins
are unused internally. Record loaded original DLL/ASI/FLT identities in the host.

## Smallest honest vertical experiment

**Target:** one real cached 2D one-shot `.snd`/WAV sound through real
SetupClientAudio, Audio::playSound, Sound2d::alter/startSample, real Audio EOS
callback, Sound2d::endOfSample, the next alter/reset and sample release.
Use original short private WAV and a real valid Sound2dTemplate loaded by the
actual Iff/template code, with fixed loop count one, zero start/loop delay and
fixed volume/pitch. Do not construct a fake Sound2d or duplicate its EOS logic.

1. First make the **Win32 in-process baseline fixture** link against genuine
   current clientAudio and dependency libraries, original Miles import library,
   real SetupSharedThread/Debug/Foundation/File/Math and template/config setup.
   Use original setup order and actual ExitChain teardown. Add only diagnostic
   trace hooks around real callback/alter boundaries, with separate hashes.
   Preserve real TreeFile loading/cache and real production allocator. No renderer
   startup is required merely to play this stereo sound, but unresolved drawing/
   virtual-function dependencies must be satisfied by real libraries, never stubs.
2. Drive actual Audio::playSound, register a fixture observer through the real
   API, and call actual Audio::alter/serve on a declared schedule. Record real
   Sound2d EOS ordering, loop count, callback thread/timer, getters and release.
   A diagnostic-only test accessor may read private state, but must not construct
   impossible state or replace any lifecycle method.
3. Build the same fixture for x64 with a separate experimental transport adapter
   and x86 original-vendor host. Client high-level policy remains the real source.
   Use unsolicited EOS, ordered synchronous results and explicit owned image
   transfer. Retain all failures and compare to the in-process fixture. Do not
   batch/coalesce setters initially. No actual game startup until this passes its
   bounded lifecycle checks.

**Why this is larger than the previous 20-call diagnostic:** real Sound2d is a
polymorphic class. Its vtable/method graph retains alter/reset/start/release paths
and their actual Audio dependencies. The earlier file-callback-only Audio probe
succeeded by discarding unused playback code; that is not evidence a real
Sound2d playback fixture can link with a tiny partial import library. Use the
actual linker map to determine retained imports. Runtime use can be a bounded
cached-PCM path, while the linked adapter surface may still need all 60/61
functions. Preserve this distinction rather than claiming a one-shot test covers
all codecs, 3D, streaming, music, driver failure or video.

## Required staging before writing a callable x64 shim

A. Build/trace the real Win32 fixture above. This is the first safe code slice:
a test executable using actual library code, **no backend changes**. Verify setup
closure and exact template/asset; record linker map. The source audit alone does
not establish that all linked libraries can initialize headlessly.

B. Implement fixed-width protocol/resource registry and original-host scalar,
handle and byte-upload calls in isolation; use compile-time ABI assertions and
actual-header function type checks. Add genuine results, never placeholder APIs.
The prior native RPC host is reusable transport evidence, not reusable engine
callback semantics. Gate integration on the complete linked surface map from A.

C. Implement reverse TreeFile requests and EOS lifecycle barriers before stream
or complete Audio startup coverage. Audio::install registers callbacks globally;
plugin/file loads can occur earlier than the first explicit stream call. The
client waiting for a vendor reply must be able to service reverse I/O without
calling disallowed vendor APIs from callbacks. Do not just move TreeFile onto an
arbitrary receiver thread: its initialization, cache access and ownership need
an explicit thread model. Publish sample maps before accepting completion;
stop/end/release may themselves produce callbacks, so no simplistic “ignore
until start reply” or “drop every event after stop command” rule.

D. Bink co-hosting is a separate real path. ClientMain gives VideoList the Miles
driver; BinkSoundUseMiles expects the real in-process pointer. Returning a proxy
from getMilesDigitalDriver and feeding it unchanged into original Bink is invalid.
Keep original Bink audio in the same vendor host or leave this integration path
unavailable pending a real design. Do not mute video or claim co-hosting alone
solves its frame transport/device/presentation lifecycle.

## Gates and remaining uncertainty

The first runnable experiment needs actual-source traces proving callback
registration, start, EOS, next-alter release, no duplicate completion, correct
playhead/loop behavior and real cleanup. Tests of the proxy registry alone are
not the vertical slice. Record actual imports and all operation outcomes; no
single completed sample establishes 60-call behavioral coverage.

IPC necessarily adds transit/scheduling time. Timestamps cannot retroactively
apply a setter before it arrived, and the used start calls have no scheduled
client timestamp argument. The recent unsolicited observer result removes
request-cadence dependence only; it does not preserve original thread identity
or arbitrary engine races. The user's 100% experience requirement remains an
acceptance requirement, not a conclusion this architecture can promise.

Actual acceptance must decide from original-vs-candidate game traces/output:
player-music synchronization, EOS/loop/fade epochs, moving 3D sources, rapid
start/stop/seek, CPU/disk pressure, loading-screen premix, driver lifecycle,
stream/plugin decoding, Bink audio/video sync and representative gameplay.
No latency/audio tolerance is introduced here. Preserve differences and return
them for assessment; do not optimize toward a predetermined “equivalent” label.

## Current delivery and implementation boundary

No production/source shim was written from this audit. The first code delivered
is the reproducible source partition, not a claimed playback implementation.
Creating a partial adapter before establishing the real fixture link closure
would invite precisely the placeholder exports and copied-observer shortcuts
this task rules out. A throwaway **baseline fixture** is the immediate safe
implementation target; main branch, Q/R mappings, vendors and assets remain
unchanged. No push, adoption, codec replacement or PR.
