# Client-only stream source result

First portable invocation passed under strict C++11 warnings with ASan/UBSan. Source was frozen before testing; no repair or rerun. Actual host/file channel, native compiler, vendor and engine were not executed.

Source SHA2568d82ce7be513f6ec3694fbbee139b0982a4c60c83a41b14cc401b198b5de12a4; manifest03ac57f78f4ba4c1a674dc980fee7864605d33e2c7497556868d8e63fc64496f; receipt495633e442ebbac3cdc8716c75eb8907b57b58d47c0231911ca2220c4b5803f2.

Three narrow patches: client pipe, opcode-specific reply validation, private API-map parent echo. Nine public stream operations and five existing borrowed controls use the common Sample pointer. Stream proxy embeds its cached borrowed proxy; allocation precedes exchange, parent echo and alias identity are validated before publication, confirmed close/shutdown reclaims both, known refusal preserves and uncertain outcomes poison.

Scripted tests cover the nine operations/five controls, signed fields, optional and aliased time outputs, stable cached identity, null before publication, wrong parent, retarget, null after publication, borrowed-release/owned-only-start refusal, known/unknown close failure, inconsistent alias outputs without mutation, shutdown with live stream and256 sequential open/close cycles. The cycle test checks no cumulative operation cap; it is not a standalone heap-allocation count measurement. Frozen34/35 tests are retained as lineage, not rerun against37.

Current Backend still refuses stream opening and has no stream lifecycle/file implementation. Host dispatcher also retains its prior owned-only Backend admission; borrowed operations are not operational on that host. SessionFiles34 provides coordinator admission preparation only. No file callback registration, readiness boolean, host-file fallback or successful stream execution is manufactured. New host opcode59 must echo its validated parent in result value0/1/2 as documented. No ABI/runtime equivalence claim.
