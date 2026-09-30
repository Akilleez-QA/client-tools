# EOS observer discriminator: completed bounded run

2026-09-30. All **24 predeclared runs** retained: sample/stream ×
immediate/queued/unsolicited × 0/500 µs observer phase × two repetitions.
Each has 600 observer records, one EOS, final vendor status DONE, position/total
204/204 ms, exit 0 and an observed producer routed to the owned null sink.
These are structural checks, not a fidelity acceptance threshold.

| Arm | Callback → observer-state publication | Callback → first observer seeing completion |
|---|---:|---:|
| Original x86 immediate diagnostic state | 0.0001–0.0003 ms | 0.0995–0.6795 ms |
| x86 queued at 50 ms maintenance boundary | 0.0361–40.5603 ms | 0.1160–41.2481 ms |
| x86 sender → unsolicited pipe → x64 receiver | 0.1053–0.1713 ms | 0.1888–0.9097 ms |

The four queued **stream** runs miss 40,40,41,41 nominal 1 ms observer epochs
relative to the first scheduled epoch at/after their own callback. All other
runs first observe at that next nominal epoch (zero additional epochs).
This comparison anchors each run to its own callback, not to the callback time
of another process: completion timing itself varied. One immediate stream EOS
occurred at 276.5855 ms after start, while most stream runs were near 260 ms.
No run was removed or repeated to obtain agreement.

The queued sample callbacks happened near a maintenance boundary and therefore
did not demonstrate a whole-boundary delay. This is not evidence that sample
completion can always be queued safely. The two chosen observer phases are a
small finite test, not exhaustive phase coverage.

## What changed from the previous self-oracle

The immediate arm now publishes the diagnostic observer state **inside the
original Miles callback**. It does not reuse the queued dispatcher. The queued
arm deliberately publishes only after the next 50 ms serve boundary. The
unsolicited arm uses a dedicated sender, independent of command requests.
The host executes the same 13 real AIL_serve epochs in all arms; no controller
request is needed to release an event.

Callback work is limited to an interlocked count/active flag, preallocated event
record, QPC, publication and SetEvent. No Miles API, allocation, pipe write or wait
occurs in the callback. The sender waits for publication and `active==0` before
writing. That flag marks the last callback work; it does not prove completion of
the vendor's callback-stack unwind. The sender calls no Miles API either.
`callback_end` records immediately before event publication/SetEvent, not an
instrumented machine return instruction. Its name must not be read as stronger
measurement than that.

## Scheduling and baseline limits

The observer uses absolute QPC targets at 1 ms intervals and records actual times.
It does not establish real-time scheduling. The largest actual observer gap was
5.4553 ms in an immediate run; that run's largest nominal lateness was 5.4157 ms.
The corresponding ranges for unsolicited runs were up to 1.3423/0.3435 ms.
CPU contention and Sleep(0) polling are part of this diagnostic environment.
No tolerance has been invented, and 0.17 ms is not accepted as inaudible or safe.

This is native MSVC v120 x86/x64 code executed under Wine using the same original
Miles DLL and asset as the earlier probe. It is not native Windows device
acceptance. The null sink consumes output silently; PCM was not captured.
No game was launched, no actual Sound2d/PlayerMusicManager callback was executed,
and no production helper/backend was selected. An interlocked receiver flag
cannot prove preservation of the game's unsynchronized callback thread context,
callback-to-alter races, sound release, band timing, TreeFile I/O or Bink driver
co-hosting. Better event timeliness is only a necessary architectural lead.

## Source spot-check

At integration a21af1630, `Sound2d::endOfSample` still performs end flag, loop
increment, game callback, fade reset, current-time reset in that order.
`PlayerMusicManager::sampleFinished` writes its flag and then calls
`PerformanceTimer::start`; the actual sharedDebug Win32 timer implementation
writes QPC to m_startTime. The music update clears the flag and unregisters the
other musicians' callbacks when it consumes completion. Therefore recording
callback occurrence and then applying game state only at the next command is
not source-equivalent. This probe demonstrates that distinction with a safe
observer model; it does not reproduce the full game policy.

## Identity, evidence, cleanup

Original DLL SHA256:
`0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe`.
Asset SHA256:
`ad880479382433a16f99e60d5d5248c30446a44ccc692bfaabb1d012c607a7a9`.
Native build uses actual Mss.h and dynamically resolves the real DLL exports.
`build.cmd`, `probe.cpp`, `run.py`, `analyze.py`, `analysis.json`, all 24 raw logs,
routing snapshots and command history are retained locally. `run-v1/results.json`
contains hashes of all test inputs and binaries. Binaries/media remain private.
Native scratch identities and deletion are in native-identities-cleanup.log.

Owned Wine processes stopped; owned null-sink module unloaded and removal
verified; host default sink/source unchanged. No physical device/default changes,
Q/R mapping changes, production source changes, commits or pushes.

**Decision:** the queued boundary is demonstrably an unsuitable oracle for
immediate EOS observation. Unsolicited delivery is worth testing against real
engine observer/lifecycle behavior, but the finite timing improvement does not
establish the required original experience. Stop this discriminator here; no
additional tuning rounds were run.
