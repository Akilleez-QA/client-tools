# Add Miles engine-worker admission and client callback ownership

Adds the real engine-worker invocation jobs, admission coordinator, session file owner, host association mapper and client file/EOS callback runtime. Their shared ownership chain keeps callback work and completion associated with the admitted session.

This source-only package adds 14 production files (+1589/−0), above `review-ready/client-miles-file-transport`. Review base: `9ef7a2c7dd99f8cdb7d351ee80704628aa53aa70`; head: `97dc8c1f9289fadf8f044dd07f07db7d57c95094`. Earlier stack changes are excluded from this delta. Direct internal source include prerequisites are foundations 1, 3; the sequential review stack also retains its preceding packages.

The existing engine-worker context files and lock-admission test are included unchanged (+209 lines). Engine-worker compilation requires real engine headers/settings; this is not a replacement thread/TLS implementation.

All files introduced here match the manifest's pinned pre-Bink blobs byte-for-byte, including existing notices. [Core checkpoint](https://github.com/Akilleez-QA/client-tools/commit/d1c5903de35586dc8cfb0939a5da1756cca43179) records the historical source provenance. The inherited foundation-1 comments in `ClientMiles.h` and `miles_wire.h` were clarified separately; the entire stack is not claimed byte-identical to the unpolished checkpoint. Exact introduced source/test identities are recorded in the per-package receipt.

These sources remain dormant. No existing project, game backend selection, build script or workflow is changed. The unchanged complete build entry points arrive in step 7 after the source closure exists. Static manifest include closure is satisfied; it is not external SDK/engine or linker qualification. Existing integrated build/test evidence remains historical, and no build, test or runtime was run for this split branch. This package does not independently qualify enabled audio, callback fidelity, heap safety or shutdown behavior.
