# Prospective EOS delivery discriminator

2026-09-30, before implementation/run. Exactly 24 runs: sample and stream,
three arms (direct immediate x86 observer, queued x86 observer, unsolicited
x86 sender -> x64 observer), phases 0 and 500 microseconds, two repetitions.
Each playback uses the same original runtime and 204ms owned WAV as RPC probe.
Observe 600 absolute 1ms epochs after a shared QPC start. Host executes real
AIL_serve at 50ms cadence; command channel stays idle (no controller requests).
Record actual epoch time rather than pretending Sleep has 1ms precision.
Callback writes one preallocated event and interlocked publication; no Miles
calls, pipe I/O, allocations or waits inside callback. Immediate arm publishes
observer flag from callback. Queued arm publishes at next 50ms host maintenance
boundary. Unsolicited sender waits for callback publication and inactive flag,
then transmits on its dedicated pipe; x64 receiver publishes observer flag.
Inactive flag is last callback action; it marks end of callback work, not proof
that vendor callback-stack unwinding has finished. Sender never calls Miles.

This observer is interlocked diagnostic state, NOT Sound2d/PlayerMusicManager.
No engine callback policy or 100% fidelity claim. No latency tolerance. Compare
callback -> publication delay, first observer epoch seeing state and transport
latency. Report every outcome, lost/duplicate events, actual scheduling gaps.
No optimization or additional rounds to seek agreement. Original-runtime source
sequence identical in all arms; native x86 host and x64 receiver, private owned
Wine prefix/null sink, no hardware/default audio changes. No production changes.
