# Zero-count read coverage supplement

Both portable sources built on their first attempts with warnings-as-errors and ASan/UBSan. Frozen file26 passed: the scripted read was invoked exactly once with local key0, requested count0 and a nonnull destination, then returned raw0 and no bytes. Its encoded successful reply contained only the128-byte fixed frame.

The private mutation changed only `resize(count ? count : 1)` back to `resize(count)`. The same test exited1 with the expected `zero-count read callback received null destination` assertion. It did not dereference null or call any engine/vendor code. This result demonstrates that the new assertion detects the earlier behavior.

Frozen source SHA256 remains0c5253d7f2a3a7b06ba54af756f170eca6c5f3b84fbbdce952a5700de6a64e27. The source archive and first157-assertion receipt already bound that nonnull-staging implementation. The parent's earlier inspection was of the in-progress source before freeze; this supplement addresses missing coverage and is not a repair of frozen26. No frozen archive, receipt or source changed.

`evidence-v1/results.json` SHA256 is35255922cac5b3f82b81169c7c29f644d8a5d25d4d8cb8c06fdbbc331201888a. It records source/compiler/test/executable identities, mutation text/hash, build exits0/0, run exits0/1, exact expected markers and unchanged inputs. Logs and commands are retained beside it.

Delivery state: checked. Outcome: passed for zero-count pointer/byte behavior and its controlled mutation. No engine, vendor, VM, real file callback or allocator-fault workload ran. This does not resolve the original executor, publication or uncertain-disconnect ownership prerequisites. Parent controls further integration. `packet-manifest.json` uses flat packet-relative paths mapped to `{bytes,sha256}`, rooted at this directory; the packet contains text only.
