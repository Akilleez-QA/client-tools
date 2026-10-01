# Allocator header and block-order package

[Upstream PR29](https://github.com/SWG-Source/client-tools/pull/29) contains two focused commits on master `949451032647e45e42c3aaef3f41b132c8af36e3`: `76892e187d5b480bda16977a93e0e6bcb1c0dfde` and `2af9f19b502e9183731656cdaf93236faacb404e`. One production file, +6/−3; no test, build or diagnostic files.

The whole `MemoryManager.cpp` matches historical `f102763f7` (SHA256 `29b0f5cd1276290ba22684c445d19129402dd667944719cb2604acf5cee62fb9`). Root and a separate source reviewer checked the layout invariant and pointer-order predicate. Root read all six recorded native outcomes: four actual-TU compilations pass, and both x64 old-padding variants fail C2338 at the retained assertion. The [immutable historical packet](https://github.com/Akilleez-QA/client-tools/blob/f015ce7abc08d98902c6febdd50df204fe58137b/review/client-x64/next-build/native-text.tar.gz) preserves commands and results.

These were integrated v120 builds, including the separate imemmove prerequisite; no fresh master rebuild or runtime ordering-check test was performed during packaging. The patch does not claim heap safety or repair allocation-size, minimum-block or owner-width issues. [PR description](PR.md) states these boundaries. GitHub's displayed base/head, two commits, one file and +6/−3 were verified after creation; no automatic checks were shown at creation.
