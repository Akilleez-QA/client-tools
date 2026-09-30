# Host file token and reply consumption — first portable gate

Outcome: passed within the component scope below. Parent re-read the raw results and logs after the first approved execution. No retest or source mutation occurred.

The strict Clang C++11 build used -Wall -Wextra -Wpedantic -Werror with AddressSanitizer and UndefinedBehaviorSanitizer. Build and positive run exited0; every frozen input was unchanged. 338 low-level positive assertions passed; these are not 338 independently distinct behaviors.

Seven positive scenario groups and six separately armed expected-terminate subprocesses passed. The subprocesses require exact exit73 and marker, and deliberately skip cleanup via _Exit: this does not establish cleanup or leak behavior. No Endpoint, SDK, engine, native ABI or game run.

See evidence-v1/results.json, command records, run logs, freeze-v1.json and REVIEW-parent-pretest.md for exact inputs/oracles. This evidence does not authorize or establish the rejected real-engine teardown or allocation-fault workloads.
