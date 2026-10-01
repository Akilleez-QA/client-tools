# Archive storage and payload bounds

Prepared above published client wire PR23 at `e6738a9f5b912f62c496f866a911fa33b2539908`; candidate `085a62e3358e7b51c5198c93bb1581864020c3fb` has five source commits, five production files, +117/−100. No test or build files are added by this package.

[PR description](PR.md), [source and evidence identities](receipt.json), and [independent review](INDEPENDENT-REVIEW.md). Root checked all five final source hashes and every referenced published evidence artifact. Original source patch identities are preserved. The separate wire prerequisite remains outside this proposed diff.

Historical native component evidence covers 85 ByteStream checks and 34 decoder checks on each ABI/configuration. Final portable source manifests match all five packaged files; preserved command records contain 71/71 Win32 and 78/78 Win64 (runtime checks plus width compilation), without a new execution. [Historical writer records](historical-unicode/RESULTS.md) and [command assessment](historical-unicode/recorded-command-assessment.json) retain that distinction.

The native Unicode decoder-stage translation unit predates the final writer guard; only its decoder function is byte-identical. No fresh full build or allocation-fault injection is claimed. Successfully decoded headers remain consumed on payload failure, prior aggregate members/callbacks are not rolled back, and later writer allocation failures may follow header publication. The private free-list and reference counts retain their existing concurrency contract. Existing runners and reproduction requirements are linked in the description; a broader fixture history is not silently imported.
