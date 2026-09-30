# TrackIR — omitted vendor family, now audited (2026-09-30)

**Genuine reachable feature, but not established as a missing-x64-SDK blocker.** Source startup calls ClientHeadTracking::install (SetupClientGame.cpp:738). It checks HKCU `Software\NaturalPoint\NATURALPOINT\NPClient Location`, reads Path, and loads **NPClient.dll unconditionally for both ABIs** (ClientHeadTracking.cpp:63). No TrackIR libraries are statically linked; current scoped Work/Downloads inventory found no NPClient DLL. This inventory is not a complete registry/all-disks inventory.

The actual TU preprocesses and compiles on native v120 Win32/x64 Debug/Release (4/4 each), with untouched source/guards (`trackir-native-v1`). A successful x64 compile masks the wrong runtime DLL filename. Native x64 loading of an ordinary i386 NPClient.dll cannot provide the intended feature.

Install resolves NP_GetSignature, validates two legacy signature strings, registers the HWND and profile **6001**, queries version, requests yaw/pitch, stops cursor mode, starts transmission, and resolves GetData. Tracking starts disabled (static bool); options UI enables the checkbox only if isSupported. CockpitCamera.cpp:826–836 consumes it only inside the locked/cockpit-mouse/POV-pan branch, clamps yaw/pitch to the existing cockpit maxima and suppresses mouse deltas. No new frame / disabled / failure produces zero yaw/pitch. This is a supported optional hardware feature with startup provider detection, not a core gameplay startup prerequisite.

## Official x64 route

[Current official developer page](https://www.trackir.com/developers) offers a Python/C++ SDK and links the [official TrackIR Godot source](https://github.com/TrackIR/TrackIR-SDK-Godot), inspected at **9802657057a8f30f655059af652ee47abe00405c**. Its `include/TrackIR/NPClientWraps.h` explicitly chooses **NPClient64.dll** for 64-bit and NPClient.dll for 32-bit, resolves the same function names, and checks the same signature strings. Its source uses the same HKCU registry path. This is primary source evidence for a native provider, stronger than community replacement wrappers.

Official current NPClient.h keeps pack(1), two unsigned shorts, unsigned long IOData, then 15 floats. Names changed (Status/FrameSignature/Yaw/Pitch, nine trailing fields now reserved), but Windows LLP64 retains unsigned long at four bytes. The inspected legacy layout is 68 bytes, yaw offset16 and pitch offset12; pointer-bearing callback/registration typedefs use HWND and ordinary function pointers, so the header is not intrinsically a 32-bit data layout. This is source layout analysis, not yet a current-provider ABI/runtime proof. Do not import the newer header wholesale merely to rename fields.

Smallest candidate likely chooses the documented provider filename by architecture while preserving profile6001 and all camera math. Before integration: obtain official current provider with identity/signature, verify exports and actual accepted profile6001, run real old/new header layout probes, and measure stock/new yaw/pitch, frame-signature handling, pause/recenter, tracking loss/recovery and cockpit mode gating on the same camera/profile. SDK availability does not establish that an old SWG profile is still recognized or that the same configuration gets applied. Do not replace the profile ID or ignore registration errors to manufacture support.

Pre-existing adjacent robustness issues (separate root causes, not changed): unchecked strcat after registry Path, unchecked getSignature call after debug-only NOT_NULL, registration/transmission return values not used, no stop/unregister on remove before FreeLibrary. They do not require speculative rewrites to make the first x64 filename investigation.

No SDK/application installed, no registry/device changes, no tracking tests or production edits. An open-source tracking emulator would change the provider/hardware algorithms and is not evidence of preserving original TrackIR behavior.

## Reviewer corrections

Composer's omission of TrackIR was real; add it to the vendor map. Composer's DPVS binary-only classification is false: existing repository source and all-four-config native builds refute it. Composer's reading of `#if DEBUG=0` as equality is false: untouched native preprocessing produced empty browser manager bodies and no widget implementation in all four configurations, confirmed by zero Mozilla object references (`native-reachability.md`). Neither claim should be propagated.

## Candidate contract (before native candidate test)

Authorized narrow change: choose NPClient64.dll on _WIN64 and NPClient.dll otherwise, update failure diagnostic, preserve profile/signatures/camera/API. Predicted: actual candidate TU compiles/preprocesses four configurations, preprocessed filename reflects architecture; legacy/current official header layouts agree for consumed fields. Failure retracts compile/layout claim and stops commit. No driver/device/runtime provider test is attempted. Candidate is authored only in ClientHeadTracking.cpp; private VM source copy keeps product untouched. Parent independently reviews and commits.

## Candidate native outcome

`trackir-candidate-v1`: actual one-file candidate preprocesses/compiles 4/4; preprocessing selects NPClient64.dll only on x64. Legacy and official Small Samples2.0 headers independently compile/run layout probes in all4 configurations: TRACKIRDATA68, SIGNATUREDATA400, status0, frame2, IOData4, pitch12, yaw16; callback pointer4/8 as expected. Package fetched from the official developer page's CDN URL `https://d2mzlempwep3hb.cloudfront.net/TrackIR_SDK/TrackIR_SDK_Small_Samples_2.0.zip`, SHA256 e11106006ee4e9e4ddb2eded6fbdf81f619798b453e6548758b2b567c5a073f0; private/excluded from Git. This SDK supplies headers/sample source, not the runtime provider. No provider execution, profile acceptance or hardware claims. Candidate source SHA is in results.json. Original-vs-candidate comparison is 9 additions/2 deletions in one file; no other source touched.

## Secondary setup consumer

Composer round 4 found NPClient.dll in SwgClientSetup/ClientMachine.cpp. That executable remains Win32-only; its loader must use the Win32 provider even when it configures a separate x64 game. Do not patch it to NPClient64.dll. If setup itself gains an x64 target, its filename and ABI checks become a separate required migration item.
