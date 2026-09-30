# Architecture cross-review

2026-09-30. One explicitly nonblind, bounded comparison of the parent [architecture](../vendor-options/miles-integration-seam/ARCHITECTURE.md) and my [independent opening](ARCHITECTURE-CRITIC.md). Neither opening was edited. Source identities remain the supplied `49d0eeed4ddaa177d7a93ea396c37c3d9b9942da`. No execution, product changes, or descendants.

Reviewed SHA-256:

- Parent architecture: `020915e073a4de5df6e29f6a47dac1644fc812c9b2dca4f06d2d2aca59e028a3`.
- My opening: `f8ddaef694bc4896b653935db42e5357d164334c779031b4c0a75fc37d2c6f5f`.

**Conclusion:** There is no critical incompatibility between the proposed boundaries. Keep one logical MediaSession and coordinator, x64 game policy, and the original x86 Miles/Bink sharing their real driver. Two physical pipes are a reasonable initial mechanism. The remaining substantive gate is a measured callback/close contract, not another IPC abstraction. These are design clarifications and integration gates, not confirmed implementation defects.

## 1. Two pipes versus one connection

**Severity: clarification, not blocker.** Parent lines 53–55 select command/results and callback/reverse-I/O pipes. My opening selected one ordered connection with independent receive progress. One logical session can use either mechanism; I withdraw any implication that a single physical stream is necessary or more faithful. Conversely, two pipes do not prove progress: an executor blocked behind its own pending operation still deadlocks even when a reactor receives the required reverse request.

Keep session failure, admission, identities and resource ownership unified. Preserve each caller's original program order across resources, including session/driver operations; parent line 63's per-resource getter rule should not be interpreted as permission to reorder across resources. Distinguish causal dependencies from an invented total order over concurrent vendor workers.

The parent task explicitly places video bulk in separate leases. Parent lines 57/92 could state this directly so an implementation does not send a whole frame ahead of a needed reverse-file reply. This requires bounded, independently progressing control traffic, not a mandate for shared memory or a third pipe.

**Discriminator:** Hold an ordinary vendor request pending; force its reverse request and reply through the coordinator while command and video traffic are backpressured. Receiving bytes alone is insufficient: the required execution lane must complete the operation. This is a proposed observation, not a performed test.

## 2. Callback return and late-event fencing remain the central gate

**Severity: high integration gate, not a demonstrated bug.** Parent lines 67–76 and 84 correctly distinguish synchronous reverse calls from unsolicited worker callbacks and require registration-specific pins/acknowledgements. They do not yet decide whether a host EOS trampoline returns after enqueue, after x64 receipt, or after the existing game callback body finishes. My opening's “normally remain live until acknowledgement” is also an unmeasured candidate, not a safe default established by source.

The distinction is observable: [Audio.cpp:4730](../../swg-source/client-build-next/src/engine/client/library/clientAudio/src/win32/Audio.cpp#L4730) changes sample status and invokes `Sound2::endOfSample` inside the callback; [PlayerMusicManager.cpp:103](../../swg-source/client-build-next/src/engine/client/library/clientGame/src/shared/scene/PlayerMusicManager.cpp#L103) starts a game timer. Returning the host callback before that body runs changes the callback's completion point. Waiting for it could instead create a lock cycle. Neither behavior follows from reliable delivery.

Counterexample: host captures EOS for registration A on the callback channel; a close result arrives first on the command channel; client retires A; delayed EOS arrives. Generation checks prevent calling replacement B, but simply dropping A is not evidence of equivalent callback behavior. Conversely, indiscriminately delivering every queued callback after unregister/close is not justified either. Eligibility and completion must follow the actual original contract.

Define what the acknowledgement means and which captured callbacks a successful close covers. A per-resource/registration completion fence can account for already captured events across channels; it cannot prove that the vendor will never initiate another callback. That requires an established vendor retirement boundary, plus synchronized capture/pinning before publication. Do not infer either from queue emptiness or a sequence number alone.

**Discriminator:** In the real-engine comparison, observe callback entry/body completion/return, close entry/return, registration changes and vendor lock ownership. Exercise close racing EOS and idle unsolicited EOS. Establish the permitted callback-return rule before implementing it as a coordinator invariant. Preference18=0/44=1 and preserved control words in the reported no-device startup probe do not settle this question.

## 3. Lifecycle preconditions and driver order are correctly constrained

**Severity: satisfied design requirement; implementation gate remains.** Parent line 49 explicitly rejects treating `callbacksQuiesced=true` as evidence. Lines 84/86 correctly preserve reverse services during closing and reject an invented early driver close. A coordinator must own admission state, active vendor/callback references, acknowledged callback completion and the actual retirement boundary. Its transition can then supply component preconditions; a public boolean does not become proof merely because the caller is named “coordinator.”

Source supports the caution. [ClientMain.cpp:303](../../swg-source/client-build-next/src/game/client/application/SwgClient/src/win32/ClientMain.cpp#L303) installs Audio before passing its driver to VideoList at 314. [VideoList.cpp:69](../../swg-source/client-build-next/src/engine/client/library/clientGraphics/src/shared/VideoList.cpp#L69) registers removal; its removal calls Bink removal at 82. [ExitChain.cpp:118](../../swg-source/client-build-next/src/engine/shared/library/sharedFoundation/src/shared/ExitChain.cpp#L118) inserts a newer equal-priority entry ahead of the older one. [Audio.cpp:1394](../../swg-source/client-build-next/src/engine/client/library/clientAudio/src/win32/Audio.cpp#L1394) stops sounds; lines 1430–1437 clear the stored driver and call `AIL_shutdown`, without an explicit `AIL_close_digital_driver` there. Preserve the product's order and call semantics rather than imposing a generic resource-tree destructor sequence.

**Discriminator:** A clean original baseline followed by the same actual engine release path through the bridge, including Bink using that driver. Component lifecycle tests cannot substitute for this observation.

## 4. Narrow one scheduling claim

**Severity: wording correction.** Parent line 70 says a single main-thread pump is already insufficient for observed unsolicited callbacks. A pump serviced only on the next getter/frame/serve does introduce an artificial dependency. Worker-origin or unsolicited delivery alone, however, does not prove every possible main-thread dispatch design invalid. The actual affinity, timely execution and game-lock interactions remain unmeasured. State the narrower dependency failure; retain the explicit candidate status of the dedicated callback lane. Do not infer universal suspension from header prose or no-device preference observations.

## Artifact and acceptance checks

The parent's relative link `../../audio-next/whole-subsystem-rival-audit.md` resolves to an existing artifact. Primary source anchors above were checked against the actual files/lines; the parent would benefit from comparable direct anchors for its world/RNG, EOS and shutdown claims. All local links in this rebuttal were checked for file existence (line fragments identify source lines).

Proceed toward the same clean-baseline, real Audio/Sound2d/TreeFile slice proposed in both openings, with callback completion and close ordering explicitly instrumented. Add shared-driver Bink before adopting the boundary for the complete client. There is no basis here to relax fidelity, declare production integration, or convert finite observations into universal equivalence.

### Same-pass revision check

The parent architecture changed during this review; the terminal hash check observed `f7a4e38acc8df81ecd115d1f87d64da561b93006dbf33c0136145c9117b5ebf0`. A targeted reread confirms revised line 70 narrows the pump claim and new line 86 explicitly supplies the cross-channel callback frontier, distinguishes it from vendor quiescence, preserves admitted callbacks during Closing, and labels trampoline ACK waiting unproven. Thus sections 2 and 4 above identify gaps in the opening snapshot that are now addressed **at design level**; the actual scheduling/retirement evidence is still an integration gate. The earlier line references refer to the original reviewed hash.

The parent also supplied a prospective combined schedule: a locked request waits for reverse TreeFile work while an unrelated worker EOS reaches shared game state. Add it to the real-engine observation matrix: separate locked-I/O and idle-EOS checks do not establish the combined admission/lock behavior. This is not an observed deadlock. Neither an exact number of callback executors nor literally zero-delay execution follows from that schedule. I did not read the other review behind this suggestion. No further review stage was undertaken.
