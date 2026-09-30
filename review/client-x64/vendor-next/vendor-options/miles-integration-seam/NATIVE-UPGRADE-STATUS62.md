# Native Miles-shaped replacement — checkpoint62

The public interface remains one plain ClientMiles header. Original game Audio calls belong above it; native SDK calls or temporary helper transport belong below it. Pipe identities, processes, queues, ownership records and private modern C++ never enter the game header. An eventual matching native library can replace the pipe implementation without introducing pipe-specific arguments into game code. This is a source compatibility target for the possessed SDK declarations, not a binary/runtime equivalence claim for unavailable versions.

## Actual progress

- Native source60 covers59 of62 declared functions: nine unchanged startup operations plus50 new direct operations. The latter include listener/sample/stream controls, telemetry, native lock/unlock and the scalar WAV metadata projection. Native callback registration remains the three missing functions; no stubs supply them.
- Actual v120 AMD64 gate62 compiled both new objects with zero diagnostics. The public wrapper references all50 private delegates and the52 failure boundary, with no AIL imports. The native delegate imports exactly the50 expected AIL exports and compiles its SDK type/constant assertions. Native54 previously compiled the unchanged startup delegates and plain header under the actual game STLport include environment. No x64 SDK library was linked or executed.
- Plain pipe61 source supplies45 of62 guarded public exports using the existing private proxy owner. Its17 omissions are listed in coverage.json and PLAN.md. That inventory is source scanning, not compilation or runtime proof. Existing limited supported values do not become full native semantics merely by matching function names.
- Paired bootstrap59 supplies actual host/client construction and command/callback observation code, but its source review found premature admission consumption before all operation-dependent reply checks. Root and Astra identified the same issue.59 is held; revision64 is being prepared. No runtime memory-corruption claim follows from this source-ordering finding.

The complete pipe still needs typed callbacks/EOS, original Audio TLS adaptation, correct paired teardown/locks and composed plain facade. Its partial failure-retention policy is not a completed shutdown design. Full x64 client link/start, original audio fidelity and representative gameplay acceptance remain unfinished. Product tree stays49d0eeed4ddaa177d7a93ea396c37c3d9b9942da, clean, with no upstream changes or new PR.

## Review limits

Composer examined60 and found no concrete forwarding inversion. Parent reconciliation rejects speculative blanket null-output checks because optional output pointers are part of the selected native shape; it anchors WAV nonzero handling to the actual original caller. Astra independently read the possessed declarations and source. These source reviews are not independent runtime evidence. Grok63 timed out with no output and earns no coverage credit.

All SDK headers, vendor binaries, objects and PDBs remain private. Published files contain authored source and textual observations. See native-operations62/NATIVE-RESULTS-v1.md and parent-attribution.json for precise compiler scope, and native55/58 for the preserved failed gate and setter-only repair.
