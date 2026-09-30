# Allocator size/root-cause audit (read-only)

## Current arithmetic limits

The OS accepts SIZE_T, but this allocator does not: SystemAllocation::m_size and
constructor are int; Block::getSize returns int; allocate rounds a size_t narrowed
to int; convertBytesToMegabytesForSystemAllocation adds a4MiB rounding bias in int.
No amount of pointer widening establishes large-allocation safety.

Let B=cms_blockSize, H=cms_allocatedBlockSize, G=cms_guardBandSize, R=4194304.
A=align16(H+2G+max(request,1)). Region request is3B+A, rounded up toR.
For the current signed-int helper to stay defined:

    3B+A <= INT_MAX-(R-1) = 2143289344
    request <= 2143289344-3B-H-2G

The right side is16-byte aligned because B,H,G are. It also leaves enough slack
for the allocator's split comparison A+H+2G+1. With tracking or guards, requested
size storage imposes an independent maximum (1<<30)-1 =1073741823. Effective maximum
is min(arithmetic bound, requested-size bound) when those paths are enabled.
Default Windows H/B differ by ABI; derive them from actual types, not hardcoded
estimates. Validate size_t input before any cast, additions, metrics or lock.

There is a separate region-size route: setLimit(...,preallocate=true) calls
allocateSystemMemory directly. Its megabytes parameter can create a region larger
than INT_MAX; casting size_t to SystemAllocation(int) then corrupts region layout.
Validate positive megabytes, <=floor(INT_MAX/1048576)=2047, and totals without int
addition overflow. Existing automatic rounded growth max is2044MiB; preallocation
is not required to be4MiB rounded. A process total can exceed one-region size only
through multiple bounded regions; blindly rejecting a limit >2047MiB changes its
meaning. Prefer bounded-region chunking for large preallocation if that path is in
scope, with tests, otherwise explicitly reject unsupported preallocation before OS
allocation. Do not pretend that a high soft limit itself is a single allocation.

## Aggregate statistics are a separate width issue

ms_currentBytesAllocated, ms_currentBytesRequested, no-leak bytes, maxima and total
allocated bytes are unsigned long (32bit on Win64). Per-allocation checks alone do
not prevent wrapping once total live memory exceeds4GiB. ms_currentBytesAllocated
also participates in free-underflow diagnostics. Allocation call counts/int
allocation counts and per-frame PixCounters have their own eventual limits.

Consumers include XmlTreeDocumentList, CachedFileManager, InstallTimer (member too),
ViewerDoc, PlotterManager, Game (history arrays and locals), SwgCuiDebugInfoPage,
manager reports and public getters. Most store unsigned long or int and format%lu.
A statistics-width repair must update the API and these consumers together; don't
silently return a truncated unsigned long from a widened internal counter. Preserve
Win32 ABI deliberately (alias unsigned long on Win32, pointer-width type onWin64,
or a separately reviewed uint64 API), and audit signed deltas before conversion.

## Failure policy and boundaries

Current exhausted allocation leaves the mutex then invokes FATAL. Checked oversized
requests should likewise fail loudly before heap/stat mutation, with correct%Iu or
portable size format. ReturningNULL from global new paths or introducing throw
policy silently would be a different contract. A rejected growth must not alter
the old block before rejection. Existing FATAL size message and two debug messages
incorrectly pass size_t to%d; fix these with the same boundary report work.

Test invalid sizes SIZE_MAX, INT_MAX,2^32 and effectiveMax+1 in separate native
processes. Require the specific rejection marker/exit, never count arbitrary crash
as pass. They must reject before OsMemory::commit; use a debugger/API trace or
independent real-OS call observation, not a replacement heap. Pure checked sizing
helper tests can exercise max-1,max,max+1 without reserving gigabytes. Small real
alloc/free/grow and existing2568 tests then validate integration. Do not allocate
effectiveMax merely to prove arithmetic accepted it.

## Null realloc semantics and callers

DO_TRACK reallocate(NULL,n>0) dereferences allocatedBlock->getOwner/checkForLeaks;
reproduced0xC0000005 in all four native configurations. Untracked code instead uses
owner0,arrayfalse,leakfalse and allocates. NULL,0 currently returnsNULL. Nonnull,0
frees. Growth preserves owner/flags; shrink returns original block unchanged.

Exactly two external direct callers found: SetupSharedXml::xmlReAllocate and OCI
OciSession reallocHook. Their paired allocators use new byte[]/new char[] and paired
frees use delete[]. Therefore null handling cannot casually pick scalar flags when
DO_SCALAR is enabled. Best explicit mapping: preserve the manager's pre-existing
untracked NULL contract (owner0,scalar,no-leak) when making tracking null-safe, and
make each adapter route NULL,n>0 through its own existing allocation function so
array/leak semantics match. Alternatively define manager NULL behavior as array+
leaktrue based on these known callers, but that changes its general public contract
and should be documented/tested. Do not infer caller address fromNULL or invent
an owner. Count and flag fixtures must cover both adapters, NULL0, NULLpositive,
nonnull0, same/shrink/grow and payload/owner preservation. Server counterparts need
an exact path audit before mirroring; no server behavior was assumed here.

## Twenty considered approaches

1. Silence narrowing warnings: reject; hides overflow.
2. Widen all ints: reject unbounded scope and layout consequences.
3. Switch allocator implementation: reject; unrelated replacement.
4. ReturnNULL for huge global-new inputs: reject silent policy change.
5. Throw bad_alloc only for range: defer explicit policy decision.
6. Existing FATAL before mutation: preferred contract-preserving rejection.
7. Uniform1GiB-1 cap: simple but tightens untracked legacy capacity.
8. Configuration-derived representable cap: preferred minimal behavior change.
9. Checked size_t arithmetic then narrow once: preferred.
10. Signed arithmetic with post-check: reject undefined overflow occurs first.
11. Saturate/clamp requested size: reject underallocation.
12. Rely on VirtualAlloc failure: reject OS can succeed past internal width.
13. Validate only allocate(): insufficient preallocation bypass.
14. Validate bounded region creation too: required.
15. Chunk large preallocation into bounded regions: viable separate implementation.
16. Cap aggregate heap at4GiB: avoid as x64 completion strategy.
17. Widen statistics plus all consumers: required independent width repair.
18. Fix trackedNULL with ternary defaults only: preserves old untracked semantics,
    but adapters still need array-policy handling.
19. Route adapterNULL through its matching allocate: preferred explicit semantics.
20. Giant real allocations as tests: reject resource risk; arithmetic boundaries+
    invalid-input subprocess rejection and small real allocations suffice.

## Primary references and boundaries

Microsoft VirtualAlloc declares SIZE_T, supporting the distinction between OS and
allocator limits: https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualalloc
Microsoft realloc documents NULL/zero/original-block-on-failure semantics; this
custom API is not automatically identical and uses FATAL:
https://learn.microsoft.com/en-us/previous-versions/xbebcx7d(v=vs.140)

No production edits in this audit. Arithmetic formulas are source-derived and need
native checked-helper/boundary tests before being implementation acceptance.

## Candidate and native acceptance (2026-09-30)

The selected repair is confined to MemoryManager.cpp. Per-request arithmetic is
checked before narrowing or allocation statistics/locking; the cap is derived
from the existing signed region representation, rounding and tracking layout.
The alignment premise is now a static assertion. Existing fatal policy is used.
Preallocation creates regions of at most 2047 MiB instead of narrowing a larger
region into an int. It does not cap the configured aggregate memory limit.
Hard-limit arithmetic subtracts remaining capacity before addition. A zero-size
preallocation no longer asks the OS to commit a zero-byte region.

Predictions recorded for the candidate: small allocations retain alignment,
payload and owner behavior; effective maximum and maximum-minus-one fit the
arithmetic; maximum-plus-one, INT_MAX and SIZE_MAX reject; rejected realloc
growth preserves the old payload; preallocation can span multiple bounded
regions without violating a hard limit. These are configuration-dependent
limits, not a promise that a near-maximum allocation succeeds in the OS.

Actual VS2013 native tests, all Debug/Release × Win32/x64, real dependencies:

| Probe | Each configuration | Source distinction |
| --- | --- | --- |
| Boundary, tracking/guards | 21/21 | DO_TRACK=5 plus guards/scalar/fills diagnostic defines |
| Boundary, product untracked layout | 21/21 | Original diagnostic defines remain zero |
| Allocator regression stress | 2568/2568 | DO_TRACK=5 plus guards/scalar/fills |
| Multiple-region preallocation | 12/12 | Only max-region constant lowered to 1 MiB for a real 3 MiB allocation |

Every executable returned zero. Four boundary rejection cases use the actual
FatalSetThrowExceptions/FatalException support, catch the specified message and
confirm no new OS region. Growth rejection preserves the original 64-byte
payload. No fake Fatal, allocator, DebugHelp, STLport or dependency symbol is used.
The region diagnostic runs the production loop against real OsMemory::commit;
it proves loop/list/counter behavior with small regions, not successful real
2047-MiB reservations. It also verifies negative limit rejection before limit
mutation, zero-region behavior and no region growth after reaching the hard limit.

Raw logs, maps, executable/objects and source snapshots are preserved under
`native-size-checks/allocator-{boundary-v1,boundary-untracked-v2,tracking-size-v2,region-v1}`.
The first tracked boundary snapshot predates only the alignment static_assert
and whitespace cleanup; subsequent untracked/stress/region snapshots contain
the final candidate. Runners and probes are adjacent to this note.

Independent critic checked cap/rounding arithmetic, bounded-region size and
remaining-capacity subtraction: no blocker. Aggregate byte statistics remain
32-bit and can wrap above 4 GiB; tracked reallocate(NULL) remains a separate
known fault. This repair does not claim either is fixed. The server tree has no
matching MemoryManager.cpp; no unrelated server implementation was replaced.
