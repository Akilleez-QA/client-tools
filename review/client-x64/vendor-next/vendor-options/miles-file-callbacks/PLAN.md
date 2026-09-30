# Prospective private original-Miles file callback experiment

2026-09-30. Authorized diagnostic only. Read ../miles-realtime/PLAN.md,
RESULTS.md, build-command.cmd, miles-command-host.cpp and private Wine runner,
and ../../parallel-review-next/grok-vendor5-log.txt. No prior EOS observation is
file-callback evidence. No game, production edits, backend decision or publication.

Build one native v120 x86 executable in a new C:\miles-fcb-20260930-a scratch
folder using the existing winps wrapper, never changing R:/Q: or shared build tree.
Copy the existing Mss.h read-only. Load the original DLL with SHA256
0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe.
Use the existing 9KB PCM sample.wav privately, no codec/large-buffer experiments.

Two fresh processes differ only by successful handle 0 or 1. Each installs real
file callbacks, tries an absent logical name (return 0, output handle 0), then
opens the valid logical name (return 1, chosen output handle). Adapter owns one
standard FILE, protected by its own lock, accepts only these names/handles,
bounds reads/positions to the known small file, and never calls Miles. Record
entry/exit events in a fixed 4096-event buffer, including sequence, thread,
per-thread depth, active callback count, phase, return, handle and read/seek data.
Depth above 8 rejects work. EOS uses the same instrumentation. Dump only after
Miles shutdown; report overflow/errors. Main calls AIL_serve every 5ms, except
an explicit first 200ms no-serve window. Playback cap 2s plus 500ms drain;
external 15s process timeout with private wineserver cleanup.

Use a fresh copied private Wine prefix with winepulse disabled and process-local
ALSA pulse config naming only a new unique clocked null sink, no fallback.
Check sink properties before playback and inspect sink-input routing. Never
change defaults/volumes or install devices/services. Stop if isolation unavailable.
No audio recording needed. Unload only created sink and kill only private prefix
processes, remove only owned native scratch folder. Preserve logs and failures.

Minimum: determine whether actual DLL reads/seeks/closes return1/handle0,
contrast return1/handle1 and failed open, and census foreign file/EOS threads.
Absence of concurrency/nesting/multiple foreign threads applies only here.
No TreeFile, game TLS, helper RPC, original Windows equivalence or fidelity claims.
No x64 extension planned; parent reviews direct evidence first.

## Initial route preflight correction (before DLL execution)
First runner stopped before Wine/probe launch: PipeWire reports factory.name
support.null-audio-sink, not device.class=abstract. The assertion was too narrow.
Its cleanup then failed because no private wineserver existed (exit1), preventing
its later cleanup steps. Preserved run-1.log and run-initial.py; explicitly unloaded
only created module536870916. Revised gate verifies factory.name and module
ownership, and cleanup tolerates absent wineserver. This is an available isolated
null sink, not a request to use a physical fallback. Retry same experiment.
