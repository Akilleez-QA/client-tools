# PCRE capacity submission package

Base: `949451032647e45e42c3aaef3f41b132c8af36e3` (maintained master).
Fork branch: `review-ready/client-pcre-capacity`.
Head: `123cce87b7b596e639a92477abde706caee08f79`.

| Commit | Scope |
|---|---|
| `8f6064f5230374a8680ada52457923322b5e71be` | Pass the existing 33-integer array extent to PCRE; one production file, +1/−1. |
| `99f8fb6d9fe0e6dc59af632d17ce656d53a2bdfb` | Previously tested caller-bound regression tool; three files unchanged from the earlier candidate. |
| `123cce87b7b596e639a92477abde706caee08f79` | Ubuntu caller-structure workflow and explicit scope documentation. |

The complete package is five files, +207/−1. Test/tooling/documentation lines are separate from the one-line production repair. The previously published `review-ready/client-pcre-count` at `1df8947d7971567c014e8e4815f95ac64b5f9963` remains unchanged.

## Evidence reuse

The current caller equals the tested caller plus one final newline, restoring upstream's original EOF. Every preceding byte is identical. Its SHA-256 changes from `4b728d8ada8b5b1eac413d817f5bc0c1037dedb246b6d9454089299925675b83` to `96aa160cd0a1d52a4b0fa6a4a59c561ac533036fa65a47edf75d4ab2c2729fce`. Probe and runner bytes are unchanged. Root and a blind reviewer independently checked those identities and the six saved native results; those inspections are not new runtime tests.

[Existing genuine-provider results](https://github.com/Akilleez-QA/client-tools/tree/3197e7ee0c20321dfb5bc9efb11c8b8ec2f1fb90/review/client-x64/pr-ready-next/pcre-count/revision2/native-text/pr-pcre18-revision2/results-final) retain 25/25 safe checks in each of six configurations: source-built PCRE 4.1 Win32/x64 Debug/Release, and the original repository provider Win32 Debug/Release. The matrix was not rerun for the EOF-only cleanup.

The safe probe uses bounded calls. It does not execute the historical over-advertised capacity. Caller compilation, reported separately in the older packet, used external development metadata and is not an isolated full-client build of this branch.

## New hosted qualification

[Run 36828791977](https://github.com/Akilleez-QA/client-tools/actions/runs/36828791977) passed on this exact head. Root downloaded and inspected [the result](hosted-result.json): matching caller hash, capacity 33, unsafe-expression reversion rejected, and `provider_executed: false`.

This hosted check is lexical source binding and a safe in-memory mutation only. It neither compiles nor executes PCRE. The workflow and native provider evidence cover different surfaces; neither establishes execution of the actual scene command or a full-client build.

The working tree was clean and the diff passed whitespace checks before publication. [Submitted body](PR.md) matches [client-tools PR #26](https://github.com/SWG-Source/client-tools/pull/26), opened on this head against maintained master. The PR contains exactly these three commits and five files.
