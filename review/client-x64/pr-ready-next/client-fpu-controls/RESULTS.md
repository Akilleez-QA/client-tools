# Windows x64 FPU controls: client package

Head `16dbf07a4e6696fa1ebc133b567619643b76c3ce`; one source commit, three files, +55/−2. [Description](PR.md), [original source/evidence receipt](receipt.json), [bounded independent review](independent-review.md).

Source applies directly on maintained client master.

Native historical FPU implementation hashes match this package. The recorded client dependency closure and numerical/state limits remain in the description; no fresh package build, configured exception startup test, collision-loop execution or full-server qualification is claimed. Win32 behavior stays unchanged, including the existing setter bug.

Submitted as [32](https://github.com/SWG-Source/client-tools/pull/32); exact head and 3-file +55/−2 GitHub delta confirmed.
