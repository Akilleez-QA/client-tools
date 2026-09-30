# Prospective protocol48 portable first gate

Status: authored for source review only. No compiler, test binary, runner, SDK, VM, native ABI, engine, mapper or endpoint has been executed for this gate. Candidate production files remain those in source-manifest-v1.json. test-freeze-v1.json separately pins the source manifest, all of its listed source inputs, this document, the authored test and runner. Reviews are not executable inputs and are excluded from the freeze. No additional copied production dependencies are introduced.

The single prospective command, after parent review and authorization, is `python3 run-portable-v1.py` from this directory. It validates the freeze, refuses an existing evidence-v1 directory, performs one strict C++11 clang++ build with ASan/UBSan, and runs the resulting binary once only if the build succeeds. Build/run limits are 120/30 seconds. Failures, including compilation failures and timeouts, remain in evidence-v1; there is no retry, cleanup or overwrite path. Any post-attempt revision requires preserving that attempt and a separately named gate, not rerunning this script into the same directory.

The translation units are portable-v1/tests.cpp plus actual candidate file_protocol.cpp, file_channel.cpp and codec.cpp. Headers come from the existing narrow candidate dependency tree. No callback services, portable worker substitutions, endpoint facsimile, native shim or external test framework is compiled.

Eight named scenarios are required exactly once, plus a single check-count summary. The raw logs, exact commands, sanitizer settings, exit statuses, input-change check, test-freeze digest, output digests and scenario counts are retained. The check count is diagnostic, not a quality score. No count is predicted before execution.

| Scenario | Concrete oracle |
| --- | --- |
| Independent golden install/reply/ACK bytes | Literal 48-byte headers, literal 8-byte registration, fixed numeric offsets and all other bytes zero; complete frame equality; historical order of all 61 API opcodes plus control values |
| Bounded/vector Call encoding | Empty, first-only, second-only and both payloads; byte equality plus independent payload/field offsets; exact capacity and surrounding sentinels; null/short buffer, invalid header/handles/reserved field and malformed/overlarge payload rejection |
| Install request validation | Exact allowed shape; every forbidden Call field, valid-but-forbidden handles, low/high origin bytes, zero registration, valid extra payload/trailing byte, every truncated length, invalid retained expected header; output remains unchanged |
| Install reply validation | Each allowed status, success exact registration and refusal zero echo, wrong/zero echo, forbidden scalar/handle/value/span/mask fields, unknown statuses, correlation mutations and malformed lengths; enum remains unchanged on rejection |
| Retained ACK validation | Expectations captured from actual decoded FileOpen/Close/Seek/Read Requests for causal and unsolicited origins; all retained origin fields, registration, original opcode; every forbidden Call field; distinct EOS ACK rejection; default Request/zero registration cannot capture expectation |
| Typed encoder bounds | Exact-size guarded buffers; null/one-byte-short rejection; invalid install/ACK expectations/status; buffer and written unchanged on failure |
| Stream success | Nonnull and null aliases both require exact parent echo; wrong/missing echo, valid wrong alias kind, partial BorrowedSample handles, all unrelated result fields, correlation and length mutations; alias output unchanged on failure |
| Old versions | v1/v2 rejection on vector and bounded Call/Result encoders, Call/Result decoders, EOS encoder/decoder, and typed protocol surfaces; old encoders/decoders preserve output sentinels |

The ACK scenario deliberately validates an identical ACK twice: stateless validation must not be confused with one-time consumption. It does not simulate a mapper or claim to prove duplicate/early/wrong-session settlement. The already-proposed later mapper composition remains separate. Likewise the stream helper exercises only success validation, not stable alias ownership or a stream backend. The generic StartupBridge reply decoder is unchanged and not copied into this narrow build; its callback-zero rule is supported by source review, not a new generic-decoder execution claim.

The fixed-writer no-allocation claim is checked by source inspection of the actual bounded path, not by a global allocation hook or engine allocator workload. Installation success is a reported protocol outcome only. No real installation, transport authentication, SDK return, callback consumption, producer quiescence or shutdown behavior is enabled by these tests.
