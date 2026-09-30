# Addendum 24: match a Miles64 in-place source upgrade

The user's clarification supersedes the earlier suggestion of a general rendering backend: **make a thin Miles-shaped source facade**, preserving the operations and their ordering. Keep game audio policy untouched. The temporary implementation forwards through the original 32-bit host; a future implementation forwards locally to an actual validated x64 Miles SDK. Do not introduce higher-level playback, stream-gain or initialization orchestration merely to make the API vendor-neutral.

This targets the existing Miles 7.2a header's actual Win64 source declarations, with the pipe hidden behind the implementation. The local `src/external/3rd/library/miles/include/Mss.h` defines the Win64 path at lines 205–214, selects `MSS64.DLL` at 507–508, and defines 64-bit `UINTa`/`SINTa` at 1253–1260. Thus real x64 header signatures are available and can be checked now. What is missing is the native x64 import library/runtime and evidence of linked runtime behavior, not x64 declarations. This is not a claim that the pipe reproduces the native binary ABI or that a newer Miles release has identical declarations. Do not distribute a substitute `Mss.h` or copy vendor declarations wholesale.

## Proposed shape

Use a private header such as `ClientMiles.h`, ordinary local functions, a small set of local opaque identity types, and one link-time-selected implementation. A vtable/plugin system is unnecessary. Representative design notation below is not an implemented header; `Driver`, `Sample`, `Stream`, `NullableText`, `WaveScalars` and `AdapterFault` require concrete local definitions.

```cpp
namespace ClientMiles {
    int32_t AIL_startup();
    void AIL_shutdown();
    Driver AIL_open_digital_driver(uint32_t rate, int32_t bits,
                                  int32_t channels, uint32_t flags);
    Sample AIL_allocate_sample_handle(Driver);
    Stream AIL_open_stream(Driver, char const *name, int32_t memory);
    Sample AIL_stream_sample_handle(Stream); // borrowed identity, no release
    void AIL_set_sample_volume_levels(Sample, float left, float right);
    void AIL_sample_ms_position(Sample, int32_t *total, int32_t *current);
    void AIL_start_sample(Sample);
    void AIL_stop_sample(Sample);
    void AIL_end_sample(Sample);
    void AIL_release_sample_handle(Sample);
    void AIL_close_stream(Stream);
    void AIL_lock();
    void AIL_unlock();
    void AIL_serve();

    // Explicit source deviations where this client needs safe local adaptation.
    NullableText lastErrorCopy();
    NullableText setRedistDirectoryCopy(char const *directory);
    NullableText versionCopy();
    int32_t setSampleFileSized(Sample, void const *image,
                              uint32_t imageBytes, int32_t block);
    int32_t wavInfoSized(void const *image, uint32_t imageBytes,
                         WaveScalars *out);
    int32_t speakerConfigurationChannels(Driver);
}
```

`AIL_set_named_sample_file` and `AIL_file_type` already have byte counts: retain their existing operation shape, do not add upload parameters. Callback registration retains return-of-previous-callback identity, and ordinary scalar getters retain signedness and output-pointer presence. Preserve `AIL_stream_sample_handle` rather than replace existing sequences with invented stream methods. `AIL_lock`, `AIL_unlock` and `AIL_serve` remain source operations; lanes, leases and reverse-response routing remain bridge internals.

For each operation, the bridge implementation performs local-handle translation and serialization; the native implementation unwraps its local resource and calls the corresponding real SDK operation. Neither `Audio.cpp` nor `SoundObject3d.cpp` sees packets, opcode integers, upload handles, host process control, registration tokens or SessionClose. SDK constants used by this client need a private compatibility mapping reviewed against each SDK, not an assumption that all future values match.

## Exact deviations and limits

1. **Opaque handles are a source adaptation, not wire tokens.** Replace exposed `HDIGDRIVER`, `HSAMPLE` and `HSTREAM` in Audio, Sample classes and SoundObject3d with facade-local identities. Preserve nullability, equality, stable repeated stream aliases and ordinary copy behavior. The bridge must distinguish borrowed stream samples from owned samples internally and reject independent release of borrowed identities. Native x64 SDK pointers can remain private to its implementation. Do not cast kind/slot/generation bits to pointers. Prevent stale identities or callbacks from addressing a replacement instance.

2. **Two input extents must be added.** Existing `AIL_set_sample_file` and `AIL_WAV_info` lack lengths. Their actual game callers have lengths: cached `m_fileSize` next to `m_sampleRawData` at Audio.cpp:2925 and `fileSize` next to `fileImage` at 3710. Add sized local wrappers; native implementation passes the image to the original SDK call after validating the local extent and bridge implementation transfers the declared span. This is an unavoidable requirement for safe cross-process forwarding without parsing untrusted headers to invent buffer sizes. Byte count does not establish lifetime: sample-file images can outlive the call; retain/copy/pin with explicit reassignment/failure and release rules. Do not redefine all buffer inputs as transferred ownership.

3. **Owned text is a deliberate small source deviation.** `AIL_last_error` and `AIL_set_redist_directory` return SDK-owned pointers. Copy into a nullable owned local value so pipe reply storage and later SDK calls cannot invalidate the caller's result. Preserve absent versus empty text. This is not mathematically mandatory: a facade could maintain shadow character buffers, but their invalidation/thread semantics would need additional evidence. Owned values are simpler for the actual immediate-use Audio callers. `AIL_MSS_version` is a macro query, not one of the 61 functions; `versionCopy()` must ask the implementation's actual loaded runtime. A native implementation must not continue asking the old 32-bit host.

4. **Only consumed structured outputs need source wrappers.** The reviewed WAV caller uses scalar metadata, so `WaveScalars` need not impersonate pointer-bearing `AILSOUNDINFO`. The speaker caller at Audio.cpp:1326 requests only channel specification and ignores the returned vector pointer, so a narrowly named channel query is justified. These wrappers intentionally do not claim full SDK API coverage. If new callers need pointer-bearing WAV data or speaker vectors, add a documented local ownership/count contract before claiming support. Never return a fabricated SDK pointer.

5. **Pointer-sized preferences stay pointer-sized locally.** Current SDK signatures use `SINTa`, not universally int32. A Miles-shaped source facade can use `intptr_t` for the preference value/return after local type checks, retaining the SDK operation names. The 32-bit bridge must constrain supported preference IDs to the observed scalar cases, range-check incoming values and sign-extend results. No pointer-valued preference can cross by integer cast. The current 7.2a Win64 declaration is available for compile-time checking now; compatibility with any separately acquired newer release would require a new check. This replaces the earlier higher-level “premix intent” suggestion; retain the actual preference/serve sequence.

6. **Callbacks are local functions with SDK-shaped behavior.** Facade callback typedefs take its own Sample/Stream identities; file callbacks use a client-local pointer-sized file identity, signed seek offset and unsigned read count. Host trampolines and registration IDs are private. Return the previous local callback from EOS/stream registration. Preserve the open success indicator separately from the file handle because zero is a valid first handle. Keep `reverse-file-seam20/ClientAudioFileCallbacks.h` as a possible local service adaptation, not something to register directly as SDK ABI callbacks. Native adapter thunks must match the existing header's Win64 calling convention, which is compile-checkable now. No facade makes arbitrary I/O-thread delivery safe: Sound2d.cpp:845 explicitly defers release until alter and invokes a game callback. Context, reentry, ordering and shutdown quiescence remain unresolved validation requirements.

7. **Bridge failures need a separate failure path.** Do not change every Miles return into a generic protocol Result, and do not map disconnect to null driver, zero preference, successful void return or SDK last-error text. Choose a documented local adapter-failure mechanism compatible with the client build (a narrowly handled typed exception if supported, or an explicit fail-stop/fault route). Successful calls keep their SDK-shaped values. The choice must precede production adoption; an assertion-based experiment is not a completed recoverable contract.

8. **Bink is a necessary exception to source-only substitution.** Audio exposes `getMilesDigitalDriver`; BinkVideo.cpp:117 can consume a real driver with `BinkSoundUseMiles`. A bridge proxy is never that pointer. A native adapter may provide a private same-process SDK binding to a compatible native Bink implementation; original 32-bit Bink/Miles must be co-located. Do not place a general `void *nativeDriver()` escape in the game facade and label it portable. Preserve this as a specific Miles/Bink integration boundary until validated. Correction from the follow-up audit: the actual main application calls `VideoList::install(Audio::getMilesDigitalDriver())` at `src/game/client/application/SwgClient/src/win32/ClientMain.cpp:314`. The initial search omitted `src/game`. The chain is source-reachable; see `BINK-BINDING-REACHABILITY24.md` for build/config/loader evidence and runtime limits.

## What to do now

Implement only the already exercised startup operations through this Miles-shaped source facade in a new candidate. Keep same-operation names where semantics are preserved; use explicit names for the small safe deviations above. Keep caller-controlled startup order, driver retry, provider updates, diagnostics and shutdown sequence. Do not declare all 61 calls implemented because declarations compile, and do not manufacture a 62-entry function table now.

The replacement test is concrete: select the future native implementation and remove all bridge protocol, process, host and transport dependencies from the build/package without rewriting Audio's Miles-operation sequences or game policy. The few sized/text/metadata facade wrappers may stay as harmless native forwarding helpers. Full fidelity still requires linking the genuine x64 library/runtime and validating playback, callback/thread behavior and Bink against it. This addendum changes the interface direction, not the evidence status.

Evidence read: `protocol-candidate/sdk-declarations.cpp` (all 61 signature assertions and callback typedef checks), `protocol-candidate/API-MAP.md`, and the actual Audio/Sound/Bink source sites documented in `REPLACEABILITY-SENIOR24.md`. No vendor code was edited or run.

## Compile-only direct-x64 target

Use the original local 7.2a header under a real x64 compiler target, not merely define `_WIN64` in a 32-bit compilation. A private direct adapter can forward to `::AIL_*` and compile to an object without possessing or running the native DLL. For unchanged-signature wrappers, compare `decltype(&wrapper)` with `decltype(&::AIL_function)` using `std::is_same`; this catches return/parameter types and compiler-recognized calling convention. The existing `protocol-candidate/sdk-declarations.cpp` demonstrates the 61-operation exact-signature assertion technique. Do not include a copied header or assume the 32-bit signature checks suffice.

Where our facade deliberately substitutes opaque handle types, owned strings or sized buffers, whole-function type equality is expected to fail; isolate those adaptations and assert the actual SDK-facing thunk signature instead. Alternatively, a strictly SDK-typed private source facade can retain the header's opaque pointer types and give the pipe implementation private local proxy objects, provided no native consumer ever receives those proxies and borrowed ownership is enforced. The direct native adapter then forwards actual SDK handles. This choice trades stronger local type separation for a closer in-place source fit; it must not expose wire tokens as pointer bits. In either design, the source deviations above must be explicit, and compile success establishes declarations/object generation only—not successful linking, callback behavior or sound fidelity.
