# Network-width revision 2 reproduction packet

`delivery_state: built`; `outcome_state: passed` for the bounded matrix below. Source head: `1092728ace02e74b4a5c9887d9ad505d2d22421b`, branch `review-ready/client-socket-widths-stacked`. The network patch's explicit base is `9eadbbbebd515a0fffad2133300703dff68bd7ef`, the separate four-file imemmove prerequisite awaiting its own review. Original master base: `949451032647e45e42c3aaef3f41b132c8af36e3`.

This closes the two round-1 review gaps: the runner is checkout-scoped with strict failure propagation, and the actual Sock.cpp/TcpClient.cpp/TcpServer.cpp are compiled with real repository headers. Both production completion-key edits are discriminated by independently reverting each full TU copy and letting the real Windows SDK type checker reject it.

## Observed results

Native Windows VM, Visual Studio 2013 v120 compiler `18.00.40629`, x86/amd64, Debug/Release. Run command exit: **0**. `native-text/pr-network18-v2-all/summary.json` records **100/100 accepted compiler outcomes**, **60 successful runtime executions**, and **1,260 assertions** (exactly 21 per executable).

| Surface | Cases | Observed outcome |
| --- | ---: | --- |
| Candidate real headers, 5 combinations × 2 include orders × 4 architecture/configuration pairs | 40 | Compile and raw API runtime pass |
| Reverted real headers, Win32 | 20 | Compile and raw API runtime pass |
| Reverted real headers, x64 | 20 | Expected C2371/C2338 type/layout failures |
| Actual Sock/TcpClient/TcpServer TUs | 12 | Compile pass; native object machine verified |
| Each reverted TCP key, Win32 | 4 | Compile pass |
| Each reverted TCP key, x64 | 4 | Expected C2664 at GetQueuedCompletionStatus argument 3 |

Thus 76 compiler invocations returned 0 and 24 returned 2 as expected. Each x64 key control has exactly one compiler error: `unsigned long *` cannot convert to `PULONG_PTR`. The corresponding actual TU compiles in the same configuration. No wrapper declarations, substitute classes, or skipped common headers are used.

The 60 executables check raw Winsock UDP loopback and two IOCP keys, including `0x12345678abcdef01` on x64. Three header controls reproduce their pre-network-patch source bytes exactly. The headers' static layout/type checks discriminate handle width even though real allocated socket handles need not have high bits set.

## Reproduction and identity

From a native Windows checkout of the stacked candidate:

```powershell
python tools/test-windows-network-widths/run.py --checkout . --out C:/network-widths-results-1 --revision (git rev-parse HEAD)
```

Requirements and exact expected counts are in the tool's README. The output directory must be new. The runner derives real include paths/definitions from sharedNetwork.vcxproj, disables PCH, and explicitly removes `_USE_32BIT_TIME_T=1` for source-level x64 checks. It does not add x64 project configurations. All native commands are retained in each case's compile.cmd and results.json.

For this run, a sparse source snapshot was transferred to `C:/pr-network18-v2-source`. `export.py` created candidate-v2.tar.gz and candidate-v2.tar.manifest.json from the named checkout. It contains repository source/header files and the test, including all four prerequisite files; no vendor binaries or historical compiler flags are imported. The native identity.json separately records hashes of the five changed files, Sock.cpp, project, all four prerequisite files, probe, runner and toolchain setup script. `/showIncludes` produced 333 unique included-file hashes covering repository, SDK/VC and reverted test headers.

`verify-packet.py /path/to/stacked-checkout` independently compared the native relevant input hashes to both the exported manifest and current stacked checkout: **166/166 identity checks passed**, with no unrecognized external include roots. The revision string is reported metadata; these byte comparisons establish input binding. `source-binding-verification.json` records the check.

Raw successful and failed attempts are in native-results-text.tar.gz and extracted native-text/. Only textual artifacts are collected; no object files, executables, PDBs, or vendor libraries are in that archive. SHA256SUMS binds packet contents.

## Retained failures and sequence

ATTEMPTS.md preserves the harness precondition failure and the genuine original candidate failure. On exact original isolated network head `a393d1233aada331f99d4edb50f678e8c186fff2`, the 20-case implementation run returned **1**: all ten Win32 cases passed, while all ten x64 candidate/control cases failed the acceptance condition because the positive TUs failed C2668 in unchanged Misc.h and STLport. Those controls are intentionally not counted as accepted just because their expected C2664 also appeared.

The parent then created the explicit stack. No dependency was silently applied by this worker or runner. Review and merge the imemmove prerequisite separately; its client/server propagation and runtime validation are outside this network test packet.

## Evidence boundary

`highest_justified_claim`: the exact stacked network production TUs compile on native v120 in the four tested configurations; header aliases/member widths and both real IOCP key output types are regression-discriminated; raw Winsock/IOCP checks pass within the recorded finite matrix.

`required_runtime_observation`: none for the predefined narrow compile/type and raw-API contract. Production Sock/TcpClient/TcpServer runtime behavior, complete library/client build, real game networking and fidelity remain unobserved here. `who_controls_next_test`: parent/user for any expanded workload.

Widened x64 members change class layout and affected signatures. Corresponding libraries and consumers must be rebuilt consistently. Header/TU compilation does not qualify existing binary providers. Existing compiler warnings are retained, not promoted to a warning-free or complete x64 support claim.
