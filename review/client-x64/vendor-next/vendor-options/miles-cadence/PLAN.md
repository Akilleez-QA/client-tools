# Prospective experiment 2: original Miles at 50 ms cadence

2026-09-30. Authorized private diagnostic support only, not a selected replacement
backend. Experiment 2 first; experiments 1 and 3 are not part of this run.
Read predecessor realtime/file-callback PLAN, RESULTS, host/probe, runner/build
and analysis scripts and ../../parallel-review-next/grok-vendor6-log.txt.

Build a direct x86 probe with native VS2013/v120 /MT in exclusively owned
C:\miles-cadence-20260930-a. No Q/R mappings or product edits. Load original
Mss32.dll by absolute private path, expected SHA256
0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe.
Use existing miles-probe/sample.wav, expected SHA256
ad880479382433a16f99e60d5d5248c30446a44ccc692bfaabb1d012c607a7a9.
No generated media/vendor implementation. One sample or stream per process,
three repeats each. Same stereo 22050/16 driver route as earlier probe. Skip
unrelated MP3 decode: this experiment does not compare sticky FPU flags to that
old decode arm. Do not change main FPU mode/provider preferences (experiment 3).

Main thread serves and queries at intervals >=50 ms measured by QPC, with no
catch-up bursts. Query status then total/current ms position. Fixed preallocated
4096-record log, critical section serializes sequence allocation, complete record
writes, cached main observations, and EOS flag mutation. Never hold that lock
across Miles calls, avoiding lock inversion/reentrant callback deadlocks.
Record serve-enter, status-enter/status-return, position-return and EOS plus
lifecycle markers; QPC, thread, status, total/current position, EOS flag, x87
control/status and MXCSR. EOS makes no Miles calls: its status/position fields
are explicitly the last main-thread cache, not callback-time getters. Getter
entry/return records bracket any overlapping callback; do not invent ordering
inside a vendor call. Callback sets flag and appends EOS under the same lock.
Capture FPU registers on the emitting thread before acquiring logging lock.
Dump only after handle release, driver close and Miles shutdown.

Retain handle >=500 ms after main first observes EOS, continuing same cadence.
Playback wait cap 3 seconds, process watchdog 15 seconds. Overflow, missing EOS,
missing DONE, nonzero exit, missing route evidence, or bad cadence invalidates
completion. Preserve every attempt and raw logs. First main SMP_DONE with flag0
would demonstrate a getter gap; flag1 in all repeats only establishes absence in
these observations. Compare first-DONE positions exactly across repeats; report
variation without tolerance. Callback overlap with getter stays explicitly
bracketed. No audio quality or bridge equivalence oracle.

Copy stopped prior Wine prefix into this owned directory. Before any playback,
create unique module-null-sink; prove owner_module and support.null-audio-sink
factory. Use process-local ALSA config defining only Pulse PCM with explicit
server/device and no fallback, disable winepulse, use private prefix registry.
Inspect producer routing, retain raw snapshots. No physical output, default or
volume changes, media capture, publication, commits, push or PR. If isolation
cannot be established stop. Cleanup only owned prefix processes, sink module,
and native scratch after saving native source/binary/compiler hashes.

Re-read old raw logs to substantiate correction: clocked route can deliver EOS
on main OR worker. Preserve prior packets unchanged; put correction with exact
rows and hashes here. Record local/runtime/source/asset identities and native
transfer identity checks. Limit conclusions to this Wine route and tiny asset.
