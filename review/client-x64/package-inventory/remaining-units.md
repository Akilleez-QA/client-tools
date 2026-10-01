# Finite client packaging remainder

Read-only accounting at maintained `eca74ffa5741f608a1417944b2e2602868936517`, last production change `da9c56054b70761b983b4b367fd4479ac344e8e6`, against master `949451032647e45e42c3aaef3f41b132c8af36e3`. Shared prior packaging context is disclosed: this reviewer prepared the Miles/Bink/build packets. No source, refs or public records were changed; no tests/build/runtime were run.

## Production and build coverage

No genuinely unassigned production/build unit was found. The actual Git diff and frozen inventory have the same 353 paths. Every one of the 220 production paths and 83 build/configuration paths occurs in the prepared package closure. The inventory already assigns all production/build origin commits; the five final media/input packages now have exact original-hunk extraction receipts. This is assignment/packaging coverage, not a newly composed tree comparison or exact-base native build result.

The map's six `remaining` package statuses are stale: TrackIR, obsolete-client-inputs, miles-game-selection, bink-host-session, bink-game-selection and media-release-build all have prepared heads. Local submission receipts record TrackIR upstream PR40 and media fork PR18–21; obsolete-input publication was still parent-owned at this check. Machine-readable heads and locally observed receipt URLs are in `remaining-units.json`. These are local recorded observations, not a new GitHub status query. Per-file `component_statuses` and aggregate `production_file_coverage_states` remain frozen/stale as well.

Keep the frozen total **220 production files, +11965/-796 (12761 changed lines)** unchanged. Explicit Myers recomputation is **+11964/-795 (12759)**: Audio.cpp is +223/-75 rather than +225/-77; MemoryManager.cpp is +118/-73 rather than +117/-72. This is a diff-algorithm difference, not lost code. Build/configuration stays 83 files +8897/-28. The later published TrackIR registry-boundary correction is beyond the maintained frozen source snapshot and must not be silently folded into its totals.

Do not sum branch diffs against master: joint prerequisite bases include already counted source. Seventeen production files and thirteen build files have multiple contributing packages. The exclusive accounting owner prevents duplicate path totals; sequential incremental patch counts need not equal a final diff. `miles-session-core` represents foundations 1–7, and `allocator-sizes` represents the size-invariant plus statistics/null/pointer packages: neither umbrella is an extra implementation packet.

## Finite nonproduction remainder

1. **Archive regression harnesses:** `tools/test-byte-stream` and `tools/test-archive-decoders` were intentionally excluded from the source-only archive package. Their historical integrated-provider evidence remains applicable only within its recorded scope.
2. **UI memory harness:** `tools/test-ui-memory` was intentionally omitted because it depends on the integrated allocator/core/STLport snapshot. This is not an unassigned UI production fix.
3. **LoginClusterStatus regression:** `tools/test-wire-compatibility/login_cluster.cpp` from `3550071ed` is absent from the selected package heads. It belongs with its corresponding runner additions as a focused wire-test follow-up. Existing coverage of the `run.py` path does not prove these later hunks are delivered.
4. **AutoArray/List wire regression:** the separate `4d3009851` shared-fixture delta identified by the wire packaging worker also remains; it requires archive source changes and is not covered merely by the older fixture path being present.
5. **Portable CI composition:** the later archive/native-provider/Miles/Bink additions to `.github/workflows/wire-compatibility.yml` were deferred. A workflow at the same path exists in prerequisite wire work; that is not evidence those later jobs are wired. Package READMEs correctly disclose absent media CI.
6. **Live-session evidence:** committed `a422c4e48` and `eca74ffa5` documentation plus the currently unstaged paired-host-shutdown section belong in a separate evidence/procedure follow-up above the wire-test package. They do not belong in Bink/Miles runtime source commits or change production/build totals.

These are bounded packaging/documentation decisions, not reasons to reopen runtime acceptance. “All production/build units assigned” is supported; “all integration artifacts delivered,” “all PRs merged,” or “all split branches freshly built and tested” is not.

## Local live-session edit

The only maintained-tree edit is `tools/test-wire-compatibility/live-session.md`. It adds the separately observed login-screen and loaded-world paired process exits, states the exact-path/parent process-handle sensor and shared 15-second bound, preserves the failed sensor setup/control distinction, and updates the old statement that media-host exit remained unmeasured. It also records delayed persistence, restoration and the cleanup exit caveat.

Place it with the preceding committed live-session evidence as one documentation-only follow-up, reviewed against its private observations by the parent who owns that evidence. No private raw logs, binaries, media or credentials should be added. The edit itself contains run identifiers, scoped outcomes and methodology rather than authentication material. This pass determined placement and read its claims; it did not reopen or independently revalidate raw runtime results. The historical allocator/teardown failure remains explicitly unresolved by these observations. The local edit was left untouched.
