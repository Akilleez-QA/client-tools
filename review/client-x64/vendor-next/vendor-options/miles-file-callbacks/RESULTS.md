# Original Miles 7.2a file callback diagnostic

2026-09-30. Private native v120 x86 probe, original DLL, Wine11.17, isolated
clocked PipeWire null sink. Direct file-callback contract established for this
small PCM stream. No production implementation or backend decision.

## Observations

| Successful output handle | U32 open return | Reads / bytes | Seeks | Closes | EOS | Process result |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 14 / 9020 | 3 | 1 | 1 | 0 |
| 1 | 1 | 14 / 9020 | 3 | 1 | 1 | 0 |

Each process first requested missing-reference.wav: open returned0 and wrote
handle0; AIL_open_stream returned null. No read, seek or close occurred in that
missing-open phase. Then owned-reference.wav succeeded. Handle0 reads, seeks
and close are direct actual-DLL observations, not inferred from EOS. Valid
stream creation still printed the previous `Unable to open file.` last-error
text; the nonnull stream and callback trace establish success. The probe does
not assume last-error text clears on success.

| Run | Main/serve thread | File callback threads | EOS thread | Foreign file threads |
|---|---:|---|---:|---|
| handle0 | 300 | 300, 324 | 320 | 324 |
| handle1 | 340 | 340, 364 | 340 | 364 |

The handle0 run observed **two distinct foreign callback threads across file
callbacks and EOS**. It did **not** observe two foreign file-callback threads.
The handle1 run observed EOS on the main thread. Across separate processes,
thread IDs must not be combined into a same-process census. These results do
not establish or refute the game's process-global TLS latch safety.

Both runs parsed headers and sought on the main thread, then read the PCM body
and closed the file on a foreign thread during phase3, with no main AIL_serve.
That window includes AIL_start_stream followed by Sleep(200); it does not prove
callbacks occurred after AIL_start_stream returned. The logged window spans
193/194ms according to Wine GetTickCount despite the requested200ms sleep.
EOS followed in the serve phase. Each run logged44 events, maximum per-thread
depth1, observed active count1, zero overflow and zero adapter errors. The
active count is an entry/exit observation, not exhaustive race detection.
No nested or overlapping entries were observed; absence is scoped to this probe.

## Inputs, bounds and provenance

DLL SHA256: `0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe`.
Copied byte-identically from the original client distribution path recorded in
run-b/results.json; loaded with an explicit absolute private path.
PCM SHA256: `ad880479382433a16f99e60d5d5248c30446a44ccc692bfaabb1d012c607a7a9`.
Existing private reference:9020-byte WAV,4488 mono22050Hz signed16 frames.
No new codec input, decoding, media capture or publication. Only one stream at
a time and one owned FILE. Callback code makes no Miles calls and uses a fixed
4096-event buffer (~180KiB), bounded depth8, file size cap64KiB, file-size-bounded
reads and seek positions. Miles owns its internal allocations; they are not
instrumented here. Main wait cap2s plus500ms drain; runner watchdog15s. Both
processes finished in approximately1.06s without timeout. Callback failures
reject work; no malformed-input stress was attempted.

Exact source, header, binary, PCM and selected Wine runtime hashes: hashes.json
and run-b/results.json. Native compiler and transferred source/binary hashes:
native-hashes-cleanup.log. Compile commands and execution chronology: COMMANDS.md,
build.cmd, run.py, run-b/commands.json. Raw events: run-b/handle0.log and handle1.log.
Computed census: analysis.json, reproducible with analyze.py.

## Isolation, preserved failures and cleanup

The first preflight failed on an incorrect device.class assertion before Wine
or DLL execution. Its cleanup encountered absent wineserver exit1. Both are
preserved in run-1.log and run-initial.py; explicit owned-module cleanup succeeded
(cleanup-initial.log). Revised preflight checks the actual
support.null-audio-sink factory and created-module ownership.

Successful run used a distinct named null sink, process-local ALSA pulse config
with explicit server/device and no fallback; winepulse disabled. ALSA emitted
Invalid CTL hw:0/hw:1 warnings: those control names are undefined by the private
config, not successful hardware PCM opens. Observed producer routing reached
only the created sink in27/26 sampled snapshots. No default-device or volume
commands were issued; before/after default names matched. No installer/service
changes. Created sink unloaded and confirmed absent; private wineserver stopped;
only owned native scratch folder removed (scratch_exists=False). Private local
prefix/assets remain here for parent review. Shared R:/Q: and native build tree
were untouched.

## Strict limits

One two-arm diagnostic, one tiny PCM file, one clocked Wine backend; no repeat
matrix, native Windows scheduling claim, fidelity judgment, game execution,
TreeFile/game state, TLS integration, long-stream load, simultaneous streams,
handle counter wrap, callback RPC, cancellation/restart or production patch.
No x64 extension performed. One foreign file thread per process is not proof
that Miles always uses only one. Different EOS threads do not themselves prove
concurrent file callbacks or diagnose the game's latch. Parent review required
before interpreting these observations as any architecture decision.
