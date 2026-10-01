# HTTP lock submission

[Upstream PR #30](https://github.com/SWG-Source/client-tools/pull/30), head `003f8757c7c1386e33c997be7d5bf5b8109669d4`, applies directly to master `94945103`. Three commits, six files: one production header +17/−0 and five test/documentation files +439/−0. No integration prerequisite or genuine-TU WIP extension is included.

Root matched production/probe/FoundationTypes hashes to the recorded native matrix and inspected all ten outcomes: four candidate and two stock-Win32 runs each pass 27 checks; stock x64 rejects its assembly; deliberate missing acquire/release copies fail the specific checks. The earlier independent maintainer and senior source/evidence reviews found no production blocker. Their scores are historical judgments, not proof or upstream approval.

The runner's former C4235 substring test was replaced with exact stock-header diagnostic path/line/order/multiplicity recognition. Root replayed all 77 classifier controls, including both original native logs. Production and probe are unchanged; the corrected runner has not been rerun natively. [Original results](../RESULTS.md), [description](PR.md), [source/input receipt](receipt.json).

This remains actual trylock()/unlock() coverage, not production lock()/yield_thread(), HTTP traffic, fairness or portable race freedom. A separate attempted full-TU Release-x64 link located genuine STLport but failed on the project's custom allocator overload; no runtime executed. That unqualified extension stays outside this PR. Completed full-client evidence remains separate from this component fixture.
