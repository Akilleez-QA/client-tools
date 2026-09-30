# Maintainer concern: original-vendor process boundary

The user supplied community feedback questioning the complexity of a separate32-bit original-vendor host. This is a maintainability concern to assess, not a technical validation or authorization to post messages. No response was sent to the community. This note records our technical disposition without reproducing that conversation.

The concern is credible. Keeping original vendor code does not preserve every property of its use: IPC changes scheduling and ownership, synchronous return timing, callback/reentry, virtual file access, cleanup and diagnostics. The existing prototype already exposes these obligations. Small class names or fewer changed game lines would not make those costs disappear.

## Disposition

Keep the bridge experimental. Do not fold it into the small independently useful client patches, claim original-DLL identity proves complete fidelity, or ask upstream to accept a generalized RPC system. Continue bounded implementation and falsifying tests under the existing architecture decision. The completed client remains the goal, while no production media choice is established by the screenshot or the prototype.

The preferred simpler route remains a matching, usable native x64 original SDK/source and plugins, if legitimately available. The user reports none available. A different native engine removes IPC but introduces mixer/decoder/effect/behavior replacement; it is not presumed equivalent. Moving all clientAudio into the helper avoids some low-level callbacks but crosses Object/Appearance lifetime, shared Random, TreeFile, template and game-callback boundaries documented in ../../audio-next/whole-subsystem-rival-audit.md. Those alternatives remain open.

## Evidence required to justify this design

1. A small, typed game-facing surface with one session owner and explicitly bounded responsibilities; no duplicate scheduler/lifetime authority hidden in wrappers.
2. A clean original-engine reference lifecycle. The retained Audio/Sound2d teardown failure is unresolved; source/symbol analysis has not identified its original free owner. Do not rerun the prohibited fixture or describe it as repaired.
3. Actual game callback, file-I/O, Bink shared-driver and shutdown behavior, including ordering and reentry. Component compile, metadata, codec and no-playback checks cannot substitute.
4. Measured command/callback latency and jitter under relevant load, with differences preserved. No latency or perceptual tolerance has been accepted on the user's behalf.
5. Reproducible packaging and failure diagnostics, then representative full-client scene/media acceptance. Original mixer/codec binaries establish implementation identity only.

Current next steps remain bounded: repair metadata input ownership and its discriminating tests; compile the original-file-callback adapter against actual Windows Audio.cpp; implement the genuine DLL-resource version query. These do not authorize production adoption or new upstream PRs.
