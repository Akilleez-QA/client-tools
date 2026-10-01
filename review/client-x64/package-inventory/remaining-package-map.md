# Remaining x64 package map

Frozen inventory of `implementation/client-miles@eca74ffa5741f608a1417944b2e2602868936517` versus maintained master `949451032647e45e42c3aaef3f41b132c8af36e3`. This covers the complete authoritative diff, including runtime code under `tools/miles-bridge/src`. It is a packaging map, not a redesign or another runtime acceptance campaign. Submission state is the recorded local checkpoint; no remote merge-state refresh was performed.

[Machine-readable map](remaining-package-map.json) records every changed path, exact originating commit SHA and subject, final Git blob identity, package ownership, prerequisite, branch/head, and accounting category. Origins use the canonical first-parent integration history; duplicate merge-side cherry-picks are not counted twice.

## Reconciled accounting

| Category | Files | Added | Removed |
|---|---:|---:|---:|
| Existing src production | 117 | 2,113 | 796 |
| Miles/Bink runtime under tools | 103 | 9,852 | 0 |
| Build/configuration (separate) | 83 | 8,897 | 28 |
| Actual tests/docs/CI (excluded from production) | 50 | 5,050 | 0 |
| **Production total** | **220** | **11,965** | **796** |
| Full diff | 353 | 25,912 | 824 |

Each production file has one **accounting owner**, even when several packages contribute hunks. Package counts below allocate the complete final file once; they are not proposed PR hunk sizes. Component ownership and already-submitted hunks remain explicit. The JSON also lists all 83 build files and all 50 excluded files, so the whole diff reconciles without an unclassified remainder.

Production file states: 161 remaining components, 35 fully submitted components, 19 prepared or submitted components, 5 mixed submitted or prepared and remaining. Mixed-file rows must not be treated as wholly unsubmitted.

## Finite package queue

| Package | Recorded status | Base/prerequisites | Exclusive production files, +/− |
|---|---|---|---|
| `wire-contract` — Legacy wire count and timestamp contract | [submitted_upstream](https://github.com/SWG-Source/client-tools/pull/23) | master | 23, +152/−87 |
| `dpvs` — DPVS Windows x64 architecture and scalar PC64 approximation | [submitted_upstream](https://github.com/SWG-Source/client-tools/pull/24) | master | 4, +35/−4 |
| `link-cleanup` — Remove unused explicit Release link inputs | [submitted_upstream](https://github.com/SWG-Source/client-tools/pull/22) | master | 0, +0/−0 |
| `imemmove` — Unambiguous checked int-length move helper | [submitted_upstream](https://github.com/SWG-Source/client-tools/pull/25) | master | 4, +7/−7 |
| `network-widths` — Windows socket and completion-key widths | [prepared_fork_draft](https://github.com/Akilleez-QA/client-tools/pull/2) | `imemmove` | 5, +9/−6 |
| `byteorder` — Windows x64 byte order | [prepared_fork_draft](https://github.com/Akilleez-QA/client-tools/pull/1) | `imemmove` | 1, +26/−0 |
| `http-lock` — Windows x64 HTTP recursive lock | [submitted_upstream](https://github.com/SWG-Source/client-tools/pull/30) | master | 1, +17/−0 |
| `allocator-layout` — Allocator header layout and block-order diagnostic | [submitted_upstream](https://github.com/SWG-Source/client-tools/pull/29) | master | 0, +0/−0 |
| `shell-results` — Pointer-width ShellExecute status | [submitted_upstream](https://github.com/SWG-Source/client-tools/pull/28) | master | 1, +2/−2 |
| `ui-pool` — UI pool natural alignment | [submitted_upstream](https://github.com/SWG-Source/client-tools/pull/27) | master | 1, +1/−1 |
| `pcre-capacity` — PCRE capture capacity in elements | [submitted_upstream](https://github.com/SWG-Source/client-tools/pull/26) | master | 1, +1/−2 |
| `platform-diagnostics` — Native Windows diagnostic primitives and pointer values | remaining | master | 4, +15/−5 |
| `ui-native-widths` — UI parsing and native-size source expressions | remaining | master | 7, +19/−11 |
| `archive-callbacks` — Game callbacks match fixed-width archive indices | remaining | `wire-contract` | 4, +12/−10 |
| `stlport-sdk` — Build bundled STLport sources using native SDK declarations | remaining | master | 1, +10/−0 |
| `allocator-address-stack` — Coupled allocator owner, stack walk and hook ABI | [prepared_fork_draft](https://github.com/Akilleez-QA/client-tools/pull/3) | `allocator-layout` | 13, +314/−125 |
| `allocator-sizes` — Allocator size invariants, statistics and realloc metadata | remaining | `allocator-address-stack` | 15, +190/−118 |
| `fpu-controls` — x64 MXCSR policy and collision caller contract | remaining | master | 3, +55/−2 |
| `math-kernels` — x64 SSE arithmetic, affine transform and collision square root | remaining | `fpu-controls` | 4, +235/−1 |
| `skeletal-kernel` — x64 hard skinning SSE kernel | remaining | `math-kernels`, `ui-native-widths` | 1, +97/−0 |
| `archive-storage` — ByteStream bounds and decoder/count preflights | remaining | `wire-contract` | 5, +127/−107 |
| `crypto-boundaries` — Crypto packing and checked public count interfaces | remaining | `stlport-sdk` | 4, +28/−5 |
| `trackir-provider` — Native TrackIR provider and bounded loader path | remaining | master | 1, +12/−3 |
| `file-manifest` — Retain FileManifest entries until removal | remaining | master | 1, +2/−2 |
| `audio-native-contract` — Miles callback/preference widths and diagnostic strings | remaining | master | 0, +0/−0 |
| `x64-projects` — Generated v120 Debug/Release x64 project closure | remaining | `link-cleanup`, `dpvs` | 0, +0/−0 |
| `obsolete-client-inputs` — Remove already unused browser/capture inputs | remaining | `link-cleanup`, `x64-projects` | 1, +0/−5 |
| `native-providers` — Genuine renderer, STLport, LCD, Vivox and parser providers | remaining | `x64-projects`, `stlport-sdk` | 2, +14/−1 |
| `link-stack-policy` — Strict x64 final link and two-MiB stack reserve | remaining | `native-providers` | 0, +0/−0 |
| `miles-session-core` — Miles facade, private host session and engine callback bridge | remaining | `audio-native-contract`, `allocator-sizes`, `stlport-sdk`, `native-providers` | 91, +8593/−0 |
| `miles-game-selection` — Opt-in Miles game integration and Debug/Release builds | remaining | `miles-session-core`, `link-stack-policy`, `obsolete-client-inputs`, `file-manifest` | 5, +305/−77 |
| `bink-host-session` — Original Bink owner and private-session video extension | remaining | `miles-game-selection` | 11, +1213/−0 |
| `bink-game-selection` — Shared video blitter and opt-in game adapter | remaining | `bink-host-session` | 6, +474/−215 |
| `media-release-build` — Matching Release builds for the paired Miles/Bink development client | remaining | `miles-game-selection`, `bink-game-selection` | 0, +0/−0 |

There are 34 aggregate accounting units: 9 submitted upstream, 3 prepared fork drafts, 22 remaining. The Miles aggregate is further divided in the linked foundation proposal. Zero exclusive files does not mean an empty package: allocator-layout owns already-submitted hunks inside the final allocator file, and build-only units have separate build-file accounting.

The checked-size/minimum-node subset of `allocator-sizes` is now [fork draft #4](https://github.com/Akilleez-QA/client-tools/pull/4), head `1f8f341aab958ac13f04b070bb6575be0af36091`. Its two commits are +70/−29 in GitHub’s diff, one file. The aggregate remains in the remaining column because statistics, pointer diagnostics and null-reallocation have separate pending packages.

Miles foundations 1–3 are now fork drafts [#5](https://github.com/Akilleez-QA/client-tools/pull/5), [#6](https://github.com/Akilleez-QA/client-tools/pull/6) and [#7](https://github.com/Akilleez-QA/client-tools/pull/7). Foundations 4–6 and the build/Audio handoff remain pending; the aggregate stays remaining until that closure is prepared. The two comment-only documentation corrections add two lines relative to the historical foundation snapshot; the frozen maintained-client accounting above is unchanged.

## Concrete next branches

- **`review-ready/client-allocator-address-stack`**: base `2af9f19b502e9183731656cdaf93236faacb404e`; apply `2fdd4639bc7a0547925d93d733cd3a8ef5838630` → `b4b4289b26772c933781dc4ebba44168fecf5600` → `d905d5254b281974e82ae80be28c01aafdcbd979`. Next substantial source package. Keep breakpoint prerequisites and the complete owner/stack/hook ABI patch together; existing PR29 is the base.
- **`review-ready/client-allocator-size-invariants`**: base `result of review-ready/client-allocator-address-stack`; apply `03fafe0cc8efb2c991a7d16ebd025929bc9812f4` → `cf82805a9d13e6082ae96977093d670ea116a82f` → `8e6b08fbd47775ca48083b102a7d14bc717be4dc` → `45fae5093c16757e2c779ad5daf6f63d170ed8a4` → `fcf54ab3fcbf4a0b2ef1c2915b620a510975a429`. Next allocator layer. Original order preserves checked sizes, full-width statistics and every consumer, free-node capacity, diagnostics, then realloc metadata/call sites.
- **`review-ready/client-math-kernels`**: base `949451032647e45e42c3aaef3f41b132c8af36e3`; apply `1c90143692936b20721a452fdb72819d018adef3` → `8cdd61ed5b373c4766d107cdad31925309bec21b` → `631c79266695e4cdffada33b954033b965fed0de` → `1a2d514b6a44c4a30badfec959db5a526d4fc767`. One branch composing FPU policy plus the three existing SSE kernel commits. Keep four commits reviewable and retain existing numerical evidence boundaries.

These recipes preserve original patch order. The address/stack recipe is now prepared as fork draft #3 at `fc667f38eafbd4a2b4d50f96a31efb5cca3ef55c`; the later recipes remain planning inputs. Preserve already-published histories and reconcile equivalent upstream content rather than blindly replaying patches.

## Causal boundaries and shared-file handling

**Allocator:** submitted layout/order PR29 → complete owner/stack/hook ABI → checked sizes/statistics/minimum free representation/realloc metadata. The owner layer includes fatal and export-template breakpoint prerequisites. Its DbgHelp, allocation wrappers, header/API and renderer/DllExport hooks travel together. The later layer retains original commit ordering and all statistics consumers; it is not an isolated typedef substitution. Existing fault limits remain intact.

**Math:** FPU declarations/implementation and CollisionWorld policy precede SSE helper/affine/collision kernels, followed by hard-skinning integration. Keep the historical numerical limits attached to the existing observations; no universal bit identity or new physics acceptance is inferred.

**Build:** compose submitted Release link cleanup and DPVS configuration, apply the generated x64 closure, then real-provider build ownership/imports, obsolete inputs cleanup, strict final-link/stack policy, and opt-in media development selection. The provider package has reviewable renderer, LCD, STLport/Vivox and PCRE/XML subcommits. It does not redistribute provider binaries or SDK bodies.

**Miles/Bink:** the aggregate session-core accounting above is superseded for review by [six source foundations and a build/Audio handoff](miles-core-package-split.md). The split keeps contracts, ownership and private-header coupling together, uses pre-Bink source blobs, and introduces unchanged build entry points after their source closure. Opt-in game selection, Bink host/session extensions, game video integration and matching Release builds follow. The public SDK-shaped facade remains replaceable; game callers do not take private IPC types.

The full game-selection step additionally needs the already-established client source/configuration closure listed in JSON. That composition requirement is distinct from prerequisites for reviewing a standalone source fix.

- `src/engine/shared/library/sharedMemoryManager/src/shared/MemoryManager.cpp`, `src/engine/shared/library/sharedMemoryManager/src/shared/MemoryManager.h`: Use PR29 as base, then owner/stack commit d905, then size/statistics sequence. Do not export final whole files for PR29 or owner-only review. No new allocator design; preserve existing commit hunks.
- `src/engine/client/library/clientAudio/src/win32/Audio.cpp`: Native SDK-width/diagnostic repairs precede admitted-worker/facade compile hooks, then game selection/template lifetime. A master-based native-contract package needs only d0fea/25f7/681 hunks, not final Audio.cpp. Last diagnostic commit has later-context ancestry; reconcile context if needed without copying facade logic.
- `src/engine/shared/library/sharedFoundation/src/win32/Os.cpp`: Already submitted shell change and remaining thread-name exception change are separate. Apply eb73 only for thread naming; final whole-file copy would duplicate PR28.
- `src/external/ours/library/archive/src/shared/Archive.h`, `src/external/ours/library/unicodeArchive/src/shared/UnicodeArchive.cpp`: Start storage/decoder package above PR23 and apply residual original commits. Final files on master would resubmit existing wire-contract work.
- `tools/configure-client-x64/client-x64.props`, `src/build/win32/swg.sln`, `src/game/client/application/SwgClient/build/win32/SwgClient.vcxproj`: Generated configuration, original link cleanup, unused-browser removal, provider imports and strict-link/stack policy are distinct chronological hunks. Standalone component branches must extract those hunks or stack exact prerequisites; never copy final central files wholesale.
- `tools/miles-bridge/build.py`, `tools/miles-bridge/sources.json`, `tools/miles-bridge/client-miles-dev.props`, `src/engine/client/library/clientGraphics/build/win32/clientGraphics.vcxproj`: Keep complete 33efad Release support last, after Audio and Bink selection. Moving Release Audio support earlier requires an explicit manual split of audio/common build and graphics-dependent property hunks. Recommended order avoids that split.
- `tools/miles-bridge/src/admission/coordinator.cpp`, `tools/miles-bridge/src/api/pipe/LiveChannel.cpp`, `tools/miles-bridge/src/api/pipe/PipeCore.cpp`, `tools/miles-bridge/src/api/pipe/Session.h`, `tools/miles-bridge/src/backend/backend.h`, `tools/miles-bridge/src/backend/reply.h`, `tools/miles-bridge/src/bootstrap/common.h`, `tools/miles-bridge/src/host/host.cpp`, `tools/miles-bridge/src/protocol/miles_wire.h`, `tools/miles-bridge/src/wire/codec.cpp`, `tools/miles-bridge/src/wire/resource_registry.h`: Miles coordinator, wire codec, registry, backend and host are reused by Bink. Apply complete tested Bink extension commits after Miles session/game phases; do not split declarations, dispatch and validation across incompatible revisions.

Shared-file status is a warning against final-file copying, not a claim that every cherry-pick will conflict. Manual hunk extraction is required when isolating one component on master without its listed predecessor, or when moving Release media support before Bink. The recommended chronological stack avoids the latter split.

## Package commit register and limits

| Package | Canonical origin commits (ordered) |
|---|---|
| `wire-contract` | `83a01f5883` → `2b5e3a4832` → `1e62bab469` → `579db9f6a8` → `a65d803277` → `a081f02370` → `f87084a3fa` → `b5bb8792f2` |
| `dpvs` | `38768130ee` → `856b493ab0` → `17d728834c` → `7b560df521` → `76a5a10a10` |
| `link-cleanup` | `332919f25e` |
| `imemmove` | `3c0535f39e` |
| `network-widths` | `83f7d24884` → `14c1bd30e8` → `782aed355a` |
| `byteorder` | `98388ee37a` |
| `http-lock` | `ff3c1742fe` |
| `allocator-layout` | `29289bd8b1` → `f102763f70` |
| `shell-results` | `12bb888097` |
| `ui-pool` | `2a06b9dcb0` |
| `pcre-capacity` | `5c481293a1` |
| `platform-diagnostics` | `9dc0e340fd` → `eb73c7e8fc` → `b8e359f414` → `b1277c963d` |
| `ui-native-widths` | `291e706032` → `1ee6a5f4b8` → `032f632a9b` → `edcf5b4610` → `c08d6c4f7c` → `aa77373637` |
| `archive-callbacks` | `966365f945` |
| `stlport-sdk` | `92b05cbd89` |
| `allocator-address-stack` | `2fdd4639bc` → `b4b4289b26` → `d905d5254b` |
| `allocator-sizes` | `03fafe0cc8` → `cf82805a9d` → `8e6b08fbd4` → `45fae5093c` → `fcf54ab3fc` |
| `fpu-controls` | `1c90143692` |
| `math-kernels` | `8cdd61ed5b` → `631c792666` → `1a2d514b6a` |
| `skeletal-kernel` | `3c172d1b13` |
| `archive-storage` | `5755f8f3be` → `8d9010900c` → `d89b9f49e2` → `4d3009851e` → `edc04cb1d8` |
| `crypto-boundaries` | `78e1f907c1` → `8fe43cca91` → `978a45d812` → `91dc05e8be` |
| `trackir-provider` | `6776d20544` |
| `file-manifest` | `4953206a26` |
| `audio-native-contract` | `d0fea5bc79` → `25f7fff28d` → `681f337c3f` |
| `x64-projects` | `cbfa4dca3e` |
| `obsolete-client-inputs` | `94a81438c4` → `d36090a8ce` → `4d4d03aac3` |
| `native-providers` | `5fe9314e00` → `10e684ba73` → `085f77cc73` → `0d2f8c1681` → `13c15b6d0e` → `3a487593a4` → `49d0eeed4d` → `f5acb69bb3` |
| `link-stack-policy` | `a21af16302` → `dd32e5dcc3` |
| `miles-session-core` | `9b3154d3be` → `c093035b7d` → `4f15b029a8` → `6bd957fcfd` → `49ab54a9c0` → `60b719bc5d` → `5252ff6e5c` → `5c31706581` → `892343c92b` → `d1c5903de3` → `b9d3408f1c` |
| `miles-game-selection` | `b41abddac0` → `967076aae9` → `0458501d2f` → `36ddb90678` → `e36c7f67a2` → `a68ceb4280` |
| `bink-host-session` | `3636d63fe3` → `ed84ba12a2` → `a904e489b4` → `da9c56054b` |
| `bink-game-selection` | `81cee3f524` → `afacd961f7` |
| `media-release-build` | `33efad1603` |

Full SHAs, subjects, precise branch heads and package-specific boundaries are in JSON. The HTTP original-header package is now at `003f8757c7c1386e33c997be7d5bf5b8109669d4`, independent of imemmove; root publication is in progress. Its WIP genuine-TU extension is excluded. Server networking is outside this client diff; the parent separately reports joint PR37/38 base `09932a32`, head `9d44e3a1`, including its +9 header prerequisite.

## All production files

Full paths are repository-relative. `Components` lists all package hunks present; the single owner is used for totals. Exact origins and blob IDs are in JSON.

| Path | Accounting owner | Components | +/− |
|---|---|---|---:|
| `src/engine/client/application/Direct3d9/src/shared/MemoryManagerHook.cpp` | `allocator-address-stack` | `allocator-address-stack` | +37/−0 |
| `src/engine/client/application/Direct3d9/src/win32/Direct3d9.h` | `native-providers` | `native-providers` | +8/−0 |
| `src/engine/client/application/Direct3d9/src/win32/Direct3d9_VertexShaderData.cpp` | `native-providers` | `native-providers` | +6/−1 |
| `src/engine/client/application/DllExport/src/win32/DllExport.cpp` | `allocator-address-stack` | `allocator-address-stack` | +93/−92 |
| `src/engine/client/application/Headless/src/shared/MemoryManagerHook.cpp` | `allocator-address-stack` | `allocator-address-stack` | +37/−0 |
| `src/engine/client/application/MayaExporter/src/win32/ExportStaticMesh.cpp` | `allocator-sizes` | `allocator-sizes` | +2/−1 |
| `src/engine/client/application/Viewer/src/win32/ViewerDoc.cpp` | `allocator-sizes` | `allocator-sizes` | +4/−3 |
| `src/engine/client/library/clientAudio/src/win32/Audio.cpp` | `miles-game-selection` | `audio-native-contract`, `miles-session-core`, `miles-game-selection` | +225/−77 |
| `src/engine/client/library/clientAudio/src/win32/AudioFileCallbacks.h` | `miles-session-core` | `miles-session-core` | +20/−0 |
| `src/engine/client/library/clientAudio/src/win32/SetupClientAudio.cpp` | `miles-game-selection` | `miles-game-selection` | +10/−0 |
| `src/engine/client/library/clientAudio/src/win32/SoundObject3d.cpp` | `miles-game-selection` | `miles-game-selection` | +4/−0 |
| `src/engine/client/library/clientGame/src/shared/HTTPpost/TCPQueue.cpp` | `imemmove` | `imemmove` | +2/−2 |
| `src/engine/client/library/clientGame/src/shared/HTTPpost/VeCritsec.hpp` | `http-lock` | `http-lock` | +17/−0 |
| `src/engine/client/library/clientGame/src/shared/core/ClientHeadTracking.cpp` | `trackir-provider` | `trackir-provider` | +12/−3 |
| `src/engine/client/library/clientGame/src/shared/core/Game.cpp` | `allocator-sizes` | `allocator-sizes` | +10/−9 |
| `src/engine/client/library/clientGame/src/shared/core/PlotterManager.cpp` | `allocator-sizes` | `allocator-sizes` | +2/−2 |
| `src/engine/client/library/clientGame/src/shared/object/CreatureObject.cpp` | `archive-callbacks` | `archive-callbacks` | +1/−1 |
| `src/engine/client/library/clientGame/src/shared/object/CreatureObject.h` | `archive-callbacks` | `archive-callbacks` | +2/−1 |
| `src/engine/client/library/clientGame/src/shared/object/GroupObject.cpp` | `archive-callbacks` | `archive-callbacks` | +4/−4 |
| `src/engine/client/library/clientGame/src/shared/object/GroupObject.h` | `archive-callbacks` | `archive-callbacks` | +5/−4 |
| `src/engine/client/library/clientGraphics/src/Bink/BinkVideo.cpp` | `bink-game-selection` | `bink-game-selection` | +12/−215 |
| `src/engine/client/library/clientGraphics/src/Bink/PipeBinkVideo.cpp` | `bink-game-selection` | `bink-game-selection` | +168/−0 |
| `src/engine/client/library/clientGraphics/src/Bink/PipeBinkVideo.h` | `bink-game-selection` | `bink-game-selection` | +51/−0 |
| `src/engine/client/library/clientGraphics/src/Bink/VideoBlit.cpp` | `bink-game-selection` | `bink-game-selection` | +215/−0 |
| `src/engine/client/library/clientGraphics/src/Bink/VideoBlit.h` | `bink-game-selection` | `bink-game-selection` | +12/−0 |
| `src/engine/client/library/clientGraphics/src/shared/RenderWorld.cpp` | `allocator-address-stack` | `allocator-address-stack` | +2/−2 |
| `src/engine/client/library/clientGraphics/src/shared/RenderWorldServices.cpp` | `allocator-address-stack` | `allocator-address-stack` | +12/−0 |
| `src/engine/client/library/clientGraphics/src/shared/VideoList.cpp` | `bink-game-selection` | `bink-game-selection` | +16/−0 |
| `src/engine/client/library/clientSkeletalAnimation/src/shared/appearance/MeshConstructionHelper.cpp` | `ui-native-widths` | `ui-native-widths` | +5/−5 |
| `src/engine/client/library/clientSkeletalAnimation/src/shared/appearance/SkeletalAppearance2.cpp` | `allocator-sizes` | `allocator-sizes` | +15/−14 |
| `src/engine/client/library/clientSkeletalAnimation/src/shared/appearance/SoftwareBlendSkeletalShaderPrimitive.cpp` | `skeletal-kernel` | `skeletal-kernel` | +97/−0 |
| `src/engine/client/library/clientSkeletalAnimation/src/shared/controller/LogicalAnimationTableTemplateList.cpp` | `allocator-sizes` | `allocator-sizes` | +3/−3 |
| `src/engine/client/library/clientUserInterface/src/shared/core/CuiChatFormatter.cpp` | `ui-native-widths` | `ui-native-widths` | +1/−1 |
| `src/engine/client/library/clientUserInterface/src/shared/core/CuiCombatManager.cpp` | `ui-native-widths` | `ui-native-widths` | +1/−1 |
| `src/engine/client/library/clientUserInterface/src/shared/core/CuiIoWin.cpp` | `obsolete-client-inputs` | `obsolete-client-inputs` | +0/−5 |
| `src/engine/shared/library/sharedCollision/src/shared/core/CollisionUtils.cpp` | `math-kernels` | `math-kernels` | +7/−0 |
| `src/engine/shared/library/sharedCollision/src/shared/core/CollisionWorld.cpp` | `fpu-controls` | `fpu-controls` | +2/−2 |
| `src/engine/shared/library/sharedDatabaseInterface/src_oci/OciSession.cpp` | `allocator-sizes` | `allocator-sizes` | +3/−0 |
| `src/engine/shared/library/sharedDebug/src/shared/CallStack.cpp` | `allocator-address-stack` | `allocator-address-stack` | +4/−4 |
| `src/engine/shared/library/sharedDebug/src/shared/CallStack.h` | `allocator-address-stack` | `allocator-address-stack` | +1/−1 |
| `src/engine/shared/library/sharedDebug/src/shared/CallStackCollector.cpp` | `allocator-address-stack` | `allocator-address-stack` | +9/−9 |
| `src/engine/shared/library/sharedDebug/src/shared/InstallTimer.cpp` | `allocator-sizes` | `allocator-sizes` | +3/−2 |
| `src/engine/shared/library/sharedDebug/src/shared/InstallTimer.h` | `allocator-sizes` | `allocator-sizes` | +2/−1 |
| `src/engine/shared/library/sharedDebug/src/win32/DebugHelp.cpp` | `allocator-address-stack` | `allocator-address-stack` | +55/−11 |
| `src/engine/shared/library/sharedDebug/src/win32/DebugHelp.h` | `allocator-address-stack` | `allocator-address-stack` | +3/−3 |
| `src/engine/shared/library/sharedDebug/src/win32/ProfilerTimer.cpp` | `platform-diagnostics` | `platform-diagnostics` | +10/−0 |
| `src/engine/shared/library/sharedFile/src/shared/FileManifest.cpp` | `file-manifest` | `file-manifest` | +2/−2 |
| `src/engine/shared/library/sharedFile/src/shared/Iff.cpp` | `imemmove` | `imemmove` | +2/−2 |
| `src/engine/shared/library/sharedFoundation/src/shared/AutoDeltaNetworkIdPackedMap.h` | `wire-contract` | `wire-contract` | +3/−3 |
| `src/engine/shared/library/sharedFoundation/src/shared/Fatal.cpp` | `allocator-address-stack` | `allocator-address-stack` | +11/−3 |
| `src/engine/shared/library/sharedFoundation/src/shared/Md5.cpp` | `imemmove` | `imemmove` | +1/−1 |
| `src/engine/shared/library/sharedFoundation/src/shared/Misc.h` | `imemmove` | `imemmove` | +2/−2 |
| `src/engine/shared/library/sharedFoundation/src/shared/Tag.h` | `ui-native-widths` | `ui-native-widths` | +2/−2 |
| `src/engine/shared/library/sharedFoundation/src/win32/ByteOrder.cpp` | `byteorder` | `byteorder` | +26/−0 |
| `src/engine/shared/library/sharedFoundation/src/win32/FloatingPointUnit.cpp` | `fpu-controls` | `fpu-controls` | +45/−0 |
| `src/engine/shared/library/sharedFoundation/src/win32/FloatingPointUnit.h` | `fpu-controls` | `fpu-controls` | +8/−0 |
| `src/engine/shared/library/sharedFoundation/src/win32/Os.cpp` | `platform-diagnostics` | `platform-diagnostics`, `shell-results` | +2/−2 |
| `src/engine/shared/library/sharedFoundation/src/win32/SetupSharedFoundation.cpp` | `platform-diagnostics` | `platform-diagnostics` | +1/−1 |
| `src/engine/shared/library/sharedGame/src/shared/quest/PlayerQuestData.cpp` | `wire-contract` | `wire-contract` | +3/−3 |
| `src/engine/shared/library/sharedMath/src/shared/Transform.cpp` | `math-kernels` | `math-kernels` | +27/−0 |
| `src/engine/shared/library/sharedMath/src/win32/SseMath.cpp` | `math-kernels` | `math-kernels` | +194/−0 |
| `src/engine/shared/library/sharedMath/src/win32/SseMath.h` | `math-kernels` | `math-kernels` | +7/−1 |
| `src/engine/shared/library/sharedMemoryManager/src/shared/MemoryManager.cpp` | `allocator-sizes` | `allocator-layout`, `allocator-address-stack`, `allocator-sizes` | +117/−72 |
| `src/engine/shared/library/sharedMemoryManager/src/shared/MemoryManager.h` | `allocator-sizes` | `allocator-address-stack`, `allocator-sizes` | +18/−4 |
| `src/engine/shared/library/sharedMemoryManager/src/win32/OsNewDel.cpp` | `allocator-address-stack` | `allocator-address-stack` | +38/−0 |
| `src/engine/shared/library/sharedNetwork/src/win32/Sock.h` | `network-widths` | `network-widths` | +3/−2 |
| `src/engine/shared/library/sharedNetwork/src/win32/TcpClient.cpp` | `network-widths` | `network-widths` | +1/−1 |
| `src/engine/shared/library/sharedNetwork/src/win32/TcpServer.cpp` | `network-widths` | `network-widths` | +1/−1 |
| `src/engine/shared/library/sharedNetworkMessages/include/public/sharedNetworkMessages/NetworkMessageTimestamp.h` | `wire-contract` | `wire-contract` | +1/−0 |
| `src/engine/shared/library/sharedNetworkMessages/src/shared/NetworkMessageTimestamp.h` | `wire-contract` | `wire-contract` | +22/−0 |
| `src/engine/shared/library/sharedNetworkMessages/src/shared/chat/ChatOnRequestLog.h` | `wire-contract` | `wire-contract` | +3/−2 |
| `src/engine/shared/library/sharedNetworkMessages/src/shared/clientGameServer/BuffBuilderChangeMessage.cpp` | `wire-contract` | `wire-contract` | +6/−4 |
| `src/engine/shared/library/sharedNetworkMessages/src/shared/clientGameServer/BuffBuilderChangeMessage.h` | `wire-contract` | `wire-contract` | +5/−4 |
| `src/engine/shared/library/sharedNetworkMessages/src/shared/clientGameServer/DroidCommandProgrammingMessage.cpp` | `wire-contract` | `wire-contract` | +10/−8 |
| `src/engine/shared/library/sharedNetworkMessages/src/shared/clientGameServer/ImageDesignChangeMessage.cpp` | `wire-contract` | `wire-contract` | +9/−7 |
| `src/engine/shared/library/sharedNetworkMessages/src/shared/clientGameServer/ImageDesignChangeMessage.h` | `wire-contract` | `wire-contract` | +5/−4 |
| `src/engine/shared/library/sharedNetworkMessages/src/shared/clientGameServer/MessageQueueCraftExperiment.cpp` | `wire-contract` | `wire-contract` | +4/−3 |
| `src/engine/shared/library/sharedNetworkMessages/src/shared/clientGameServer/MessageQueueDraftSlotsDataArchive.cpp` | `wire-contract` | `wire-contract` | +3/−2 |
| `src/engine/shared/library/sharedNetworkMessages/src/shared/clientGameServer/MessageQueueMissionListResponseArchive.cpp` | `wire-contract` | `wire-contract` | +4/−2 |
| `src/engine/shared/library/sharedNetworkMessages/src/shared/customerService/CustomerServiceCategoryArchive.cpp` | `wire-contract` | `wire-contract` | +3/−2 |
| `src/engine/shared/library/sharedRegex/src/win32/RegexServices.cpp` | `allocator-address-stack` | `allocator-address-stack` | +12/−0 |
| `src/engine/shared/library/sharedStatusWindow/src/win32/StatusWindow.cpp` | `platform-diagnostics` | `platform-diagnostics` | +2/−2 |
| `src/engine/shared/library/sharedUtility/src/shared/CachedFileManager.cpp` | `allocator-sizes` | `allocator-sizes` | +3/−3 |
| `src/engine/shared/library/sharedUtility/src/shared/NetworkIdAutoDeltaPackedMap.cpp` | `wire-contract` | `wire-contract` | +3/−3 |
| `src/engine/shared/library/sharedXml/src/shared/core/SetupSharedXml.cpp` | `allocator-sizes` | `allocator-sizes` | +3/−0 |
| `src/engine/shared/library/sharedXml/src/shared/tree/XmlTreeDocumentList.cpp` | `allocator-sizes` | `allocator-sizes` | +4/−3 |
| `src/external/3rd/library/dpvs/implementation/include/dpvsPrivateDefs.hpp` | `dpvs` | `dpvs` | +13/−1 |
| `src/external/3rd/library/dpvs/implementation/include/dpvsSystem.hpp` | `dpvs` | `dpvs` | +9/−1 |
| `src/external/3rd/library/dpvs/implementation/sources/dpvsImpObject.cpp` | `dpvs` | `dpvs` | +1/−1 |
| `src/external/3rd/library/dpvs/implementation/sources/dpvsMath.cpp` | `dpvs` | `dpvs` | +12/−1 |
| `src/external/3rd/library/soePlatform/VChatAPI/utils2.0/utils/UdpLibrary/UdpLibrary.hpp` | `network-widths` | `network-widths` | +2/−1 |
| `src/external/3rd/library/stlport453/src/stlport_prefix.h` | `stlport-sdk` | `stlport-sdk` | +10/−0 |
| `src/external/3rd/library/udplibrary/UdpLibrary.hpp` | `network-widths` | `network-widths` | +2/−1 |
| `src/external/3rd/library/ui/src/shared/core/UiMemoryBlockManager.cpp` | `ui-pool` | `ui-pool` | +1/−1 |
| `src/external/3rd/library/ui/src/win32/UILoader.cpp` | `ui-native-widths` | `ui-native-widths` | +1/−1 |
| `src/external/3rd/library/ui/src/win32/UIOutputStream.cpp` | `ui-native-widths` | `ui-native-widths` | +1/−1 |
| `src/external/3rd/library/ui/src/win32/UITabbedPane.cpp` | `ui-native-widths` | `ui-native-widths` | +8/−0 |
| `src/external/ours/library/archive/include/Archive/ArchiveCount.h` | `wire-contract` | `wire-contract` | +1/−0 |
| `src/external/ours/library/archive/src/shared/Archive.h` | `archive-storage` | `wire-contract`, `archive-storage` | +20/−12 |
| `src/external/ours/library/archive/src/shared/ArchiveCount.h` | `wire-contract` | `wire-contract` | +23/−0 |
| `src/external/ours/library/archive/src/shared/AutoByteStream.h` | `archive-storage` | `archive-storage` | +2/−2 |
| `src/external/ours/library/archive/src/shared/AutoDeltaMap.h` | `wire-contract` | `wire-contract` | +11/−10 |
| `src/external/ours/library/archive/src/shared/AutoDeltaPackedMap.h` | `wire-contract` | `wire-contract` | +3/−3 |
| `src/external/ours/library/archive/src/shared/AutoDeltaQueue.h` | `wire-contract` | `wire-contract` | +6/−5 |
| `src/external/ours/library/archive/src/shared/AutoDeltaSet.h` | `wire-contract` | `wire-contract` | +10/−9 |
| `src/external/ours/library/archive/src/shared/AutoDeltaVector.h` | `wire-contract` | `wire-contract` | +11/−10 |
| `src/external/ours/library/archive/src/shared/ByteStream.cpp` | `archive-storage` | `archive-storage` | +63/−66 |
| `src/external/ours/library/archive/src/shared/ByteStream.h` | `archive-storage` | `archive-storage` | +22/−18 |
| `src/external/ours/library/crypto/src/shared/core/FirstCrypto.h` | `crypto-boundaries` | `crypto-boundaries` | +11/−0 |
| `src/external/ours/library/crypto/src/shared/original/cryptlib.cpp` | `crypto-boundaries` | `crypto-boundaries` | +1/−1 |
| `src/external/ours/library/crypto/src/shared/original/filters.h` | `crypto-boundaries` | `crypto-boundaries` | +9/−2 |
| `src/external/ours/library/crypto/src/shared/original/mqueue.h` | `crypto-boundaries` | `crypto-boundaries` | +7/−2 |
| `src/external/ours/library/unicodeArchive/src/shared/UnicodeArchive.cpp` | `archive-storage` | `wire-contract`, `archive-storage` | +20/−9 |
| `src/external/ours/library/unicodeArchive/src/shared/UnicodeAutoDeltaPackedMap.cpp` | `wire-contract` | `wire-contract` | +3/−3 |
| `src/game/client/application/SwgClient/src/win32/WinMain.cpp` | `shell-results` | `shell-results` | +2/−2 |
| `src/game/client/library/swgClientUserInterface/src/shared/page/SwgCuiDebugInfoPage.cpp` | `allocator-sizes` | `allocator-sizes` | +1/−1 |
| `src/game/client/library/swgClientUserInterface/src/shared/parser/SwgCuiCommandParserScene.cpp` | `pcre-capacity` | `pcre-capacity` | +1/−2 |
| `tools/miles-bridge/src/admission/coordinator.cpp` | `miles-session-core` | `miles-session-core`, `bink-host-session` | +156/−0 |
| `tools/miles-bridge/src/admission/coordinator.h` | `miles-session-core` | `miles-session-core` | +88/−0 |
| `tools/miles-bridge/src/api/ClientBink.h` | `bink-host-session` | `bink-host-session` | +30/−0 |
| `tools/miles-bridge/src/api/ClientMiles.h` | `miles-session-core` | `miles-session-core` | +180/−0 |
| `tools/miles-bridge/src/api/native/native_callbacks70.cpp` | `miles-session-core` | `miles-session-core` | +11/−0 |
| `tools/miles-bridge/src/api/native/native_calls60.cpp` | `miles-session-core` | `miles-session-core` | +276/−0 |
| `tools/miles-bridge/src/api/native/native_file_setter67.cpp` | `miles-session-core` | `miles-session-core` | +24/−0 |
| `tools/miles-bridge/src/api/native/native_startup_calls.cpp` | `miles-session-core` | `miles-session-core` | +55/−0 |
| `tools/miles-bridge/src/api/native/native_types70.h` | `miles-session-core` | `miles-session-core` | +12/−0 |
| `tools/miles-bridge/src/api/pipe/Channel.h` | `miles-session-core` | `miles-session-core` | +22/−0 |
| `tools/miles-bridge/src/api/pipe/ClientBinkPipe.cpp` | `bink-host-session` | `bink-host-session` | +137/−0 |
| `tools/miles-bridge/src/api/pipe/ClientMilesPipe.cpp` | `miles-session-core` | `miles-session-core` | +218/−0 |
| `tools/miles-bridge/src/api/pipe/LiveChannel.cpp` | `miles-session-core` | `miles-session-core`, `miles-game-selection` | +163/−0 |
| `tools/miles-bridge/src/api/pipe/LiveChannel.h` | `miles-session-core` | `miles-session-core` | +15/−0 |
| `tools/miles-bridge/src/api/pipe/PipeCore.cpp` | `miles-session-core` | `miles-session-core`, `bink-host-session` | +1006/−0 |
| `tools/miles-bridge/src/api/pipe/PipeCore.h` | `miles-session-core` | `miles-session-core` | +177/−0 |
| `tools/miles-bridge/src/api/pipe/ScopedSourceImage.h` | `miles-session-core` | `miles-session-core` | +23/−0 |
| `tools/miles-bridge/src/api/pipe/Session.h` | `miles-session-core` | `miles-session-core`, `bink-host-session` | +87/−0 |
| `tools/miles-bridge/src/api/pipe/VideoState.cpp` | `bink-host-session` | `bink-host-session` | +36/−0 |
| `tools/miles-bridge/src/api/pipe/VideoState.h` | `bink-host-session` | `bink-host-session` | +25/−0 |
| `tools/miles-bridge/src/api/plain_callbacks.cpp` | `miles-session-core` | `miles-session-core` | +26/−0 |
| `tools/miles-bridge/src/api/plain_file_setter.cpp` | `miles-session-core` | `miles-session-core` | +18/−0 |
| `tools/miles-bridge/src/api/plain_operations.cpp` | `miles-session-core` | `miles-session-core` | +266/−0 |
| `tools/miles-bridge/src/api/plain_startup.cpp` | `miles-session-core` | `miles-session-core` | +107/−0 |
| `tools/miles-bridge/src/api/private/failure_boundary.cpp` | `miles-session-core` | `miles-session-core` | +29/−0 |
| `tools/miles-bridge/src/api/private/failure_boundary.h` | `miles-session-core` | `miles-session-core` | +24/−0 |
| `tools/miles-bridge/src/api/private/native_callbacks70.h` | `miles-session-core` | `miles-session-core` | +8/−0 |
| `tools/miles-bridge/src/api/private/native_calls60.h` | `miles-session-core` | `miles-session-core` | +60/−0 |
| `tools/miles-bridge/src/api/private/native_file_setter67.h` | `miles-session-core` | `miles-session-core` | +8/−0 |
| `tools/miles-bridge/src/api/private/native_startup_calls.h` | `miles-session-core` | `miles-session-core` | +21/−0 |
| `tools/miles-bridge/src/audio-callbacks/ClientAudioFileCallbacks.h` | `miles-session-core` | `miles-session-core` | +50/−0 |
| `tools/miles-bridge/src/backend/backend.h` | `miles-session-core` | `miles-session-core`, `miles-game-selection`, `bink-host-session` | +411/−0 |
| `tools/miles-bridge/src/backend/reply.h` | `miles-session-core` | `miles-session-core`, `bink-host-session` | +144/−0 |
| `tools/miles-bridge/src/bink/bink_protocol.h` | `bink-host-session` | `bink-host-session` | +106/−0 |
| `tools/miles-bridge/src/bootstrap/common.h` | `miles-session-core` | `miles-session-core`, `miles-game-selection` | +112/−0 |
| `tools/miles-bridge/src/buffer/buffer_upload.cpp` | `miles-session-core` | `miles-session-core` | +27/−0 |
| `tools/miles-bridge/src/buffer/buffer_upload.h` | `miles-session-core` | `miles-session-core` | +26/−0 |
| `tools/miles-bridge/src/callback-guard/invocation_guard.cpp` | `miles-session-core` | `miles-session-core` | +27/−0 |
| `tools/miles-bridge/src/callback-guard/invocation_guard.h` | `miles-session-core` | `miles-session-core` | +23/−0 |
| `tools/miles-bridge/src/client-runtime/client_file_runtime.cpp` | `miles-session-core` | `miles-session-core` | +411/−0 |
| `tools/miles-bridge/src/client-runtime/client_file_runtime.h` | `miles-session-core` | `miles-session-core` | +55/−0 |
| `tools/miles-bridge/src/dev/AudioBootstrap.cpp` | `miles-game-selection` | `miles-game-selection` | +52/−0 |
| `tools/miles-bridge/src/dev/AudioBootstrap.h` | `miles-game-selection` | `miles-game-selection` | +14/−0 |
| `tools/miles-bridge/src/dev/AudioSelection.h` | `miles-session-core` | `miles-session-core` | +100/−0 |
| `tools/miles-bridge/src/dispatch/host_dispatch.cpp` | `miles-session-core` | `miles-session-core` | +337/−0 |
| `tools/miles-bridge/src/dispatch/host_dispatch.h` | `miles-session-core` | `miles-session-core` | +17/−0 |
| `tools/miles-bridge/src/dispatch/registry_resolver.h` | `miles-session-core` | `miles-session-core` | +21/−0 |
| `tools/miles-bridge/src/eos/client_eos.cpp` | `miles-session-core` | `miles-session-core` | +59/−0 |
| `tools/miles-bridge/src/eos/client_eos.h` | `miles-session-core` | `miles-session-core` | +31/−0 |
| `tools/miles-bridge/src/eos/eos_protocol.cpp` | `miles-session-core` | `miles-session-core` | +39/−0 |
| `tools/miles-bridge/src/eos/eos_protocol.h` | `miles-session-core` | `miles-session-core` | +11/−0 |
| `tools/miles-bridge/src/eos/host_eos.cpp` | `miles-session-core` | `miles-session-core` | +70/−0 |
| `tools/miles-bridge/src/eos/host_eos.h` | `miles-session-core` | `miles-session-core` | +13/−0 |
| `tools/miles-bridge/src/failure/failure_boundary.cpp` | `miles-session-core` | `miles-session-core` | +29/−0 |
| `tools/miles-bridge/src/failure/failure_boundary.h` | `miles-session-core` | `miles-session-core` | +24/−0 |
| `tools/miles-bridge/src/file-callbacks/ClientMilesFileCallbacks.h` | `miles-session-core` | `miles-session-core` | +6/−0 |
| `tools/miles-bridge/src/file-channel/file_channel.cpp` | `miles-session-core` | `miles-session-core` | +308/−0 |
| `tools/miles-bridge/src/file-channel/file_channel.h` | `miles-session-core` | `miles-session-core` | +130/−0 |
| `tools/miles-bridge/src/file-control/host_association_mapper.cpp` | `miles-session-core` | `miles-session-core` | +170/−0 |
| `tools/miles-bridge/src/file-control/host_association_mapper.h` | `miles-session-core` | `miles-session-core` | +74/−0 |
| `tools/miles-bridge/src/file-executor/EngineFileWorker.cpp` | `miles-session-core` | `miles-session-core` | +169/−0 |
| `tools/miles-bridge/src/file-executor/EngineFileWorker.h` | `miles-session-core` | `miles-session-core` | +38/−0 |
| `tools/miles-bridge/src/file-executor/FileInvocationJob.cpp` | `miles-session-core` | `miles-session-core` | +83/−0 |
| `tools/miles-bridge/src/file-executor/FileInvocationJob.h` | `miles-session-core` | `miles-session-core` | +39/−0 |
| `tools/miles-bridge/src/file-owner/session_file_owner.cpp` | `miles-session-core` | `miles-session-core` | +152/−0 |
| `tools/miles-bridge/src/file-owner/session_file_owner.h` | `miles-session-core` | `miles-session-core` | +64/−0 |
| `tools/miles-bridge/src/file-protocol/file_protocol.cpp` | `miles-session-core` | `miles-session-core` | +89/−0 |
| `tools/miles-bridge/src/file-protocol/file_protocol.h` | `miles-session-core` | `miles-session-core` | +46/−0 |
| `tools/miles-bridge/src/file-replies/file_tokens.cpp` | `miles-session-core` | `miles-session-core` | +60/−0 |
| `tools/miles-bridge/src/file-replies/file_tokens.h` | `miles-session-core` | `miles-session-core` | +45/−0 |
| `tools/miles-bridge/src/file-replies/reply_transaction.cpp` | `miles-session-core` | `miles-session-core` | +79/−0 |
| `tools/miles-bridge/src/file-replies/reply_transaction.h` | `miles-session-core` | `miles-session-core` | +37/−0 |
| `tools/miles-bridge/src/file-services/selected_services.cpp` | `miles-session-core` | `miles-session-core` | +51/−0 |
| `tools/miles-bridge/src/file-services/selected_services.h` | `miles-session-core` | `miles-session-core` | +16/−0 |
| `tools/miles-bridge/src/host-bink/bink_file_io.cpp` | `bink-host-session` | `bink-host-session` | +479/−0 |
| `tools/miles-bridge/src/host-bink/bink_file_io.h` | `bink-host-session` | `bink-host-session` | +12/−0 |
| `tools/miles-bridge/src/host-bink/bink_owner.cpp` | `bink-host-session` | `bink-host-session` | +149/−0 |
| `tools/miles-bridge/src/host-bink/bink_owner.h` | `bink-host-session` | `bink-host-session` | +73/−0 |
| `tools/miles-bridge/src/host-bink/bink_service.cpp` | `bink-host-session` | `bink-host-session` | +135/−0 |
| `tools/miles-bridge/src/host-bink/bink_service.h` | `bink-host-session` | `bink-host-session` | +31/−0 |
| `tools/miles-bridge/src/host-context/call_context.cpp` | `miles-session-core` | `miles-session-core` | +30/−0 |
| `tools/miles-bridge/src/host-context/call_context.h` | `miles-session-core` | `miles-session-core` | +26/−0 |
| `tools/miles-bridge/src/host-runtime/host_file_runtime.cpp` | `miles-session-core` | `miles-session-core` | +192/−0 |
| `tools/miles-bridge/src/host-runtime/host_file_runtime.h` | `miles-session-core` | `miles-session-core` | +51/−0 |
| `tools/miles-bridge/src/host-runtime/host_install.cpp` | `miles-session-core` | `miles-session-core` | +28/−0 |
| `tools/miles-bridge/src/host-runtime/host_sdk_callbacks.cpp` | `miles-session-core` | `miles-session-core` | +56/−0 |
| `tools/miles-bridge/src/host/host.cpp` | `miles-session-core` | `miles-session-core`, `miles-game-selection`, `bink-host-session` | +141/−0 |
| `tools/miles-bridge/src/image/upload_policy.h` | `miles-session-core` | `miles-session-core` | +27/−0 |
| `tools/miles-bridge/src/metadata/metadata.h` | `miles-session-core` | `miles-session-core` | +37/−0 |
| `tools/miles-bridge/src/metadata/metadata_host.cpp` | `miles-session-core` | `miles-session-core` | +43/−0 |
| `tools/miles-bridge/src/metadata/metadata_wire.cpp` | `miles-session-core` | `miles-session-core` | +57/−0 |
| `tools/miles-bridge/src/protocol/miles_wire.h` | `miles-session-core` | `miles-session-core`, `bink-host-session` | +111/−0 |
| `tools/miles-bridge/src/protocol/pair_outputs.h` | `miles-session-core` | `miles-session-core` | +22/−0 |
| `tools/miles-bridge/src/transport/endpoint.cpp` | `miles-session-core` | `miles-session-core` | +118/−0 |
| `tools/miles-bridge/src/transport/endpoint.h` | `miles-session-core` | `miles-session-core` | +59/−0 |
| `tools/miles-bridge/src/upload/upload_state.h` | `miles-session-core` | `miles-session-core` | +189/−0 |
| `tools/miles-bridge/src/version/session_version.cpp` | `miles-session-core` | `miles-session-core` | +27/−0 |
| `tools/miles-bridge/src/version/session_version.h` | `miles-session-core` | `miles-session-core` | +12/−0 |
| `tools/miles-bridge/src/version/session_version_host.cpp` | `miles-session-core` | `miles-session-core` | +39/−0 |
| `tools/miles-bridge/src/version/session_version_host.h` | `miles-session-core` | `miles-session-core` | +9/−0 |
| `tools/miles-bridge/src/wire/codec.cpp` | `miles-session-core` | `miles-session-core`, `bink-host-session` | +267/−0 |
| `tools/miles-bridge/src/wire/codec.h` | `miles-session-core` | `miles-session-core` | +26/−0 |
| `tools/miles-bridge/src/wire/resource_registry.h` | `miles-session-core` | `miles-session-core`, `bink-host-session` | +233/−0 |

## Build-property files with mixed ownership

| Path | Accounting owner | Components |
|---|---|---|
| `src/build/win32/swg.sln` | `x64-projects` | `x64-projects`, `obsolete-client-inputs` |
| `src/engine/client/application/Direct3d9/build/win32/Direct3d9.vcxproj` | `x64-projects` | `x64-projects`, `native-providers` |
| `src/engine/client/application/Direct3d9/build/win32/Direct3d9_ffp.vcxproj` | `x64-projects` | `x64-projects`, `native-providers` |
| `src/engine/client/application/Direct3d9/build/win32/Direct3d9_vsps.vcxproj` | `x64-projects` | `x64-projects`, `native-providers` |
| `src/engine/client/library/clientAudio/build/win32/clientAudio.vcxproj` | `x64-projects` | `x64-projects`, `miles-session-core` |
| `src/engine/client/library/clientGraphics/build/win32/clientGraphics.vcxproj` | `x64-projects` | `x64-projects`, `bink-game-selection`, `media-release-build` |
| `src/engine/shared/library/sharedNetworkMessages/build/win32/sharedNetworkMessages.vcxproj` | `x64-projects` | `wire-contract`, `x64-projects` |
| `src/external/ours/library/archive/build/win32/archive.vcxproj` | `x64-projects` | `wire-contract`, `x64-projects` |
| `src/game/client/application/SwgClient/build/win32/SwgClient.vcxproj` | `x64-projects` | `link-cleanup`, `x64-projects`, `obsolete-client-inputs` |
| `tools/configure-client-x64/client-x64.props` | `native-providers` | `x64-projects`, `native-providers`, `link-stack-policy`, `miles-game-selection` |
| `tools/miles-bridge/build.py` | `miles-game-selection` | `miles-session-core`, `miles-game-selection`, `bink-host-session`, `media-release-build` |
| `tools/miles-bridge/client-miles-dev.props` | `miles-game-selection` | `miles-game-selection`, `bink-game-selection`, `media-release-build` |
| `tools/miles-bridge/sources.json` | `miles-game-selection` | `miles-session-core`, `miles-game-selection`, `bink-host-session` |

## Evidence and inspection boundary

Current scope/status: `CLIENT-X64-GOAL.md`, `CURRENT-STATUS.md`; prior package notes: `pr-submissions/NEXT-PACKAGES.md`, current submission bodies/receipts and `ci-followup/ledger.md`. Older notes that still say the full client is unfinished are historical evidence boundaries, not a new work queue. The maintained build/tests remain the accepted baseline.

Existing published/prepared sources were compared to the frozen implementation. Most are exact; wire storage files, Os.cpp and MemoryManager.cpp contain explicitly assigned later components. PCRE differs only in trailing newline preservation. No differences were converted into fresh test-pass claims.

The map checks Git/path/hash accounting only. No builds, test execution, product changes, source-tree copies, public writes, or new broad acceptance requests were made. A new package must describe inherited integrated observations at their actual input identities; this inventory does not manufacture exact-branch results.
