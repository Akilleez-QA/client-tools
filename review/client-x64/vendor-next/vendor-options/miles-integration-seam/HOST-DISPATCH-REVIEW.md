> Historical review of the earlier owned-sample-only dispatcher. Current v3 adds five parent-guarded borrowed operations; see host-candidate/RESULTS.md. Original findings below are preserved with their original scope.

# Independent read-only review: 39-case host dispatcher

2026-09-30. No vendor execution, probe, production edit or candidate edit.
Reviewed host_dispatch.cpp SHA256
`7a499c2dda34557c24691dfc0f0fd05b80cf94be0dd511286fd755f916b8ba7c`
and API-MAP.md SHA256
`c8fa6763460a8633b435cbd80ec997089655cc66be72172ddfb7d2e86212c90c`
against original Mss.h and current Audio.cpp/SoundObject3d.cpp callers. The prior
61 exact-signature assertions are separate compile metadata, not this semantic
review and not runtime coverage.

## Verdict within the advertised subset

No wrong argument order, dropped vendor return, or signed-width mismatch found
in the 39 implemented cases. This is a compile-only callable component, not an
engine-ready adapter. SUPPORTED.md correctly limits sample handles to owned
samples and explicitly excludes borrowed aliases/lifecycle.

Verified details:

- S32 bit-copy preserves signed representation; U32 status/byte-position/timer
  values stay unsigned. CPU percent, latency, room type, playback rate, stream
  status and file_error are genuinely S32, not floats or unsigned guesses.
- F32 request/response bit copies avoid text conversion. Passing floats through
  actual SDK calls still has compiler/FP-environment semantics; bit-copying the
  transport is not a numerical equivalence proof.
- 3D distances are **max, min, S32 auto-wet**, matching Mss.h:5875 and Audio's
  call. Orientation is face XYZ then up XYZ. These often-swapped slots are right.
- Loop offsets/counts and millisecond seeks use S32; byte position uses U32.
  Void setters in this subset really are void. In particular room type and
  stream/sample loop-block setters do not return a hidden previous value.
- Four two-output getters map mask bit0 to first output and bit1 to second.
  Actual Audio getters supply both pointers, so mask3 is the first justified
  runtime pattern. Header types alone do not establish that mask0/1/2 is legal.
- `output_mask & ~0u` intentionally rejects any output bits for APIs without
  pointer outputs; it is not a mistaken “always false” expression.

## Concrete narrow issues

1. **Noncanonical unused spans are accepted.** At host_dispatch.cpp:57 the guard
   rejects bytes/text lengths but ignores their offsets. API-MAP says unused
   fields are zero. A call with a nonzero bytes.offset or text.offset and zero
   length reaches the vendor. This is not an out-of-bounds dereference in this
   component (it never reads these spans), but it violates the declared exact
   field contract. Either reject both offsets here or make canonical span
   checking an explicit verified decoder precondition. No frame decoder exists
   in this candidate to establish the latter today. A registry-only/schema test
   can check this without invoking the DLL.
2. **API-MAP's reverb slot names should be exact.** Opcodes23/47 say “left/right
   or dry/wet”; Mss.h:4548/4584 define dry then wet, whereas volume opcodes25/48
   are left then right. The implementation's positional ordering is correct.
   This is a documentation ambiguity that could mislead the future client shim,
   not an observed dispatch bug. Name v0 dry/v1 wet for reverb specifically.

## Explicit integration gates, not new defects in the declared subset

- All sample resolutions use OwnedSample only. Real streams call
  AIL_stream_sample_handle and then sample_volume_levels, set_sample_volume_levels,
  set_sample_reverb_levels and set_sample_playback_rate (Audio.cpp:3209–3212,
  3262,3306). Those legitimate stream paths will currently fail InvalidResource.
  SUPPORTED.md discloses this correctly. Do not broaden a kind bitmask before the
  resolver enforces the borrowed alias's parent stream/generation lifetime.
  Conversely do not describe start_stream support as support for the game's
  complete streaming path.
- Start/stop/end/serve can run callbacks. Their function signatures being correct
  does not implement callback registration, old-callback return identity,
  unsolicited delivery, replacement/retirement or engine side effects.
  A session/handle created outside this component can make a bounded dispatch
  test possible, but cannot establish the missing integration contracts.
- The dispatcher precondition delegates initialized session, vendor state,
  execution lane and lock lease to its caller. supports(opcode) is not a runtime
  admission check. Separate wrappers must not turn this predicate into a public
  claim of complete operation support.
- DispatchStatus is returned separately from Result.transport_status. After
  memset, later InvalidFields/InvalidResource returns leave the Result field
  zero; early Unsupported/InvalidFields can leave a previous Result untouched.
  This is safe only if the caller consumes DispatchStatus and constructs the
  transport failure response without treating Result alone as authoritative.
  No transport caller exists to review yet. State that invariant in its API or
  require the future adapter to set transport_status on every path.
- Getter locals start at zero. With legitimate live resources the expected
  vendor getter writes the outputs. This does not establish the vendor's
  behavior for invalid state, nor emulate arbitrary caller-initialized output
  values if the SDK elects not to write them. Do not claim those cases covered.

## Most discriminating ordinary-runtime cases next

Once initialized real registry/admission is available, use original DLL/owned
sink and a known valid short sample, without malformed vendor input:

1. Set unequal valid channel levels (e.g. left0.25/right0.75), then both-output
   volume getter; set distinct valid dry/wet levels then reverb getter. Compare
   direct original calls versus dispatch on equivalent initialized resources.
   Equality of both channels, as the current game often requests, hides a swap.
   Report any original normalization rather than assuming the stored values.
2. Set an ordinary allowed playback rate, query it, perform a within-duration
   millisecond seek and query total/current with mask3. This discriminates S32
   slot handling and command order. Playback progress adds elapsed time; compare
   stable state while stopped where the SDK permits, rather than asserting
   identical live playhead times across sequential calls.
3. For a real 3D sample use distinct max/min distances and a nontrivial valid
   listener orientation. Observe original SDK getters directly if those getters
   are not in the transport subset. Their absence is not permission for fake
   verification output. Valid inputs only; preserve the original coordinate
   convention and declare call order.
4. Only after borrowed-alias registry integration: open a real stream, obtain
   its borrowed sample, exercise the actual stream volume/reverb/rate routes,
   then close normally. Assert host-side token invalidation without passing a
   stale vendor pointer back into Miles. This is the most important next
   **integration** discriminator and remains unavailable today.
5. Callback registration/order must be tested separately using genuine engine
   callbacks or the explicitly limited prior observer, not credited to any of
   these39 successful scalar cases. The real engine fixture's unresolved teardown
   remains independent; do not rerun a fault workload to validate this component.

No accepted timing/audio tolerance and no overall fidelity conclusion follow
from this review. The two concrete narrow issues need little code/doc work;
the alias/callback/lane gates remain substantive implementation work.
