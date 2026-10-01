# Add Miles file transport and reply transactions

Adds the Windows endpoint/bootstrap support, file request protocol/channel, callback signatures, opaque file tokens, selected services, callback invocation guard and host call context. Reply transactions track preparation, send, consumption and acknowledgment before exposing their result.

This source-only package adds 20 production files (+1331/−0). Review base: `0fb8da90bd7e59c054b4932513ca6ce60b020c6a`; head: `9ef7a2c7dd99f8cdb7d351ee80704628aa53aa70`. It is stacked on `review-ready/client-miles-native-facade`; predecessor source is excluded from this delta.

The Audio admitted-callback header is a declaration only here; its existing implementation and project adaptation arrive in step 7. Engine worker, client callback owner and host callback runtime are later packages.

Introduced files match their pinned pre-Bink blobs byte-for-byte except the standalone comment clarifications in `ClientMiles.h` and `protocol/miles_wire.h` from foundation 1. Existing notices are preserved; all non-comment source lines are unchanged. [Historical core checkpoint](https://github.com/Akilleez-QA/client-tools/commit/d1c5903de35586dc8cfb0939a5da1756cca43179) records their source provenance; the per-file receipt retains exact revision/blob/SHA-256 identities. Later Bink and game-selection edits are not imported.

These foundations are dormant: no existing project, game backend selection, build script or workflow changes are included. The unchanged complete build entry points arrive only in step 7 after the source closure exists. Existing integrated build/test evidence remains historical; no build, test or runtime was run for this split branch, and it does not independently enable audio or establish callback fidelity, shutdown behavior or heap safety.

Direct source includes require step 1; step 2 is an ordering prerequisite of this review stack, not an asserted direct include dependency.
