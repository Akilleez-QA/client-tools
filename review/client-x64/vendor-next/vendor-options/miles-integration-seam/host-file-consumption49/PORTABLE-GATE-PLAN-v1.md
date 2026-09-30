# Host49 prospective first portable gate

Authored only; no compilation or test execution. Production source is unchanged from source-manifest-v1.json. The gate compiles actual FileTokens, ReplyTransaction, protocol48 helper, file-channel and codec. It links no Endpoint, SDK, EngineFileWorker or filesystem implementation and needs no native-header compatibility macro wrapper.

The proposed first attempt is strict clang C++11 (-Wall/-Wextra/-Wpedantic/-Werror) with ASan/UBSan, nonrecovering sanitizer errors and leak detection. The runner refuses to overwrite evidence-v1, verifies frozen inputs before and after, requires seven named positive scenario markers once and a single raw check-count summary, and stops at the first failed phase with no retry. All commands/status/output are preserved.

## Seven positive scenario groups

1. One live slot with client wire identities File/777/91 then File/888/92: SDK tokens resolve to those exact remote identities even though the host registry has only one slot. Close/reopen returns a strictly newer token; the prior token cannot resolve. First status0x80000001 remains exact.
2. Normal failed open status0 publishes no token; later success status7 remains exact and cannot reuse the failed attempt's token.
3. Explicit pre-send cancellation and Prepared destructor cancellation both free reservation capacity while consuming token numbers permanently.
4. Requested5/returned3 read copies exactly three bytes into the original destination with before/after sentinels intact; zero read accepts a null zero-capacity destination. ACK is absent before consumption, validates against the exact retained Request/registration afterward, and result is withheld until observed ACK write completion. Close invalidates the token only after normal result consumption.
5. Null read destination, short capacity, and mismatched client wire target reject during construction before send and leave an existing live token resolvable.
6. Signed seek INT32_MIN is preserved as exact wire bits through the real decoder and reconstructed without implementation-defined signed conversion.
7. One-slot capacity rejects a second reservation before another send and preserves the caller's output value.

Token exhaustion at UINT32_MAX remains source-reviewed: the gate does not issue billions of opens or add a production testing backdoor. The host never receives the client's native local file handle; zero-client-handle fidelity remains established by44/46, not newly inferred here.

## Six isolated negative lifetime subprocesses

Modes are `issued`, `failed-context`, `failed-status`, `failed-read`, `failed-close`, and `consumed-ack-uncertain`. Each creates a real transaction, asserts the required pre-death state, absence of a normal result, retained capacity where applicable, and no retry/rollback. Read malformed-return extent must leave the destination untouched. Close scalar-result corruption must not free the closing record. Consumed read with missing ACK write completion retains data/token responsibility without exposing an SDK result.

Only after all prospective assertions pass does the subprocess arm its terminate oracle. Destroying the unresolved transaction must call the real production destructor's std::terminate. A test-only terminate handler prints exactly `EXPECTED_TERMINATE <mode> checks=<n>` and exits73 using _Exit. Earlier assertion failures/unwinding cannot accidentally count: an unarmed handler exits74 with a different marker. Returning from the prohibited destructor is a failure. The runner requires the exact expected output and status for each mode, separately from positive assertions.

These subprocesses intentionally test nonreturning failure policy. _Exit skips cleanup and leak reporting; their outcomes are **not** normal cleanup, absence-of-leaks, vendor shutdown, or file-close evidence. There is no intentionally leaked live object in the positive gate. Death modes model transport/validation uncertainty with crafted wire data, never a real SDK, allocator-fault workload or external process termination.

Review tests.cpp, runner and freeze before authorizing one attempt. This document itself authorizes no execution, native work, or modifications to production source.
