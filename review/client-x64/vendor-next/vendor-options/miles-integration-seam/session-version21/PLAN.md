# SessionVersion bounded component: prospective record

Recorded before implementation/build/runtime, 2026-09-30. POODO entry: the parent assignment supplies the exact intended outcome, scope, DLL and native VM, so a redundant opening exchange is waived. “Faithful” here means the actual Windows SDK macro's 256-byte query of the original 32-bit DLL resource, followed by owned bytes and checked x64 copying. It does not mean full-client adoption or a complete bridge.

## Frame and observations

Audio.cpp:2466 uses a local 256-byte char buffer and calls AIL_MSS_version before returning a string. Private Mss.h's Windows branch queries DLL string resource 1; its Linux branch uses a compile-time string. Source inspection is evidence of intended code path, not runtime outcome. Protocol already defines SessionVersion, Result.text and fixed LE encoding; those files are frozen. No pointers may cross the boundary. Module ownership, session admission and transport delivery remain caller responsibilities.

Input identities, SHA-256:
- Audio.cpp: c729174ada8104331702422879ecbfa4986a6c4bba49bc3d763ab62a2e401406
- Private miles/include/Mss.h: 966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e
- Original Mss32.dll: 0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe
- protocol-candidate/miles_wire.h: 8efe3915744250a6aebdc51caa712790f4930c2b32877e9425dcf79c191df0b9
- transport-candidate/codec.cpp: 15ab7134eb837fa7c36323d28423ecfa33e8fec69e8a03e4411bef924aade33e
- transport-candidate/codec.h: d95094b974c053ac4b9e0da1e442c0d7ce5291b22339acc9eafb821e209e60c0
- transport-candidate/resource_registry.h: f2a4131c73d831a0e407bd67eb1803ec1f8a72ccd0cf36e6af979cae3e8a3768

Topology: resource/encoding/bounds observed in private header and public APIs; local pointers versus wire ownership observed in schema; runtime text, loaded identity and unload balance require probe; arbitrary buffer sizes, vendor startup, device/audio/playback, transport/session admission and product integration excluded. Strong rival: substituting MSS_VERSION can look correct if both strings happen to agree. Discriminator: poison MSS_VERSION at compile time in a separate control build; actual macro output must still match direct LoadStringA and real resource text.

## Research gate

Queries: Microsoft LoadStringA buffer bounds/null termination; LoadLibraryA loaded-module identity/refcounts; disconfirmation via alternate loader paths; Wine LoadStringA implementation. Retrieved 2026-09-30; inspected source content, not just snippets.
- Microsoft LoadStringA (updated 2024-11-20): https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-loadstringa — buffer count includes terminator, truncates, ANSI call does not accept zero capacity. Governs API contract, not this DLL's text.
- Microsoft LoadLibraryA (updated 2023-02-09): https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-loadlibrarya — basename can reuse a previously loaded module; normal load executes DllMain. Loader behavior means resource-only query does not imply zero vendor loader execution.
- Microsoft FreeLibrary (updated 2021): https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-freelibrary — each owned load reference requires release. Same documentation family as above.
- Wine maintainers, current resource.c (moving master, inspected 2026-09-30): https://raw.githubusercontent.com/wine-mirror/wine/master/dlls/user32/resource.c — independent implementation corroborates bounded ANSI copy and terminating zero; not native Windows evidence.
Semantic addition: “resource-only” describes explicit API workload, not absence of DllMain. Require a held original module and basename identity check before macro invocation; exact launcher hash/path before execution. Gate satisfied for this bounded decision, no assertion of cross-platform equivalence.

## Exactly 20 paths before convergence

1. Actual x86 macro adapter: preserve vendor-selected Windows implementation.
2. Compile-time string substitution: cheaper but cannot establish DLL version; reject.
3. Export lookup: protocol-like dispatch but no actual export exists; reject.
4. x64 macro invocation: selects different DLL and changes artifact; reject.
5. Direct resource query implementation: plausible alternative, use only as independent API-path oracle.
6. PE resource parser: offline version discriminator, does not execute macro.
7. Pointer serialization: violates architecture boundary; reject.
8. Owned C-string wire span: copy bounded result plus terminator, selected.
9. Unbounded text transfer: unnecessary surface and semantics; reject.
10. Exact 256-byte array transfer: risks uninitialized trailing bytes; reject.
11. General caller-length API: broader support deferred until a real call site needs it.
12. Canonical fixed-query request: reject unexpected fields, selected.
13. Poison compile-time string: discriminates a substitution defect, selected.
14. Real resource truncation mutation: changes vendor artifact; excluded.
15. Synthetic max-length text: safe pure bound control, selected.
16. Missing/truncated response controls: expose fake success and partial writes, selected.
17. Full live pipe composition: useful next stage, outside component scope.
18. Full Audio::install fixture: integration evidence but excluded by authority.
19. Defer runtime until native VM available: fallback if exact environment inaccessible.
20. Independent parent review: handoff source/evidence for separate critique.

Decision: combine 1, 5, 8, 12, 13, 15, 16, 20; native v120 x86/x64 Debug/Release portable tests plus x86 actual-resource probe and poison control. Bounded saturation covers fixed call, wire fields, decoding, ownership, output identity, resource text, build provenance. Unresolved: actual engine integration, concurrent host teardown, session routing and unavailable response policy at product layer.

## Prospective acceptance and orchestration

Prediction P1: six primary v120 builds (four portable, two x86 host) compile; pure controls pass on both architectures/configurations. P2: x86 host's 256-byte actual macro output equals direct resource-1 query of verified current DLL, is NUL-terminated within 256, and remains owned after buffer reuse and module release. P3: x64 consumer reproduces exact text from serialized result; missing, truncated, mismatched or malformed results leave output unchanged. P4: a poisoned MSS_VERSION build continues returning actual resource text and differs from poisoned constant.

Oracle v1: explicit CHECK counters in C++ and explicit Python launch conditionals (never disabled assertions), direct LoadStringA, source/header/tool/library before/after identities via frozen revision4 receipt helpers, immediate post-link PE machine/hash and immediate prelaunch executable/DLL hash. Use isolated C:/session-version21; executable artifacts stay private on native VM. Local files contain our source and text receipts only; never publish SDK macro body/vendor binaries.

Failure means failed prediction, not automatically invalid test; preserve failed build/runtime evidence in separate immutable output. Monitor each bounded subprocess (30 seconds runtime, 180 seconds compile); stop dependent work on identity mismatch or unexpected runtime behavior. Rollback removes only newly owned staging after results are copied; no product/frozen component edits. No Audio install, startup, devices, playback, vendor allocator, engine fixture, upstream push/PR or vendor publication.

Fan-out transitions considered throughout: this is already a separately assigned worker. Parent retained all concurrency slots; no descendant capacity allocated. No nested spawn; parent review is the independent-method opportunity, not assumed corroboration. Native goal remains owned by parent; this component cannot complete it.

Pre-runtime review amendment: fail closed before macro dispatch if loaded-module/path identity or resource presence checks fail. Guard test diagnostics from reading an unterminated destination after a failed copy, and do not read beyond capacity when checking a trailing sentinel. The first native build snapshot remains preserved; runtime uses a newly receipted revision if these probe guards change source.

Contradiction C1: native build-v1 P1 is **failed**, not invalid. Receipt ede41494dd16decbfbbb12e2527848aeab07a4a303f0f283759e5a98a1856d09 preserves four wire discovery failures and four host/poison build passes; no PE launched. v120 /WX diagnoses C4309 on the high-bit pure test's constant-to-signed-char conversion. The component did not cause that diagnostic, but the complete build prediction failed. New P1b: copy the high-bit object byte using memcpy; preserve /W4 /WX and all original controls, plus pre-runtime probe guards. No favorable runtime claim exists to retract.

Repair research inspected Microsoft C4309 documentation (https://learn.microsoft.com/en-us/cpp/error-messages/compiler-warnings/compiler-warning-level-2-c4309) and C++ working draft object representation/integral conversions (https://eel.is/c++draft/basic.types and https://eel.is/c++draft/conv.integral), retrieved 2026-09-30. These are independent specification/compiler-documentation families; current C++ wording is not a claim of v120 conformance. Byte copying tests the intended object representation without relying on signed conversion. The byte-copy edit was authored while that focused research was finishing; native execution remains gated until the completed record. No broader orientation was changed.

Repair alternatives considered (20): (1) memcpy object byte, selected; (2) negative signed literal, relies on representation; (3) escaped char literal, compiler interpretation; (4) runtime integer conversion, same signedness uncertainty; (5) unsigned char test buffer, changes API type; (6) remove high-bit control, loses coverage; (7) warning suppression, hides evidence; (8) lower warning level, weakens gate; (9) remove /WX, weakens gate; (10) unsigned-char compiler mode, changes target; (11) newer compiler, outside v120 acceptance; (12) use only Linux evidence, insufficient; (13) only compile host, misses x64; (14) isolate micro-reproducer, optional if fix fails; (15) inspect disassembly, no need for source-level warning; (16) change API to byte arrays, unnecessary scope; (17) add conversion helper, unnecessary abstraction; (18) use external fixture bytes, adds dependency; (19) stop with compile failure, fallback; (20) parent escalation, if repeated failure. Narrow convergence: retain fixed API and all runtime gates, build new revision. No nested fan-out capacity allocated. Subsequent matrix identities, not v1 hashes, will identify runnable artifacts.
