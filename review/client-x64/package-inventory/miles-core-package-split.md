# Miles core: proposed foundational split

Client scope only; the server counterpart map is a separate queued task. This addendum replaces only the oversized `miles-session-core` grouping. It is a static packaging proposal, not seven newly reviewed or qualified branches.

Authoritative final implementation: `eca74ffa5741f608a1417944b2e2602868936517`; base: `949451032647e45e42c3aaef3f41b132c8af36e3`. Reuse core blobs at `d1c5903de35586dc8cfb0939a5da1756cca43179`, plus the independent host-runtime lifetime repair `b9d3408f1c8c2b39c8ce0ba8dc777cb7a215ab72`. Final accounting remains **91 production files, +8,593/-0**. The initial foundations contain **8526 lines**; later game/Bink deltas restore the exact final blobs recorded in the JSON. Supplemental Audio/build/workflow hunks keep their existing parent-map accounting.

| Step | Focus | Files | Core lines | Final accounted +lines | Direct include prerequisites |
| --- | --- | ---: | ---: | ---: | --- |
| 1 | Contracts, wire codec and owned replies | 17 | 1246 | 1263 | None |
| 2 | Native Miles facade and ABI adapters | 15 | 945 | 945 | 1 |
| 3 | File protocol, transport and reply transactions | 20 | 1331 | 1332 | 1 |
| 4 | Engine worker, admission and client callback ownership | 14 | 1589 | 1589 | 1, 3 |
| 5 | Native host backend and callback runtime | 14 | 1568 | 1600 | 1, 3, 4 |
| 6 | Pipe facade and session composition | 11 | 1847 | 1864 | 1, 3, 4 |
| 7 | Core build entry points and existing Audio adaptation | 0 | 0 | 0 | 1–6; Audio source prerequisites |

Steps 1–6 add dormant source foundations; none selects the new game backend. Step 7 adds the unchanged existing build entry points after their source closure exists, plus the original Audio callback extraction and guarded facade-compilation hunks. Actual backend selection stays in the existing later game-integration package. No stubs, altered contracts, temporary implementations or truncated runners are proposed.

## Concrete dependency boundaries

- **1 — contracts:** public `ClientMiles.h`, wire/resource registry, codec, version/metadata reply formats, image/buffer declarations and EOS protocol. `backend/reply.h` belongs here because both host and client consume the owned reply. Use its pre-Bink blob; copying final HEAD would pull Bink types into the foundation.
- **2 — native facade:** `api/native`, `api/private`, and `api/plain_*`; the public API comes from step 1. Native SDK headers are build requirements, not a dependency on the pipe implementation.
- **3 — transport/file transactions:** endpoint/bootstrap, file channel/protocol, tokens/reply transactions, selected file services, callback signatures/guard and host context. The engine `AudioFileCallbacks.h` declaration is introduced here; its implementation comes with the existing Audio adaptation in step 7.
- **4 — client callback ownership:** coordinator, engine worker/job, file owner/association mapper, client reverse runtime and EOS dispatch. Real engine headers/settings are compile/evidence prerequisites. These files share admission, completion and ownership behavior; no include SCC forces a larger host/client bundle.
- **5 — host backend:** dispatch implementation/resolver, native SDK operations, image upload state, native metadata/version, host reverse runtime/EOS trampolines and host entry point. Include the existing deleted-destructor repair. This introduces the host without selecting it from the game.
- **6 — pipe session/facade:** complete `api/pipe`, failure boundary and `dev/AudioSelection.h`. Session, proxy/image lifetime and public pipe forwarding form the remaining client composition unit.
- **7 — build/Audio handoff:** original core `build.py`, `sources.json`, README and ignore file; exact core-only deltas to `Audio.cpp` and its project. Stack Audio deltas on `audio-native-contract` or preserve equivalent patch context. Project conversion belongs to the build/evidence dependency category; do not claim it is a source dependency of every dormant bridge file.

## Actual coupling

The direct file include graph has **0 nontrivial SCCs**. Folding same-stem implementation/header files yields:
- `api/pipe/PipeCore`, `api/pipe/Session`.

`PipeCore.cpp` implements `Session` and `ScopedSourceImage`; keep those declarations with their implementation. This is the concrete private-header coupling. The host SDK trampolines/install/runtime and client worker/owner/runtime groupings also preserve semantic and link ownership, but are not falsely labeled include cycles. The JSON retains every resolved include edge and external include.

## Tests, builds and shared deltas

| Step | Existing test files introduced |
| --- | --- |
| 1 | `eos_protocol.cpp` |
| 4 | `engine_worker_context.cpp`, `engine_worker_context.h`, `lock_admission.cpp` |
| 5 | `upload_binding.cpp` |
| 6 | `pipe_lock_probe.cpp` |

Tests move unchanged with their source closure. The existing runner is introduced only in step 7. The EOS protocol CI hunk from `892343c92` may accompany step 1 if the wire workflow is already present; otherwise defer the hunk until that workflow base exists. This changes no test claim.

Shared paths cannot be restored wholesale from final HEAD: `protocol/miles_wire.h`, `wire/codec.cpp`, `wire/resource_registry.h`, `admission/coordinator.cpp`, `backend/reply.h`, `backend/backend.h`, `api/pipe/PipeCore.cpp`, `api/pipe/Session.h`, `host/host.cpp`, `api/pipe/LiveChannel.cpp` and `bootstrap/common.h` contain later game/Bink deltas. Each exact originating commit and foundation/final blob is recorded per file. Keep later Bink header/types, command handling and admission changes in their Bink packages. `Audio.cpp`, its project, and the workflow require component-only hunk extraction, not final-file copying.

## Assembly recipes

1. Create a foundation stack from the verified upstream base. Introduce step 1 paths and its EOS test using the JSON `foundation_revision`/`foundation_blob`; commit. Steps 2 and 3 can follow in separate commits/branches using the same exact-blob procedure. Original broad commits are provenance, not safe whole-commit cherry-pick recipes.
2. Stack steps 4, 5 and 6. Use the core checkpoint for each file except `host_file_runtime.h/.cpp`, which use the recorded lifetime-repair revision. Add existing tests at their assigned steps. Do not introduce game-selection properties, AudioBootstrap or Bink sources here.
3. Stack the step 7 core runner/manifest and original `4f15b029a`/`5c3170658` Audio/project deltas. Then apply the existing game-selection, Bink and release-build packages in their existing dependency order. Verify their resulting blobs against the authoritative IDs; that future assembly check preserves implementation byte-for-byte.

No branch, build, test or runtime campaign was created for this analysis. Existing integrated evidence remains the baseline and must be described as historical, not fresh proof for each split branch. The per-file machine-readable manifest is [miles-core-package-split.json](miles-core-package-split.json).
