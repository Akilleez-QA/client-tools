# Live bridge v3 repair validation — bounded checks completed

The v2 evidence and its explicitly retracted 32-KiB aggregate-memory claim remain unchanged. Four source findings were accepted. This packet reports a new candidate, not retroactive validation of v2.

The retained store now copies the input once into a staging vector, inserts an empty map entry, and swaps the vector storage into the entry before publishing accounting and the output token. Same-default-allocator swap performs no byte allocation. Existing state is unchanged if allocation throws before insertion; this guarantee is source-derived, with no allocation-fault injection. The ordinary successful-allocation probe observes exactly one 9,020-byte allocation in `stage`; the old implementation produces extra payload-sized allocations. This is not a capacity, RSS, endpoint-overhead or allocator-overhead bound.

The host's simultaneous logical full-image copies at named bind are upload + sealed temporary + retained candidate/entry (the last two exchange the same storage). This source accounting is 27,060 image bytes, plus suffix bytes, for the single permitted attempt. `stage` allocation observations corroborate removal of its extra image copy; whole-process peak allocation was not measured. Controller-side media and framing copies are outside this host-image accounting.

Admission transitions to Draining only after validated backend shutdown returns success and the admission completes. Rejected shutdown leaves Active; Draining admits only SessionClose. The first v3 native synthetic matrix exposed a local ordinal bug: rejection consumed the caller's ordinal, so the next legitimate close failed. That failure is preserved in native v3. The v3b helper advances the shared ordinal only on successful admission, and both integration and synthetic controls use that helper.

Receive checks the callback endpoint before accepting a ready command response. Fault-aware drain checks endpoint reasons before and after storage cleanup. Only PeerClosed at the explicitly ordered final-reply/close boundary is permitted; final SessionClose reply fields still require validation. Already-classified corruption never gains that exemption. Endpoint cancellation can discard bytes or errors first observed after Open transitions to Stopping; this is not an established cross-channel close frontier.

A child owner exists before CreateProcess returns to assignment/resume code. Failure before job assignment terminates and waits for its suspended child and closes process/thread/job handles. The bounded native control uses this same owner with a benign self-child and a genuinely invalid job handle; no SDK code or child instruction is executed.

The prospective gate required native component controls and independent source inspection before any v3 genuine vendor run. Those checks passed before the bounded runs below. The native policy tests supply synthetic operation results and do not themselves constitute vendor success. No engine, malformed-media, playback or allocator-fault workload is included.

## Completed evidence

The v3b native Win32/x64 Debug/Release matrix passes 25 repair checks and all 41 retained-buffer checks per configuration. All four bridge builds pass `/W4 /WX`. New stage behavior makes one exact-payload-size allocation; the unmodified old source makes three and exits 1 in the discrimination probe. v3b's old-control diagnostic short-circuited before filling its view, so it printed zero for that view. v3c changes only evaluation order and confirms the actual published view is 9,020 bytes for both implementations. Both raw versions are preserved.

After independent source review, genuine Debug and Release runs each completed 21 framed requests with the same actual 204/407-ms duration, 22050/11025 rates and 0.25/0.75 volume observations. Released tokens were rejected and normal sample release, original `AIL_shutdown`, and host exit completed. The valid L/R-swap private mutation again returned mismatch status 5; controllers exited 1 as expected only after all 21 requests and normal teardown. Default audio settings remained unchanged, and only each run's private sink was unloaded.

The controller checks child PID identity on both pipes. The host conditionally checks the command pipe's server PID and records a LIMIT if unavailable; it does not provide unconditional mutual authentication or callback-server PID validation. This limitation remains explicit. The final-reply allowance classifies PeerClosed at the ordered close boundary; it does not establish a general cross-channel callback frontier or production close protocol.

Curated text evidence: `evidence-v3-failed/` retains the rejected-ordinal failure; `evidence-v3b/` contains component matrix and genuine runtime; `evidence-payload-v3c/` contains the corrected print observation; `evidence-mutation-v3/` contains the valid-input negative and normal cleanup. `verified-results-v3.json` summarizes only these bounded observations. No SDK, DLL, media, native binary or Wine prefix belongs in a public packet.

The no-playback slice remains a candidate. Playback, callbacks, streams, engine teardown, scheduler fairness, host recovery, real device behavior and full-client fidelity are not tested here. The v2 aggregate-memory assertion remains retracted.

## Oracle and protocol limits

The direct and framed samples share one vendor session, driver, retained image and original DLL. Their agreement checks the exercised bridge calls, not the vendor implementation or an independent audio oracle. The controller checks that initial duration is positive and current position is zero; it does not require the exact observed 204-ms/407-ms totals. The second duration is compared against the direct sample by the host and logged, not asserted against an independent PCM-duration formula. Those figures are observations, not separate fixed-value assertions.

Transport success and vendor success are separate: a framed bind may complete transport with a zero vendor return; this fixture controller explicitly rejects that return. Fixture statuses intentionally group several rejection reasons. Host exit zero after an expected comparison mismatch in the mutation run means ordered teardown completed; only the controller aggregate determines the negative test verdict. No claim of a general application error model is made.

## Independent follow-up

[The independent Astra source/evidence review](REVIEW-v3-independent.md) supports all four targeted repairs within their tested scope. It also identifies two remaining limits: errors first observed during cancellation are not fully classified, and the native build records do not retain output executable hashes at build completion. Runtime hashes match the retained binaries and source records are internally consistent, but this packet does not establish an unbroken source-to-build-to-run attestation. The next tooling revision will capture output identities during the build; no stronger provenance is retroactively claimed for v3b.
