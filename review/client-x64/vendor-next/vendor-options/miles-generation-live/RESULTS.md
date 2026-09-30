# Live-generation Miles guard diagnostic

2026-09-30. **Six bounded runs completed: four guarded passes and two expected diagnostic failures.** The new experiment independently discriminates the generation predicate while the slot has a valid live original-Miles handle. This establishes a narrow diagnostic protocol guard, not original game experience or game fidelity. No production changes, backend selection, commits, pushes, or publication occurred.

## Oracle and lifecycle

`PLAN.md` was written before compilation/playback. Each sample/stream mode has one direct guarded, one real x64-controlled guarded, and one x64-controlled diagnostic bypass run. All use the original x86 Miles DLL through a native v120 x86 host. Each execution plays the same finite original 204 ms asset exactly once in generation 1, then recreates the slot in generation 2 without START/playback. There are two handle lifetimes per run; only the first is played. Six executions total; no playback retries.

Every run finishes 69 requests, 138 command boundary records, one EOS, two creations, two releases, one START, final generation 3 and no live handle. Generation-1 playback reaches DONE and final position 204/204 ms. The decisive tail is:

| Request | Operation | Request generation | Slot lifetime/result |
|---|---|---:|---|
| 64 | RELEASE | 1 | Real release, pointer cleared, generation advances to 2 |
| 65 | CREATE | 2 | New real live vendor handle, lifetime 2; never started |
| 66 | STATUS | 1 | Stale-generation discriminator against live lifetime 2 |
| 67 | STATUS | 2 | Current-generation legal vendor STATUS |
| 68 | RELEASE | 2 | Real release, pointer cleared, generation advances to 3 |
| 69 | QUIT | 3 | Clean shutdown |

All four guarded runs reject request 66 with diagnostic result 1 and **zero vendor-call / STATUS-call increments**, while its current live pointer remains nonzero and lifetime remains 2. Request 67 succeeds, makes exactly one real STATUS call, and returns vendor status 2. No unstarted-status constant was imposed by the prospective oracle.

Both diagnostic bypass runs change only evaluation of the generation predicate; slot and live-pointer checks stay enabled. Request 66 incorrectly succeeds, makes exactly one genuine vendor STATUS call on the current live lifetime-2 handle, and returns status 2. The unchanged validator reports precisely `stale request accepted`, `stale request called vendor`, and `stale request called STATUS`. Both controllers exit 9 for the expected violation; both hosts finish all commands, release the live handle, and exit 0. Standalone postprocessing returns 1 for both mutant logs and 0 for all four guarded logs (`postprocessing-checks.json`). The matrix validator returns 0 because these failures are the required discrimination result.

`audit` records contain explicit request/current generations, realhandle address, logical lifetime, total dispatched vendor-call counter, STATUS-call counter, creations/releases/starts and QPC before/after each command. Counters cover dispatcher calls, excluding startup/driver-open and final driver shutdown. Guarded totals are 73 vendor calls for sample and 71 for stream; mutants add exactly one. STATUS totals are 21 guarded and 22 mutant. Vendor allocations reused numerical addresses within these runs; the release-to-null and separate creation records establish distinct lifetimes. No released pointer was passed back to Miles. No null dereference, malformed buffer, allocator fault, or other invalid vendor invocation was used.

## EOS and getter comparisons are separate

Direct versus controlled guarded getter vectors match exactly for both modes, including current-generation STATUS. This is finite sampled equality, not continuous playhead or audible equivalence. `analysis.json` retains complete vectors and separate EOS context/timing differences without normalization or an accepted timing tolerance.

All six EOS callbacks were on foreign threads **BETWEEN commands** (`active_command=0`). Sample callbacks observed last command 8 (POSITION), stream callbacks last command 17 (POSITION). These are observed-last labels, not active-command or causal attribution. The analyzer checks adjacent command boundaries for BETWEEN callbacks; only a callback explicitly marked ACTIVE must lie inside its active-command window.

| Guarded run | EOS after observed-last command end (ms) | Notification request | EOS to receipt observation (ms) |
|---|---:|---:|---:|
| direct sample | 50.0376 | 9 | 0.0512 |
| controlled sample | 49.3403 | 9 | 0.9534 |
| direct stream | 29.9879 | 18 | 20.1094 |
| controlled stream | 28.2710 | 18 | 21.9991 |

EOS is queued in bounded host memory and delivered by the next dispatcher. Stream's roughly 20 ms direct delay exists before adding IPC. Native thread IDs, QPC and FPU fields are retained; raw cross-process thread IDs are reported but do not imply equivalent identities. QPC frequencies match. `verify.py` additionally checks a synthetic BETWEEN callback outside the last command window is accepted, false ACTIVE attribution is rejected, a valid ACTIVE callback is accepted, and inconsistent observed-last attribution is rejected. These are postprocessing checks, not extra vendor executions.

## Retained failure and evidence

The first analyzer pass failed on CRT buffering: complete stdout replies/requests interrupt 4096-byte stderr chunks, sometimes within an audit field. `analyze-initial.py` and `analyzer-initial-failure.log` preserve this failure. Final `analyze.py` extracts only complete exact-schema stdout records and joins the untouched stderr fragments, rejecting unparsed fragments. It does not invent values, edit rawlogs, or derive event timing from line order. Full record counts, per-command QPC boundaries, lifetimes and counters validate the reconstructed streams. No playback was rerun to hide the logging issue.

- `probe.cpp`, `build.cmd`, `native.py`: compiled diagnostic and reproducible native build/transfer/cleanup commands.
- `run.py`, `rawlogs/`: six original combined logs, process exits, command argv, route observations, input hashes and private ALSA configuration.
- `analyze.py`, `verify.py`, `analysis.json`, `*-validation.json`: guard oracle, independent EOS/getter comparisons and retained expected failures.
- `prior-evidence-hashes.json`: all five requested predecessor files remain byte-identical; originals were read only.
- `native-identities.log`, `build.log`, `native-commands.json`, `native-cleanup.log`: source/compiler/binary identities, successful VS2013 builds, the retained fopen deprecation warning, and removed C: scratch.
- `cleanup-evidence.json`, `evidence-sha256.json`: consolidated cleanup and final local evidence hashes.

Original DLL SHA256: `0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe`. Asset SHA256: `ad880479382433a16f99e60d5d5248c30446a44ccc692bfaabb1d012c607a7a9`. PE machine checks require x86 host (0x14c) and x64 controller (0x8664). Native identities and local binaries agree; loaded DLL path is the private `C:\generation-private\Mss32.dll`. Vendor data remains private/local; no vendor binaries or assets were published.

## Isolation, cleanup and limits

Builds used only new `C:/miles-generation-live-20260930`, now removed. No R/Q mappings or global build settings changed. Playback used Wine 11.17 with a copied owned prefix, explicit process-local ALSA-to-Pulse route, winepulse disabled, and a verified `support.null-audio-sink` at 22050 Hz. Every run has an observed producer on that owned sink. ALSA's existing invalid CTL hw:0/hw:1 warnings are retained; no hardware PCM fallback is configured. No host default audio or physical routing was used or changed.

Owned wineserver stop/wait both returned 0, owned sink unload completed and its absence was verified, host default sink/source remained unchanged. The owned private prefix and local diagnostic binaries remain as private reproducibility material. Prior evidence is unchanged. All authored local files are confined to this directory.

Direct and controlled paths share the diagnostic dispatcher; the experiment is not an independent vendor implementation comparison. It covers one slot and two ordinary lifetimes, one asset, six Wine executions, and queued observer callbacks. It does not establish production transport robustness, native-Windows scheduling, game callback equivalence, multivoice behavior, audible fidelity or the original game experience. Pipe reads rely on the outer 15-second watchdog, not a production transport timeout policy.
