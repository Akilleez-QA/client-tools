# SessionVersion22 prospective design-repair record

Recorded before source edits/native builds/runtime, 2026-09-30. Parent assigned a targeted correction to the senior22 finding while preserving session-version21. Existing detailed assignment waives a redundant opening exchange. Root goal remains parent-owned; no product adoption is authorized.

Decompression: preserve Audio's observed 256-byte ANSI version text contract, obtaining resource 1 from the externally verified original held HMODULE. Revision21's macro/current-handle equality is insufficient for duplicate basenames because GetModuleHandle and LoadLibrary have different documented selection contracts. The restricted revision21 single-module evidence remains valid; broader module-identity claim is withdrawn. The new adapter will directly use LoadStringA(currentDll,1,buffer,256). Original SDK macro is only a controlled single-basename fixture oracle. A resource API failure returns false with unchanged frame, never fabricated empty success. Lifetime/module verification remain caller responsibilities.

## Input/source identities and boundaries

- Parent-authorized original DLL SHA-256: 0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe.
- Original private SDK header SHA-256: 966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e. Compile-time 7.2a is not the result oracle.
- Frozen revision21 source-v2.tar SHA-256: 9df919c78297f91e20db85ceebaa41a1d4319bdda5425826d919e93459bf3040; native receipt da0b0381f67667e030c909f32ae6e1a2fbfd368224de37a294278d24c3a90857.
- Review: sibling session-version21/REVIEW-senior22.md, source/specification identity finding; not a reproduced wrong-module observation.
- Portable component/codec/schema are copied or reused without semantic edits; only new session-version22 owns new source, probe and receipts. Existing frozen components, product, upstream, PR and vendor files remain unchanged.
- New native isolation C:/session-version22. Two private original DLL copies may be staged; both hashes must equal the authorized identity. No corrupt vendor fixtures, Audio install, Miles startup, device, playback, allocator or engine fixture.

## Observation and research gate

Topology: actual call bound and wire validation already observed; basename ambiguity documented; held-module resource selection documented; precise native direct-adapter comparison and failure behavior await probe. Loader ownership/concurrency, session admission, live transport, actual Audio failed-response policy and product use remain outside this repair.

Queries used: Microsoft GetModuleHandle duplicate base name unpredictability; LoadStringA HINSTANCE and zero return; LoadLibraryEx resource mapping without initialization; independent Wine resource.c mechanism. All retrieved and full relevant source content inspected 2026-09-30.

1. Microsoft GetModuleHandleA (updated 2023-02-09), https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-getmodulehandlea : duplicate basename return is unspecified; datafile modules are absent from this lookup. This challenges revision21's identity inference, not its restricted observations.
2. Microsoft LoadLibraryExA, https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-loadlibraryexa : full path targets file; basename may select first loaded module; DATAFILE_EXCLUSIVE|IMAGE_RESOURCE supports resource reads without normal DLL initialization. Datafile handles do not support GetModuleFileName/GetModuleHandle. Therefore verify both file hashes externally and pass exact full paths when mapping, rather than using those APIs on resource handles.
3. Microsoft LoadStringA (updated 2024-11-20), https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-loadstringa : resource source is the supplied module handle, max includes NUL, zero return means missing resource (also cannot distinguish empty text). Adapter deliberately rejects zero; ordinary known original version is nonempty.
4. Wine maintainers source (moving master retrieved today), https://raw.githubusercontent.com/wine-mirror/wine/master/dlls/user32/resource.c : independent implementation passes the supplied instance to resource lookup and bounds/terminates ANSI output. This is mechanism context, not Windows runtime corroboration.

Research families: Microsoft API contract and independent Wine implementation. No public source proves this private DLL's bytes; native test must do that. Gate satisfied. Strongest rival: new adapter still resolves a basename or uses the constant. Discriminator: source contains only a direct supplied-handle LoadStringA; poison compile-time value; after normal module unload, successful reads from two differently mapped same-basename datafile handles absent from GetModuleHandle. The identical copies cannot discriminate two different version contents; do not claim that they can.

## Exactly 20 materially distinct paths

1. Direct held-HMODULE LoadStringA: remove basename resolution from adapter, selected.
2. Enforce single basename externally: smaller documentation change but retains restriction.
3. Enumerate modules and reject duplicates: broader loader framework, unnecessary.
4. Align extra LoadLibrary with macro: preserves basename semantics but adds ownership complexity.
5. Dedicated resource process: isolation architecture, outside scope.
6. Parse PE resources offline: alternative mechanism, lacks macro/API equivalence directly.
7. Preserve current code with warning: finding stays open, insufficient repair.
8. Load exact full path inside adapter: expands loader ownership, unnecessary.
9. Caller supplies raw version string: moves trust boundary without fixing source identity.
10. Compile-time string result: wrong source, reject.
11. Export lookup: macro is not export, reject.
12. SDK macro as single-module oracle: retain known behavior reference, selected.
13. Poison compile-time string: detect static substitution, selected.
14. Two original copies normally loaded: duplicate ordinary modules, extra initialization unnecessary.
15. Two original copies resource-mapped: narrow basename-independence control with no extra initialization, selected.
16. Distinct valid system DLL resources: potentially discriminating text but unknown resource contract, unnecessary.
17. Custom resource fixtures: outside named artifact options, unnecessary.
18. Resource-free probe EXE handle: safe missing-resource failure control, selected.
19. Live pipe integration: valuable later, outside repair.
20. Stop/escalate if native module-resource contract contradicts prediction: preserve boundary.

Decision combines 1,12,13,15,18. Bounded saturation: module/resource identity, copy bounds, resource failure and wire ownership have source or planned native sensors; wider lifecycle/loader races explicitly deferred. Fan-out considered at each transition: this worker is the assigned repair spike and no descendant slot is allocated. Parent independent review remains separate, not presumed approval.

## Prospective predictions and acceptance

P1: Four portable plus normal/poison x86 host Debug/Release builds compile under original v120 /W4 /WX with frozen revision4 source/header/tool/library receipt helpers; all before/after identities remain equal and immediate PE hashes are captured.
P2: Direct adapter and original macro produce byte-identical nonempty version output from exact original DLL in a fixture with exactly one normal matching basename. Poison MSS_VERSION changes neither observed version.
P3: The two exact copies mapped as resource data have distinct valid handles and no normal MSS32 module present; direct adapter returns their resource bytes and remains independent of basename namespace. This is not an empirical claim about competing different-version DLLs.
P4: Null handle, invalid query and genuine missing resource on valid own EXE handle return false with unchanged response. No fake empty version results.
P5: Native x64 consumer preserves the owned result after original module/resource handle release. Existing pure 600-check wire suite remains unchanged.

Oracle version source-v1: original SDK macro in restricted fixture, direct resource API, explicit C++ checks (not assert), receipt-bound native Python launcher under -O, immediate prelaunch and postrun exact PE/both DLL hashes. Runtime 30-second and compile 180-second subprocess bounds. New build/runtime directories cannot overwrite existing attempts. Any failed prediction remains failed in preserved evidence; no dependent execution after identity failure. Stop and report unexpected resource/mapping behavior; do not introduce engine/device work. Rollback limited to newly owned staging. No private SDK macro body or vendor binary publication.
