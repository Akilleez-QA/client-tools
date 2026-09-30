# startup-composition23-v1 prospective plan

Recorded before implementation/build/runtime, 2026-09-30. Parent authorizes a new startup-bridge23 sibling, one Release native v120 x86-host/x64-controller pair, and one private owned Wine-prefix/null-sink no-playback composition run. Existing detailed assignment waives opening questions. Root goal remains parent-owned. No product adoption, commits/push, prior packet edits, Audio/ExitChain/allocator-fault fixture, playback, samples, streams or new callback work.

## Frame and source basis

Compose startup-metadata-v4 and SessionVersion22 with live-bridge-candidate/common.h and admission.h, existing Coordinator, codec and Endpoint. Retain one Backend lifecycle owner for actual startup, driver and shutdown. Do not use SessionLifecycle. This narrower startup/metadata/driver slice does not rerun or inherit the original21-request sample outcomes. The old packet stays frozen.

The main inspected sources are live bridge.cpp/common.h/admission.h; metadata-v4 metadata.h/metadata_wire.cpp/metadata_host.cpp; version22 portable/host adapter; coordinator and registry; original source-owned private Wine run helpers and metadata cleanup helper. Exact source hashes will be frozen in source-manifest.json before compilation and checked against native build inputs. DLL SHA256 remains 0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe; SDK header 966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e. Version22 receipt b278f8582d5f5d6d4d77d3b8436403668f909a39331470d1f31e15b05c78e30e identifies prior component scope only.

Maintainer MAINTAINER-DESIGN23.md requirements adopted: one lifecycle owner; explicit local shared transport-status vocabulary; metadata status4/5 mapped to unique named codes rather than old lifecycle/control meanings; comparison mismatch is a fixture assertion, never transport status; each metadata operation delegates its semantic shape rules to the reviewed validator. Composer audit was spot-checked against source and is advisory, not evidence of behavior. Broader callback progress, registration retirement, reverse TreeFile/Bink, concurrency and product failure policy remain unresolved.

## Research gate and topology

Inspected 2026-09-30 after queries on Windows named pipe peer identity, held module resource identity, and destructor order:
- Microsoft GetNamedPipeClientProcessId (updated2024-02-22), https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getnamedpipeclientprocessid : identifies connected peer under API contract, not universal authentication.
- Microsoft GetModuleHandleExA (updated2023-02-09), https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-getmodulehandleexa : FROM_ADDRESS resolves actual imported function's module and owned reference prevents unload until released. Validate its mapped full path against exact staged DLL before first vendor startup.
- Microsoft LoadStringA (updated2024-11-20), https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-loadstringa : supplied module + bounded ANSI text; exact DLL result still needs runtime observation.
- C++ draft class.dtor, https://eel.is/c++draft/class.dtor : destructor body precedes member destruction, supporting SessionInputs retention until actual Backend shutdown returns; current draft does not alone prove v120 behavior.
- Project Zero original research (2019-09-25), https://projectzero.google/2019/09/windows-exploitation-tricks-spoofing.html : pipe PID can be misleading in other trust contexts. Preserve private pipe ACL/nonce/process controls and limit this experiment; no universal secure-authentication claim.

Independent evidence families: platform contracts, language specification, original security research. Gate satisfied for this composition decision. Map covers byte shape/context, semantic validation, registry liveness, admission, single vendor owner, retained paths/returned text, status mapping, real process transport, pinned module and cleanup. Stale sessions, arbitrary lanes/reentry, callback progress, adversarial loader races and actual client use remain explicit frontiers. Strong rival: per-component success fails when return spans outlive reply frames or lifecycle/status meanings collide; live owned-text retention, mapped errors and exact ordered count discriminate.

Exactly20 paths considered: (1) compose existing components, selected; (2) keep disconnected components, insufficient; (3) add SessionLifecycle, duplicate owner rejected; (4) keep Backend startup owner, selected; (5) return borrowed last-frame views, reject; (6) typed owned replies, selected; (7) renumber frozen schema, unnecessary; (8) one local explicit error map, selected; (9) leave raw metadata statuses, ambiguous rejected; (10) repeat prior21 sample workload, unnecessary; (11) no-sample driver/metadata slice, selected; (12) live callbacks now, prohibited; (13) reverse real TreeFile now, prohibited; (14) mock metadata, insufficient real-path evidence; (15) fixture-only direct oracle, selected; (16) backend oracle API, reject; (17) broad Debug/Release matrix, unnecessary absent failure; (18) one Release pair/run, selected; (19) pure signed/extreme error controls alongside real positive observations, selected; (20) stop on identity/mismatch/nonterminal cleanup, selected. Bounded saturation covers this named slice, not complete startup/fidelity. This worker is already a parent-assigned spike; no descendant capacity allocated. Parent/maintainer review remains independent work, not inferred runtime corroboration.

## Exact prospective request order (23)

Every frame: monotonic request1..23, lane1, causal0, lease0, existing full nonce Hello; unchanged Coordinator admits after liveness, completes admitted operations and begins drain only after successful real shutdown.

| Request | Opcode | Input / expected signal |
|---|---|---|
|1|Hello|existing32-byte nonce, success|
|2|SessionVersion|fixed empty call, owned actual version5bytes expected against macro fixture|
|3|AIL_set_redist_directory|dot, owned exact direct-oracle response|
|4|AIL_set_redist_directory|miles, distinct owned exact direct-oracle response|
|5|AIL_set_redist_directory|interior-NUL malformed bytes, InvalidFields; no adapter dispatch/retention growth|
|6|AIL_startup|actual nonzero return; sole Backend ownership|
|7|AIL_get_preference|1, signed actual direct comparison|
|8|AIL_get_preference|42, signed actual direct comparison/save initial fixture value|
|9|AIL_last_error|fixture-controlled first text, owned reply|
|10|AIL_last_error|fixture-controlled changed text; earlier reply remains unchanged|
|11|AIL_set_preference|42=16, signed prior return/direct readback|
|12|AIL_get_preference|42=16|
|13|AIL_set_preference|42=64, signed prior/direct readback|
|14|AIL_get_preference|42=64|
|15|AIL_set_preference|42=0xffffffff, InvalidFields; unchanged state/no adapter dispatch|
|16|AIL_get_preference|42 still64|
|17|AIL_open_digital_driver|22050/16/stereo, real nonnull driver|
|18|AIL_speaker_configuration|valid driver mask24, InvalidFields before adapter/vendor call|
|19|AIL_speaker_configuration|unregistered driver mask8, InvalidResource before admission/vendor call|
|20|AIL_speaker_configuration|real driver mask8, exact direct channel-spec match|
|21|AIL_shutdown|fixture restores saved initial preference first; Backend actual shutdown then registry retirement; retained paths still live|
|22|AIL_get_preference|42 after shutdown, LifecycleRefused from existing draining admission; no vendor call|
|23|SessionClose|existing cleanup admission, actual prior shutdown required|

Success requires exact count/order/status, no callback frames, all fixture comparisons, x64 owned version/error/directory data still valid after later responses, real-host orderly exit and independent resource cleanup. Signed return mapping is tested with actual positive vendor values plus pure negative-bit controls; no unsupported negative preference is sent to vendor. Direct comparisons/state restoration stay entirely in fixture code and introduce no extra startup/shutdown owner. MetadataInvocations counts successful semantic dispatch entry only; rejected controls must not increment it. SessionInputs is a Backend member and retains both successful path inputs through actual shutdown and close; failed malformed path adds nothing.

## Error vocabulary and intended observations

Local StartupBridgeStatus uses0 Success,1 Unsupported,2 InvalidResource,3 InvalidFields,0x1001 LifecycleRefused,0x1002 TextTooLong,0x1003 InputBudgetExceeded,0x1004 VersionQueryFailed. Metadata0..5 map explicitly once; a small pure check verifies mapping/disjointness. No control-oracle mismatch code is sent on the wire. Frozen protocol field remains uint32 transport_status, unchanged.

Prediction P1: the Release x86/x64 pair builds with v120 /W4 /WX; revision4 helpers record transitive headers, selected tool/library and source before/after plus immediate PE machine/SHA. P2: one real x64-to-x86 private Wine run follows23 requests and real original adapter answers agree with fixture, while three malformed/resource controls plus postshutdown refusal produce the named errors without state/ownership mutation. P3: exact retained-byte count survives actual shutdown; typed owned text survives later frames. P4: null sink is removed, only owned Wine prefix is stopped, default sink/source are unchanged even on failure.

Before runtime: send this plan to parent, freeze source, verify native receipt external pin and both executable bytes/machines, exact DLL and staged runtime dependencies. Hash local imported receipt/cleanup helpers actually used; no assert-only gates. Runtime records each received encoded frame's request/opcode/size/SHA256 and copied text/scalar values, not merely transient unretained file names. No broad repeat matrix absent a new failure.

30-second process watchdog; existing channel/drain watchdogs retained. Unexpected status, oracle mismatch, identity mismatch, timeout, emergency Backend cleanup, or failed defaults/owned-resource cleanup fails the scoped prediction and stops. Preserve first failure. No retry/fake-success path. Cleanup helper independently attempts owned wineserver termination, owned null sink unload and defaults read before durable result write. Rollback is removing only new candidate inclusion/staging, never product rollback. Private copied DLL/plugins and PEs stay excluded from published evidence; only our sources/text receipts/logs are eligible.
