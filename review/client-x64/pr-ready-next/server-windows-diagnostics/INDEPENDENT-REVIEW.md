# Independent review: server Windows diagnostics

Result: no introduced source defect or blocking claim found. Reviewed source and existing records only; no build, test, runtime, network verification or public action was performed.

Reviewed `review-ready/server-windows-diagnostics` at `fc300fe802730f1ce837e6f4b593cef9c68bf780` above `1c0152794e5597f16cd9e4b03930df654f73aa03`, plus `server-windows-diagnostics-body.md`, preparation and receipt. The five-commit delta is four production files, +21/−3, with no tooling or vendor additions. The shared source worktree was clean and remained unchanged.

Every original/candidate pair has identical added/removed lines and the same stable patch ID:

| Original → candidate | Stable patch ID |
| --- | --- |
| `2a3b1463` → `f3158732` | `c7c454b67ce4192e5a1c73d21844d6b090daf4ee` |
| `b6967a02` → `12390009` | `4b170301002fdd5ef66ba22679fd6ca22f03d032` |
| `e10e858f` → `2004e3d3` | `17ce5c6a17b8d4348a58f245c25cb81e4a9f7888` |
| `51373f7f` → `73197bf4` | `f4684b9b5939a1f86af6ed304344e11952a9dcac` |
| `1b662b4d` → `fc300fe8` | `cb42f62f70233f0ec54a52eda2a803454e4a5f39` |

The timer and fatal changes select compiler intrinsics only for `_M_X64`, preserving existing Win32 assembly and surrounding behavior. `%p` matches the exception address's pointer type. Thread naming now uses `ULONG_PTR` entries and the corresponding element count; it retains the existing native structure, SEH policy and debugger mechanism. The ShellExecute result stays `INT_PTR` through the unchanged `> 32` comparison. No unrelated PR35 call-stack or directory-search hunks were imported.

The PR38 base is the maintained master plus its three workflow commits. These selected source hunks need no additional source prerequisite; PR38 supplies CI infrastructure, not Windows qualification. Master already contains `const char *lastSection.clear();` in `Os.cpp` at line 896. That unrelated syntax defect remains in the candidate and is explicitly disclosed in the draft. It must not be folded into this diagnostic patch or mistaken for a newly introduced failure.

All four receipt SHA256 values match the Git objects. The timer file is exactly the recorded client counterpart (`bfa1dd7cada2bced9a80d102e77fe579a9c894b3f940ccecd50879ffaa9acbeb`). Saved timer records contain four passing 10,000-sample candidate runs, stock Win32 success, stock x64 assembly rejection and failing zero-return controls. The other three complete files differ from their client counterparts, as the receipt says. Saved crash-format records contain 36 checks in each configuration; the shell-width record contains eight successful client TU compilations, four successful extracted probes and two failing x64 old-width controls. These are historical component/client results, not an exact server build. The fatal record is attributed as historical client/extracted coverage, and thread naming makes no runtime claim.

The body correctly excludes profiler calibration, full fatal/exception lifecycle, actual browser launch and full Windows server support. `git diff --check` is clean. No further source change or new check is needed for this bounded review.
