# Current experimental source selection

This directory contains frozen experiments, not one production library. Product `integration/client-x64-next` at49d0eeed4 has no Miles bridge adopted. Only explicit build recipes select sources; neither historical snapshots nor all candidate classes should be linked together.

The user has designated this bridge temporary. The durable source boundary must
follow the [native-Miles upgrade shape](TEMPORARY-MILES-BACKEND.md); none of the
wire types below belongs in game-facing audio policy. The new startup facade
candidate remains separate from the frozen 23-request proof.

| Responsibility | Selected source | Current boundary |
|---|---|---|
| Fixed-width frames | protocol-candidate/miles_wire.h; transport-candidate/codec.h/.cpp | Structural encoding/decoding only |
| Resource identity | transport-candidate/resource_registry.h; host-candidate/registry_resolver.h | Session/admission and vendor completion supplied by caller |
| Admission/leases | coordinator-candidate/coordinator.h/.cpp; live-bridge-candidate/admission.h | Model plus limited one-lane integration; callback retirement not implemented |
| OS pipe I/O | pipe-transport-candidate/endpoint.h/.cpp | Existing slice input; pipe-drain23 is a separate tested-candidate repair pending independent review |
| Process/channel fixture | live-bridge-candidate/common.h | Experimental launch/watchdog/cleanup; no production failure UX |
| Startup and driver | startup-bridge23/backend.h | One owner in the new composition candidate; not yet product code |
| Startup values and text | startup-metadata-v4/metadata.h, metadata_wire.cpp, metadata_host.cpp | Reviewed five-operation component; retained path bytes survive shutdown |
| Version resource | session-version22/session_version.h/.cpp, session_version_host.h/.cpp | Direct query of supplied verified/held module |
| Framed startup response | startup-bridge23/reply.h | Owns copied text; maps distinct status meanings |
| Fixture oracle and scenario | startup-bridge23/fixture.h, bridge.cpp | Test-only expectations and restoration kept out of backend |

`startup-bridge23/PLAN.md` defines the new23request, no-sample experiment. Its build/runtime result must be read before making any integrated claim. It does not rerun the older21request bind/parameter/release slice. `parent-startup23` independently tests only reply validation/ownership, not the transport or DLL.

Other components remain useful but are not automatically part of that slice: scalar dispatch, retained sample buffers, chunked upload, WAV metadata and the dormant Audio file seam. `SessionLifecycle` is an alternative older lifecycle candidate with different driver-close ordering; do not combine it with Backend. Resolve actual lifecycle policy against the game's behavior before production adoption.

The fixture's one-lane/no-callback restriction is deliberate scope, not a scheduling design for the game. Missing integration still includes real reverse TreeFile execution, unsolicited EOS and allowed reentry, registration retirement/close frontiers, Bink with the original shared driver, actual game policy, and representative fidelity acceptance. The original-engine teardown baseline remains failed and its prohibited workload is not rerun here.

Do not count history directories, mutations, staging copies or test tools as production client code. Conversely, dense physical-line counts understate review effort. The maintainer review and each source-bound result define evidence limits; their existence is not full-client acceptance.
