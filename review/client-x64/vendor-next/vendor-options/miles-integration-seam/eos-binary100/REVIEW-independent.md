# Independent bounded binary interpretation100

Read the original DLL and saved private analysis only; no DLL load/execution, diagnostic run, compiler, VM or change to frozen97. No implementation bytes or disassembly are reproduced here. independent-identities.json pins the original file and private evidence. Original DLL SHA2560785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe; preferred image base0x21100000. Independently parsed its PE export directory rather than inferring names from adjacent disassembly labels. All listed exports are actual code RVAs, not forwarders.

| Export | Ordinal | RVA |
|---|---:|---:|
| AIL_lock |94|0x18a0|
| AIL_unlock |309|0x18b0|
| AIL_lock_mutex |96|0x18c0|
| AIL_unlock_mutex |310|0x18d0|
| AIL_register_EOS_callback |156|0x17930|
| AIL_register_stream_callback |164|0x1c120|
| AIL_end_sample |56|0x153d0|

AIL_lock/unlock perform interlocked changes to the same global counter (RVA0x8e600) and return. They do not call the mutex helper, wait for an owner or drain callbacks in their own bodies. An inspected timer/service path tests that counter at RVA0x1469 and skips work when it is positive. This supports an inhibition-counter interpretation for that path, not a global producer-termination guarantee. In particular, incrementing a counter does not by itself wait for a callback already running.

AIL_lock_mutex transfers to helper0x1090. With its separate enable flag set, that helper obtains/creates a global mutex and waits indefinitely; its corresponding release paths call the imported ReleaseMutex. Import-table mapping confirms the inspected indirect targets are CreateMutexA, WaitForSingleObject and ReleaseMutex. With the enable flag clear, the helper returns without that wait. Thus even the mutex observation is conditional; this review did not establish all initialization/configuration states.

The sample registration export calls that helper, reads the prior callback field at sample offset0x160, stores the new pointer, then follows the conditional release path and returns the saved prior value. The stream export does the analogous prior/store at offset0xec. It also has a conditional path that installs or removes an internal sample callback through the sample registration export. These are direct observations of typed pointer exchange under the selected synchronization path; no game pointer translation or cancellation/drain protocol appears in the inspected registration operation itself.

Two relevant invocation paths sharpen the limit:

- AIL_end_sample enters the same helper at RVA0x15422, loads the sample EOS callback at0x15460, invokes it at0x1546b and follows the conditional release afterward. For this inspected path with locking enabled, callback invocation lies within that mutex scope. A replacement from another thread may therefore wait for this callback; that statement is path/condition-specific, not a universal callback scheduling rule.
- The stream-service routine beginning0xffa0 reads the stream callback near0x10031 and invokes it at0x10042. Its local control flow uses another counter and a per-stream guard, and does not itself call0x1090 before this invocation. The internal sample-to-stream bridge at0x11930 also reads the stream callback and tail-transfers to it. This review has not established all callers' held locks or all producer paths, so it does not claim the stream service is globally mutex-free. It does establish that registration's mutex call alone is insufficient evidence that every stream callback shares the sample end-call exclusion.

For EOS97 interpretation: a blocking active-null registration can be explained by a particular shared mutex path; a nonblocking result can arise under another path/configuration. Neither proves what AIL_lock does to all producers. Callback-target reads occur before indirect invocation; whether replacement can interleave there depends on surrounding synchronization. A fixed helper trampoline resolving a newly current client callback remains unproven as equivalent to the native selected pointer. Exact prior-pointer tests remain useful, while timing classifications must stay observations rather than universal assertions.

No broad whole-DLL control-flow proof, runtime flag values, producer-quiescence guarantee, unregister cancellation, close barrier, or future Miles64 equivalence is claimed. Do not convert the plain AIL_lock/unlock API into an assumed owner-thread mutex/drain contract. Frozen97 source and planned run remain unchanged.
