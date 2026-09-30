# Minimum allocator block size

The candidate requires every allocated block and every split remainder to fit its future free-list representation. In the untracked product layout, native x64 reports `Block=24`, `AllocatedBlock=24`, and `FreeBlock=56` bytes; the aligned free-node size is 64. The previous size calculation permitted 48-byte small allocations and its split rule could leave a 48-byte remainder. Win32's corresponding values are 12, 12, 28 and 32, so its existing minimum already fits.

The patch adds a minimum to the checked size calculation and retains the old subdivision condition with an additional free-node-size check. It changes five added lines and one removed line in the production file.

| Native VS2013 configuration | Build | Runtime checks |
| --- | --- | --- |
| Release Win32 | pass | 1,622 / 1,622 |
| Release x64 | pass | 1,622 / 1,622 |
| Debug Win32 | pass | 1,622 / 1,622 |
| Debug x64 | pass | 1,622 / 1,622 |

The probe checks 513 requested sizes, payload preservation, actual allocation/free/reallocation cycles, block-chain integrity and region-edge requests below 4 MiB. It checks the Win32 size formula against the previous expression. All runs use the product's untracked definitions. The exact expected count, native structure sizes, build/run exits and candidate source hash are in `native/results.json`.

Production source SHA-256: `172dcd8958b78af24ef4b08f1f0a2409e89ae81665fb2ef6717b9a24d161467f`. The private diagnostic includes this implementation with include-path adaptations, recorded separately. Real native core libraries are linked; no allocator implementation is stubbed.

These are candidate invariant tests, not a full-client heap proof. The parent did not run the previous invalid allocation sequence. A separate Audio fixture now reaches its real TreeFile callbacks and passes on Debug x64 when linked with this candidate; its commands and logs are recorded in the Audio packet. Full-game operation, tracked layouts and unrelated allocator behavior remain separate acceptance work.
