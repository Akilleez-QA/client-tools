# VideoCapture Debug x64 linker audit

2026-09-30, read-only. No provider replacement, feature removal, product overlay, or native runtime executed.

## Observed linker dependency

Actual diagnostic Debug x64 link at `allocator-next/integration-current-v2/vivox-lcd-link-v1/Debug/link.log`:

- lines34056–34058: `VideoCapture::SingleUse::run` referenced by `clientUserInterface.lib(CuiIoWin.obj)` loads `clientGraphics.lib(SwgVideoCapture.obj)`.
- lines34551–34554: `SourceConfigAud2SourceFmtAud(int,int)` referenced by that object selects `VideoCapture_debug.lib(EncoderConstants1.obj)` and fails LNK1112, X86 versus x64.

This is an actual linked source dependency, not merely a stale library-name guess.

## Baseline reachability

Repo paths below relative to client-tools:

- `src/engine/client/library/clientUserInterface/src/shared/core/CuiIoWin.cpp:208–210`: each Debug/nonproduction draw calls `VideoCapture::SingleUse::run()` under `PRODUCTION == 0`.
- `src/engine/client/library/clientGraphics/src/shared/SwgVideoCapture.cpp:476`: static smart pointer starts null (`Smart/SmartPtr.h:39` constructor); `run()` at585 only enters its body if the pointer is nonnull. The only assignment/Attach found is inside `start()` at563.
- `src/engine/client/library/clientGame/src/shared/core/Game.cpp:3015,3025,3060`: config, start/callback, stop all already behind `#if 0`.
- `src/game/client/library/swgClientUserInterface/src/shared/parser/SwgCuiCommandParserScene.cpp:536–538`: command registrations commented; handlers4895/4912/4921 also `#if 0`.
- Source-wide search finds no other calls to SingleUse::start/config or VideoCapture::install outside those disabled Game methods. Public declarations remain available; hypothetical external modification is not a current baseline caller.
- Baseline94945103 Game.cpp independently inspected and has the same disabling. CuiIoWin draw poll is unchanged since initial commit. Therefore current Source v3.0 exposes no found capture-start route but retains a no-op Debug poll that brings the legacy implementation into the link.

The smart-pointer null constructor/destructor has no capture operation when never started. `getVideoCaptureProps()` is function-local static reached through config/start, not the idle poll. This is source evidence of an inactive feature, not a live gameplay trace.

## Source and architecture inventory

`src/external/3rd/library/videocapture` has headers, docs, and prebuilt archives/DLL, no implementation C/C++ source or build project. Full Work filename search for EncoderConstants*, VideoCaptureManager, EncoderThread implementations found none; a separate whitengold checkout has SwgAudioCapture.cpp, which is the client adapter rather than the encoder implementation.

`binary-inventory.json` records SHA-256 and llvm-readobj COFF Machine results for all16 supplied `.lib`/`.dll` files: every machine is IMAGE_FILE_MACHINE_I386. Includes VideoCapture, AudioCapture, ImageCapture, CaptureCommon, Smart, SoeUtil, ZlibUtil and PICTools. No source-rebuild claim can be made from these headers.

## Narrow next decision and prospective proof

A candidate can remove the residual Debug draw poll of this already disabled Source feature, retaining vendor code and declarations. That is baseline cleanup, not a fake run implementation or x64-only empty stub. It must be reviewed explicitly as removing an unreachable-start poll; never claim full capture support. Keep it separate from removing any link-list entries.

Before acceptance, compile the real CuiIoWin TU for both architectures/configurations, relink real Debug clients (Win32 and x64), and verify no capture objects are pulled through another route. Preserve the before/after link maps and check that the only newly unreferenced path is the already disabled capture path. Release should have no generated-code difference because its existing preprocessing excludes the poll. A Win32 Debug normalized executable need not be identical because removing unused compiled capture machinery can change layout; require a scoped symbol/import and source behavior explanation instead.

If an enabled capture route is subsequently found, stop this cleanup proposal: the genuine encoder source or licensed x64 provider/explicit backend decision is then required. The broader restoration/bridge is not authorized or necessary on current evidence.

## Authorized candidate and native compilation

Parent approved the narrow cleanup after independent source inspection. Throwaway `client-capture-cleanup-candidate` based2a06b9dcb changes only CuiIoWin.cpp: five deleted lines (SwgVideoCapture include and conditional idle poll). Final source SHA-256 `e331b21582c88c282e1fb8fb6c8a01a67ec04145307e7b41f189b77f24ce662c`. Vendor implementation remains unchanged; no stub or capture-support claim.

Native v120 actual TU compiles successfully in Debug/Release Win32/x64. Original .tlog commands retained, original include/define/compiler options used; source, object/PDB output paths isolated and minimal-rebuild database disabled. Win32 uses genuine v1 product snapshot metadata; x64 uses latest v2 snapshot metadata. No Q/R mapping or source/library mutation. Private copies of clientUserInterface.lib replace exactly its original CuiIoWin.obj member; before/after lists establish one member, and source/archive/object digests recorded.

Downloaded `native-v2.zip` holds source, command/log/member-list/hash records, not large binaries; private VM archives remain C:/capture-poll-candidate-v2. First v1 compilation also passed but used older x64 metadata; v2 is the relevant set. Build agent owns subsequent real Debug Win32 and x64 progression relinks. At this checkpoint no full-link success or live-client behavior claim.
