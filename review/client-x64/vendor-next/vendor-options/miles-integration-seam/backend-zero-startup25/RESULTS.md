# Zero-startup supplement

The pure test passed against frozen facade24 with ASan/UBSan. Its test-only framed channel returned one valid startup0 reply. The facade returned0, then both shutdown and private close refused locally with WrongState. Exactly one channel request occurred; finish was never called; scope destruction destroyed the test channel. Input hashes remained unchanged.

This records the current missing graceful-close path. No SDK, Wine or native executable was invoked, and no SDK shutdown policy or recovery behavior is inferred. Frozen facade24 was not changed. The test source and `evidence-v1/results.json` retain the command, source/compiler/executable identities and observed flags.
