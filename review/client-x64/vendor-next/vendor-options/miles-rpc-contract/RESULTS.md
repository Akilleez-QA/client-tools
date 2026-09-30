# Bounded original Miles request/reply contract

2026-09-30. Eight final runs completed: two direct and two x64-controlled runs for each original sample/stream path. One tiny existing204ms WAV and unchanged original32-bit Miles DLL. No backend selected, no production changes, no game startup, no media/binary publication.

## Observed contract

Each run completes66 identical numbered commands, one EOS notification,133 serialized host log records and exactly one release. Requests are fixed24-byte v1 records; replies40bytes, field widths statically asserted. The x64 controller receives synchronous real status/position results from the x86 host; vendor pointers stay in the host. RELEASE advances opaque slot1 generation1→2; subsequent status with generation1 is rejected with diagnosticSTALE before a Miles call. This tests one slot and one stale-generation path, not resource reuse/scaling or arbitrary invalid packets.

All sampled status/position sequences are exactly equal between paired direct/controlled runs, with no value normalization. Samples first return DONE on request10; streams on19. Their following position returns204/204ms. Every last position is204/204. This equality is finite sampled data, not continuous playhead equality.

| Variant | EOS host context/sequence | Delivered during request | EOS→delivery observation ms |
|---|---|---|---|
| direct sample1/2 |9/17,9/17 |9,9 |0.0080,0.0029 |
| controlled sample1/2 |8/16,8/16 |9,9 |0.9089,0.9750 |
| direct stream1/2 |17/34,17/34 |18,18 |19.9816,20.4758 |
| controlled stream1/2 |17/34,17/34 |18,18 |21.8180,22.3213 |

Host context means last/current dispatched request, not a causal claim. Callbacks may occur between commands. Callback records contain native thread,QPC,x87 control/status,MXCSR. The first direct sample callback is foreign-thread; the second is main-thread; all controlled callbacks and stream callbacks are foreign-thread in this matrix. This preserves the previously observed possibility of either callback thread.

The callback only records into a locked preallocated log. Main dispatcher emits pending EOS before its response. No Miles call or pipe operation occurs while the callback log lock is held. Direct mode deliberately uses this same queue/dispatch code; it is a transport discriminator, **not the actual SWG in-process callback policy**. In particular20ms stream notification delay is already present in direct mode because notification waits for the next50ms dispatch. Do not attribute that entire delay to IPC or approve such queueing for game callbacks.

Observed non-CREATE request intervals: direct0.0004–0.1703ms; controlled0.0581–0.8108ms. There is no accepted latency tolerance. Controller QPC frequency is printed and matches host frequency; reply intervals are measured within the controller process, EOS delivery observations compare the shared Windows/Wine QPC clock. Instrumentation/stdio/scheduling affect these numbers; this is Wine11.17 on a virtual clocked sink, not native hardware latency. CREATE's124–128ms controlled interval includes process/vendor/driver startup, while direct CREATE is timed after startup: those CREATE figures are explicitly not a transport-only comparison.

## Validation and identity

`analyze.py` requires zero exits, exact ordered response IDs1..66, precisely oneEOS, correct generation/rejection, command event pairs, monotonic serialized QPC, correct final positions and realPE architectures. `analysis.json` retains each complete status/position vector, pair differences(empty here), timings and logs' hashes. `run-b/` retains raw logs, route snapshots and commandargv. V1 `run-a/` also succeeded; v2 adds explicit controller frequency, reruns all8, and preserves v1 sources/binaries. No hidden failed playback attempts.

Native VS2013 /MT /O2 /W4 compilation: genuine x86host and x64controller, no vendor replacement or fake implementation. fopen deprecation warning retained. Source SHAae7361f65b8245fd21cfd93367fc96582752aea9c4e12394e45e743c9c13ecd2; hostfb7535f5f31dee79aca0eadf7c94be22679a250efc404deddf56a4072979eda5; controlleree42b56239d7b43207de0ac3d9176aabb2f7161571a4d34b97873e888e03e9d5. Native transfer/compiler identities in native-identities.log. DLL0785b5f2... and assetad880479... full hashes verified by runner against precedingPLAN. Loaded DLL path is C:\rpc-private\Mss32.dll in each host log.

## Isolation and unresolved contract

Both runs used separately copied owned Wine prefixes and verified support.null-audio-sink modules. ALSA config contains only explicit Pulse server/device, no PCM fallback; winepulse disabled. Every run has observed producer routing to the owned sink. Existing ALSA InvalidCTL hw0/1 warnings retained; no hardware PCM route configured. No default sink/source/volume changes. Owned wineservers stopped, sinks unloaded/absence verified, defaults unchanged. Native owned build scratch removed after identities saved; private local evidence/prefixes retained.

Blocking pipe reads rely on the experiment's outer15s watchdog, not a production transport timeout implementation. No callback reentrancy, reverse file-I/O RPC, crash/restart, event cancellation, multi-voice/spatial/reverb/loop/seek behavior or PCM fidelity compared. Queued event delivery visibly changes callback timing context even when sampled getter values agree. Same original DSP remains insidehost, but100%original experience remains unproven. This supports feasibility of this narrow request/reply seam only; no helper adoption or permission to replace missing APIs follows.
