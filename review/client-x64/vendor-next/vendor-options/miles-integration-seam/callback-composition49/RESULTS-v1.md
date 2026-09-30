# Composed callback coverage49

First strict Clang C++11 ASan/UBSan portable attempt passed: 391 assertions across23 named scenarios, each exactly once. Build log empty; build/run exits0; all29 frozen inputs unchanged. Production46 sources are unchanged.

Adds exact zero local-handle forwarding, status-zero open with nonzero output and reuse of a single file slot, forward return while the scripted job is Pending, and isolated actual Invocation ownership with no live SessionFileOwner retaining its services. This closes the bounded false-pass gaps identified in blind46; it does not establish native queue timing, cross-thread races, Windows ABI, endpoint transport or vendor/engine lifetime. The worker/job remains the explicit portable substitution; selected services, mapper, owner, Invocation and codec are real candidate source.

Raw evidence: evidence-v1/build.log, run.log, results.json. Parent inspected exact test deltas before execution and checked the result and unchanged identities afterward. One experiment, not independent reproduction.
