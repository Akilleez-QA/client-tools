# Native-shaped Miles adapter: callback composition checkpoint

The public boundary remains ordinary Miles-shaped calls with opaque native-width handles and the possessed Miles7.2a Win64 callback declarations. Direct adapters compile against those declarations and retain real unresolved SDK imports. The temporary pipe sits behind the same source interface; its tokens, protocol, processes and scheduling do not enter game-facing headers. A future suitable native Miles adapter can remove this private machinery. This is not a claim that any later Miles release is ABI-compatible. No actual x64 Miles library is available here, and no stub library has been fabricated.

## New checked work

- Composed selected callbacks46: real table adapter→owner→scripted job→real Invocation,333 assertions across20 scenarios under strict Clang ASan/UBSan. Five corresponding production objects compiled with actual VS2013 x64; job references the supplied services and real engine-worker entry, with no old canonical-service fallback. This is object/portable evidence, not worker execution.
- Blind46 identified exact-zero forwarding, failed-open publication, pending-job return and isolated ownership gaps. Tests-only successor49 passed391 assertions across23 scenarios. It checks zero handles exactly, status-zero open that writes a nonzero local value without publishing a resource, one-slot reuse after failures, return while work is pending, and Invocation retention without SessionFileOwner keeping the table alive. Production46 remains unchanged.
- Reentry47 guards actual selected/request/close entry points before shared-session access. A caught rejection still poisons the containing file invocation; it cannot encode success. The first portable gate failed at link because a real existing dependency was omitted. V2 added only that dependency and passed strict GCC ASan/UBSan thread/nesting/unwind checks. Both attempts remain recorded. Three production objects compiled cleanly under actual VS2013 x64, including real MSVC TLS references. No Windows runtime is claimed.

The blind review and parent reads are source reviews of shared evidence, not independent executions. Composer47 produced coverage observations that are reconciled against the complete source; Grok47 timed out with no output and supplies no clearance.

## Current connection work

A private version3 installation/consumption-ACK schema is under portable qualification. Client ACK dispatch and host file-result consumption are being connected in separate source candidates. The operational design keeps each overlapped callback endpoint on one owning thread and pins file state until an exact consumed-result ACK. SDK installation remains disabled until those components and failure/teardown paths are composed. Source plans do not establish an operational bridge.

Still open: real SDK callbacks through continuous idle I/O, engine-worker/native scheduling and quiescence, input-buffer retirement, audio-boundary floating-point state, timing/playback fidelity, Bink and complete-client acceptance. The rejected engine/allocator workloads were not repeated.

Product remains49d0eeed4ddaa177d7a93ea396c37c3d9b9942da. This fork evidence checkpoint does not claim a linked, running or finished x64 client. No upstream change or new PR.
