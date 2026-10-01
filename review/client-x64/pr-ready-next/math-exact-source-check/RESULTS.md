# Exact packaged SseMath source: native v120 check

The historical packet records source `701111df…`, while the published implementation and prepared package contain `7d23411f…`. This named PR evidence gap justified two native TU/probe checks. No game session or full-client build was run.

| Configuration | Compile / link / run | Corrected records | Comparison with original candidate |
|---|---|---:|---|
| x64 Debug | 0 / 0 / 0 | 33,280 | Byte-identical, SHA256 d7e08b523bff6e406a67e7bc5f2b46160090b3f2a429621ee9a457187b5d7ddc |
| x64 Release | 0 / 0 / 0 | 33,280 | Byte-identical, SHA256 f729d25c5f2123b67cc6ecb8fb3d72b66f53a638367c90b9110213e0089e5a4c |

The [prospective contract](precommitted-contract.json) required exact schema/count and unchanged bytes; no tolerance was adjusted. [Raw results](native/results.json), [Debug comparison](native/Debug-x64-candidate/raw-comparison.json), [Release comparison](native/Release-x64-candidate/raw-comparison.json) and sibling command/log files identify source/header/probe/compiler/dependencies and native outcomes. Compilers consumed the actual current source; linker maps bound the arithmetic APIs to its fresh production object. Original commands changed only output paths.

The initial dispatch found only a Windows Store alias; an existing Python runtime was then used. Two collector-only map parsers mistook section/header labels for libraries and stopped before probe execution. The original failure receipts are preserved beside final results. No native recompilation or link rerun was used; each corrected probe executed once. Source inputs remained unchanged.

Root independently checked packaged source/header SHA256 values, the corrected probe identity, both oracle hashes against the original result JSON, exact 33,280-record headers, and compile/link/run logs. This provides current-source evidence for the sampled x64 arithmetic behavior in the existing integrated client dependency environment. It does not supply a full master-based client build, server dependency qualification, new Win32 behavior, normal dispatch/gameplay coverage, or general NaN/signed-zero equivalence. Historical exceptional differences and the stock Win32 register-clobber diagnosis remain as documented.
