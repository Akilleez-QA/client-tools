# Next assembly fixes — bounded read-only audit

Source: client-build-next observed through f102763f701193b72d975a6f6a7822dde4bd1f23;
server-client-compat a3f496be71c26f2ed4e71a6c0323344db2434fa5. No edits, VM
commands, commits or pushes performed. Parent owns implementation.

## ProfilerTimer: small isolated shared repair

Client/server Win32 ProfilerTimer.cpp are byte-identical. The only architecture
blocker is the naked readTimeStampCounter helper's rdtsc/ret assembly. On x64,
use intrin.h and __rdtsc(), explicitly converting its unsigned 64-bit result to
the existing signed __int64 Type; retain the original x86 helper. Mirror this
shared source change server-first. Do not alter calibration, QPC default,
DebugFlags or timing units in this commit.

Microsoft documents that __rdtsc emits RDTSC and returns unsigned __int64 on
x86/x64: https://learn.microsoft.com/en-us/cpp/intrinsics/rdtsc
This does not establish cross-core monotonicity, serialization, calibrated
accuracy or constant frequency. The existing RDTSC path already shares those
limitations. getCalibratedTime's zero/short elapsed window and float arithmetic
are pre-existing concerns, not reasons to fold a clock redesign into this port.

Acceptance: actual MSVC Win32/x64 TU builds; native fixture toggling the registered
useRdtsc flag, exercising both getTime/getCalibratedTime branches after nonzero
elapsed time. Confirm QPC default remains unchanged and generated x64 helper
contains RDTSC. Runtime sampling proves only sampled operation, not timing accuracy.

## OsNewDel: cannot safely change assembly alone

Five overloads manually recover the caller's return address then call
MemoryManager::allocate(size, owner, array, leakTest). Their exact flags are:
not-a-leak scalar false/false; ordinary scalar false/true; ordinary array
true/true; file/line scalar false/true; file/line array true/true. File/line are
already intentionally ignored. Keep deletes, initialization ordering and the
static MemoryManager object unchanged.

For x64, capture _ReturnAddress() directly inside each non-inlined operator,
convert to a pointer-sized owner type, and forward to allocate. Capturing inside
a shared non-inlined helper would identify the operator instead of its caller.
Microsoft explicitly warns that inlining changes the return address observed:
https://learn.microsoft.com/en-us/cpp/intrinsics/returnaddress
Do not use _AddressOfReturnAddress to locate arbitrary stack arguments; Microsoft
forbids that assumption:
https://learn.microsoft.com/en-us/cpp/intrinsics/addressofreturnaddress

The owner path is still uint32 end to end. Required associated audit/repair:
- MemoryManager.h allocate signature; both enabled/disabled implementations.
- AllocatedBlock getOwner/setOwner/m_owner, local owner variables in reallocate
  and report; temporary owner arrays in allocate and own(); all address logging.
- DebugHelp getCallStack/lookupAddress interfaces and all caller buffers.
- DllExport.cpp's exported MemoryManager::allocate signature (DLL ABI).
- Direct3d9 and Headless MemoryManagerHook localAllocate wrappers,
  RenderWorldServices and RegexServices allocator wrappers.

DO_TRACK is currently zero on Windows, so stored-owner paths are compiled out;
that is not evidence their existing 32-bit types are safe. Debug logging still
uses the owner argument. Widening stored owners when tracking is enabled also
changes allocation-header sizes, requiring layout/alignment checks.

There is no sharedMemoryManager/OsNewDel counterpart in server-client-compat.
The server Win32 DebugHelp has uint64 storage/interfaces, but is NOT an x64
implementation: it still uses inline asm, context.Eip/Esp/Ebp and
IMAGE_FILE_MACHINE_I386. Copying it wholesale does not fix client stack walking.
It even passes process as StackWalk64's thread handle; keep a caller-aware audit
and native stack oracle before asserting correctness. Linux DebugHelp evidence
cannot establish this Windows behavior.

Acceptance: five overload forwarding tests on real Win32/x64 code, owner address
above 4GiB on x64 preserved; owner resolves to known allocation callsite with
symbols, not an operator/helper frame. Use separate noinline callers to prevent
optimizer folding. Exercise array/scalar and not-a-leak flags, realloc ownership,
and DLL hook ABI linkage. Test tracking-enabled header alignment and stack-buffer
canaries separately. Actual native stack fixture must show multiple known nested
frames with nontruncated addresses, and empty/unavailable-symbol behavior.

## Recommendation and limits

Take ProfilerTimer as its own small mirrored commit. Treat OsNewDel, allocator
owner widths and Windows stack capture as a sequenced but coupled address-width
repair. A compile-only cast that truncates _ReturnAddress or returns zero would
hide the defect and is rejected. No runtime claims are made by this source audit.
