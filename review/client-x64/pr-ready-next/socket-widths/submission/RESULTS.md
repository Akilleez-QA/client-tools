# Client Windows network width package

Base: submitted helper PR25 `a7954b5e78274ab3a9eb558fa10186697ff5e848`. Head: `dbcd4d7d95a2c55be0fdf4b2185c117d21d400ed`, branch `review-ready/client-network-widths`.

Production: **five files, +9/−6**. Tests, documentation and CI: six files, +536/−0. The complete delta is eleven files, +545/−6. The previous published branch at `23849687c` remains unchanged; the new branch uses the submitted helper history.

## Commits

- `b5efaab425e4cdf576e0d4650096e7641f8d0b76`: network: preserve pointer-width Windows socket handles.
- `3ea1ae21e105e5b9798ec9c1e53bba041c319e7e`: network: receive IOCP completion keys at pointer width.
- `2e2fdadc205276788f43ade24d4414efe8436439`: network: receive TCP client completion keys at pointer width.
- `aa57a659afd78c0c1a4dd647c1baa6044fc0a032`: test: reproduce Windows network ABI checks from the checkout.
- `9aa2160f55238a809184c07ac5c80b13a585b223`: test: qualify network widths with explicit MSVC and strict controls.
- `dbcd4d7d95a2c55be0fdf4b2185c117d21d400ed`: test: scope hosted network checks to supported headers.

## Qualification

| Run | Outcome | Boundary |
|---|---|---|
| Original recorded VS2013 matrix | 100/100 expected compiler outcomes; 60 API executions and 1,260 assertions | Includes 12 actual Sock/TcpClient/TcpServer TU compilations and deliberate reversed declarations. |
| Updated VS2013 runner at `14d54af89` | 96/100 accepted; all 60 API executions passed | Four expected key failures were rejected by the test classifier's line selection. |
| First hosted full matrix at `9aa2160f5` | 64/100 accepted; all 60 API executions passed | Legacy CRT include incompatibility blocks 20 TU/control cases; modern assertion wording rejects 16 header controls. |
| Final hosted header matrix at `dbcd4d7d9` | 80/80 expected outcomes; 60 executions, 1,260 assertions; 45 classifier checks | Explicitly excludes production-TU/key-control cases; native default retains all 100 cases. |

The restacked pre-CI head `aa57a659a` matched all 166 recorded source/header/test comparisons and 2,846 exported input hashes. The later test runner changed; the production edits and API probe did not. Root also matched the updated native run's 11 named source/project/prerequisite hashes and 152 included checkout headers to the candidate. Another 181 environment/control header hashes are recorded separately.

The v120 classifier originally used the opening call line; MSVC reports the closing argument line. The corrected rule binds that line in the actual API call. All four saved diagnostics pass root's offline replay. This is not a corrected native rerun. [Native summary](native-summary.json), [case results](native-results.json), [identity](native-identity.json), [compiler versions](native-toolchains.json), and [text-only logs and receipts](native-text-evidence.zip). The [earlier receipt](source-receipt.json) identifies the pre-CI restack; the [final receipt](final-receipt.json) identifies this package.

The [first hosted run](https://github.com/Akilleez-QA/client-tools/actions/runs/36831903992) remains failed. Every TU/control failure reports legacy STLport `ctype.h(23)` looking for `../include/ctype.h`, absent from the modern CRT layout. Every rejected header control reports the expected C2371/C2338 causes, with modern C2338 adding quoted assertion wording. Root inspected all failed cases and matched all 11 named source hashes against Git's Windows checkout. [Preserved hosted text evidence](hosted-failed-text-evidence.zip).

The follow-up accepts only the exact legacy or observed modern assertion text, retaining source, line, code and paired-positive checks. Its 45 classifier tests and offline replay of 24 native and 20 hosted negative logs pass. Hosted CI explicitly runs `--only headers` (80 cases); the native v120 default remains 100. No production/STLport edits or missing-header suppression were used to support modern compilation.

## Scope

The native x64 TU check derives real Win32 project includes/definitions and explicitly removes `_USE_32BIT_TIME_T`; it supplies no x64 project configuration or full-library link. Runtime fixtures exercise Windows APIs, not production TCP lifecycle or traffic. Type/layout assertions detect handle narrowing; IOCP executions include a high-bit key. Affected x64 libraries and consumers must be rebuilt together. No prebuilt-provider, game-runtime or fidelity claim follows.

The server counterpart at `43249ae0` has matching patch sites but different surrounding source and build files. It requires its own bounded Windows qualification; client results do not prove server compilation.

[Passing hosted run](https://github.com/Akilleez-QA/client-tools/actions/runs/36832580060), [summary](hosted-summary.json), [case results](hosted-results.json), [root identity check](hosted-root-assessment.json), and [text-only logs](hosted-text-evidence.zip). Root checked all 80 outcomes and matched all 11 named source/project/prerequisite files plus three runner/probe/classifier files against Git’s Windows checkout conversion. The production files and probe remain unchanged from the recorded v120 checks.

Displayed JSON files use LF line endings; archives retain the downloaded/native bytes. No result values were changed.
