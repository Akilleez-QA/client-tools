# Miles-shaped startup source boundary 24

The new partial facade passed portable adapter tests, a physical pipe-deletion build check and a native v120 x64 object-only compile against the possessed WIN64-capable Miles header. No vendor library was linked and no native/vendor integration was executed. Frozen startup23 remains unchanged.

`ClientMiles.h` exposes nine plain Miles-shaped functions. Startup, shutdown and preference get/set preserve their separate calls; the x64 native compilation directly verifies those four function signatures against the actual SDK declarations. `intptr_t` exactly matches this header's WIN64 SINTa; U32/S32 also match uint32_t/int32_t. Driver identities remain opaque to callers. Owned text preserves absent versus nonnull-empty strings. `MSS_versionOwned` is the explicit bounded256 adaptation; `speaker_configuration_spec` explicitly returns only the channel-spec output used by Audio. These adaptations preclude a claim of complete SDK source or binary compatibility.

The pipe implementation privately owns opcodes, frame/status handling, signed32 extension and checked preference narrowing, driver mapping, Hello and SessionClose. An ordinary game-facing sample contains no protocol types, process configuration or bootstrap calls. The composition root selects one session for the full lifetime. The direct `native/native_miles64.cpp` delegates to the actual SDK calls and resource macro; it supplies no fake import library or implemented replacement DLL.

## Checked evidence

| Gate | Result and boundary |
|---|---|
| Portable adapter | ASan/UBSan executable passed202 low-level assertions across scripted test-only scenarios. These are assertion counts, not202 independent behaviors or vendor observations. |
| Mapping and ownership | Actual new adapter and frozen codec/reply decoder checked operation order/arguments, signed negative results, wide/unsupported input refusal before encoding, valid zero preference/null driver, nullable/empty owned text, foreign opaque handle refusal, and copies surviving overwritten reply buffers. |
| Failure policy | Known validated InvalidFields remains distinguishable/recoverable. Transport error, reply-context refusal and unknown status latch terminal failure; subsequent ordinary calls/shutdown/close produce no new channel request. A finish failure cannot replay SessionClose. |
| Driver allocation | Source places proxy allocation before the side-effecting open request. No allocator-fault workload was run or claimed. |
| Physical deletion build | Five copied files—public header, sample header/source and guarded test-only implementation/main—compiled and linked with no pipe/protocol/native source in the isolated tree. Dependency files resolve only to those copied files. The executable was not run. Removing the test-only implementation fails linking with missing ClientMiles symbols. |
| Native source shape | Five translation units compiled v120 amd64 /MT /O2 /W4 /WX: direct native implementation, pipe adapter, concrete live channel, sample and fixture composition. All objects are AMD64; source/header/tool inputs remained unchanged. No PE output. |
| Real SDK imports | Native object retains eight unresolved `__imp_AIL_*` imports: startup, shutdown, get/set preference, last_error, set_redist_directory, open_digital_driver and speaker_configuration. Resource version is the actual header macro, not a ninth exported AIL function. |

The test double exists only under `tests/` and requires an explicit test macro to compile. It proves source/link isolation, not an alternative renderer. Scripted replies are labelled test-only; they do not replace genuine DLL observations. No broad matrix or runtime retry was performed. Both the portable checks and native object compilation passed on their first attempts.

## Frozen identities

| Artifact | SHA256 |
|---|---|
| source-v1.tar | `9a020d7a4af3419726ffbcbcf3193cca8890c51b0ea1980ebc7c4a22c7d78761` |
| source-manifest.json,33 members | `099986e64f6872ba1c3721bf006e9adf483819218d1dbee5722f5053aa6de97b` |
| evidence-portable-v1/results.json | `7664e75311a74f3c4c21155db9b428e0ec9a941f09a61bca20d7aa0051740f0f` |
| evidence-native-v1/receipt.json | `53c6167ca4604bf6f24d2351fd645de6a37057d6f1faaa5b9810c6af0d81e5dc` |
| Native object, retained privately in VM | `4a8535101177fc1664858421c5432a06b0761e3bf3277354936c4a52e1b1cc98` |
| Actual private SDK header | `966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e` |

The isolated build compiles the exact unchanged sample source/header, not a rewritten substitute caller. All33 source-manifest members were rechecked unchanged after native compilation. Native objects remain at C:/backend-boundary24/native-v1. Text receipts contain commands, hashes and unresolved symbol observations; the shareable source packet includes no SDK body, vendor binary or compiled object.

## Unexecuted composition and limits

`fixture/live_controller.cpp` routes startup23's valid calls through the facade while injecting its five raw negative controls privately at the original request IDs. `pipe/LiveChannel.cpp` reuses frozen common.h/Endpoint helpers and returns validated known refusal statuses to the facade rather than throwing on every nonzero result. The source retains the intended23-request order, but this new composition has only been compiled. Startup23's prior real runtime result does not prove this new facade's execution.

The live channel's reply hashing/logging, fixed bootstrap and process guard are experimental fixture mechanisms. The separate pipe-drain23 repair is not integrated. There is one lane/global selected session, with no thread-safety, reentry, reconnect, callback, stale-across-new-instance or whole-client replacement guarantee. Terminal channel failure records an uncertain outcome; destruction abandons the session under the existing process owner and does not manufacture graceful vendor shutdown.

The sample's early return on startup0 is fixture policy; actual Audio.cpp ignores AIL_startup's return. Zero startup was not tested here. The current pipe host permits SessionClose only after shutdown, while the facade requires a running session for shutdown: startup0 therefore has no demonstrated graceful-close path and remains abandonment/failure-policy work. Valid zero preference and null driver tests do not establish zero-startup recovery. No source or runtime claim covers all host failure or allocation paths.

Parent source review identifies an actual startup media dependency: ClientMain.cpp calls VideoList::install(Audio::getMilesDigitalDriver()), reaching BinkSoundUseMiles through VideoList/Bink installation. This partial facade contains no media binding; its opaque proxy must never be passed as a native driver. Real Bink binding, image/stream lifetimes, file callbacks, EOS/reentry, locks/service and full audio/video fidelity remain separate requirements before the bridge can be discarded. No native x64 Miles runtime availability, compatible binary or licensed replacement has been established by this compile check.

Parent approved the public shape and source checks; independent CLI source reviews were launched against the frozen manifest and are pending at this report's writing. Their findings must be reconciled before the separately authorized live composition gate. No product edits, commits or pushes were performed by this worker.

`delivery_state`: checked source and compiled objects. `outcome_state`: passed for source/mapping/build-boundary gates; new vendor runtime unobserved. `highest_justified_claim`: the narrow Miles-shaped caller can compile with the pipe implementation physically absent, and direct native/pipe implementations compile behind it with explicit adaptations. `required_runtime_observation`: reviewed, separately authorized new23-request facade composition; later native/full-client replacement acceptance remains. `who_controls_next_test`: parent/user. This child does not complete the parent faithful-x64 goal.
