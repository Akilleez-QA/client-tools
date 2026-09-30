# Bink/Miles binding reachability at product 49d0

**Conclusion: the main SWG client has a direct, active startup-source path that hands Audio's Miles digital driver to Bink.** This is not merely unused optional library support, and resolving an external caller is not needed to establish it. Invocation of the actual vendor sound binding remains conditional on a non-null audio driver and successful Bink DLL loading. No runtime execution, successful product link, audible output or vendor-internal behavior is claimed by this source audit.

Repository inspected: `/home/akilleez/Work/swg-source/client-build-next`, HEAD `49d0eeed4ddaa177d7a93ea396c37c3d9b9942da`; working tree was clean when checked. Paths below are relative to that root. The audit read source and project XML only. It neither ran engine/vendor code nor relied on peer review opinions.

## Direct application call graph

1. `src/game/client/application/SwgClient/src/win32/ClientMain.cpp:127` defines `ClientMain`. At line 303 it calls `SetupClientAudio::install()`. At 312 it calls `SetupClientGraphics::install(setupGraphicsData)`; inside that success branch, **line 314 calls `VideoList::install(Audio::getMilesDigitalDriver())`**. There is no platform/debug/production preprocessor exclusion enclosing that call. This precedes the rest of game setup and `Game::run` at 365.
2. `src/engine/client/library/clientAudio/src/win32/SetupClientAudio.cpp:28–40` installs Audio and registers audio teardown. `Audio.cpp:1301` opens the requested digital device; 1307 retries stereo on failure. `Audio.cpp:1492–1494` returns that same `s_digitalDevice2d` as `void *`; it does not return another device or a query token.
3. `src/engine/client/library/clientGraphics/src/shared/VideoList.cpp:61–72` passes the argument unchanged to `BinkVideoNamespace::install`, returning early if that fails, otherwise registering teardown and creating the video map.
4. `src/engine/client/library/clientGraphics/src/Bink/BinkVideo.cpp:92–125` binds Bink, installs its memory callbacks, then at 115–117 calls `BinkSoundUseMiles(hMilesDigitalDriver)` when the pointer is non-null. The binding return is not checked at this site.
5. The private local Bink SDK header's macro at `src/external/3rd/library/bink/include/bink.h:618` expands this into a sound-system selection using `BinkOpenMiles` and the driver value. Its declaration is under the non-Mac branch; this Windows client satisfies that branch. This audit does not reproduce the vendor header or infer undocumented lifetime behavior from the macro.

The earlier report's uncertainty was a search-scope error: it searched `src/engine` for the getter caller and omitted `src/game`, where the main application lives. The chain above is positive source evidence and replaces that uncertainty. No “absence of an rg match means no external use” inference is necessary.

## Conditions and playback use

- `[ClientAudio] disableMiles` defaults to false (`Audio.cpp:1214`). If true, `Audio::install` returns early at 1219, leaving the initially null driver (`Audio.cpp:104`). Failure of both driver opens also prevents a valid driver. Audio setup ignores the install Boolean and application startup can continue to video installation; therefore Bink loading can happen without invoking the shared-driver branch.
- The separate user `enabled` option is registered at `Audio.cpp:1271` and logged at 1275; it does not guard subsequent startup/driver allocation. Do not equate muted/disabled game audio preference with the `disableMiles` early return or conclude the driver is absent solely from that option.
- Graphics installation failure bypasses VideoList installation entirely. `SetupClientGraphics.cpp:69–93` can return false when Graphics installation fails.
- Failure to load Bink makes Bink installation return false, and VideoList remains uninstalled. The video fetch path checks installation (`VideoList.cpp:98–103`). These are failure/disabled paths, not evidence the successful feature is unused.
- Cutscene policy is downstream of startup binding: `Game.cpp:1524–1606` checks `disableCutScenes`, current cutscene state, client state and replay policy before `CutScene::start`. `ConfigClientGame.cpp:1018–1019` defaults `disableCutScenes` to false and `replayCutScenes` to true. That option does not remove the startup Miles-to-Bink handoff.
- `CutScene.cpp:172–188` fetches a video with `VideoList::fetch`; `VideoList.cpp:118` calls `BinkVideo::newBinkVideo`. `BinkVideo.cpp:362–403` sets Bink's file I/O and opens the movie. `USE_BINK_TREE_FILE_IO` is explicitly 1 and `USE_BINK_MEMORY_FILE` is 0 at lines 26–27; the active path sets `BinkTreeFileIO::getBinkOpenFileFunction()` and I/O size before `BinkOpen`. Thus media file I/O and image rendering remain obligations alongside audio sharing.
- `VideoList.h:25–27` documents null-driver installation as playback without sound. The actual wrapper merely skips sound-system selection on null; this audit does not assert what every vendor DLL's default output would do. Passing null to avoid integration cannot be accepted as fidelity-preserving based on this source.

## Project inclusion and the actual loader

`src/game/client/application/SwgClient/build/win32/SwgClient.vcxproj:340` includes ClientMain.cpp without an ExcludedFromBuild child. Its configurations include Debug/Release x64 and Debug/Optimized/Release Win32. The project links `clientAudio.lib` and `clientGraphics.lib` in those configurations. The literal project XML also names `binkw32.lib` and Miles32 libraries in x64 configurations. This audit did not evaluate imported property sheets, strict-link-policy overrides or the effective MSBuild link command, so those literal names do not establish the actual x64 link inputs or current unresolved dependencies. The loader and pointer-width findings below stand on the actual source independently of those XML names.

`src/engine/client/library/clientGraphics/build/win32/clientGraphics.vcxproj` is a static-library project. It includes BinkDLL.cpp (279), BinkTreeFileIO.cpp (282), BinkVideo.cpp (285) and VideoList.cpp (463), without per-file build exclusions. The only per-file metadata on those entries is an Optimized Win32 optimization setting. Debug/Release x64 configurations exist. Thus the checked project does not intentionally strip this source chain from x64 or release. XML inclusion is not a substitute for a successful native product link or executed startup.

The game's Bink adapter is explicitly built around the original 32-bit loader:

- `BinkVideo.cpp:55` selects `binkw32.dll` by a fixed string, not a configuration-driven native-x64 replacement.
- `BinkDLL.cpp:139` calls `LoadLibrary(i_name)`; `_bind` at 65–70 uses `GetProcAddress`.
- At 181–182 it resolves decorated `_BinkSetSoundSystem@8` and `_BinkOpenMiles@4` names. The rest of the table also uses 32-bit-style decorated symbols.
- The manually declared wrapper pointers at `BinkDLL.h:183–190` / `BinkDLL.cpp:58–59` use a `U32` driver parameter, while the supplied vendor header's relevant API uses its address-sized type. This wrapper is not made native-x64-correct by changing only Audio's Miles DLL. Casting a 64-bit device pointer through its current U32 parameter can lose information.
- `_construct` checks module loading, while `_bind` reports missing symbols through `DEBUG_FATAL`; `isBinkReady` at 223–225 only tests module presence. This audit does not treat it as proof all exports resolved successfully in every build mode.

These details explain why both same-process ABI compatibility and actual dynamic loader behavior must be handled. Merely retaining identical AIL facade function names cannot repair the Bink adapter.

## Lifetime and replacement implication

Audio setup registers its removal before successful VideoList setup registers video removal. `ExitChain.cpp:116–126` inserts new entries before existing entries of the same priority; `ExitChain::run:194–204` consumes the head. Both setup calls use the same default priority of zero (`ExitChain.h:70`). Consequently normal same-thread default-priority teardown orders VideoList removal ahead of audio removal. `VideoList.cpp:74–82` expects no outstanding videos and calls Bink removal; `BinkVideo.cpp:131–152` unregisters graphics hooks and unbinds the DLL. Audio removal later shuts Miles down. This is a source-level lifecycle dependency to preserve, not a guarantee about abnormal teardown or future asynchronous bridge drains.

For the temporary original-vendor strategy, keep original Bink's Miles consumer and the real Miles driver in the same 32-bit process, with an explicit private media binding. The client-side Miles proxy cannot be handed to a real Bink DLL. Retaining co-hosting is justified by this chain; no feature should be removed or silently bypassed on the theory that the sharing path is dead.

For a future in-place native64 upgrade, the game-facing Miles facade can remain SDK-shaped, but its Bink integration must also use a compatible native media implementation and actual same-process native driver. Updating only Miles while leaving this DLL name/export table/U32 wrapper unchanged is insufficient. A validated independent Bink audio output could decouple the shared device, but that would be a separately demonstrated behavior change with synchronization, volume, file I/O and playback fidelity requirements; this audit provides no basis to choose it or call it equivalent.

Disposition: **retain the co-host/private-binding requirement pending root review. Source reachability is settled positively. Runtime fidelity, vendor compatibility and full-client x64 linking remain unproven by this audit.**
