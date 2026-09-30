# Startup metadata composition 23

The new Release pair passed one genuine x64-controller to x86-original-Miles, 23-request startup/metadata/driver run in an owned Wine prefix and null sink. This is the planned no-sample composition gate. It is not full startup fidelity, Audio integration, or a replay of the older 21-request sample experiment.

## Reviewable change

`bridge.cpp` uses the frozen live candidate's channel/bootstrap helpers and admission policy with the existing Coordinator. `backend.h` is the sole startup/driver/shutdown owner; it routes metadata through the reviewed v4 validator/adapter and version requests through the reviewed v22 adapter. It does not instantiate SessionLifecycle. Its SessionInputs member survives actual vendor shutdown and registry retirement. `reply.h` gives the client a typed result with owned text; successful decode clears borrowed spans and failed decode leaves the destination unchanged. `fixture.h` holds direct vendor comparisons and preference restoration separately from backend transport status.

One explicit boundary map preserves shared errors0–3 and names lifecycle refusal4097, text limit4098, retained-input budget4099 and version failure4100. Legacy ambiguous status4/5 is rejected by the decoder. Fixture mismatches throw; they do not become runtime error codes. Pure controls exercise status disjointness, negative signed-bit conversion and malformed-reply destination preservation. The actual negative preference request is rejected before vendor dispatch; it is never supplied to the vendor.

The x86 owner obtains an owned module reference using GetModuleHandleExA FROM_ADDRESS of the genuine imported AIL_startup. The SDK declaration is dllimport, and the observed module full path matches the pinned staged original DLL. Version22 reads resource1 from that held HMODULE directly. No basename lookup is added to the production adapter. The original SDK macro is only a fixture oracle in this single-original-module setup.

## Observed results

The exact planned opcode sequence is recorded in PLAN.md and all23 encoded reply lengths/SHA256/scalar/text values are in `evidence-runtime-v1/results.json`. The host log independently records request IDs and admitted ordinals. The controller, host and optimized-Python runner all exited0.

| Surface | Actual observation |
|---|---|
| Version | Resource bytes `37 2e 32 61 00`, or `7.2a` plus NUL, equal the original macro fixture result |
| Directories | Dot returns a nonnull empty string; miles returns `miles/` plus NUL; prior owned results survive all later replies |
| Startup | Actual vendor return1 |
| Preferences | Mixer64; fragment count starts8; set16 returns8/readback16; set64 returns16/readback64; fixture restores8 before shutdown |
| Error text | Controlled first and changed vendor strings copied before later calls; first host and client copies remain intact |
| Driver | Actual nonnull driver at22050Hz/16bit/stereo; requested speaker field equals direct vendor spec2 |
| Malformed path, unsupported preference and output mask | Requests5,15,18 return InvalidFields3 before metadata dispatch; retained bytes unchanged, invalid preference leaves64 |
| Invalid resource | Request19 returns InvalidResource2 before admission/metadata dispatch |
| Shutdown and subsequent request | Actual shutdown returns before registry retirement; retained directory bytes remain8 through SessionClose; request22 is refused by draining admission with4097 |
| Cleanup | No callback frames or emergency vendor cleanup; orderly host exit; owned wineserver stopped and sink removed; default sink/source unchanged; cleanup error list empty |

The host invocation count and retained-byte snapshots check the rejection boundaries; this is not vendor-internal tracing. Signed negative values are pure controls; real vendor values in this slice were positive. The log preserves ALSA control warnings for hw:0/hw:1 during driver opening. They did not prevent the real driver or speaker query from succeeding. No audible-output or native-Windows device claim follows.

The runner verifies its actual local receipt helper, cleanup helper and own source hashes against build-receipt entries before imports and again before launch. It verifies both staged PEs against the externally captured native receipt and the original DLL/plugin copies before launch and after execution. This is named-input attribution, not universal provenance for the OS, Wine, Python or all dependencies. Encoded reply hashes attribute transient received frames; owned values and scalar fields are retained in the text evidence, while raw full frames are not archived.

## First failure and artifact identity

The first native build was a genuine failed prediction: x86 /W4 /WX reported C4512 for the fixture's reference member and implicit assignment; x64 built. No PE was launched from that build. The first source archive, native receipt and logs remain intact. BUILD-REPAIR-v2.md prospectively records the minimal private copy/assignment declarations and separately staged v2 build. Both v2 Release targets then built with unchanged before/after inputs. No runtime retry occurred.

| Artifact | SHA256 |
|---|---|
| source-v1.tar, failed compile input | `2c75741f746e980294a785bc63185b0657c582d08da88e6f17f5d5ee623be27f` |
| evidence-native-v1/receipt.json | `272083988e82c98411eb08760059fd6b619c9b660e8fcf953b65d0720f74344b` |
| source-v2.tar, executed source | `8e7849382825d6d98734d38b1718b654b2d68452fed0c008785ce7aa4a1b78e8` |
| source-manifest.json | `069c8c4b12d6ef8c748442044d9ad83fdb1d62c06d00c22a478ebd1efc28bc16` |
| evidence-native-v2/receipt.json | `94d2e537b1b85e49a505cb6d9bddc04c001ecaedce75ad62f9d472b0de8755e5` |
| x86 host PE, private | `613320e5dd4fab46928ca7349f8a0affaf1fa7c59510b772f90dafe683a97f92` |
| x64 controller PE, private | `0cfd576eec09b3872d08affadafbba677f6fac154af58df2bb98505213077fd8` |
| evidence-runtime-v1/results.json | `bc8a6a32adc18fcc214d6c528d40ec301d3b90e8c3dfc191f58904fb0bd344d8` |
| Original Mss32.dll, private | `0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe` |
| Original private SDK header | `966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e` |

Native compilation uses v120, Win32/x64 Release, /MT /O2 /W4 /WX. Runtime is one private Wine-prefix run under `python3 -O`; all launch gates are explicit checks. The runtime postcheck confirms all31 manifest members remain unchanged and the owned sink is absent. The frozen v4/v22 and original live files were read/reused without edits. No product source, SDK body, vendor binary or private PE is in the shareable source archive. No commit or push was made.

Parent's separately authored pure-boundary check reports24/24 ASan/UBSan checks against the formatted reply.h and a mutation admitting raw status4 fails its intended assertion (`../parent-startup23/result.json`, `mutation-result.json`). Those records were inspected but not rerun by this worker; they are supplementary boundary evidence, not a second vendor/runtime observation.

## Maintainer findings and remaining boundary

| MAINTAINER-DESIGN23 finding | Disposition in this bounded slice |
|---|---|
| Competing startup/lifetime owners | One Backend owner here; SessionLifecycle excluded. General callback termination/retirement capability remains open. |
| Missing combined progress and registration retirement | Unchanged and unqualified. Both channels retain existing drain behavior; no callback registration or reverse I/O is exercised. |
| Conflicting status4/5 | Addressed by one named boundary map and decoder rejection of legacy values; tested by pure checks and live lifecycle refusal. |
| Duplicated opcode shape rules | Metadata routing delegates the exact reviewed validator. Broad descriptors/encoded-size cleanup remains deferred; no frozen schema rewrite. |
| Fragmented storage/aggregate retention | Directory inputs have one retained owner through shutdown; sample/upload policies and aggregate resource budgets are outside this no-sample slice. |
| Mechanism/oracle/policy mixed in backend | Direct expected-value comparisons moved to fixture.h. Restricted driver shape, watchdogs and throwing failures remain experimental policy, not product requirements. |

Session/version stale-request handling, arbitrary lanes, reentry, live callbacks, registration retirement, malicious peers, concurrent module replacement/unload abuse and product reconnect/failure policy are not established. Resource19 is an unregistered-token control, not a broad stale-generation matrix. The version query uses an exact held module in this process and bounded lifetime; it does not solve a general DLL-loader framework. The direct macro oracle is valid only for this controlled single-basename fixture. Product Audio/ExitChain, allocator failure, actual TreeFile scheduling, unsolicited EOS, shared Miles/Bink driver behavior, latency and full audio/video fidelity remain required separate work. Existing no-playback sample outcomes remain only in the old packet and were not rerun here.

`delivery_state`: built and exercised. `outcome_state`: passed for the named composition. `highest_justified_claim`: reviewed metadata and held-module version adapters compose through the existing live no-callback x64/x86 channel and single startup owner in this exact23-request private run. `required_runtime_observation`: none remains for this gate; product/runtime frontiers above remain. `who_controls_next_test`: parent/user within their existing authorization. Parent-owned faithful-x64 goal remains incomplete; this child exposes no native goal and changed no goal status.
