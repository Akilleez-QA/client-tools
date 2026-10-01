# ByteOrder submission package

Base: `a7954b5e78274ab3a9eb558fa10186697ff5e848` (submitted client imemmove PR #25).
Head: `b0a977f8dfffdb46f2ae7d412a6e4dbf4d135fd5` on `review-ready/client-byteorder`.
The production change remains one file, +26/−0. The original published `review-ready/client-byteorder-x64-stacked` branch is unchanged. The complete delta above the prerequisite is six files, +307/−0.

| Commit | Scope |
|---|---|
| `659620122972c845eecc1af1d4e7484f3a685b69` | Production x64 byte-swap implementation. |
| `b96965dd561d6368c46bd9df2dcde156eab23e7c` | Checkout-scoped native fixture and documentation. |
| `b7a58b17f9443cac0d3d9f02bbbf7011c2c668d0` | Hosted matrix, compiler support and strict diagnostic controls. |
| `28d5b41d3c08eb0f54e3fe9b2d0cf57a9b949324` | Explicit diagnostic language for native controls. |
| `b0a977f8dfffdb46f2ae7d412a6e4dbf4d135fd5` | Verified modern parser diagnostics and executed check count. |


The package explicitly includes the prerequisite history. It is not submitted upstream as an independent master PR while that prerequisite remains unmerged. [Prepared body](PR.md) states this dependency.

## Qualification

| Environment | Source/test head | Outcome |
|---|---|---|
| Native Windows VS2013 | `28d5b41d3c08eb0f54e3fe9b2d0cf57a9b949324` | 10/10 expected matrix outcomes; recorded inputs unchanged. |
| Hosted Windows-2022 MSVC, first | same head | Failed: 8/10 outcomes; both original x64 compilation failures were rejected by the strict diagnostic classifier. |
| Hosted Windows-2022 MSVC, final | `b0a977f8dfffdb46f2ae7d412a6e4dbf4d135fd5` | 10/10 expected matrix outcomes and 30 diagnostic-classifier checks. |

[Passing hosted run](https://github.com/Akilleez-QA/client-tools/actions/runs/36829714456), [preserved failed run](https://github.com/Akilleez-QA/client-tools/actions/runs/36829151690), [final summary](hosted-summary.json), [case results](hosted-results.json), and [text-only logs/commands/input identities](text-evidence.zip).

Each matrix compiles the actual production TU. Candidate Win32/x64 Debug/Release runs each check 166,631 inputs in both directions. Original Win32 passes; original x64 fails on unsupported assembly; the no-swap x64 mutation fails the independent oracle. The latter four are expected failure controls, not passing production executions. Symbol binding and COFF architecture are checked.

Root compared all 192 native-run input hashes against the local tree at the native checkpoint. The independent staging receipt covers 194 inputs including the classifier and baseline. The final hosted manifest has 2,338 inputs because hosted checkout contains the full header tree: 9 match local bytes directly and 2,329 match Git’s Windows checkout conversion (`git -c core.autocrlf=true cat-file --filters HEAD:<path>`); none is unmatched. Do not describe cross-platform checkout hashes as all byte-identical.

## Retained corrections and limits

The first hosted compiler parsed unsupported assembly into different syntax-error cascades than VS2013. Root inspected both raw logs against the pinned original source. The follow-up accepts only the observed code/location pairs, still requires the primary unsupported-assembly errors and exact source path, and rejects unexpected diagnostics. Four historical failure logs and synthetic wrong-file, wrong-line, missing-header and tool/link-error controls were checked. The original failed run remains failed.

The first classifier script printed 12 despite executing 11 checks. The current counter derives its reported 30 from executed checks. Separately, its initial standalone invocation under the VM’s embedded Python failed to import its sibling module; that startup failure is retained. It did not execute assertions. The native matrix’s in-process classifier passed, and the ordinary hosted Python runs execute the independent classifier script successfully.

The final source and numerical probe are unchanged from the VS2013 rerun. Later changes only qualify the diagnostic classifier against the inspected modern errors and correct its check count; the full native matrix was not repeated for that correction. The final hosted matrix was run on the final head.

The link suppresses an unused legacy STLport default-library directive. No allocator, STL implementation or engine header is substituted. This covers the four conversion functions and stated controls; it is not a full sharedFoundation/client build or packet/gameplay acceptance.
