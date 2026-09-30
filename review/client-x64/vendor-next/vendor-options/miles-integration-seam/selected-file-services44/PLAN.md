# Selected file services 44 — source-only candidate

This bounded candidate starts from owner37 production sources and implements the service-selection dependency in host-callback-binding42/INTEGRATION-MAP.md. It changes no existing snapshot or product source. No build or test was executed, no vendor code was copied, and no SDK/runtime result is claimed. The exact plain native-file-callbacks35 ClientMilesFileCallbacks.h is copied unchanged; it requires the Windows MSVC calling convention. There is no native64 API library.

## Implemented source path

`retain(open, close, seek, read, callbackLifetime)` creates an immutable table using the actual native35 callback typedefs and returns private FileServices containing four context-aware ordinary C++ thunks and a shared owner. There is no global or TLS-selected table. Every Invocation copies FileServices and therefore retains its table and callback lifetime. Its separate existing lifetime pin retains session/engine context.

FileSessionContext now requires explicit selected services and stores them const. SessionFileOwner validates them before coordinator registration and forwards them to the actual FileInvocationJob::enqueueAdmitted. FileInvocationJob passes them into Invocation rather than silently using canonicalServices. There is deliberately no default/canonical overload. Production dependencies are copied; old owner37 portable_job/tests are excluded because they hardwire their own table and must not be mistaken for tests of selection44.

Open preserves the exact uint32 status and native-width output handle separately, including non-1 success and successful handle zero. Close forwards the local handle once, seek forwards signed offset and signed return, and read forwards the requested extent and destination. Existing Invocation exception capture and result validation remain responsible for uncertainty; the adapter does not catch and convert exceptions to EOF or failure status. It initializes the output handle storage to zero for defined local storage, without interpreting a zero handle as failure. This does not establish semantics for a callback claiming success without writing its output.

Null callbacks and absent lifetime owners are rejected before invocation. `retain` creates a private value only: it does not install callbacks or authorize table replacement. Registration, replacement/default-table semantics, exact x86 host thunks, continuous pipe I/O, ACKs, TLS admission, and cleanup remain unimplemented. The callback lifetime pin must actually own the relevant callback code/state; shared_ptr<void> alone cannot prove that external contract.

## Reentry boundary audit

A guard must cover the entire dynamic extent of executing a selected client callback on EngineFileWorker, with exception-safe removal. Every synchronous pipe-backed ClientMiles entry must check that callback-origin guard BEFORE taking a session/command lock, posting a command, or waiting. Checking only host thunk recursion is insufficient: the client worker can otherwise wait for a host command loop already waiting for that worker's reverse reply. The guard identifies execution context only; it must never select the table or carry callback results.

Rejecting reentry by throwing alone is insufficient if user callback code catches that exception and returns normally. The final composition needs a sticky per-invocation reentry-failure observation reported to the callback owner; that owner must prevent a fabricated normal completion and follow terminal failure handling. The active worker callback must unwind/finish before its resources are released. No generic nested dispatch is proposed. No guard is added in this service-selection unit because the synchronous facade and operational terminal-failure protocol are outside it; installation must remain disabled until that integration exists. Audit the actual selected canonical callbacks and their callees for synchronous facade reentry before enabling them.

## Review and verification sequence

1. Review the exact source.patch and the ownership/ABI boundaries above.
2. Author the tests specified in PROPOSED-TESTS.md using the actual Invocation, codec, and selected-services source, plus a narrowly labeled portable Windows job shim if testing the actual FileInvocationJob translation unit. Do not substitute a portable job that chooses its own services.
3. Seek the parent's test-execution decision after this concrete plan. No test execution has occurred in this unit.
4. Any later native compilation or engine/vendor runtime work requires its separately authorized scope. Portable tests cannot prove MSVC ABI, Thread TLS, engine allocator, Windows event publication, or original DLL behavior.
