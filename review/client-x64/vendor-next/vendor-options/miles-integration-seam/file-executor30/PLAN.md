# File-executor30: source proposal, not product adoption

Scope: one engine-owned FIFO file thread, using the existing `sharedThread::Thread` implementation and file26 `Invocation`; link only against step29's extracted common operations. Four source files implement that mechanism. No compiler, VM, native runtime, Audio/ExitChain workload, test or product modification is part of this proposal. Frozen step29 remains unchanged.

## Concrete mechanism

`EngineFileWorker.cpp` is compiled with original engine/STLport flags. Its header exposes only opaque context and a nonthrowing function pointer. Engine queue nodes are allocated/freed in that TU; modern typed state is never deleted there. Factory/destroy functions keep the worker's own allocation/destruction in the engine TU. `FileInvocationJob.cpp` is a separate modern-STL TU holding file26 Invocation, Binding and the existing shared lifetime pin; it owns/deletes its private pending context. No STL container, smart pointer, exception, or exception_ptr crosses the engine boundary. Do not switch the engine's STL to compile this.

Thread facts from product49d0:

- `sharedThread/src/win32/Thread.cpp:74–77` stores `_beginthreadex`'s possibly-null result and returns void. The prototype uses a narrow subclass to inspect its protected handle; blindly waiting after runNamedThread would hang on creation failure.
- Thread begins with refcount one (`:64–70`). Prototype adds one owner ref before starting. On creation failure it releases both refs, without a join. On success `threadFunc` installs TLS, calls run, removes TLS, and `kill` releases the self ref (`:94–119`). Owner calls wait, then releases its retained ref. Destructor cannot race self-release.
- Ready is signaled from inside run, therefore after TLS installation. Prototype never installs/probes TLS, never uses the legacy once block and never calls FileStreamerThread. Startup may still terminate/hang if the engine's own TLS initialization fatals; no cancellation/recovery guarantee is invented for that existing fatal path. Thread's own pre-run naming/id behavior remains inherited.
- Gate readiness and queue wakeups reuse the engine's existing Gate; queue mutation and reset/open happen under its Mutex, preventing lost wakes. Each node is removed once; operation runs with that lock released. No nested pumping occurs during the FileStreamer TLS-gate wait.

`submit` returns after FIFO publication. Its typed pending context retains the Job and Invocation even if the enqueueing stack ends. A private completion event publishes the immutable result; the control loop polls status and the designated waiting thread can wait. Neither pipe reader nor control thread may block on the file result. The helper's SDK callback remains synchronous by waiting for the resulting reply. There is no callback into the receiver from the worker. Normal adapter exceptions are retained in file26 Completion; an unexpected dispatch exception becomes DispatchUncertain. No retry, fabricated EOF, new close policy, or publication decision is supplied.

## Existing owner and admission contract

The backend/session owner must own exactly one worker, create it on the engine installation thread, and retain it through callback production and all queued work. It must stop all potential submitters before destroy. Its existing request/registration/file registry remains the only source of valid identities and pins. `FileInvocationJob::enqueueAdmitted` takes the existing `shared_ptr<void>` lifetime pin plus immutable Binding and constructs the existing Invocation; that pin is not proof of TLS, vendor quiescence or scheduling authorization.

`Coordinator` is a single-control-thread model. Keep its admitCallback / acknowledge / completeAdmission operations on that thread, not the worker. completeAdmission refuses while causal callbacks remain; beginDrain permits separate cleanup admission; readiness includes vendorTerminationUnproven=true. Do not acknowledge merely because an item was dequeued: preserve callback accounting until the owner's actual completion/publication/ack protocol permits it. CallThrew/DispatchUncertain never authorize retry or automatic retirement. Callback observations admitted in Failed are not execution permission.

**A concrete owner integration gap remains:** Coordinator::registerCallback requires an existing valid resource. Global file callbacks are installed before driver creation (Audio.cpp:1293 vs :1300), and FileOpen has no preexisting File binding. No current source establishes the root registration/admission mapping for these callbacks. Define that mapping in the existing owner before product adoption; do not invent a fake resource in this worker. Bound outstanding jobs through that owner's existing capacity/pin accounting; this FIFO intentionally has no second capacity/replay/lifecycle model.

## Exact lifetime placement

Future hook: establish worker readiness before callback registration, and make the pipe-facing file dispatcher its only consumer of the step29 admitted interface. Preserve the native callback path separately. Concurrent original SDK callbacks and worker operations would violate the map's single-owner contract; this prototype cannot be adopted while both can execute uncoordinated.

Normal removal sequence owned by Audio/backend session:

1. Stop new ordinary game admission using existing coordinator drain semantics. Keep reverse file intake, worker and engine resources alive during stopAllSounds/close_stream and vendor shutdown. Do not call worker drainAndJoin yet.
2. Establish vendor callback-production termination independently of the worker. A shutdown RPC reply alone is not currently proven sufficient. Continue receiving file messages and observing admitted completions during the shutdown wait.
3. Once producers are quiescent, resolve every admitted completion, publish any successful open into the owner registry, and queue the required residual known-file closes through the same operation path. Every such cleanup close needs existing owner identity/admission and lifetime pins; the worker neither scans Audio's map nor fabricates wire requests. The concrete owner cleanup adapter is not implemented here. Uncertain open/close outcomes cannot be silently replayed or treated as closed.
4. Stop submitters, call drainAndJoin, then destroy worker and release registry/session pins. This drains queued closes before Thread removes its TLS. No forced thread termination, timeout-based abandonment, or destructor join is used. If a read remains blocked, owner cannot destroy the worker or its backing resources.

Partial install requires separate `workerCreated/started` ownership and actual vendor-startup ownership, not Audio's late `s_installed`. Driver failure calls Audio::remove before that flag is set (`Audio.cpp:1314–1323` vs :1373); the existing AIL_shutdown block would otherwise be skipped. Failed native thread creation safely releases both refs without TLS teardown. After readiness, any later failure must run the same producer-quiesce/close/drain/join sequence before releasing file resources. Do not register teardown inside worker TLS.

Actual application order supports an Audio-owned join: ClientMain.cpp installs sharedThread/TLS at :138, sharedFile at :235, clientAudio at :303; SetupClientAudio registers its remove after Audio installation. ExitChain inserts equal-priority entries in reverse installation order. ClientMain calls Foundation remove at :384 and explicit sharedThread/TLS remove at :385. Keep the join inside Audio cleanup before it returns; do not add a late generic ExitChain hook. Fatal-path ordering remains separate, unproved acceptance.

## Limits before adoption

No successful-path source evidence currently requires causal requests on the original waiting game thread. All file requests therefore share this worker. Actual DLL worker dependencies/reentry, global callback registration mapping, termination evidence, residual-close adapter and partial Audio install integration remain unresolved. Main-thread-only TreeFile cache diagnostics and fatal ExitChain context differ from direct main-thread execution; the AbstractFile audio hook is not in the inspected normal callback path. This proposal does not claim gameplay or shutdown fidelity.

Next permitted discriminator would be separately reviewed object-only compilation of these engine and modern adapter TUs plus file26 dependencies, using the recipe below. Source approval does not authorize the rejected Audio/ExitChain runtime workload or any new engine runtime. No gate has been run for step30.
