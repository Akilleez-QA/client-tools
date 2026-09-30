# Replaceable Miles interface — checkpoint55

The game-facing boundary is plain ClientMiles functions shaped to the possessed Miles7.2a Windows x64 declarations. Game code sees opaque driver/sample/stream handles, native scalar values and typed callbacks. It sees no pipe, process handle, wire token, standard-library object or backend selector. A build selects one private implementation for the startup lifetime. Future native replacement changes that implementation and its build inputs; it does not change the game API. This is a source design target, not a promise that an arbitrary later Miles release has the same ABI.

## New results

- Plain startup52: seven normal scripted scenarios,258 assertions and61 isolated rejection/exception cases passed with Clang ASan/UBSan. The real wrapper and failure code ran against explicitly scripted native suppliers. No Miles or game execution occurred.
- Native54: four actual AMD64 v120 objects compiled with warnings-as-errors, including the real native delegates against the private SDK and the plain header under actual SWG STLport headers. The SDK delegate imports exactly eight expected AIL functions. The version query uses the actual SDK macro. No x64 Miles library was linked.
- Native55: **failed**, as preserved. The host runtime object compiled; the second object failed C4702, promoted by /WX, on an unreachable catch around the SDK's extern-C setter. Three subsequent objects were unattempted. The callback ABI/import gate was not reached. All39 input files and tool identities stayed unchanged. New58 removes only that setter catch; each callback's C++ exception guard stays intact. The new58 gate passed all five objects with unchanged flags/oracles: three Win32 and two AMD64, zero diagnostics. The thunk object imports exactly __imp__AIL_set_file_callbacks@16. Its actual SDK type assertions now compiled. This is not a runtime or linked-pipeline result.

Results and raw records are in plain-startup52, native-plain54 and native-runtime55. Parent attribution is a second reading of the same experiment, not independent execution.

## Concrete remaining connections

The public surface is larger than the nine startup operations implemented by52. The remaining native declarations and temporary pipe exports are being connected separately; missing functions are not stubs. Existing pipe constraints still need qualification against actual callers. Typed EOS callback delivery, original Audio callback TLS adaptation, normal paired shutdown, locks and final Session/LiveChannel wiring remain incomplete. The source review in pipeline-integration56 identifies actual ownership transfers and send/return observation points.

Passing standalone source/object gates does not make an operational client. The product integration/client-x64-next stays clean at49d0eeed4ddaa177d7a93ea396c37c3d9b9942da. Native x64 Miles library availability, full x64 client link/start, full media behavior and representative gameplay/fidelity acceptance remain unresolved. Private vendor SDK/binary bytes are excluded from this packet. No upstream mutation or new PR.
