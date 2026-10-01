# Windows diagnostic x64 source package

Head `855b299004da38f48aa6517c76d30338488eeba2` on master `949451032647e45e42c3aaef3f41b132c8af36e3`. Four source commits, four files, +14/−4.

[Description](PR.md), [exact source/evidence receipt](receipt.json), [independent review](independent-review.md). Timer and crash-handler file hashes match recorded candidate source manifests.

Historical tests compile the profiler TU and execute its extracted counter helper, or execute the extracted crash-format statement. They do not establish full profiler/crash-handler integration. Thread/window changes are source-reviewed without an isolated runtime claim. No new package build/runtime was run.

Submitted as [https://github.com/SWG-Source/client-tools/pull/33](https://github.com/SWG-Source/client-tools/pull/33); actual GitHub base/head and diff counts verified.
