# Component and architecture review reconciliation

Product head `49d0eeed4` remains unchanged. This round responds to the requested fanout and coherent bridge design. The native goal remains active. No PR, upstream write or production backend adoption occurred.

## Observations and changes

- The blind Astra opening and later nonblind addenda are preserved separately. The original-runtime helper remains conditional on a clean real-engine callback, TreeFile and teardown comparison. Shared sources do not count as independent runtime corroboration.
- The parent independently compiled and ran the codec/registry (449 checks), retained ownership (41), and SOUNDINFO codec (93) under ASan/UBSan. Native worker results and deliberate defect controls have source hashes. These tests do not establish vendor callback quiescence.
- Codex CLI transport15 found no implementation bug in its frozen review. It identified missing successful dispatch coverage and a failure-output test gap. The parent strengthened the latter: all reply bytes except transport status must be zero. Removing dispatch clearing now fails both native Debug and Release controls. No fake vendor exports were introduced; successful real-vendor dispatch remains untested.
- Composer callback15 identified an overly broad API-MAP claim for borrowed sample status/position. The parent narrowed Sample to OwnedSample except the five source-used borrowed operations. This changes documentation, not vendor behavior. Composer's SUPPORTED.md drift claim was false: its following sentence already listed those five operations. The version macro is also already represented by a planned SessionVersion control; it is not a missing function export.
- Earlier Composer startup13 incorrectly claimed that head49d0 lacked NPClient64. The parent verified the head contains commit6776d2054 and the WIN64 provider name. That statement is excluded from current evidence.
- Grok lock15's restricted slice stops on unsolicited or foreign callbacks. Existing runtime observations include both, so that slice cannot be a complete bridge. Lock depth does not establish callback recursion depth. The architecture requires independent callback progress and a measured execution policy.
- Grok Bink13 retracted free-running, latest-frame and BGRA-only proposals as behavior preserving. Original Bink scheduling and requested pixel formats remain design requirements. Co-hosting preserves the real driver relationship but does not prove video timing.
- Codex FPU14 raised caller-state differences as plausible, not measured output failures. The parent's native original-DLL probe confirms preference18 off, preference44 on and selected x87 precision preserved through startup/shutdown without a device. No global PC64 policy follows.

## Architecture review barrier

Astra's independent architecture opening and the parent's design converge on the semantic boundary: x64 game policy, x86 original Miles and Bink, one MediaSession authority. Their transport packaging differs: one logical connection versus two independently drained channels. This is compatible; continuous progress and separation from bulk frame transfers are the requirements. Agreement on this source-based reasoning is not runtime evidence.

Astra's cross-review identified a callback fence requirement across channels: a close reply cannot retire an earlier unacknowledged callback. The architecture now names the callback frontier, pins during Closing and the still-required original-vendor termination guarantee. Astra narrowed its own suggestion of waiting for acknowledgment inside the vendor callback to an unproven scheduling candidate. The updated design makes no claim that it is safe under the original driver's locks.

Composer design16 confirmed the current code lacks a coordinator and pipe frontend. It read the parent's reconciliation despite the requested separation, so its assessment is explicitly nonblind. Its stale HOST-DISPATCH finding is addressed by labeling the earlier review historical, preserving the opening rather than rewriting it.

Grok design16 adds a useful combined schedule: reverse TreeFile during a locked pending command while a foreign EOS reaches game state involved in that command. It is now a prospective adversarial test, not a demonstrated deadlock. Grok's prescribed single foreign executor and requirement to execute at an exact instant exceed the evidence. The parent does not adopt those prescriptions. Measured request-boundary batching changed observer epochs; this does not establish a particular client thread count or zero allowable latency. Causality must come from the actual host call stack, not merely an active request.

All CLI15/16 workers completed with exit0. These are source/design reviews, not additional vendor outcomes. Astra's architecture rebuttal found no critical boundary conflict after the revisions. Callback return, vendor quiescence, combined scheduling and the failed real-engine teardown remain open.

## Decision

Proceed with the single-session design as the organizing contract for experimental implementation. Do not assemble the independently tested components into a production backend yet. The next work is one resource authority and coordinator admission/completion model, followed by real-engine progress and lifetime tests once the original baseline is clean. No tolerance or fidelity requirement was relaxed.
