# Independent file-owner37 successor review

The exact36→37 candidate diff preserves both reviewed lifecycle repairs and every test assertion. The recorded first portable gate passed189 checks. No new concrete defect found in this bounded successor review. This concerns **file-owner37**, not stream-proxy37; no compiler, executable, native worker, engine or vendor was run by this reviewer.

Only the production alignment expression changed, from `alignof(Binding)` to `std::alignment_of<Binding>::value`. The replacement allocation functions and their state moved from tests.cpp into test_allocators.cpp, with extern declarations in test_allocators.h. Their control flow is unchanged. No warning suppression, optimization change or removed assertion appears in the diff. Actual native-toolset acceptance remains a separate gate; this review does not infer it from the portable build.

The compile command explicitly includes test_allocators.cpp. Its global replacement new checks the shared denyAllocation variable before allocating; new[] delegates to it. The test's post-reservation hook shares the same externally linked state and sets reservationFailureTriggered before throwing. The test explicitly requires that flag, no open call, no retained operation, no remaining file identity and zero callback pins. A silently disconnected allocator hook therefore would not satisfy this case. Source inspection identifies the targeted next allocation as Coordinator callback-map insertion after registry/files publication and before operation publication.

Allocation denial still surrounds owner.poll for successful open/read/seek/close and failed-open publication, and surrounds fixed-buffer codec parity calls. The reserved output buffer and fixed writer are unchanged. These tests support no C++ allocation through the tested replacement-new route in those paths; they are not a claim that every possible allocator or native operation is covered.

Both uncertain-sibling order cases remain intact: uncertain read then known close in ordinary slot order, and uncertain seek in a higher slot while a subsequently queued close reuses a lower slot. Both require retention of Uncertain identity after close ACK. The healthy case requires retention after close ACK followed by retirement only after the preceding read ACK. Sticky uncertainty, sibling retention and reservation rollback remain exactly the source reviewed in36 apart from the alignment expression.

Verified all23 frozen manifest entries with zero mismatches. Raw results record compile_exit0 and run_exit0 with ASan leak detection and UBSan halt-on-error. Compile log is empty; run log contains exactly `PASS 189 portable owner/encoding checks; scripted platform only`. The command compiles portable_job.cpp, **not production FileInvocationJob.cpp**: engine worker/event behavior, canonical callbacks, host mapper adoption, vendor shutdown and native fidelity are not established. The portable job deliberately simulates DispatchUncertain after executing an Invocation; that validates owner reaction to the status, not real Windows failure behavior.

SHA256 attribution:

- candidate-manifest-v1.json: `529a71251dc5e4094a54d2e907c668146fd0a7abfbb553aee635517b7067b711`
- candidate/file-owner36/session_file_owner.cpp: `55ed82c47d65452aeac3073ab98dd5f1d5a1a91e2b19d19f2a5fcd66048c7664`
- candidate/file-owner36/tests.cpp: `8efe9969077c2e83d3b2e837f6c366f008932b763c89e682fc02af5b39c3b261`
- candidate/file-owner36/test_allocators.cpp: `bfac51933a5b6b2bf197ae9366d18006636d1d794292ab3f6256a529b4b9ed9a`
- candidate/file-owner36/test_allocators.h: `250754b304e4ac81203701c642116d583707ca425de1aa7f85172a69f59850a9`
- portable-v1/results.json: `2bc10b8b07fefa4739bf37f9345a25a02b544601cf8f1710ed150ca2cad246a6`
- portable-v1/run.log: `2db1fc760839a1664b3c93aa1091ff9469262f04336258fdf3d7c34e0ae94f78`
- portable-v1/compile.log: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
