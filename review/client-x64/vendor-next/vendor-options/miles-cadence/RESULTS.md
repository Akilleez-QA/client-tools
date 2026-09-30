# Original Miles experiment 2: 50 ms getter/callback ordering

2026-09-30. Six completed direct original-x86-DLL runs: three sample, three
stream, one existing 9020-byte PCM WAV. No observed getter gap in this matrix.
This is private diagnostic support, not a selected replacement backend.

| Run | Main / EOS thread | EOS sequence | First DONE sequence / flag | Following total / position ms |
|---|---|---:|---|---|
| sample-1 | 300 / 320 | 11 | 14 / 1 | 204 / 204 |
| sample-2 | 336 / 356 | 11 | 14 / 1 | 204 / 204 |
| sample-3 | 372 / 392 | 11 | 14 / 1 | 204 / 204 |
| stream-1 | 408 / 428 | 23 | 26 / 1 | 204 / 204 |
| stream-2 | 448 / 468 | 23 | 26 / 1 | 204 / 204 |
| stream-3 | 488 / 508 | 23 | 26 / 1 | 204 / 204 |

Sequences are zero-based, scoped to each process. In every run, the synchronized
EOS event falls between the previous position-return and the next serve-enter.
The next status getter returns SMP_DONE (2), flag already 1, and the immediately
following position getter reports 204/204. Before EOS the cached status is
SMP_PLAYING (4). No callback overlapped a getter bracket in these observations.
Thus first-DONE positions are exactly identical across each three-repeat arm.
No DONE/flag0 was observed; no universal absence-of-gap or scheduling guarantee
follows. All six EOS callbacks were foreign-thread callbacks, so this new matrix
does not compare main-thread versus worker-thread getter ordering.

Observed serve intervals: 50.1757–50.9277 ms. Status and position getter intervals
also passed >=50 ms checks. Handles retained 500.0083–500.4743 ms after the main
thread observed EOS, with continued 50 ms cadence. All exits 0, one EOS per run,
zero log overflow, contiguous sequences and nondecreasing QPC timestamps.
Raw logs, route snapshots and subprocess argv: run-a/. Reproducible assertions,
full events selected for the oracle and old-log census: analyze.py, analysis.json,
verification.log. No PCM scoring or new media capture.

## Synchronization and interpretation

The fixed 4096-event array and a critical section protect complete writes,
sequence allocation, last-getter cache, and callback flag updates. No Miles
call occurs under that lock. EOS only updates flag and records; it does not
call getters or write files. All serve/status/position calls are main-thread
only. Records are dumped after release, driver close, and AIL_shutdown.

A status-return record is a synchronized observation just after the API returns;
a callback in that small interval could precede the observation. Entry/return
brackets expose logged overlap but cannot timestamp an internal DLL transition.
Here EOS preceded the next serve-enter, so that ambiguity does not affect the
reported first-DONE rows. Status-return position fields are the previous cache;
use its following position-return for the new position. Callback status/position
are explicitly cached previous main getter values, never callback-time getters.
The two getters are separate calls, not an atomic vendor snapshot. Instrumentation
can perturb scheduling; this is not the game or a proof against rare races.

x87 control/status and MXCSR are captured on the emitting thread before acquiring
the log lock; QPC/sequence mark the serialized record. Main and EOS control words
were 027f and MXCSR 00001f80 in these runs; x87 status varies in the raw logs.
No game FPU restoration/provider experiment was performed. Unlike the earlier
host, this narrow probe omits unrelated MP3 decode, so it does not reproduce
that host's decode-induced MXCSR sticky flags.

## Correction to earlier clocked-route wording

The realtime RESULTS sentence saying this clocked route delivers EOS on a
separate Miles thread is too broad. Its four command runs did, but its own
six drain logs include main-thread EOS. The correct statement is: **on this
clocked route, EOS has been observed on either main or worker threads.**

| Old run | Main / EOS | EOS MXCSR |
|---|---|---|
| drain-sample-1 | 300 / 324 | 1f80 |
| drain-sample-2 | 356 / 404 | 1f80 |
| drain-sample-3 | 436 / 436 | 1fa0 |
| drain-stream-1 | 516 / 516 | 1fa0 |
| drain-stream-2 | 600 / 600 | 1fa0 |
| drain-stream-3 | 684 / 732 | 1f80 |

All four old command runs used foreign EOS threads: 304/328, 360/408,
440/488, 524/572 (direct sample, controlled sample, direct stream, controlled
stream). File-callback handle0 likewise main300/EOS320; handle1 main340/EOS340.
Grok's criticism is substantiated by raw logs, not merely repeated from prose.
Exact paths and SHA256 for all 12 old logs are in analysis.json. Prior packets
were left unchanged. Different thread IDs are never combined across processes.

## Identity, isolation, cleanup and limits

Original DLL SHA256:
0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe.
Original client distribution and private loaded copy match. Each process prints
C:\cadence-private\Mss32.dll as its loaded path. Both probe and DLL are PE x86
machine 0x14c. Existing asset SHA256:
ad880479382433a16f99e60d5d5248c30446a44ccc692bfaabb1d012c607a7a9.
Source SHA256: 20986699b2927be2fe00f9101151a5e9f781771e3398ac2328ff5b6fc368cf0a.
Executable SHA256: 3a321baacd0e2d49f31d4747bce3e6be844a59428d180ddd4c04b49cdcb976d0.
Native source/header/executable hashes match local files; compiler hash and
scratch deletion proof are in native-hashes-cleanup.log. identities.json and
hashes.json provide machine checks and file/runtime provenance.

Native v120 /MT /O2 /W4 builds ran only in owned C:\miles-cadence-20260930-a.
Both compiled successfully, with fopen deprecation warning retained. V1 source
and binary are preserved but were never played. V2 adds post-getter cadence
anchoring before the first experiment. No run failed or timed out.

Wine11.17 used a separately copied private prefix, winepulse disabled, explicit
process-local ALSA Pulse server/device with no PCM fallback. Created sink
swg_cadence_a4f3071c4664 was verified as support.null-audio-sink with matching
owner module before execution. Producer snapshots were observed on that sink
in every run; full sink-input snapshots are retained. ALSA's Invalid CTL hw:0/1
warnings are retained; those control definitions are absent in the private
config, not successful hardware PCM routes. No monitor capture was needed.
No default-device or volume mutation commands were issued; defaults matched
before/after. Owned sink unloaded and confirmed absent, private wineserver
stopped, native scratch removed (scratch_exists=False). Local private evidence
and prefix remain. No Q/R remapping, product source edits, publication, commits,
push or PR. No native-Windows scheduling, physical-device, game integration,
quality tolerance, bridge equivalence or original-experience claim. Experiments
1 and 3 remain unperformed.
