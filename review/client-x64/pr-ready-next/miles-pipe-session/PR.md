# Add the Miles pipe facade and session composition

Adds the pipe-backed ClientMiles API, channel/live channel, session/core and scoped source-image ownership, fatal boundary and guarded development Audio mapping header. PipeCore.cpp implements both Session and ScopedSourceImage; those declarations and implementation remain together.

This source-only package adds 11 production files (+1847/−0), above `review-ready/client-miles-host-runtime`. Review base: `7bedd5e2f9778e891c29c2bae0eb4092ab6ede4e`; head: `3430934cedf230e7c5c2a77ae8b9e6f607fb1fe8`. Earlier stack changes are excluded from this delta. Direct internal source include prerequisites are foundations 1, 3, 4; the sequential review stack also retains its preceding packages.

The existing pipe lock probe is included unchanged (+311 lines). `AudioSelection.h` requires explicit development opt-in and is not included by game source in this package. Native and pipe facades are alternative targets, not objects to link together.

All files introduced here match the manifest's pinned pre-Bink blobs byte-for-byte, including existing notices. [Core checkpoint](https://github.com/Akilleez-QA/client-tools/commit/d1c5903de35586dc8cfb0939a5da1756cca43179) records the historical source provenance. The inherited foundation-1 comments in `ClientMiles.h` and `miles_wire.h` were clarified separately; the entire stack is not claimed byte-identical to the unpolished checkpoint. Exact introduced source/test identities are recorded in the per-package receipt.

These sources remain dormant. No existing project, game backend selection, build script or workflow is changed. The unchanged complete build entry points arrive in step 7 after the source closure exists. Static manifest include closure is satisfied; it is not external SDK/engine or linker qualification. Existing integrated build/test evidence remains historical, and no build, test or runtime was run for this split branch. This package does not independently qualify enabled audio, callback fidelity, heap safety or shutdown behavior.
