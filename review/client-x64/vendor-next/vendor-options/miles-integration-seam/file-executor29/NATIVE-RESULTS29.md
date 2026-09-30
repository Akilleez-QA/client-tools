# Step29 native compile result

The single authorized full-Audio matrix passed: **8/8 object compilations**, Debug/Release × Win32/x64 × original49d0/candidate. Every compiler exit code is zero. Baseline and candidate logs contain no compiler warnings/errors; after include traces, each contains only `Audio.cpp` and `_MSC_FULL_VER=180040629` from the v120 guard. No repair or native retry occurred.

Evidence: `native-evidence-v1/curated/results/results.json`, all eight raw `command.json`, `compile.log`, and `actual-includes.json` files, plus `native-evidence-v1/verification.json`. Each command uses `/c`. Guest-side post-run inspection rehashed all eight actual objects and independently read their COFF machine field: `0x14c` for Win32 and `0x8664` for x64; these match the runner receipts. Objects/PDBs and the SDK/snapshot remain private. This establishes object compilation, not linking, Miles SDK64 availability, or runtime compatibility.

Input manifest: `a02c162efe3dfd320f50cc4e0d8f56f236b99d770904c3c22e988e5dc48b135d`.
Runner: `ca93eb658f8dd70d78bfcd285385074d7ed34dd9a449ba5c32964099709bef73`.
Curated evidence ZIP: `0f03918c7267a62d5f46447ff8f4754dda0609618766bb6783e56e72116ebe79`.

All 9,538 transferred manifest entries were verified before compilation, rechecked by the frozen runner, and verified unchanged afterward. All actual included-header hashes remained unchanged afterward. Each baseline traced 370 includes; each candidate traced 372. Product remains clean at `49d0eeed4ddaa177d7a93ea396c37c3d9b9942da`. Frozen source/artifact manifests and driver were retained unchanged.

`native-evidence-v1/commands.json` records the one matrix invocation and transfer/collection commands. The local receipt's field `compiler_invocations: 1` counts the matrix runner invocation; the matrix contains eight separate `cl.exe /c` compilations. A Python tarfile future-default DeprecationWarning occurred during staging only and is preserved in `03-stage.log`; it is not an inherited or new Audio compiler warning. Local evidence verification initially encountered Windows backslash path keys; normalizing those keys completed verification without modifying native inputs/results or rerunning compilation.

Earlier frozen README/recipe statements that compilation was unrun describe the preparation gate; this report records the subsequent separately authorized execution. No engine code, generated binary, original DLL, Audio/ExitChain teardown, fault test, worker, transport adoption or SDK64 runtime was executed.
