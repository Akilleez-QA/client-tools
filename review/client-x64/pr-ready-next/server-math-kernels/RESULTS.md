# Server Windows x64 math kernels

Server head `9aa3e319beb7f9be3a20f62b2b36400073e1be79` on workflow prerequisite1c015279; [source-equivalence and prerequisite receipt](workflow-stack.json).

Three source commits, four files, +235/−1. [Description](PR.md), [original source/evidence receipt](receipt.json), [independent source review](independent-review.md). The review and original receipt retain the historical source-hash gap; the subsequent exact-source native check below closes that gap for its sampled surface without changing source.

[Exact-source check](../math-exact-source-check/RESULTS.md): Debug/x64 and Release/x64 each compile/link/run the exact packaged SseMath.cpp/.h, producing all 33,280 records byte-identical to the corresponding historical candidate. Root independently matched packaged source/header, corrected probe and original oracle hashes and inspected logs. Source and native observations remain bounded to recorded client dependencies; no full server/client rebuild or universal numerical equivalence.
