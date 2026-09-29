# Preserve legacy wire widths on 64-bit clients

64-bit host types can widen existing four-byte network fields and shift the fields that follow. This series fixes the reviewed container counts and timestamps at their legacy widths, preserves unsigned delta-counter arithmetic and signed timestamps, and checks narrowing conversions before writing.

For the tested representable values, the expected bytes also pass with stock Win32 source. Oversized counts and timestamps now throw `std::out_of_range` rather than silently narrowing. That rejection is an intentional behavior change; graceful caller recovery is not established.

## Scope

- Production and project/header registration: 27 files, +165/-95 lines (260 changed).
- Portable test harness: 10 files, +828/-0 lines.
- 13 commits based on upstream `94945103`; final head `b5bb8792f2a4a95b047dd62eb62f5f040596feb7`.
- The harness stays in this draft's branch so reviewers can reproduce its fixtures. No separate harness branch or PR has been created.

## Server counterpart

This wire work pairs with [SWG-Source/src#35](https://github.com/SWG-Source/src/pull/35). At client `b5bb8792`, `NetworkMessageTimestamp.h` is byte-identical to server `4889e6aa`, and `ArchiveCount.h` is byte-identical to server `30cf4531`; both helpers remain identical at server `8e57911e`, the per-message-count counterpart. The shared helpers therefore use the same checked-conversion policy and throw `std::out_of_range` on either side. This does not establish identical caller recovery or end-to-end handling of those exceptions.

## Independent validation

| Source and fixture suite | Win32 | Win64 |
| --- | --- | --- |
| `ae51d0a6`, its own suite | 46/46 | 53/53 |
| `b5bb8792`, its own suite | 50/50 | 57/57 |
| stock `94945103`, final suite | 47/47 | not rerun in this validation |

The portable tests use clang, MinGW-w64 and Wine, not MSVC. Win32-only skips and the stock source's absent helper checks are reported and are not counted as passes. The runner enforces the exact pass count and successful compilation of changed count-writing overloads.

Native VS2013 v120 Win32 Release `SwgClient` build also passes: 0 errors, 170 warnings. It used the exact clean branch sources without the separate x64 configuration work. This is compile/link evidence, not a runtime session.

## Limits

This is not a complete x64 build or gameplay acceptance. Several writers have compile coverage only. `LoginClusterStatus`, oversized containers at actual call sites, byte-buffer overflow, nested serialization rollback, uncaught exceptions and live mixed-width sessions remain open. No claim is made that all wire fields or all Win32 behavior are unchanged.

No upstream PR template was found in the tracked base tree; the sections above are proposed organization, not a repository-mandated template.

Evidence: [validation report](https://github.com/Akilleez-QA/client-tools/blob/review/client-x64-evidence/review/client-x64/B-wire/RESULTS.md), [portable results](https://github.com/Akilleez-QA/client-tools/blob/review/client-x64-evidence/review/client-x64/B-wire/portable-results.json), [native build log](https://github.com/Akilleez-QA/client-tools/blob/review/client-x64-evidence/review/client-x64/B-wire/pr-wire-review-build.log), and [historical commit-message qualifications](https://github.com/Akilleez-QA/client-tools/blob/review/client-x64-evidence/review/client-x64/B-wire/COMMIT-REVIEW.md).
