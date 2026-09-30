# Miles replacement boundary — checkpoint51

The intended shape is one plain native-Miles-style C++ interface used by game audio. A direct native implementation can replace the temporary pipe implementation without changing that interface. The pipe protocol, helper process, file identities, callback scheduling and modern C++ ownership stay private. This is a source-compatible design target for the possessed Miles7.2a Windows declarations; no arbitrary future SDK ABI or game-fidelity equivalence is claimed. No x64 Miles binary is available to link.

## Newly checked components

- Protocol48 portable: eight scenario groups,8085 low-level assertions, strict Clang ASan/UBSan; installation registration echo, exact fixed ACK context, old-version rejection and stream parent echo. Most assertions are byte/truncation checks, not8085 independent behaviors.
- Host49 portable:338 positive assertions in seven groups plus six explicitly armed terminate subprocesses. Host-local tokens, client-wire file identities and private registry entries stay separate; validated consumption precedes ACK and actual result exposure. Death cases deliberately skip cleanup and cannot prove leak/teardown behavior.
- Client50 portable:407 assertions in seven groups. ACK routing uses existing mapper rows; causal command settlement waits for consumption. Rejected or uncertain work remains retained. The worker/job supplier is scripted.
- Native host49: all six actual v120 objects compiled cleanly with warnings-as-errors, three units on Win32 and AMD64. No link or SDK execution.

Every first gate preserved exact inputs and raw outcomes. Results and limits are in each component directory; repeated source reviewers are not independent runtime confirmation.

## Interface correction

Native surface audit50 found public std::string and std::runtime_error in the previous proposed facade. Actual game code uses STLport; isolated modern-library object builds had not established that boundary. Public proposal51 now exposes plain scalars, opaque sample/stream/driver pointers and native-shaped callbacks only. Its independent source review caught three missing live seek constants; corrected v2 retains the original v1 and review.

Private exception containment, separate C-string snapshots and typed completion callback adapters are implementation obligations. Plain declarations alone do not satisfy them. Source52 implements nine startup operations against private real SDK declarations with contained exceptions, but was uncompiled when this checkpoint was written.

## Actual pipeline work

Host runtime50 and client runtime53 are newly authored source compositions with separate cross-review. They join the earlier components to actual Endpoint ownership and actual worker interfaces. Neither is yet enabled in the executable, built or run. Normal teardown, lock/cleanup transitions, EOS callbacks, complete public facade implementation and final LiveChannel/Session wiring remain open. Runtime53 specifically retains failure-owned state; it supplies no successful destructor-based cleanup.

Product integration/client-x64-next remains clean at49d0eeed4ddaa177d7a93ea396c37c3d9b9942da. No new PR or upstream mutation. The next gate is the plain public/private boundary and native source integration, followed by reviewed paired lifecycle and bounded intended-use tests. The earlier real-engine teardown/allocator workloads remain excluded. Full x64 client link/start and representative gameplay/audio acceptance remain outstanding.
