# Temporary Miles compatibility backend

Decision, 2026-09-30: the user explicitly designates the out-of-process original
Miles implementation as temporary, until Miles can be upgraded or replaced.
The interface should resemble the native Miles x64 in-place upgrade we would
otherwise make. This changes the implementation direction, not the fidelity
requirement. Product `49d0eeed4` still has no bridge adopted.

## Source boundary

Keep SWG's Audio/Sound2d/Sound3d policy in place: sound selection, RNG use,
priorities, fades, spatial updates, music and callback effects. Introduce a thin
Miles-shaped source facade at the existing vendor calls, not another audio
engine or a generic remotely callable DLL. Preserve the operations, their order,
return meanings and completion semantics. Do not batch setters, cache getters,
substitute silence, or move work to the next frame as an interface convenience.

```text
SWG audio policy
       |
       v
Miles-shaped source interface (no pipe types)
       |
       +-- temporary: original Miles x86 backend
       |                private codec / pipes / helper process / original DLL
       |
       +-- future: native Miles x64 backend
                        direct calls to an available, licensed SDK
```

Only one implementation is selected at build/composition time, before Audio
installation, and remains selected through complete teardown. No runtime plugin
loader, hot swapping or automatic fallback is needed. A replacement mixer is a
separate future implementation with its own behavioral acceptance, not presumed
equivalent because it implements the same functions.

Representative facade operations follow the existing vendor boundaries:
`startup`, `open_digital_driver`, `allocate_sample_handle`,
`set_sample_volume_levels`, `start_sample`, `sample_status`,
`release_sample_handle`, and `shutdown`. These are interface intent, not a claim
that the playback facade has been implemented. A native implementation calls its
SDK at those points; the temporary implementation marshals privately at those
same points. The current SDK has 61 linked functions plus the version macro in
the inventory; only the reachable game surface needs support.

## Differences that cannot safely be hidden

- **Opaque handles.** Game code can hold typed driver, sample and stream handles,
  but must not cast them to vendor pointers or wire identities. Native pointers
  and bridge session/slot/generation records are private implementation details.
  A stream's sample alias remains borrowed from its stream, never independently
  released. Check SDK-facing types against the existing header's Win64 branch;
  do not infer a newer SDK's layout from it.
- **Owned results.** Version and error/directory text are copied with explicit
  null-versus-empty semantics. A facade must not expose a pointer into a pipe
  reply or make the game manage protocol buffers. Any legacy pointer-return
  compatibility wrapper belongs inside the adapter and needs a defined lifetime.
- **Input extent and retention.** Some old APIs accept a pointer without its
  full byte extent. Where transport needs it, pass an extent already known by
  the real caller through a narrow, documented adaptation. A native backend can
  use that same input without serializing it. Do not guess size from a pointer,
  read past a buffer or assume Miles copied it. Retention ends at a proven vendor
  lifetime boundary.
- **Callbacks and files.** The source contract describes callback registration,
  execution/reentry and retirement. Pipe lanes, causal IDs and acknowledgments
  belong solely to the temporary backend. Existing TreeFile behavior stays in
  the game; no second filesystem is introduced. These runtime contracts are
  still unresolved for the full bridge.
- **Video/audio binding.** Original Bink's use of a real Miles driver must bind
  inside the selected media implementation. A wire token is not an HDIGDRIVER.
  The exposed getter/Bink surface needs explicit integration review; current
  end-to-end call reachability has not been established merely by finding the
  declarations.
- **Failure.** Preserve actual vendor results, including negative and null
  results. Backend/transport failure is separate and must never masquerade as
  successful playback, EOF or completed callbacks.

The new facade is a source boundary we control, not a counterfeit `Mss64.dll`,
vendor ABI emulation, or a guarantee that a future SDK is source compatible.
The existing 7.2a `Mss.h` already declares the Win64 interface: platform detection
at lines 205–214 and pointer-sized UINTa/SINTa at 1253–1260. Its SHA256 is
`966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e`.
We can compile a direct adapter and signature/width checks against that actual
header under the native x64 compiler now. The matching native x64 import library,
runtime and codecs remain unavailable; compile-only checks cannot establish
linking, runtime behavior, licensing or a newer release's compatibility.

The user subsequently confirmed the native x64 Miles shape should be built first
and the pipe connections made to fit it. Thus the SDK-facing contract drives
the adapter, not the existing wire schema. `intptr_t` preferences stay
pointer-sized locally; the temporary x86 implementation must explicitly reject
unsupported values before narrowing. Merely retaining 32-bit wire fields must
not silently redefine the native API.

Public context checked 2026-09-30: RAD's [Miles page](https://www.radgametools.com/miles.htm)
offers an evaluation SDK and describes Miles 10 as having a new API. Its
[development history](https://www.radgametools.com/msshist.htm) records Win64
support. Neither source proves binary compatibility with SWG's 7.2a runtime.
The local pinned header supplies the concrete legacy declarations. No third-party
DLL download, evaluation request, licence bypass or vendor-header republication
is needed for this source-boundary work.

## Deletion criterion

Keep the following only in the temporary backend target: helper launch/security,
pipe I/O, framing, protocol resource IDs, reverse-RPC plumbing, upload chunks,
watchdogs, and transport diagnostics. Audio policy and the public facade may not
include those headers or link those objects. Build definitions select the
implementation once; the native target must not transitively depend on the
temporary target.

A replacement is structurally ready when the temporary backend, helper and
protocol sources can be removed from a clean build, leaving the game policy and
facade call sites unchanged. A test double can check that dependency boundary
only; it is never shipped or counted as real audio. A real native replacement
must additionally pass the same intended-use media, callback, lifetime, timing,
ground/space and mixed-width acceptance before the bridge is retired. Keep the
old implementation for comparison until that acceptance passes; then delete its
target and deployment artifacts, retaining historical evidence separately.

## Current delivery boundary

`startup-bridge23` is the frozen 23-request startup/metadata proof. Its controller
still uses wire operations, so it is not proof of the new replaceable source
interface. The next `backend-boundary24` experiment isolates a narrow Miles-shaped
startup slice and tests dependency removal. It does not qualify playback,
callbacks, TreeFile or Bink. The pipe cancellation repair remains a separately
tested component until it is composed and rechecked.

Full original game fidelity remains required. This temporary designation neither
asserts universal fidelity nor authorizes diminished behavior. The explicit
upgrade-shaped direction comes from the user; earlier architecture research and
20-path comparison remain in ARCHITECTURE.md. We are continuing execution within
that design space, not restarting or claiming another research cycle.
