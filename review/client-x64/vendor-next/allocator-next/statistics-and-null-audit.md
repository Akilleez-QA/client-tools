# Allocator statistics and null reallocation: separate next repairs

2026-09-30, read-only production audit of client-build-next after the checked-size
candidate. Parent owns implementation selection, product VM and commits.
POODO framing waiver: the existing user/parent scope already identifies the goal
(real x64 client, preserved valid Win32 behavior, no fake allocator), authority
(read-only audit) and acceptance limits. This note selects no production edit.

## Observed statistics mechanism

Windows LLP64 leaves unsigned long at 32 bits. The following MemoryManager.cpp
byte counters are unsigned long: ms_allocateBytesTotal, ms_currentBytesRequested
(tracking/guards), ms_currentBytesAllocated, ms_currentBytesAllocatedNoLeakTest
(tracking), ms_maxBytesAllocated. All three public byte getters return unsigned
long. Allocation/free update under the existing lock; getters read directly.
Cumulative total can overflow even when current usage never approaches 4 GiB.
Per-frame PixCounter::ResetInteger has its own int API; it is another metric
width limit, not heap policy. Allocation-count ints are a distinct count domain.

This is **not merely wrong display**:

- Game::garbageCollect compares current bytes / MiB with 90% of configured limit.
  At an actual 4 GiB + 128 MiB and limit 4096 MiB, legacy wrapped getter reports
  128 MiB: automatic collection is incorrectly suppressed. Explicit/immediate
  collection paths still work. No live multi-GiB gameplay run has tested this.
- MemoryManager::free's DEBUG_FATAL tests current-byte total against block size.
  A wrapped total smaller than a legitimate freed block falsely signals underflow.
- ms_maxBytesAllocated ceases to record correct high-water usage after wrap.
- Heap-fit, free-list traversal and the system hard-limit check use block sizes
  and system-MiB counters, not these wrapped byte totals. This specific defect
  does not directly bypass the allocator hard limit.

Getter declarations are not DLLEXPORT. No matching DllExport.cpp stub or .def
export was found. Changing return width requires all static callers rebuilt,
not a new renderer allocation-hook import signature. MemoryManager's allocation
owner API is independent. Public forwarding header forwards the real header.

## Caller closure (all direct getter occurrences searched across checkout)

| File | Consumer / required handling |
| --- | --- |
| MemoryManager.cpp | 3 APIs in normal and disabled branches; five counters; destructor/debugReport formats; free underflow cast |
| Game.cpp | GC threshold; debug freed-MiB message; loader before/after; five-entry crash-report history and %lu formatting |
| SwgCuiDebugInfoPage.cpp | converts bytes to int MiB; bounded by existing signed-int MiB capacity, use explicit conversion after division |
| PlotterManager.cpp | unsigned long previous snapshot then int delta; signed wide subtraction before float plotting |
| CachedFileManager.cpp | unsigned long snapshot and signed-int cumulative byte delta; signed wide delta/total, then float MiB display |
| InstallTimer.h/.cpp | unsigned long member/end snapshot; signed-int displayed difference |
| XmlTreeDocumentList.cpp | debug before/after and int-cast logged delta |
| LogicalAnimationTableTemplateList.cpp | debug before/after snapshots, float MiB delta |
| SkeletalAppearance2.cpp | snapshots plus three int debug accumulators and max(0,int(delta)); maintain positive-delta policy with wide arithmetic |
| ViewerDoc.cpp | unsigned long snapshot/int delta and %i report |
| MayaExporter/ExportStaticMesh.cpp | direct getter arguments passed to %lu |

Signed deltas must remain signed: operation can free more than it allocates.
Simply widening unsigned operands and casting the resulting wrap to int64 is
not the clearest contract. Convert each snapshot to int64 before subtracting;
current signed-int MiB aggregate ceiling is far below INT64_MAX. For consumers
that intentionally discard decreases, compare snapshots and subtract only when
end > start, preserving that policy. Audit accumulator format strings together.
Game's `(limit * 9) / 10` also overflows int for large configured limits. Multiply
in uint64/int64 first and retain integer truncation; do not use floating rounding.

## Smallest defensible statistics proposal

A public ByteCount alias: unsigned long on Win32, uint64 on x64 (and an explicit
policy for other targets, preferably size_t or uint64). Use it consistently for
byte counters, all three API results and snapshots. Preserving Win32's underlying
unsigned-long type retains its source ABI and atomic-width snapshot reads; a
blanket uint64 conversion also on Win32 introduces new torn-read considerations.
Widen signed deltas/accumulators where needed, use PRIu64/PRId64 with explicit
casts in variadic messages, and repair GC comparison arithmetic. Keep count
counters and block/region sizes out of this commit. Non-Windows disabled API
implementations must match the new declarations; do not silently truncate their
/proc arithmetic. Server repo has no corresponding MemoryManager.cpp.

No giant allocations needed for a discriminating native test: a **disclosed
synthetic-statistics diagnostic** can seed actual internal counters just below
UINT32_MAX, then call the real allocator/free with a small block, verify getters,
high-water and restoration. Preserve/restore all seeds before global teardown.
This validates the arithmetic on real operations, not actual 4-GiB residency.
Separately test the extracted actual GC threshold expression against 4GiB+128MiB
and large-limit cases. Product four-config compilation catches caller formatting
and conversion errors; native GUI/gameplay remains separate.

## Tracked reallocate(NULL): separately observed defect

Real tracked DO_TRACK=5 probes in all four configurations already crash with
0xC0000005 for reallocate(NULL,16). Source explains it: allocatedBlock remains
null, oldSize=0, then DO_TRACK reads getOwner(0)/checkForLeaks unconditionally.
Untracked mode currently supplies owner=0, leakTest=false and array=false; NULL0
returns NULL before metadata access. Non-null growth retains owner/array/leak
flags and copies then frees; zero frees existing input with its own array flag.

Only two direct production callers were found:

- SetupSharedXml::xmlReAllocate paired with xmlAllocate=new byte[] and xmlFree=
  delete[]. It is installed as libxml's realloc callback.
- OciSession reallocHook paired with mallocHook=new char[] and freeHook=delete[].

Small repair in MemoryManager: read metadata only when allocatedBlock is nonnull,
otherwise preserve the existing untracked defaults (owner0, no-leak, scalar).
Do not globally decide that every null realloc is an array: API itself carries
no array parameter. At each actual adapter, NULL and positive size must route to
its existing allocation callback so later delete[] matches. Preserve NULL0's
existing return behavior unless a separate caller contract establishes otherwise.
The OCI hook owner-context argument can be passed to mallocHook; XML directly
calls xmlAllocate. No exception/failure policy change is needed.

Acceptance: actual MemoryManager NULL0, NULLpositive/free(false), tracked flags,
non-null scalar/array growth and zero, no-leak preservation; real XML callback
NULLpositive then xmlFree with DO_SCALAR/guards enabled; equivalent OCI hook
compile/runtime requires real OCI dependencies, so do not fake them. A source-
only synthetic copy of callback text does not establish actual callback linkage.

## Twenty materially distinct paths considered before convergence

1. Leave wrap documented (fails x64 policy correctness).
2. Saturate statistics at UINT32_MAX (loses accurate totals and decrement meaning).
3. Cap entire heap below4GiB (defeats x64 memory goal).
4. Wide counters but unchanged getters (hides true usage from GC).
5. Wide getters but unchanged consumer locals (moves truncation).
6. Conditional native-width ByteCount plus full caller closure (preferred narrow ABI policy).
7. Fixed uint64 all ABIs (valid broader change, needs Win32 read synchronization).
8. Add new wide getter APIs retaining old wrappers (extra migration/API burden).
9. Replace counters with recomputation from region/block walk (cost/synchronization change).
10. Add locked atomic snapshot struct (broader concurrency redesign).
11. Use existing system-MiB counter for GC (measures reserved regions, not live allocations).
12. Synthetic-statistics real-operation boundary probe (bounded discrimination).
13. Actual >4GiB resident integration stress (later resource-heavy corroboration).
14. Preserve counters but fix GC alone (leaves false free assertion).
15. Treat byte and allocation-count width as one patch (reject unnecessary coupling).
16. Reject NULL realloc outright (breaks existing untracked and callback expectations).
17. Null-aware metadata defaults in allocator (preferred narrow crash repair).
18. Make all null reallocs arrays (reject ambiguous core API contract).
19. Route adapter null-positive through matching allocator (preferred paired ownership).
20. Replace allocator/callbacks with CRT realloc (reject allocation-domain mismatch).

## Primary research gate and evidence boundaries

2026-09-30 queries: Microsoft LLP64 long widths; MSVC realloc NULL/failure contract.
Primary sources consulted:
- https://learn.microsoft.com/en-us/windows/win32/winprog64/abstract-data-models
- https://learn.microsoft.com/en-us/windows/win32/winprog64/designing-64-bit-compatible-interfaces
- https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/realloc?view=msvc-170
- https://learn.microsoft.com/en-us/previous-versions/xbebcx7d(v=vs.140)
LLP64 documentation supports width diagnosis; CRT realloc documents useful
expectations, but cannot impose return/fatal/array policy on this custom API.
Vendor libxml xmlmemory.h/globals.c confirms callback role in this checkout.
Source audit supports identified policy consumers, not observed live heap usage.
Independent peer critic requested specifically to challenge scope/default policy;
shared-source agreement is not independent runtime corroboration.

Delivery: audit authored, no production edits. Outcome: source-observed closure;
null crash previously native-observed. Next test controlled by parent/native agent.

## Authorized statistics candidate and bounded acceptance

Parent subsequently authorized only the statistics candidate; null repair remains
untouched. Thirteen production paths changed. ByteCount is uint64_t on Win64 and
unsigned long elsewhere, preserving existing Win32/Linux ABI. Each live getter
consumer is updated. Existing shared server copies explicitly lack these getter
uses, so these consumer hunks have no matching server API to mirror.

Prediction: synthetic counters just below UINT32_MAX plus real small allocate/free
will cross the boundary without truncation on x64; Win32 retains its existing
underlying unsigned-long type and modulo behavior. No giant resident heap claim.
Native VS2013 seeded-statistics fixture v5: **11/11 each on Debug/Release ×
Win32/x64**, exit0. It checks all five counters/three getters, high-water update,
restoration on x64 free, and return to saved real state before process teardown.
The Win32 test restores synthetic counters before free to avoid deliberately
triggering its preserved historical underflow assertion. Real MemoryManager,
DebugHelp, InstallTimer TU and real static dependency libraries are linked.

Native caller compile fixture v4: **32/32 successful compilations** (8 changed
client dependency TUs ×4 configs). Viewer and MayaExporter have no existing
native audit/config in the client closure: eight matrix rows explicitly report
not compiled, never passes. Their type/format edits are source-reviewed only.
This is TU compilation, not a fresh full product link or live GC test.

Scratch adaptation: changed real MM/InstallTimer headers are prepended with their
real FoundationTypes/FirstPlatform prerequisites and their relative includes
resolved to existing absolute VM source paths, before the old product First
headers can include unchanged MM. No declarations or dependencies substituted.
Earlier fixture failures preserved: STLport incompatibility with MSVC type_traits
(v1); include-order failures selecting old MM (v2), missing platform selector(v3)
and missing FirstPlatform declarations(v4). V5 corrects diagnostic packaging,
not production behavior. Artifacts in `native-statistics/`.
