# ByteOrder and network revision 2 — independent senior review

Read-only reassessment of the clean committed stacks:

| Candidate | Reviewed head | Engineering | PR readiness |
|---|---|---:|---:|
| ByteOrder | `110c7b4ba7cf317760119c1b298fabe7d30b61d8` | **9.5/10** | **9.0/10** |
| Network widths | `23849687c697520d8934049efc49f62e44fd9b6a` | **9.3/10** | **9.0/10** |

These replace my round-1 scores of 9.0/7.0 and 8.0/5.5 respectively. Scores concern each candidate relative to its declared prerequisite. They are not approval of the prerequisite or readiness to merge either stack directly into master without reviewing it.

I inspected the current committed tests and production diffs, PR-v2 drafts, reproduction instructions, source manifests, raw native outcomes and selected compiler/linker logs. I independently recomputed repository-file hashes and source-binding comparisons. No test runner, compiler, application or provider runtime was executed; no source was modified. I did not read maintainer reports. The initial review remains unchanged.

## Shared dependency and scope

Both branches explicitly contain `9eadbbbebd515a0fffad2133300703dff68bd7ef`, the four-file imemmove prerequisite, before their feature commits. The inspected initial ByteOrder x64 logs fail at Misc.h(233) with C2668 for memmove. The new evidence does not disguise that failed standalone attempt or claim that original master builds x64. Network documentation likewise retains the standalone failure and states the dependency.

Relative to that prerequisite, ByteOrder's production diff remains the same 26-line addition, and network remains the same five-file width correction reviewed in round 1. Their tests neither modify headers to suppress the prerequisite failure nor silently copy integration-tree fixes into the checkout. This is the right scope boundary.

**Required merge condition:** review and approve imemmove independently, and target the candidate PRs at the prerequisite branch or merge it first. Its presence in a passing function/TU test does not validate all changed imemmove callers. I have not performed that separate review here. A later rebase that changes actual source/header bytes needs a fresh identity comparison and appropriately scoped validation; a commit-ID change alone is not proof of changed behavior.

## ByteOrder

The production judgment is unchanged: correctly typed 16/32-bit swaps under `_M_X64`, unchanged public signatures and Win32 assembly, with no newly discovered defect. The significant improvement is that the runner now compiles the actual checkout TU with its own real headers using a small explicit command instead of private audit-log metadata.

I independently verified **all 192 recorded source/probe/runner/header hashes** against the committed stacked tree, with zero mismatches. The production file remains SHA-256 `84d6a070f6412908e2fb95cf4dfb9268478f9dc0be5b2fe4cd10f4b77b7a2f17`. The stack identity accurately separates tested production commit `6bd1e1a275c9405e2e3da324df491d93ad374b97` from the final test commit. The added README does not alter tested executable inputs.

The archive contains ten expected outcomes: four passing candidate runs, two passing Win32 baseline runs, two x64 baseline compile failures, and two x64 mutants that compile and fail the value oracle. I checked that the archived baseline is byte-for-byte the base commit's ByteOrder.cpp. The inspected baseline failures contain the intended C2485/C4235 diagnostics; the mutant reports `FAIL long 80000000`. Candidate map files for both x64 configurations bind all four conversion symbols to production.obj, and recorded COFF machine values match the requested architectures. The source oracle is still independent of the intrinsic and exhausts 16-bit inputs while sampling 32-bit inputs and boundary patterns.

The new reproduction document supplies the control-enabled command, prerequisite, exact heads and toolchain context. The ordinary runner defaults to four candidate cases; the reported ten-case regression matrix requires `--baseline`, now explicitly documented. The baseline deliberately uses the same prerequisite headers, so it isolates ByteOrder behavior rather than purporting to build unchanged upstream master.

Remaining limits are appropriately small. This is a finite function test, not exhaustive 32-bit proof, a library build, packet serialization test or startup validation. The `/NODEFAULTLIB` suppression is restricted to an unused legacy STLport directive; no container or allocator implementation is substituted. The subsequent toolchain executable hashes are clearly labeled as later observations on the same VM, not a contemporaneous complete toolchain lockfile. These qualifications warrant retaining headroom below 10, but not expanding the production patch or demanding full-client execution.

**Optional improvements:** record toolchain executable versions/hashes in the runner at execution time, and preserve partial compiler/run output plus an explicit failure summary on timeout. Current subprocess exceptions correctly fail the command but can leave less useful diagnostics. Neither affects the correctness of the observed passing matrix.

## Network widths

The main round-1 requirement is now met: tests are bound to **both actual changed IOCP implementations**, not only correctly typed destinations invented inside an SDK probe. The runner compiles Sock.cpp, TcpClient.cpp and TcpServer.cpp from the checkout for Win32/x64 Debug/Release. It then copies each TCP TU and changes only `ULONG_PTR completionKey = 0;` to `unsigned long completionKey = 0;`. I compared those retained copied files to the current production files and confirmed that exact single substitution for each.

All four x64 key-control logs fail specifically with C2664 at the actual GetQueuedCompletionStatus call, converting argument 3 from unsigned long* to PULONG_PTR. Each corresponding candidate TU compiles, and each Win32 control compiles. The runner requires both the targeted diagnostic and the corresponding positive case, so an unrelated compile failure cannot satisfy the intended key control. This is sufficient discrimination for the narrow declaration fix; production TCP runtime execution is not needed to establish it.

I independently reproduced the packet's **166/166 source-binding comparisons without running its verifier**: native reported revision versus export, 11 recorded source/project/prerequisite hashes, 152 included checkout-header hashes, and runner/probe identity. No mismatch or unexpected external-include root was found. The complete include manifest has 333 records, including SDK/compiler and private output-control paths; 333 is not the number of repository headers. The committed runner hash is `0f1c776f8683e5378af9c84c89a5220bb0f534c49232c48011956cc64810001d`; the probe hash is `fd706d95605e0d98b9d5e18c859dd3f96247de4fefdf02aac1d8c3845fbdd26e`. Both match the retained native input copies.

Raw records contain **100 accepted compiler outcomes: 76 compile successes and 24 expected control failures**, not 100 successful compilations. The matrix consists of 40 candidate header cases, 40 reverted-header cases, 12 actual-TU compiles and eight independent key controls. Sixty executable runs contribute 1,260 assertions. These repeated API assertions exercise header/include-order/configuration combinations; they are not 1,260 distinct production behaviors.

The x64 adaptation is bounded and disclosed: derive include directories and definitions from this checkout's Win32 project, omit `_USE_32BIT_TIME_T=1` for x64, use no PCH or stubs, and record commands. It is not a newly supported x64 project configuration or complete sharedNetwork build. Both x64 TcpClient compile logs retain two C4267 warnings in existing Archive.h at lines 306 and 309. They do not invalidate the successful type checks and are outside this patch; do not describe this as a warning-free x64 build. The other ten inspected production compile logs contain no compiler warnings.

The runtime remains an honest raw-Winsock/IOCP check. It does not instantiate Sock or execute TCP update loops. Actual socket handles can have zero high bits, while the static width/layout assertions detect truncation; IOCP explicitly checks a key with nonzero high bits. The README and draft now clearly state the x64 class-layout/signature rebuild requirement and do not qualify prebuilt binary providers. That closes the ABI-documentation gap from round 1.

**Optional improvements:** force English compiler output or fail explicitly when the expected include-trace format is absent, rather than relying only on the documented locale requirement; optionally state the two retained Archive.h warnings in the evidence summary. The current packet has the required include traces and hashes, so this is future-run robustness and narrative precision, not a defect in the observed evidence. There is no need to add production runtime or a vendor workload for this approval scope.

## Submission recommendation

Both candidates are technically ready for review as explicitly dependent PRs. Before publishing, link each final evidence packet and prerequisite PR from its description and preserve the production-head/final-test-head distinction. Before merging, obtain the separate prerequisite approval. No further source change or runtime campaign is required by this reassessment.

The ratings increased because the new artifacts establish exact checkout inputs, reproduce the narrow test without hidden metadata, and discriminate the actual regressions. They remain below 10 because the imemmove prerequisite is separately pending, full toolchain reproducibility is not established, and the documented test boundaries remain real. Those are specific limits, not an invitation to broaden these repairs.
