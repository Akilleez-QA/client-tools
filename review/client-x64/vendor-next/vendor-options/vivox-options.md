# Vivox: baseline reachability before replacement

Research date: 2026-09-30. **Target is the existing SWG Source v3.0 experience, not restoration of removed retail features.** No replacement, bridge, login, service launch or network request was implemented or performed. The local loader tests below are useful architecture evidence; they do not make voice restoration a prerequisite for the x64 client.

## Baseline source gates

Paths below are under client-build-next/src. The actual source currently has:

- `engine/client/library/clientUserInterface/src/shared/core/CuiPreferences.cpp:391`: voice enabled defaults false.
- `CuiVoiceChatManager.cpp:745`: setVoiceChatEnabled immediately returns; it cannot enable or disable the preference. This is deliberate upstream disabled-feature code.
- `game/client/library/swgClientUserInterface/src/shared/page/SwgCuiOpt.cpp:114`: construction of the voice options page is commented out. Its volume setter paths remain compiled but are not evidence of accessible UI.
- `CuiVoiceChatManager.cpp:797–815`: update first calls ProcessEvents, then returns if voice is disabled. `vivoxSharedWrapper/Vivox.inl:292–295` explicitly returns from ProcessEvents when the DLL is not loaded; it does not load the DLL merely to poll.
- The constructor's mute setup does not force a load: SetLocalMicMute returns while disconnected (`Vivox.inl:2075–2079`).

**Residual saved-preference path:** `CuiPreferences.cpp:842` still registers voiceChatEnabled with CurrentUserOptionManager. `sharedUtility/.../OptionManager.cpp:254–264` stores the variable address and assigns the saved boolean using findBool. The later forced-false call at CuiPreferences.cpp:870 goes through the no-op manager setter, so it does not actually clear a saved true. The getter returns that variable. No real user profiles were inspected or changed.

If a saved true and the other existing conditions hold, update can reach doLoginStateUpdate (`CuiVoiceChatManager.cpp:1859`): connected game server, nonempty server-supplied account information, no prevent-login state and no hands-off state. Then BeginConnect can run. This is a source-reachable conditional path, not an observed functioning voice session. Server account/channel handlers remain compiled. It would be incorrect both to call voice a proven active baseline requirement and to claim every historical path is eliminated.

In the scanned SWG Source v3.0 client root, SWGVoiceService.exe is absent. A separate whitengold/exe/win32 root contains it. Missing service prevents that service path completing, but does **not** prove no DLL load: BeginConnect calls DisconnectVoiceService, whose implementation loads vivoxsdk.dll before service startup.

## Actual binaries and local probe

[Complete inventory](vivox-probe/binary-inventory.json) records hashes and PE-machine fields, not filename guesses. In both inspected roots, vivoxsdk.dll, vivoxplatform.dll, wrap_oal.dll, ortp.dll and libsndfile-1.dll are PE machine0x14c. The whitengold SWGVoiceService.exe is also0x14c and imports vivoxsdk.dll. vivoxsdk's local static dependencies are wrap_oal, ortp and libsndfile; remaining imports are system libraries. Dynamically loaded provider completeness was not established.

The actual DLL resource and SDK version API identify **3.0.0005.7314**; wrap_oal has file version2.1.9.3. Other scanned binaries lack reported version-resource strings, so hashes identify them.

The source wrapper imports **52 names**, including version3 conditional functions. Every name is present in each inspected provider export table. Native v120 Win32 loads the original DLL and resolves all52; a string duplication/free and an **unissued** aux request creation/destruction pass. A second probe round-trips that unissued request's type and synthetic cookie through the original XML helpers. Native x64 gets Windows load error193 against the same x86 DLL, as expected. This is not a successful x64 backend.

[Probe source/plan](vivox-probe/PLAN.md), [native logs](vivox-probe/run32.log), [version records](vivox-probe/versions.json). The probe never calls vx_issue_request, vx_alloc_sdk_handle, connector/account initialization or the service executable. Loading a proprietary DLL is a black-box action; no packet-capture claim about its internals is made.

## Why the existing service does not solve the client ABI

`Vivox.cpp:220` loads vivoxsdk.dll into the client and resolves its entrypoints. In service mode, `Vivox.inl:1221–1267` still loads that DLL, allocates an SDK handle, creates pointer-containing request objects, duplicates strings and issues requests. `m_generateID:3078` writes request cookie and sdk_handle; `m_issueRequest:3101` calls the provider and tracks pending cookies. Responses/events are polled and destroyed through that same SDK.

An x64 process cannot directly use the existing x86 DLL merely because another x86 service exists. A matching x64 SDK proxy could potentially speak to the old service, but protocol/version compatibility is unverified. A new x86 bridge could host the original SDK and preserve its objects inside that process; that adds an IPC boundary and may coexist with the existing service. The local XML roundtrip demonstrates serialization functionality only. It does not establish socket framing, connection management, service protocol compatibility or a complete cross-process contract.

## Conditional options if baseline requirements later demand voice

| Option | Potential advantage | Evidence/decision still needed |
|---|---|---|
| Preserve current disabled baseline | Avoids accidentally restoring a removed feature; no new dependency | Native baseline reachability trace, including saved-preference corner, to establish exact intended behavior |
| Authorized matching-era x64 SDK proxy | Could preserve original service/codec behavior without a new bridge | Matching version availability, licensed rights and service protocol tests; none established here |
| Modern official Vivox Core | Supported engine-agnostic native path | New SDK/API/auth and service contract; legacy accounts, channels, codecs and event behavior cannot be assumed compatible |
| Original x86 SDK in helper | Retains old provider object/codec code | Ordered command/result/event serialization, lifecycle, failures and PTT latency; existing remote service availability still needed |
| Direct old-service protocol implementation | Avoids loading x86 SDK in client | Not justified by XML helpers alone; requires documented complete protocol and compatibility evidence |
| Different voice system | Could provide a maintainable future feature | Changes service, account/channel semantics, codec/spatial behavior and community deployment; a new feature project, not preservation of current disabled baseline |

No vendor contact or new credentials are authorized/performed. Public SDK availability is separate from entitlement and existing service availability.

## Behavior that a future migration must preserve

Source has dirty positional updates limited to10Hz (`Vivox.inl:20,300–307`) with speaker/listener position, orientation and velocity (`3321–3358`). PTT mic requests defer while one is pending, then reconcile desired state; commands cannot simply be reordered. Pending request cookies and response/event order influence login/session state. Voice activity affects the game's audio: `CuiVoiceChatManager.cpp:1833–1840` calls Audio::fadeAll/unfadeAll on speaking transitions. Thus changed event timing can change music/effects even if voice sounds similar.

If this becomes an explicitly required active feature, compare muted/unmuted transitions, positional routing, channel joins/leaves, participant controls, event/cookie order, error/reconnect/shutdown and ducking with a working authorized original baseline. Current local tests establish none of those network/audio properties.

## Primary research, date and limits

Queries on2026-09-30: `site.docs.unity.com vivox native sdk Windows 64 bit`, `site.docs.vivox.com native SDK out of process service vxplatform`, `site.docs.unity.com vivox core before you begin access token SDK download`.

- [Unity Vivox Core overview](https://docs.unity.com/vivox-core) describes an engine-agnostic integration; a Unity game-engine conversion is not required.
- [Official Core setup](https://docs.unity.com/en-us/vivox-core/core-vivox-setup) provides a Custom-engine/dashboard SDK acquisition route. No account created or SDK downloaded here.
- [Windows development](https://docs.unity.com/en-us/vivox-core/developer-guide/windows) is current native documentation, not proof of old3.0 binary compatibility.
- [Official token examples](https://docs.unity.com/en-us/vivox-core/access-token-guide/access-token-examples/access-token-examples-toc) establish a modern authentication integration surface; no actual token/endpoint/credential is recorded here.
- Archived v5 messaging docs/search expose out-of-process API names, but full page retrieval failed. They are not used to claim a modern SDK talks to SWGVoiceService3.0.

Status: local architecture/lifecycle observed, baseline source gates inspected, live reachability and voice functionality unobserved. No production edits. Preservation of the existing disabled baseline takes priority over speculative voice restoration.
