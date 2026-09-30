# Actual product integration at 49d0eeed4

Immutable source: 49d0eeed4ddaa177d7a93ea396c37c3d9b9942da. All 20,552 tracked source files verified before and after all four actual MSBuild SwgClient builds. This is audited incremental integration, not a clean rebuild or runtime acceptance. No product executable was started.

| Configuration | Result | Final blocker |
|---|---|---|
| Win32 Release | exit 0, zero errors | none |
| Win32 Debug | exit 0, zero errors | none |
| x64 Release | exit 1; no compiler errors | 60 unresolved Miles imports, LNK1120 |
| x64 Debug | exit 1; no compiler errors | 61 unresolved Miles imports, LNK1120 |

Actual x64 product Link commands individually name the source-built providers, omit /FORCE, and contain /STACK:2097152. Both configurations recompile SwgCuiCommandParserScene.cpp. Debug adds only AIL_active_sample_count to Release's 60 imports. Audio.obj references 57/58 imports (Release/Debug); SoundObject3d.obj references 3 in both. Full symbol-to-object inventory is miles-imports.json. Provider/API wrappers compiling and static imports resolving do not prove dynamic vendor DLL availability or runtime behavior.

The preceding a21af1630 matrix is preserved separately: both Win32 configurations passed; both x64 configurations failed LNK1181 due escaped dependency-list tokens. Commit 49d0 fixes those tokens using MSBuild::Unescape. Native metadata tests had displayed the flattened values and failed to expose this issue; the real product Link task does.

Only four tracked files changed between the frozen a21 and 49d0 runs: Scene capture count, two provider list expressions, and x64 stack reserve. Source manifest and patch are in sibling current-head-v2-input. Original raw logs, commands, structured results and post-build hash verification are retained here. Warning totals are incremental-run observations, not clean-tree warning counts.
