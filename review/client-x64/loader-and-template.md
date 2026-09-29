# Loader and PR-template source audit

Reviewed clean client wire head `b5bb8792f2a4a95b047dd62eb62f5f040596feb7` against upstream `94945103`. The Bink, Vivox, voice-manager, ClientMain and VideoList files named below have no differences across those revisions. These are source-derived control-flow findings, not runtime verification or proof of x64 feature availability. Paths below are repository-relative.

## Bink: eager startup attempt, nonfatal missing-DLL path

- `src/game/client/application/SwgClient/src/win32/ClientMain.cpp:312` checks successful graphics installation, then line 314 unconditionally calls `VideoList::install(Audio::getMilesDigitalDriver())`. The load does not wait for a cinematic or intro request.
- `src/engine/client/library/clientGraphics/src/shared/VideoList.cpp:61` calls `BinkVideoNamespace::install`; lines 64–67 simply return if it fails.
- `src/engine/client/library/clientGraphics/src/Bink/BinkVideo.cpp:55` names `binkw32.dll`; lines 100–104 attempt binding, warn and return false on failure.
- `src/engine/client/library/clientGraphics/src/Bink/BinkDLL.cpp:139` performs `LoadLibrary`; lines 140–143 return false if loading fails. Symbol binding uses explicitly decorated Win32 names, starting `_BinkOpen@8` at line 147. Therefore an x64 binary is not the only adaptation required.
- `VideoList.cpp:97` guards a subsequent fetch when video was not installed, warns and returns null. This establishes nonfatal handling in these paths, not that every cinematic caller or all gameplay works without Bink. Missing export binding has a separate `DEBUG_FATAL` at `BinkDLL.cpp:69`.

**Conclusion:** Bink is startup-attempted once graphics initialization succeeds. Absence/wrong architecture follows a nonfatal load-failure path in the inspected code. That is existing behavior, not authorization to remove the feature or claim an x64 client can run.

## Vivox: startup wrapper, lazy vendor loading

- `src/engine/client/library/clientUserInterface/src/shared/core/CuiManagerManager.cpp:105` installs `CuiVoiceChatManager` during UI-manager setup.
- `CuiVoiceChatManager.cpp:601` installs `SwgVivox` and creates the manager. `CuiVoiceChatGlue.h:86` defines SwgVivox as the shared wrapper template.
- `src/external/3rd/library/vivoxSharedWrapper/Vivox.h:131` only constructs the singleton. Its constructor at `Vivox.inl:156` initializes state and has an empty body ending at line 197; installation itself does not load the vendor DLL.
- `CuiVoiceChatManager.cpp:801` processes events, but `Vivox.inl:291` explicitly returns if the DLL is not loaded, without loading it.
- The normal update/login path is gated by voice-enabled preference (`CuiVoiceChatManager.cpp:804`). Preference defaults false (`CuiPreferences.cpp:391`), but persisted user options can override it (`CuiPreferences.cpp:842`). `doLoginStateUpdate`, line 1862, additionally requires connection-server connection, nonempty voice username, no auto-login suppression and not hands-off. It invokes `BeginConnect` at line 1876.
- `Vivox.inl:1221` loads the DLL in BeginConnect. The service-capable path at lines 1195–1215 may first start the named `SWGVoiceService.exe`; the existence of a service does not eliminate the in-process SDK requirement.
- `Vivox.cpp:209` implements the loader; line 221 calls `LoadLibraryA("vivoxsdk.dll")`. A failed load returns false, with a failed-attempt latch preventing retries. Import failures also return false after warning/unloading.
- Other feature APIs also invoke `LOAD_DLL()` (e.g. device operations/tests). Thus “only when joining voice” is too narrow. Normal startup wrapper construction/event polling does not load it; explicit feature operations can, including outside a successful voice login.

**Conclusion:** Vivox vendor loading is lazy, while its wrapper is installed at startup. A dynamic SDK dependency remains despite the voice-service executable. This audit does not establish runtime success with absent/incompatible vendors.

## PR template

`git ls-tree -r --name-only 94945103`, searched case-insensitively for `pull_request`, `pull-request`, `pr_template`, `contributing`, and `.github`, contains no matches. No repository-tracked PR template or template sections exist at the requested base. An organization-level GitHub default template was not checked; local absence is not a claim about remote UI defaults. Suggested locally authored description headings: Problem and scope; Changes; Validation; Limits.

## Claim correction for wire PR

Avoid “none changes Win32 behavior.” The wire repair preserves tested legacy bytes for representable values, but `src/external/ours/library/archive/src/shared/ArchiveCount.h:17` now rejects lengths above the chosen signed 32-bit count maximum rather than narrowing them. A 32-bit size_t can exceed INT32_MAX, so this is a deliberate Win32 failure-behavior change too. `NetworkMessageTimestamp.h:15` adds checked time conversion where host time_t can represent out-of-range values. Describe compatibility for the tested representable inputs plus the explicit rejection policy, rather than universal behavioral identity.
