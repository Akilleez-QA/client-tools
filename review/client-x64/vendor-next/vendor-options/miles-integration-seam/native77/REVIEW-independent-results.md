# Independent saved-evidence review77

Read-only source/evidence audit; no compiler, test, VM, linker, SDK/engine runtime, Git or product action. Only this separate review was written. Existing freezes, raw logs and results were not changed.

## Composer claims reconciled against actual77

The two alleged implementation defects in parallel-review-next/composer-diagnostics77-log.txt are not supported:

- Public ClientMiles.h:138 places `sample_reverb_levels` before the explicitly enumerated five borrowed-capable names at140–146: volume set/get, reverb SET, playback-rate set/get. The reverb GET would be a sixth operation, not an omitted member of those five. Backend's OwnedSample-only arm, Core's sampleFloatPair condition (borrowed only for volume getter), and host_dispatch.cpp:165–170 consistently keep that getter owned-only.75's lower case block contains reverb SET only, despite the critic saying both cases were there. This is the declared bounded subset, not a new universal statement about native SDK capability; no change is justified by that claim.
- PipeCore.cpp:405–415 routes each driver diagnostic through `driverCall(session, driver)`. That helper calls `session.requireRunning()` at110 before checking the trusted selected driver row. It must finish before Session::request is invoked with its resulting Call. Timer and file-error call requireRunning directly. The critic inspected direct calls in the outer functions and missed the helper's lifecycle check; room_type uses the same pattern.

The critic's test-scope observation is valid and was already explicit: portable77 executes the actual decoder/codec/signedValue dependency path, not Core/Backend runtime gating or borrowed-resource admission. The native gate compiles those real production bodies but does not execute their behavior.

## Actual native evidence

Audited native77/native-evidence-v1/curated, independently parsing each raw symbols.log and reading all35 compile logs/actual-includes records rather than relying only on aggregate passed. The curated ZIP hashes to `c0e0b65ac6feb8e326fce0a904ebe52dd6d871bd3476c9904f99e0b545703878`, matching the reported artifact.

All35 reached production objects report exit0, compiled status and no warning/error diagnostics:18 x86 COFF0x14c and17 AMD64 COFF0x8664. The after-collection identities agree with every recorded object SHA/machine. Objects remain private; this review inspected recorded identities, not local object contents.

Raw undefined-symbol parsing matches each recorded undefined list. Exact expected AIL name sets and actual x86 `__imp__...@N` decoration match all four SDK units; all other units have none. Across those four objects there are50 AIL import observations (not50 exported facade functions). Separately, the public wrapper's raw undefined Core delegate set is exactly the frozen50-name list, including the five diagnostics. No extra or missing delegate was found.

Checked the actual quoted-header observations for every unit against the71 staged-input manifest entries. No expected local header mismatch/absence was found across3945 total include observations (this is a per-object observation count, not unique headers). Source/code/tool identity checks reconcile independently: saved authored before, saved authored after and inputs_after.json all equal the frozen map; reused35_after.json equals all9536 reused manifest entries; saved tools_before/tools_after equal the pinned x86/AMD64 tool map. Current local frozen input bytes still match. System header hashes are single-time observations, not before/after system header proof.

## Actual portable evidence

Read portable-diagnostics77/evidence-v1: build log is empty; compile_exit0 and run_exit0; run.log contains each of the five frozen group markers exactly once and `PASS assertions=1241`. The recorded command uses strict C++11 warnings-as-errors plus ASan/UBSan with no recovery. No sanitizer failure appears in the log. All15 frozen inputs still hash identically and the receipt reports no changed inputs. No test rerun was performed.

These observations support the existing bounded pass statements: actual assembled object/type/import/header coverage and the real scalar decoder's specified portable cases. They do not establish a linked client/host, native SDK behavior, real Runtime scheduling, Core/Backend behavioral tests, stream ownership, EOS/TLS/locking semantics, Audio adoption or paired shutdown. No publication readiness claim beyond that scope is added.
