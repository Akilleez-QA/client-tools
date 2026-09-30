# Native stream28 — prospective source and compile-only gate

Prepared before implementation/checks, 2026-09-30T14:40:36.216595+00:00. This continues the native-Miles64-shaped plain facade with exactly eight actual Audio stream operations. The public opaque OwnedStream pointer reuses the existing HDIGDRIVER; it does not introduce a lifecycle owner, virtual engine, registry, plugin loader or pipe implementation. Parent received the exact selected scope before coding. Broad option generation is explicitly waived by the parent for this continuation; existing task context supplies the objective and acceptance. No descendants are authorized or needed for these small direct delegates.

## Scope and source observations

The pinned possessed SDK is Miles7.2a, December20,2007, already declares WIN64. The private header and actual Audio.cpp identities, plus frozen facade dependencies, are recorded in input-identities.json. The SDK body is not copied into the packet. The selected calls and source locations are:

| Facade operation | Audio.cpp lines | SDK declaration lines | Source shape preserved |
|---|---|---|---|
| open_stream | 605 | 5162 | Existing driver, const filename, signed32 stream_mem, nullable owned stream |
| close_stream | 3367 | 5164 | One close for each successful open, void |
| start_stream | 3083,4417 | 5170 | Separate side-effect call, void |
| set_stream_loop_count | 3059,3067 | 5176 | Signed32 count, zero used by Audio for infinite looping |
| set_stream_loop_block | 3041 | 5178–5180 | Two signed32 native offsets, no unit conversion |
| stream_status | 2716 | 5182 | Raw signed32 status, no new narrowed enum |
| set_stream_ms_position | 4421 | 5201–5202 | Signed32 milliseconds, unchanged |
| stream_ms_position | 4224,4282,4328,4368 | 5204–5206 | Separate nullable signed32 output pointers |

The real HSTREAM is an SDK stream pointer (5080); only private direct adaptation may see it. OwnedStream denotes ownership by convention, not a C++ unique_ptr or runtime alias detector. Copies alias the same stream; the owner closes once before driver shutdown. Open preserves the real null result. No allocation is introduced after a successful real open.

The actual stream_sample_handle calls at3211–3212,3260,3305,3334 yield a borrowed sample owned by the stream. Those calls and their sample controls are deferred, along with callback/EOS registration3072, until a separate parent-bound borrowed lifetime contract is selected. This slice exposes no borrowed-sample getter, no conversion to the allocated OwnedSample identity and no release route for borrowed samples. Pause at3366 is commented and is not selected. Shared unknown-buffer extent APIs remain deferred.

## Research and meaning boundary

Research retrieved2026-09-30: [RAD development history](https://www.radgametools.com/msshist.htm) describes historical stream start/status/close issues, millisecond seeking and support for negative end-of-stream loop offsets. It challenges any claim that signatures alone establish correct playback or callback/lifetime behavior. [Microsoft /Zs](https://learn.microsoft.com/en-us/cpp/build/reference/zs-syntax-check-only?view=msvc-170) and [/c](https://learn.microsoft.com/en-us/cpp/build/reference/c-compile-without-linking?view=msvc-170) distinguish syntax checks and object creation from linking. Queries were RAD AIL_set_stream_loop_block byte offsets/stream_mem and AIL_stream_ms_position nullable outputs, followed by primary pages. No external replacement or mirrored SDK body is used.

Only the SDK's signed offset and stream_mem values are forwarded: do not reinterpret loop offsets as milliseconds/sample counts, rescale stream_mem, clamp negative sentinels or synthesize statuses. Audio's table supplies integer offsets (4686–4727); the possessed declaration itself does not state byte-origin/alignment policy, and this candidate does not infer such a policy. The explicit ms API uses milliseconds. Null pointer shapes are compiled and passed unchanged; runtime acceptance of any particular null combination remains unobserved.

## Prospective acceptance and limits

Author the eight-function header/direct source, a compile-only usage excerpt and type contract, and a prepared v120 AMD64 object-only driver. Exact SDK scalar and signature assertions must pair each public function's non-handle parameters with its actual declaration. Opaque stream/driver/allocated-sample identities must not be implicitly convertible. All bodies must invoke their corresponding real AIL function once, with no new interpretation or stub result.

The usage excerpt will show a valid owner supplied by open, normal-return close, and individual loop/start/status/millisecond calls. It is only a source example: it does not reproduce Audio's callback/volume/playback policy, does not run, and does not claim exception recovery for a future pipe backend. Caller filename and owning driver/session remain stable through close as a conservative example lifetime precondition. Filename special syntax is forwarded, not normalized. The native adapter does not manufacture an image buffer or file provider.

Portable acceptance: g++ warnings-as-errors object compilation of header/type/example sources; two objects; exactly eight unresolved ClientMiles function names from the example; source/compiler/nm identities unchanged; no link/executable/vendor call. Native prediction, pending exact parent approval: actual v120 amd64 /Zs then /c against pinned Mss.h at fresh C:/native-stream28 produces three AMD64 COFF objects; dumpbin shows exactly eight unresolved real AIL imports; source/header/tool/helper receipts stable; no library/PE/link or runtime. Preserve first failure, exit nonzero on any mismatch, and do not automatically repair/retry the frozen source.

Only new native-stream28 files and local portable object preparation are authorized. Stop for root review before any VM staging/native execution. No vendor/engine/Audio/ExitChain/runtime, callbacks/playback execution, product/frozen edits, SDK publication, binary publication or push. Highest possible current claim is a portable declaration/example boundary with authored native forwards and a pending actual-header gate. Native compilation, if later authorized, still cannot prove an available x64 library, lifetime behavior, working streaming or whole-client fidelity.
