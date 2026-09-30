# Startup metadata revision 4 — two-path forwarding discrimination

The precise remaining v3 false pass is closed by this test: dispatch both valid private `.` and `miles`, each after resetting the SDK to the other path, then compare each immediately copied result to its direct-call expectation. End at `miles` before startup. The metadata component and owner implementation are byte-identical to v3; only this host fixture and build/runner identities changed. V3 evidence remains frozen.

| Check | Debug | Release |
| --- | --- | --- |
| Native v120 Win32 portable component | 39/39 | 39/39 |
| Native v120 x64 portable component | 39/39 | 39/39 |
| Genuine original DLL, private Wine/null sink, idle driver | 35/35, exit0 | 35/35, exit0 |
| Private hardcoded-`miles` mutant | 34/35, exit1 | 34/35, exit1 |

The mutant fails exactly `host_test.cpp:31`, the new dot response comparison. Direct `.` yields one NUL byte; direct `miles` yields seven bytes including NUL. The mutant instead reports seven bytes for the dispatched dot. These observations show the test detects this exact ignored-input defect; they are same-vendor return-text comparisons, not complete engine fidelity or a documented non-mutating SDK state query.

Native six-entry matrix uses `/W4 /WX`; all build input snapshots remain unchanged. Genuine and mutation PEs were checked against immutable pinned build receipts before execution. `build-source-match.json` also verifies current component/header/test contents match those recorded at native build time.

- Positive receipt: `215e8cd3e725f5d4d6c33978ebbdb710764e4e358607ebb2f49adabf1360f47b`
- Positive Debug PE: `af4112f13563aae0772b93683cc2b2156c40ef2b9f284bec29e1d0e1017a64b1`
- Positive Release PE: `afe90c6fc8cadb6f3f0eda0b26e063042a32f42ec6ab9abac14babba252b138c`
- Mutation receipt: `03a12d11b54dd3c0905edf1bdc7de1f55003a64b7aa6e7a1ecd13ba1dfe62dc5`
- Mutation Debug PE: `44f319468a07511888146048f2f6db5a4be18b5b17bed616c0a4341eba118202`
- Mutation Release PE: `9e3e709c493808b81dbc57ac40f273c8d75954f9477c4e0ad7f28a7bd955e830`

Both positive and mutated runs report preference restore and shutdown called. Owned sinks were unloaded, cleanup errors were empty, and desktop defaults were unchanged. This banner proves call flow, not every internal SDK resource's destruction. Two cleanup injection tests pass again; both entrypoints reject optimized Python before side effects. ALSA control-device lookup messages remain visible in raw logs.

SessionInputs still requires readable valid input spans and must outlive vendor shutdown. It retains attempted requests through failed response construction; its logical byte budget is not an allocator-capacity/RSS claim. Huge frame tests are codec-only; arbitrary SDK path sizes are unproven. Session/lane admission, complete driver ownership, error causality and client-visible text lifetime remain future integration responsibilities.

No playback, samples, streams, callbacks, media parsing, Audio/engine fixture, product source changes, commits or pushes occurred. The known PCM hash in runner setup is not media-parser coverage. Original SDK/DLL/plugins/media, PE files and private prefixes are excluded from the review packet. This does not adopt the component as a production backend.

Any later supplemental retention test has its own source, binary and results. It does not change this 39-check native baseline or these 35-check vendor observations.
