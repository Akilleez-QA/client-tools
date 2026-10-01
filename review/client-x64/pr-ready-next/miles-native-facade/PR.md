# Add native Miles facade adapters

Adds the direct-provider implementations of the ClientMiles declarations, native ABI/callback adapters, startup/file registration adapters and exception-to-fatal boundary. This is the native facade, not the pipe backend or game selection.

This source-only package adds 15 production files (+945/−0). Review base: `8ebfbe2c8b8f7efa72250558ea45cba208c43f6f`; head: `0fb8da90bd7e59c054b4932513ca6ce60b020c6a`. It is stacked on `review-ready/client-miles-contracts`; predecessor source is excluded from this delta.

Compiling this native target requires the genuine Miles SDK and matching provider/toolchain. No SDK headers, libraries or binaries are redistributed.

Introduced files match their pinned pre-Bink blobs byte-for-byte except the standalone comment clarifications in `ClientMiles.h` and `protocol/miles_wire.h` from foundation 1. Existing notices are preserved; all non-comment source lines are unchanged. [Historical core checkpoint](https://github.com/Akilleez-QA/client-tools/commit/d1c5903de35586dc8cfb0939a5da1756cca43179) records their source provenance; the per-file receipt retains exact revision/blob/SHA-256 identities. Later Bink and game-selection edits are not imported.

These foundations are dormant: no existing project, game backend selection, build script or workflow changes are included. The unchanged complete build entry points arrive only in step 7 after the source closure exists. Existing integrated build/test evidence remains historical; no build, test or runtime was run for this split branch, and it does not independently enable audio or establish callback fidelity, shutdown behavior or heap safety.
