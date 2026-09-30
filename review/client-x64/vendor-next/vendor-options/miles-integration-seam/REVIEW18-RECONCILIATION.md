# Composer/Grok round 18 reconciliation

These CLI workers inspected the earlier live-bridge v2 source and reports. Their raw reports remain unchanged. The parent inspected the current source and raw observations before classifying findings. Model agreement is not a new runtime test.

## Accepted limits and fixes

- Grok correctly identifies the control sample as a second handle in the same vendor session, using the same retained image. This is a call-path comparison, not an independent vendor/audio oracle; RESULTS-v3 now states that explicitly.
- Exact 204/407-ms durations were observed. The first controller check requires positive duration/zero position, and the later read is compared to the direct handle in the host. Neither checks an independent fixed-duration oracle. The claim is narrowed accordingly.
- Host peer-PID validation is conditional and command-channel only; the controller checks both child pipe PIDs. Full nonce exchange does not turn this into unconditional mutual authentication. This remains an explicit boundary before a production transport.
- Premature shutdown-to-Draining transition was a genuine source issue. The separately recorded v3b repair commits the transition after successful backend completion and preserves ordinals across rejected admissions. Native policy controls cover that helper; they do not exercise a refused real vendor shutdown.
- Mutation-v1 metadata originally carried the positive bridge hash in a runtime summary. Its explicit PROVENANCE file records the discrepancy and the actual mutation input/binary hashes. Those old logs are preserved. New mutation-v3 has its own source identities and a deliberately adapted controller that continues through cleanup after the expected mismatch.

## Claims not adopted as production defects

- Composer said the evidence directories were absent; they exist locally and were not yet published at its inspection. That part of its report cannot establish anything about the actual native/runtime evidence.
- Separate control/framed sample handles and duplicated setters are intentional parts of this limited comparison. They do not make the test an independent oracle, but their mere duplication is not an ownership defect.
- Transport status zero with a zero vendor bind result preserves the distinction between a completed call and a failed vendor operation. The controller requires nonzero bind success. General error taxonomy remains future design work, not an observed false pass here.
- Host PASS after mutation means normal session cleanup. The mutation controller records status 5, completes all 21 requests, and exits 1. It is incorrect to read that host line alone as the aggregate result. The production positive controller aborts on an unexpected status, as its source shows.
- Retained input cannot be retired while the vendor may reference it. The limited fixture holds it through real shutdown; no successful playback or callback-quiescence contract follows from that lifetime choice.

## Next discrimination before broader claims

Independent PCM-duration expectations and distinct control input storage would strengthen the limited numerical oracle. They do not replace playback, callback, stream, engine-lifetime, device or game-fidelity acceptance. No such broader acceptance was run in this round, and the failed real-engine teardown fixture remains unresolved and was not retried.
