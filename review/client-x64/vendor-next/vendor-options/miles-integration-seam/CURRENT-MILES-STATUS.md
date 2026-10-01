# Maintained Miles/Bink status

Updated 2026-10-01. The maintained implementation is [`eca74ffa5741f608a1417944b2e2602868936517`](https://github.com/Akilleez-QA/client-tools/tree/eca74ffa5741f608a1417944b2e2602868936517/tools/miles-bridge), published on `implementation/client-miles` and `integration/client-x64-next`. It has progressed beyond the old unlinked prototype: recorded x64 game builds and bounded original-provider audio/movie sessions exist. [Overall status and evidence limits](../../../FORK-STATUS.md).

## Replacement boundary

The temporary backend keeps the original x86 Miles engine and Bink decoder in a separate process. Game-facing audio uses the selected SDK's native handle/callback types through `ClientMiles`; process transport, private identities and callback machinery remain behind that interface. A future licensed native x64 backend can replace the transport implementation at this boundary. Source-level native adapters exist, but no licensed native x64 Miles runtime has been linked or qualified.

Bink uses `ClientBink` to carry original decoding through the same media host while retaining the game's renderer and controls. The opt-in development integration, provider prerequisites and build commands are in the [maintained README](https://github.com/Akilleez-QA/client-tools/blob/eca74ffa5741f608a1417944b2e2602868936517/tools/miles-bridge/README.md). Default legacy builds and the opt-in x64 composition are distinct; successful component tests alone do not establish a game run.

## Upstream packages

| Responsibility | Client PRs |
|---|---|
| Private contracts and native facade | [#41](https://github.com/SWG-Source/client-tools/pull/41), [#47](https://github.com/SWG-Source/client-tools/pull/47) |
| File transactions, callbacks, host and pipe/session | [#48](https://github.com/SWG-Source/client-tools/pull/48), [#49](https://github.com/SWG-Source/client-tools/pull/49), [#50](https://github.com/SWG-Source/client-tools/pull/50), [#51](https://github.com/SWG-Source/client-tools/pull/51) |
| Component builds, guarded Audio handoff and game selection | [#55](https://github.com/SWG-Source/client-tools/pull/55), [#63](https://github.com/SWG-Source/client-tools/pull/63) |
| Bink host, renderer adapter and Release components | [#64](https://github.com/SWG-Source/client-tools/pull/64), [#65](https://github.com/SWG-Source/client-tools/pull/65), [#66](https://github.com/SWG-Source/client-tools/pull/66) |
| Composed protocol regressions | [#67](https://github.com/SWG-Source/client-tools/pull/67) |

The [full index](../../../REVIEW-INDEX.md) names prerequisite branches and exact submitted heads. These are separate package trees, not all the same maintained implementation SHA.

## What has been observed

The [movie replay procedure](https://github.com/Akilleez-QA/client-tools/blob/eca74ffa5741f608a1417944b2e2602868936517/tools/miles-bridge/tests/bink-replay.md) and [live-session record](https://github.com/Akilleez-QA/client-tools/blob/eca74ffa5741f608a1417944b2e2602868936517/tools/test-wire-compatibility/live-session.md) retain original-provider runs, source/binary identities, warnings and cleanup limits. Recorded Debug-x64 Proton runs played two original Falcon movies, then closed during a third; the Win32 reference followed the same procedure. Bounded ground-scene login/movement/persistence and ordinary-close observations are recorded separately for the client/server architecture combinations.

The final submitted CI composition passed 298 EOS, 1,047 Bink protocol and 22 video-admission sanitizer assertions in [fork run 36903954547](https://github.com/Akilleez-QA/client-tools/actions/runs/36903954547). Those synthetic component checks are distinct from actual-provider runtime observations.

These results do not establish waveform/pixel/timing equality, arbitrary movie sizes, all failure/lifetime paths, native Windows GPU behavior or representative gameplay. Matching the original provider implementation does not by itself prove 100% fidelity across the new process boundary. The original failed allocator/Audio teardown workload remains historical; later game close observations do not make that failed workload pass.

Use the [maintained source index](RUNTIME-SOURCE-INDEX.md) for code. The [old prototype status](STATUS-historical-prototype.md) remains available with its original failures, counts and scope.
