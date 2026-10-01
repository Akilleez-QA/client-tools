# Windows x64 FPU controls: server package

Head `01755444ed579611bc3cfa75d2cf67d880d44bfb`; one source commit, three files, +55/−2. [Description](PR.md), [original source/evidence receipt](receipt.json), [bounded independent review](independent-review.md).

Stacked above the existing server build-workflow repair (upstream #38); [exact source-equivalence and workflow prerequisite receipt](workflow-stack.json). The master-based source head remains preserved.

Native historical FPU implementation hashes match this package. The recorded client dependency closure and numerical/state limits remain in the description; no fresh package build, configured exception startup test, collision-loop execution or full-server qualification is claimed. Win32 behavior stays unchanged, including the existing setter bug.
