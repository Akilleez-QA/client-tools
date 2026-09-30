# Native86 affected-closure gate — preparation only

No staging/VM/compiler/link/runtime, SDK load, Git or product edits. After independent and parent review, prospective invocation is `python3 native86/run-approved-native-v1.py --approved-28-objects`. Fresh C:/native86 and native-evidence-v1; one run, stop first failure, preserve raw output, no silent repair/retry.

Actual source is new pipe-composition86 (77+80+81+83), public70 header unchanged. Explicit public merge retains81's two text delegates and80's exact file delegate:53 Core delegates total. Backend gains genuine stream open/getter/close; registry adds typed Stream parent/reservation/invalidation. from77.patch and per-file provenance make the merge reviewable. No portable tests/providers or unused historical native wrappers are staged.71 gate inputs use the same production source/header paths as77, all copied from86. All composition files are separately pinned by its full source manifest.

## Exact selection

selection.json records the six changed source/header paths and each unit's intersecting native77 quoted closure. inputs/units.json contains only selected objects, in original order:28 total,14x86/14AMD64. Source changes select public wrapper/Core and actual host Backend anchor; changed Session/PipeCore/registry headers select all other affected real consumers. No source/include-edge changes require guessing beyond the recorded closures. Actual compiler include hashes are still required for every frozen quoted header.

Seven omitted unchanged units: x86 host-callback-context41/call_context.cpp, host-candidate/host_dispatch.cpp, session-file-admission34/coordinator.cpp, callback-reentry47/invocation_guard.cpp; AMD64 plain-boundary52/failure_boundary.cpp, session-file-admission34/coordinator.cpp, callback-reentry47/invocation_guard.cpp. Their sources and transitive recorded local headers are unchanged. This gate does not rebuild them or link prior objects. A later link/composition must select matching known objects explicitly.

Actual Win32 host.cpp is first and compiles Backend against genuine SDK. Its exact AIL import set is previous5 plus AIL_open_stream, AIL_stream_sample_handle, AIL_close_stream. Other selected units' exact import sets are unchanged. AMD64 public wrapper must reference exact53 private Core delegates plus reporter/fail/reentry guard, with zero AIL imports. Existing real LiveChannel/runtime/job/selected-service references remain required; no canonical fallback or worker supplier. Same native77 symbol parser and recorded decorations; no function-pointer casts are added.

## Tools, source identity and stopping

Runner delta from77 changes only destination, approval token, computed matrix cardinalities and scope text; units/import/delegate input deltas are explicit. Preserve /c /W4 /WX /EHsc /MTd /Od /Ob0 /Y- /showIncludes and actual architecture forced guards. Genuine SDK included only by selected host SDK units; actual engine/STLport headers remain forbidden in this modern closure. External EngineFileWorker implementation remains unlinked; object refs are not engine runtime evidence.

Pinned toolchain.json and reused35-manifest.json are copied byte-identically from77. Verify all9536 reused snapshot entries and actual selected cl/dumpbin/vcvars hashes before/after; Mss.h SHA966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e. System headers are observed once per reached compile, not blanket before/after attested. All71 staged inputs are checked before/after. Local driver checks product49d0/clean state and unique paths, uploads only frozen archive, invokes once, then collects curated commands/logs/headers/symbols/receipts. SDK/objects/PDB remain private. Inherited environment-ARCH files remain VM-only under the curated allowlist; no complete environment-log export claim.

IDENTITIES.json pins source/input manifests, remote runner and local driver. Source hash/copy and Python syntax checks during preparation are not compilation. No native64 library, product adoption, operational streaming, EOS, file replacement/null semantics, callback quiescence or paired normal teardown is established by this prospective object gate.
