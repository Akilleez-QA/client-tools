# Actual original Miles host-dispatch subset — 2026-09-30

| Native v120 executable, runtime under private Wine | Result |
|---|---|
| Debug candidate | 75/75 checks,13 distinct dispatch arms; exit0 |
| Release candidate | 75/75 checks,13 distinct dispatch arms; exit0 |
| Debug, valid left/right setter arguments deliberately swapped | 69/75; exit1, expected |
| Release, same mutation | 69/75; exit1, expected |

Builds use real host_dispatch.cpp, genuine SDK imports and ResourceRegistry resolver. Both candidate builds are /W4 /WX clean. The first build stopped on existing RegistryResolver C4512; parent made its implicit nonassignability explicit with a private undeclared assignment operator. Native manifests bind that header change; earlier component evidence remains earlier evidence.

Runtime uses the exact private original Miles DLL SHA0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe and existing9020-byte valid PCM WAV SHAad880479382433a16f99e60d5d5248c30446a44ccc692bfaabb1d012c607a7a9. Each executable verifies its loaded DLL path. Each run starts real Miles, opens a real22050Hz16-bitstereo driver, allocates/binds two equivalent samples and opens two equivalent streams. No sample/stream is started. No EOS callback is registered. All samples, streams and input bytes remain live through comparisons.

Direct calls on control resources precede the matching dispatch/readback. Runtime exercised arms: sample volume setter/getter; rate setter/getter; loop-count setter; loop-block setter; byte-position setter/getter; millisecond-position setter/getter; sample status; stream status; stream millisecond position. Distinct-opcode inventory is in raw logs. Getter masks0/1/2/3 are compared with genuine direct calls using the corresponding null outputs. Direct-only loop getters verify real vendor state rather than treating a void setter return as proof. Different volumes/rates/counts/positions were selected prospectively. Stale-generation and unused-field controls reject without changing genuine volume state.

All four processes (two positive,two mutations) close streams, release samples, explicitly close the driver, call shutdown, print cleanup completion and exit. This is fixture lifecycle, not evidence that an explicit driver close equals the game's shutdown sequence. Mutation changes only the two valid volume argument positions inside a scratch dispatcher copy. Six volume-bit comparisons fail while cleanup still succeeds, proving the positive oracle detects this semantic defect. No invalid memory or engine allocator workload was used.

Isolation: separate copied Wine prefix per positive/mutant run; process-local ALSA configuration routes only to a unique owned clocked null sink. Default sink/source names match before/after. Only owned sink modules are unloaded and owned-prefix Wine servers stopped. No hardware/default/desktop changes. No timing, audible output or playback-fidelity claim follows from quiescent property comparisons.

## Publication boundary

Curated text-only packets: evidence-positive/ and evidence-mutation/, plus authored source/scripts and this report. DO NOT publish private-run-*/ or private-mutation-*/ (contain Wine prefixes,original DLL/private media); DO NOT publish native-v3/ or native-mutant-v1/ executable files. Curated packets already contain native compile/import manifests and runtime logs without SDK/media. Genuine private headers/import libraries are referenced from the local VM installation, not vendored here.

## Limits

This proves useful actual effects/readbacks for13 of39 supported scalar/control dispatch arms on the listed states under Wine. It is not all39 arms, native Windows device evidence, IPC/framing/session admission, x64 client integration, input-upload/bind/lifecycle handlers, worker-callback fidelity, original engine teardown, Bink, full audio behavior or gameplay acceptance. Fixture-only direct SDK setup/cleanup is listed in PLAN.md. The coordinator/oracle and product files were not changed.
