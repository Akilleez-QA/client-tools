# Native handle boundary69: selected compiler experiment

Bound to active x64 client goal; local POODO loop inside Orchestrate. Existing context waives another intent question: user wants an in-place native Miles-shaped interface, with temporary removable pipe backend and preserved fidelity. Scope is authored/compiler-checked prototype only, not operational adoption. Freeze51/60/67/64 unchanged.

## Observed problem and map

Current51 uses different nominal opaque handle types from actual SDK, forcing native EOS adaptation that in turn creates callback replacement/return identity and row lifetime obligations. Actual SDK declares global struct _DIG_DRIVER/_SAMPLE/_STREAM and callbacks taking those exact pointers. Relevant surfaces: native registration and previous return; pipe proxy identity/owned-borrowed lifetime; game include boundary and compiler; vendor naming/calling convention; future upgrade; unavailable native runtime. Genuine SDK shutdown/thread semantics remain unknown.

## Research gate, 2026-09-30

Queries: Microsoft opaque handles/forward declarations; WG21 callback function-pointer type compatibility; RAD EOS history. Primary sources read:

- https://learn.microsoft.com/en-us/cpp/cpp/aliases-and-typedefs-cpp?view=msvc-170 — alias is same type; prior forward declarations and matching redeclarations are supported. Does not certify this SDK.
- https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2012/n3337.pdf — dcl.typedef/expr.reinterpret.cast/global.names. Distinct callback function types cannot be equated by size. Pointer conversion/alignment limits and reserved underscore-uppercase identifiers prevent claiming a platform-independent facade. This is a language draft, not a v120 execution record.
- https://www.radgametools.com/msshist.htm — callback/stream-close changes across SDK history caution against inferring identical semantics from signatures. It does not establish our SDK timing.

Local pinned SDK declarations and real compiler remain stronger evidence of selected types than general docs. Public docs provide no missing native64 runtime or quiescence guarantee.

## Twenty materially distinct paths considered before selection

1. Use complete SDK header directly in engine TUs (strong type identity, broad vendor include coupling).
2. Forward-declare actual three SDK tags in plain boundary and assert identity privately.
3. Keep separate facade tags and native per-object typed callback mapping.
4. Handwritten native thunks for only the three actual Audio callbacks (tighter caller coupling; incomplete generic registration contract).
5. Compile-time templated callback binding (changes public registration API and existing callers).
6. Finite precompiled thunk slots keyed by registration (capacity/lifetime costs, not transparent).
7. Generated executable thunks for each callback registration (runtime code/security/portability burden).
8. SDK per-object user-data/context mechanism if genuinely available and exclusively reserved (requires evidence; currently none).
9. Capture EOS events and poll at game update (changes delivery timing and reentry semantics).
10. Host all original clientAudio in x86 helper (moves much more engine state across boundary).
11. Obtain licensed matching native x64 SDK (best runtime reference; unavailable here).
12. Obtain licensed source and port SDK internals (different ownership and much larger scope).
13. Qualify a replacement audio engine behind existing SWG policy (requires full fidelity acceptance).
14. Translate original x86 SDK in process (separate loader/ABI/runtime qualification).
15. Keep complete client Win32 with larger-address mitigation as interim (does not meet x64 goal).
16. Restrict registration to first pre-start callback only (narrows broader native API semantics).
17. Defer EOS implementation and continue other 60 direct functions (current bounded state).
18. Request official vendor compatibility shim or timing specification (external path, no message authorized).
19. Test actual header in both include orders with handle/callback equality and direct unresolved imports before architecture adoption.
20. Replace callback parameters with untyped void pointers/public C API (loses typed callback identity, still needs adaptation).

## Decision and criticism

Select2 plus19 as the next reversible prototype experiment. Actual native registration should pass user callback through and return actual previous callback with no side table, trampoline, epoch policy, or fabricated result. It delegates scheduling to the SDK rather than interpreting it. Keep1 as fallback if forward declaration attributes/class-key fail actual compiler checks. Do not adopt3 solely to work around a nominal distinction we introduced.17 remains baseline until new checks pass. Broader vendor alternatives remain tracked, not selected.

Astra65 independently checked possessed declarations and supports the conditional simplification. Composer69 saw authored header/source and three tag facts only; it prefers distinct types for hygiene but agrees actual identical types remove native callback substitution. Root accepts the explicit Windows/selected-SDK name coupling over a new stateful interposition layer. Reserved vendor names are an implementation dependency, not a claim of ISO portability. No vendor bodies or fake vendor structures are written. Agent agreement is shared-source analysis, not runtime corroboration.

## Prospective falsifiers and limits

Author new70 header + direct EOS delegates; actual handle/callback equality and both include orders must compile without casts against pinned Mss.h on v120 AMD64. Recompile affected native TUs and actual engine-header probe; no reuse of old nominal-type objects. Exact unresolved SDK imports, no library substitution/link. Failure stops gate and preserves evidence.

Pipe revision must use separate private proxy rows and lookup validated opaque tokens without dereferencing/deleting vendor-tag pointers, define no vendor bodies, preserve borrowed parent identity and existing tombstones. One backend per process and consistent rebuild required; never feed pipe tokens to real SDK. Pointer-token behavior needs platform-scoped checks. Direct native callbacks remain caller-owned and nonthrowing; no setter catch can guard later callback execution. Pipe delivery/normal shutdown/TLS/fidelity still need implementation and measurement.

Delivery: decision/proposed experiment. Outcome: not yet compiled. Root controls next bounded gate. Product remains49d0.
