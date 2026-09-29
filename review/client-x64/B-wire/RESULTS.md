# Branch B: fixed-width wire validation

## Identity and isolation

- Branch: `x64-fixed-width-wire`.
- Head: `b5bb8792f2a4a95b047dd62eb62f5f040596feb7`.
- Base: upstream `94945103`.
- Thirteen commits; full messages are retained in `commits.txt`.
- `git status --porcelain` is empty. No diagnostic source or build configuration changes were added to the branch.
- Production/project files: 27, +165/-95; harness files: 10, +828/-0. Total: 37 files and 1,088 changed lines.

## Portable suite reproduced independently

| Source | Runner/fixtures | Win32 | Win64 |
| --- | --- | --- | --- |
| `ae51d0a6` | `ae51d0a6` | 46/46 | 53/53 |
| `b5bb8792` | `b5bb8792` | 50/50 | 57/57 |
| `94945103` | `b5bb8792` | 47/47 | not rerun |
| `94945103` | `ae51d0a6` | 43/43 | not rerun |

All six processes exited zero. Each pass total includes the compile-time width check; runtime PASS lines are one fewer. Raw logs and exits are retained as `<commit>-<bits>.log` and `.exit`, with a machine-readable summary in `portable-results.json`.

Commands follow the checked-in runner:

```sh
python3 tools/test-wire-compatibility/run.py --bits 32
python3 tools/test-wire-compatibility/run.py --bits 64
python3 tools/test-wire-compatibility/run.py --bits 32 --root /path/to/stock-checkout
```

Host tools: clang 22.1.8, MinGW-w64 GCC 16.2.0, Wine 11.17. This host uses Wine WoW64, so the unchanged runner was invoked through an external adapter that changes only the Wine subprocess environment to `WINEARCH=win64` and an existing WoW64 prefix for both PE architectures. It does not alter fixture bytes, source, compiler flags, pass-count enforcement or return statuses. The adapter is retained as `run-portable.py`; the published copy reads the initialized WoW64 prefix from `SWG_TEST_WINEPREFIX`.

Win32 reports six timestamp rejection cases and one unsigned size overflow case skipped, not passed. Stock reports the count helper absent; its three applicable checks are deducted rather than counted as successes. Four per-message writers and generic count-site instantiations have compile coverage only.

## Native product build

The isolated native VS2013 v120 Win32 Release build passed: exit 0, 170 warnings, 0 errors, elapsed 5 minutes 35.98 seconds. Full output is retained in `pr-wire-review-build.log` and `.exit`. The guest tree was seeded with the existing product environment's SDKs and ignored build artifacts, then every tracked source/project file was overwritten by a full Git archive of the exact head. No diagnostic changes or the 67 outstanding x64 configuration edits were applied. The archive refreshed tracked inputs and the log shows native recompilation of the relevant source projects and final product link. Effective compile commands include `/EHsc` and `_USE_32BIT_TIME_T=1`.

```bat
MSBuild.exe src\build\win32\swg.sln /t:SwgClient /p:Configuration=Release /p:Platform=Win32 /m:2 /v:normal
```

The resulting `SwgClient_r.exe` is 29,017,600 bytes, SHA256 `0b9097146001f1ad0c891f0a14dadced0458a66880bdfa53eb067de47e818668`. Build success does not imply the warnings are resolved or a native runtime session was tested.

**Dependency answer:** branch B does not require any of the 67 uncommitted configuration files for this Win32 Release build or its portable Win64 serializer suite. It still requires the installed VS2013/SDK environment and existing third-party Win32 libraries; that is not a self-contained SDK bootstrap claim. A full native x64 client build remains outside this branch validation.

## Review and limits

See `COMMIT-REVIEW.md` for historical wording that should not be repeated as current guarantees. In particular, signed count rejection changes oversized-input behavior on Win32 too. Passing fixtures establish the listed serializers and boundaries, not complete protocol compatibility, full x64 builds or live gameplay.

Open: `LoginClusterStatus`, oversized containers at actual call sites, byte-buffer overflow, nested serializer rollback, uncaught exceptions and mixed-width sessions. No PR template was found in the tracked upstream base; `PR-B.md` is a local draft only.

## Shared-helper identity check

Git-blob comparison at client `b5bb8792`: `NetworkMessageTimestamp.h` matches server `4889e6aa`, `30cf4531` and `8e57911e` (SHA256 `1724878ec03e51e84213b6b4f76a510595219c53a75c3bb5cf0a56afcbc7ebf4`). `ArchiveCount.h` matches server `30cf4531` and `8e57911e` (SHA256 `52ca20c1c72fe75650cb845a3a3ac7a25dddf368d75438ead071a0c4a0561e38`). These checks establish identical helper contents at those commits, not live protocol acceptance or caller recovery.
