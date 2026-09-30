# Private callback mapper and return/ACK join

The first frozen portable run passed all11 named scenarios (155 individual assertions) with strict GCC warnings and ASan/UBSan. The real mapper, Coordinator, SessionFileOwner, file adapter and codec ran with the explicitly scripted worker/job. Native worker events, the two Windows pipe owners, host thunks, callback installation and vendor/runtime behavior were not tested.

A forward return arriving before a causal consumption ACK remains ReturnedWaiting, retaining the command pin. Processing that ACK settles the command without blocking the control thread. The inverse arrival order also passed. Reverse request IDs are looked up in retained records instead of treating peer numbers as local intake ordinals. Tests include background requests during a command and while idle, replay, early/stale/duplicate ACKs, malformed input, storage capacity and uncertain file execution.

The source-only pretest reviewer identified that accepting lock actions without their semantic vendor outcome could manufacture a lease on a validated refusal. Before the first freeze, this slice was narrowed to Ordinary actions; explicit negative tests require AcquireLock/ReleaseLock to reject before admission. The original review is preserved. Full lock/unlock integration is still required; a valid forward frame alone does not prove the vendor acquired a lock.

Manifest: `80d4e559f9301e9a2c5ab94625feaf690972155f19a9a7127f07771b29b9660b`. Raw command, compile/run logs and unchanged-input result are under portable-v1. The only owner37 source change is the separately established native39 redundant-typename removal. Frozen source was not modified after execution. No product edit or engine/allocator workload occurred.

Follow-up composition tests are planned for multiple causal callbacks with out-of-order ACKs, new causal intake while ReturnedWaiting, incorrect forward-return observations and a valid envelope rejected by the file owner. Passing these component tests will still not constitute full bridge or gameplay acceptance.
