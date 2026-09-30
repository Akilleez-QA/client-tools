# Seven-operation live composition: prospective gate

Prepared by the parent on 2026-09-30 while the separately approved pipe-native26 object check is running. This is a continuation of the selected native-Miles-shaped temporary implementation. It grants no execution authority itself. Native26 must pass; then the parent must review the complete new source, build driver and runtime runner before either build or runtime invocation. Preserve all frozen inputs and prior outcomes.

The question is whether the seven new facade operations reach the existing original-DLL dispatcher with the intended values in the actual two-process composition. Portable tests exercise client framing and scripted replies but omit host execution; the blind review demonstrated that limitation with a poisoned host header. Native compilation establishes ABI/source validity only. A real original-DLL query of resulting listener/room state supplies a different, bounded observation.

## Source boundary

Use the exact pipe26 overlay and original host dispatcher compiled by native26. New fixture-only host/controller sources use the existing framing, admission, resource resolver, private LiveChannel and cleanup infrastructure. Include host_dispatch.cpp explicitly. Do not modify the old 23-request fixture to make its old result apply to a new sequence. Do not add file callback registration, samples, streams, playback, Audio/ExitChain, Bink, generic plugin APIs, new wire IDs, native x64 vendor substitutes, or the separate pipe-drain23 patch in this experiment.

The host fixture may query the actual DLL's listener position, velocity, orientation, rolloff factor and room type after successful dispatch. It must not supply a fake vendor implementation or bypass the dispatcher for the setters under test. Check expected values chosen here, not values copied from the just-decoded request. These diagnostic getter calls are test observations, not new public facade operations.

## Precommitted sequence

One fresh-process Release pair, x64 facade controller and x86 original-DLL host, no retry. All public facade calls below remain separate synchronous calls. Raw malformed requests are private fixture controls.

1. Private Hello.
2. Bounded actual DLL version query, expected 7.2a.
3. Set redistribution directory to `miles`; keep input storage through shutdown.
4. Startup: require nonzero actual result.
5. Open 22050 Hz, 16-bit stereo, zero flags: require a real driver. The fixture immediately records the actual signed original room and requires it differ from ROOM (2); no fixture setter is allowed.
6. Query speaker configuration: require stereo.
7. Set listener position to (-1.25, 2.5, -3.75); actual getter must agree.
8. Set velocity vector to (0.001, -0.002, 0.003) metres per millisecond; compare returned F32 bits to the exact F32 inputs. If the vendor normalizes/transforms them, preserve a failed prediction before assessing it; do not silently tune the oracle.
9. Set orientation to forward (1,0,0), up (0,1,0); actual getter must agree.
10. Set rolloff to 0.5; actual getter must agree.
11. Set room to the actual header's ENVIRONMENT_ROOM (2); assert that enum value at compile time. Direct getter must return 2, different from the original observation.
12. Query room through the facade; require 2 and agreement with the direct original-DLL getter.
13. Set room to ENVIRONMENT_GENERIC (0); assert that enum value at compile time. Direct getter must return 0.
14. Query room through the facade; require 0 and agreement with the direct getter.
15. Call serve once, with no target; require normal return. No audio-work claim follows from an idle serve returning.
16. Raw listener-position request with unused value[3] nonzero: require InvalidFields; listener state remains the expected position.
17. Raw room query with an unregistered driver: require InvalidResource before admission; no fabricated vendor return.
18. Raw serve with the live driver as a forbidden target: require InvalidResource.
19. Query room again; require unchanged generic room.
20. Shutdown once.
21. Raw targetless serve after shutdown: require LifecycleRefused, no replay of shutdown.
22. Private SessionClose and complete orderly process teardown.

These fixed room predictions deliberately exercise support beyond Audio's fresh-install no-op. Initial room 2, unsupported provider behavior, or readback mismatch remains a failed probe; no dynamic alternate enum or hidden setter is permitted. See PREDICTION-LINEAGE.md for the original unexecuted 20-request draft and its source-review correction.

Record exact opcode, frame/request identity, admission ordinal, status and result on both sides. Derive and freeze the expected ordinal table from the existing admission contract before building; do not infer a passing sequence from the run. Require exactly 22 requests/replies. Admission ordinals are [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,15,16,17,18,18,19]. The exact opcode/status/admission table is checked in sequence.h and sequence.json before execution. Neither negative-control acceptance nor final-state agreement by itself proves that no intermediate SDK call occurred; keep source evidence and runtime state observations separate.

## Build and environment

Build source into a unique VM directory with real v120, actual possessed Mss.h SHA256 966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e and the existing real x86 import library. Capture exact source, includes, tools, libraries, commands and PE machine/hash identities. No produced code runs during the builder. Stop and retain first build failure.

Only after a second parent execution gate, run once in an owned private Wine prefix with an owned null sink, original Mss32.dll SHA256 0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe and original plugin identities. Bind the runner to the externally captured build receipt and PE hashes. Use bounded process-group and prefix-specific termination/wait, independent sink cleanup and durable receipt writing. Never change host defaults; compare default sink/source before and after. No rejected engine or allocator workload is permitted.

Success requires all fixed sequence/state checks, both normal exits, no emergency cleanup, unchanged DLL/plugins/PEs/defaults and complete owned-resource cleanup. A failure stops dependent work and remains a failure unless outcome-independent evidence invalidates the test. No automatic retry. The outcome ceiling is seven-operation original-DLL composition under this environment, not native Miles64 linking, full Audio installation, file I/O scheduling, callbacks, Bink, playback fidelity or client completion.

## Concrete source and invocation gates

`controller.cpp` invokes the seven facade operations separately. `host.cpp` uses the existing admission/resource/dispatcher path; `oracle.h` adds getter-only observations. The full 22-entry `sequence.h`/`sequence.json` is precommitted, including raw rejections at 16/17/18/21. The ROOM query at open is diagnostic, not another wire request. There are no direct fixture setters, preference mutations or restoration setters. If an exception occurs after startup, the inherited Backend emergency shutdown remains a failure marker, never success.

`prepare-source.py` verifies the exact native26 composed manifest (8a04b23f...), copies selected sources into a new private snapshot, and separately verifies admission.h, coordinator.h/.cpp, endpoint.cpp, metadata_host.cpp and session_version_host.cpp against frozen23. Those six link/host-loop inputs were not needed by native26's object-only anchor. It adds only authored live27 sources, tools, JSON and documentation. No SDK header, import library, DLL, plugin or PE belongs in the source archive.

Prospective build invocation on the fresh VM directory is `C:/ci-dpvs-review/python/python.exe C:/pipe-live27/pipe-live27/build-live27.py --approved-build-only`. The driver verifies all manifest entries and the actual SDK/header and original Mss32.lib hash (e8c57b30...), uses v120 /W4 /WX /EHsc /MT /O2, explicitly includes host_dispatch.cpp, and stops after the first failure. It captures actual /showIncludes, linker library search coverage, source/tool/library identities before/after, both PE machines and import reports. X86 must import the seven functions plus diagnostic getters from the possessed DLL; x64 must have no Miles DLL import. Builder execution launches only compiler/tooling, never produced code. A build approval is not a runtime approval.

The separate prospective Linux invocation is `python3 run-live27.py --approved-runtime --receipt-sha256 <externally captured build receipt SHA256>`. It creates an exclusive one-attempt marker, verifies runner/cleanup/table/plugin-pin identities against that receipt and checks PE machines/hashes. Original plugins are pinned to the earlier original-DLL live25 receipt, not learned from this runtime. Prefix and sink names are unique; only owned process groups, prefix-specific wineserver and exact owned sink modules are cleaned. Inputs/defaults and final traces remain in a durable result record. No automatic invocation or retry is part of source preparation.

Authored-only `check-source.py` checks Python syntax, agreement of both fixed tables, and parser acceptance/rejection using synthetic text. Its success is not native compilation, DLL behavior or transport evidence.
