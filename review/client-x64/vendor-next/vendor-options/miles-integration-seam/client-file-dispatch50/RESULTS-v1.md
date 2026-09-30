# Client file dispatch and consumption acknowledgement — first portable gate

Outcome: passed within the component scope below. Parent re-read the raw results and logs after the first approved execution. No retest or source mutation occurred.

The strict Clang C++11 build used -Wall -Wextra -Wpedantic -Werror with AddressSanitizer and UndefinedBehaviorSanitizer. Build and positive run exited0; every frozen input was unchanged. 407 low-level positive assertions passed; these are not 407 independently distinct behaviors.

Seven scenario groups passed using real mapper, owner, selected services, Invocation, guard and codec with scripted worker/job. ACKs use receiveControl. Windows callback ABI, actual endpoint authentication/I/O, native worker, SDK installation and runtime fidelity are not covered.

See evidence-v1/results.json, command records, run logs, freeze-v1.json and REVIEW-parent-pretest.md for exact inputs/oracles. This evidence does not authorize or establish the rejected real-engine teardown or allocation-fault workloads.
