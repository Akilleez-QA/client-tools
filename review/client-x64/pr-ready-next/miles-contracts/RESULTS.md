# Miles contracts foundation

[Description](PR.md) states the isolated module scope and later build/integration requirements. [Receipt](receipt.json) pins the exact branch, introduced source blobs, and any comment-only polish. Independent senior-engineer review found no packaging blocker: owned includes resolve, no vendor implementation bodies are introduced, and existing project/backend selection is unchanged.

The original portable EOS test ran on this exact contracts branch: **298 checks passed**, using Clang with ASan/UBSan. [Plan, input hashes, toolchain and result](eos-result.json); [raw output](eos-run.log). No engine, Miles DLL or IPC runtime was exercised.
