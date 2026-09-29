# Remaining acceptance work

Tracked follow-ups, 2026-09-29. These records separate required observations from
successful bounded fixtures. They are not completed GitHub issues or promises of
maintainer approval. Implementation owners are the contributor unless noted.

| ID | Scope | Acceptance evidence still required | Status / next dependency |
|---|---|---|---|
| S01 | src#23 delivery to master | Dependency map and maintainer agreement on vendor/type separation | Assessment underway; no history rewritten |
| S02 | src#35 current-head cluster | Fresh32/64 builds, Oracle fixtures, cluster health/restart/shutdown at named SHA | Completed at8e57911e for builds/DBfixtures/health/restart/shutdown; no new client/gameplay session |
| S03 | Genuine pre272 upgrade | Database actually created by legacy32 server before update272; backup, upgrade and client acceptance | No authentic old database identified;272-to272 replay is insufficient |
| S04 | Gameplay parity | Named scenarios: combat, travel, inventory, currency, crafting, resources, auctions, mail | Not established by server startup or serializer tests |
| S05 | Crash recovery | Disposable database snapshot, specified fault injection, restart and persistence oracles | Planned only; no personal/production database fault injection |
| S06 | Logical DB parity | Two identical input databases, deterministic script perABI, normalized logical diff | Not complete |
| S07 | Shutdown saves | Per-subsystem final-save acknowledgements tied to shutdown completion | Process exit alone insufficient |
| S08 | JNI destruction | Ownership/lifetime ordering analysis plus instrumented termination tests | Separate lifecycle follow-up |
| S09 | Console completion | Defined receiver completion/join contract and race tests | Separate lifecycle follow-up |
| W01 | Compile-only writers | Runtime fixtures for four message writers and generic count-writing overloads | Existing compile coverage remains labelled |
| W02 | LoginClusterStatus | Stock32 byte oracle and decode fixtures, including2+galaxies | Required before first mixed-width connection |
| W03 | Oversized containers | Actual call-site rejection before output mutation, not helper-only tests | Open; avoid allocating billions of elements solely for a fixture |
| W04 | Byte buffer sizes | Checked allocation/arithmetic and overflow regression cases | Separate production repair |
| W05 | Nested rollback | Defined transaction guarantee and partial-output failure tests | No claim of rollback today |
| W06 | Uncaught exceptions | Caller-level recovery/termination policy and observable tests | Helpers throwing does not establish recovery |
| W07 | Traffic replay | Sanitized real captured traffic, provenance and legacy oracle | Synthetic fixtures do not substitute |
| W08 | Mixed-width sessions | Real clients/servers, connection and representative gameplay | Fullx64client/vendor blockers remain |
| W09 | Shared readability | Compare redundant casts/loop types against exactserverhead before any edit | Cosmetic alignment must not change counter signedness |
| D01 | Native D3D FPU | Native GPU ground/space traces at collision/render boundaries | Proton evidence does not close this |
| D02 | FPU setter decision | Evaluate numerical behavior with/without separate setter repair | C2 retained by prior explicit choice; any split is a separate review decision |
| D03 | Numerical visibility impact | Representative scenes cover oneULP and signedzero differences without hiding visible objects | Existing bounded fixtures insufficient |
| D04 | Other x87/integer paths | Isolated numerical/integer comparisons, edge cases and dispatch proof | Three integer fallback paths remain unisolated |
| D05 | DPVS allocations | Checked count/capacity arithmetic underx64 stress | Known narrowing/capacity risks remain |
| D06 | Full client integration | Actual x64 SwgClient link/run with supported vendorSDKs | No stubs/feature removal authorized |
| D07 | Hosted DPVS automation | Provisioned legitimate toolchain builds DLLs/probes on isolated runners | Nativev120 entrypoint and fresh committed-head matrix passed; hostedv120 still unprovisioned |
| L01 | Debug/Optimized link cleanup | Independent before/after full-executable comparison perconfiguration | Follow-up; Release proof does not transfer |
| L02 | Remaining Release inputs | Remove only proven-unused entries, compare fresh executable | Names like debug/Xbox/duplicate alone do not prove unused |
| L03 | Runtime/linker directives | Trace LoadLibrary/delay-load/pragma imports for removed candidates | Static link equality has narrower scope |
| L04 | Hosted full Win32 proof | Legal SDK/toolchain provisioning and reproducible stock build | v120 product environment is not standard hosted runner |

No universal numerical equivalence, complete protocol coverage or gameplay
acceptance follows from a green portable CI job. Upstream maintainers control
workflow approval, review, merge policy and delivery to master.
