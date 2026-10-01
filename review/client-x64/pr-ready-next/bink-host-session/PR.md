# Carry original Bink decoding through the existing media host

Add a genuine Bink owner and reverse TreeFile adapter to the x86 Miles host, using its local digital driver. Extend the paired session with driver-owned video resources, native controls, metadata and bounded pixel transfer. The game-side renderer adapter is a separate dependent package.

Keep both required repairs in this unit: admit Video resources through the real coordinator, and reapply Bink's consumed IO callback/buffer settings before every open so repeated playback retains TreeFile access.

Base: `78428d8c3f63048bccca579421f170a627be8fda` (`review-ready/client-miles-game-selection`), including its explicit Miles/x64-provider/FileManifest prerequisites. Production: 20 files, +1274/-21; build entrypoints: 2 files, +14/-2; tests/procedure: 4 files, +300; README: +28/-1 (Myers). Four source/build/test commits preserve the selected original changes, followed by scoped component documentation.

The host requires genuine Bink 1.9c headers and the matching privately supplied x86 DLL. No SDK binaries, vendor implementation or movie assets are included. Private protocol version 4 requires matching client/host builds; it does not change the SWG network protocol.

Existing integrated evidence is preserved at the [original checkpoint](https://github.com/Akilleez-QA/client-tools/blob/da9c56054b70761b983b4b367fd4479ac344e8e6/tools/miles-bridge/README.md) and [replay regression](https://github.com/Akilleez-QA/client-tools/blob/da9c56054b70761b983b4b367fd4479ac344e8e6/tools/miles-bridge/tests/bink-replay.md). Included portable tests cover protocol/reply/admission logic; they were not rerun for packaging and CI wiring is deferred. Exact selected-change and whitespace checks passed. Historical full-game results are not exact-base build/runtime results for this split branch. The actual-client replay procedure requires the later renderer package and complete client build dependencies.
