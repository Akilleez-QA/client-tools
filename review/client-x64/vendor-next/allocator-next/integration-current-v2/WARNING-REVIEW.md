# Native x64 warning review: immutable94a81438

Read-only review of completed real SwgClient dependency builds, Release/Debug. Source inspected with git show94a81438 and case-insensitive path matching. No source changes or corruption probes.

## Census, not defect counts

Release7748 and Debug7442 raw lines contain `: warning`, including repeated diagnostics in MSBuild summaries. Collapse compiler diagnostics by normalized file,line,code across both: **808 locations** (516engine/game,25external/ours,267third-party). C4267=579; C4244=90; C4103=62; C4291=33; C4067=18; C4996=16; C4100=6; C4313=1; C4189=1; C4505=1; C4918=1. Messages/configurations/projects/occurrences retained in warnings-grouped.json; exact log hashes recorded. Relative DPVS locations resolve against their project directory.

376 excluded lines are non-location diagnostics:248MSB4121,114LNK4221,12MSB8012,2“warning treated as error” lines. They remain preserved, not silently discarded. MSB4121 mostly reports solution tools with no x64 mapping, not linked game features. Header repetitions are substantial: AutoByteStream.h460 appears1572times, AutoDeltaVector.h443 and451 each1210. These counts are neither root causes nor a completion percentage.

No C4311/C4312/C4302 appeared in parsed warnings. Explicit casts, disabled warnings, unreachable targets, early project failures and dynamic providers remain blind spots. A clean compile is not evidence of their absence.

## Three focused source spot-checks

###1. AutoArray/AutoList pack counts: actual wire-writing path

AutoByteStream.h460 and634 assign container.size() to unsigned int, write that count, then iterate **every** element. An out-of-range container could therefore write a truncated header followed by a larger payload. These paths do not use the existing ArchiveCount helper. AutoList<SearchCondition> is an actual AuctionQueryHeadersMessage member; AutoArray appears in survey, map-location, travel and permission messages. For example the real HUD receives PermissionListCreateMessage and reads its AutoArrays. This is not an editor-only library. Not all listed inbound message types prove client-side pack reachability; auction query has a confirmed outgoing construction at AuctionManagerClient.cpp1304 (advancedSearch), followed by the game message send path. Practical UI search-condition limits still need assessment.

No realistic giant container or full call-site rejection was exercised. Existing per-allocation limits may prevent some vector cases, but a linked list can accumulate many separately allocated nodes, so do not infer a blanket bound. Proposed narrow root: checked header count, same unsigned32 wire type; preserve ordinary-byte oracle and reject before writing the header. AutoByteStream::getItemCount and AutoDeltaVector size-to-index conversions need separate meaning-aware review, not an automatic global cast.

###2. UiMemoryBlockManager cache key: latent allocation bypass

UiMemoryBlockManager.h63 uses hash_multimap<int,void*>. allocMem(size_t) looks up `find(size)` at cpp186; freeMem inserts stored size_t through make_pair at228–230. If a very large size_t aliases a cached small int key, lookup returns the cached small block **before** poolAllocate/global allocation checks. The fresh path also computes alignment additions unchecked. Source supports the arithmetic/ownership risk, not a demonstrated user-controlled request or current gameplay failure.

Actual callers found are scalar operator new from UI_MEMORY_BLOCK_MANAGER_INTERFACE (UIBaseObject and derived UI classes, widget boundaries, packing info). The pool is reachable in normal HUD/UI work, but these ordinary requests are compile-time object sizes; no giant variable-size caller was found in this bounded scan. Therefore do not inflate this into an observed exploit or migration blocker. Proposed candidate: preserve size_t cache identity plus explicit request/alignment/pool-size contract; validate cached-small then rejected-huge request arithmetically or without touching returned storage. Do not merely cast to silence the warning. Debug m_bytesAllocated remains a separate aggregate-stat counter question.

###3. ExceptionAddress logging: definite pointer/varargs mismatch

SetupSharedFoundation.cpp63 MyUnhandledExceptionFilter passes ExceptionAddress (PVOID) to `%08x`. On x64 this cannot faithfully represent the pointer and violates the format contract. This function is installed via SetUnhandledExceptionFilter at SetupSharedFoundation.cpp187 for the client exception path, not an unused tool; manifestation requires an exception. It harms crash evidence, rather than demonstrating ordinary gameplay memory corruption. Narrow repair is `%p` with the proper pointer argument while keeping exception-code formatting. A synthetic high-address formatting fixture can validate without crashing the game. No production edit made.

## Additional prioritized families and deprioritized leads

- **C4103 packing:**62locations are Crypto++ original/STLport header leakage, already isolated by build agent. Highest ABI concern, but don't count each downstream STLport header as its own fix. V2 Debug stopped there; candidate repair is separate from immutable run.
- **MemoryManager455:** pointer difference returns int, but regions/requests retain explicit int-sized allocator limits and calculateAllocationSize now validates. Do not change block layout merely because ptrdiff_t widened. cpp1216 is bytes-per-frame statistics after the allocation-size guard; aggregate overflow needs separate policy. cpp933 strlen is bounded local diagnostic buffer. cpp1874 `_write` length also diagnostic string, not general asset allocator.
- **DPVS memory pool529/581/623:** pointer-sized pool-size arithmetic feeds int aggregate/createPool. Real DPVS path; inspect practical per-pool bounds and total-memory statistics separately. No fresh proof of corrupted pool links from these warning lines.
- **UDP pointer differences:**16C4244 locations measure spans within packet/coalescing buffers, not direct pointer-to-address truncation. Validate their buffer/packet bounds before widening network lengths. TCP IOCP width is already an independent compiler-error repair by build agent.
- **UI counts/string lengths:** many C4267 return/index conversions into int/long UI APIs. Group by container/domain; do not promise arbitrary multi-billion element widgets or silence wholesale.
- **C4291 DPVS placement new:**33locations share missing matching placement-delete warning. Allocation already occurred; caller ownership/constructor-throw cleanup must be traced. Not33leaks or evidence of a new x64 allocator defect.
- **C4067 browser guards:**18locations mostly preserved odd `#if DEBUG=0` directives. Native prior24TU proof and deprecated baseline show browser disabled; do not re-enable to clear a warning.
- **BinkTreeFileIO and capture/provider paths:** compilation alone does not establish runtime DLL availability; existing vendor dossier remains authoritative on pending external providers.

## Suggested bounded order

Finish existing crypto/IOCP roots and actual linker diagnosis. Independently queue the narrow crash-format repair and checked AutoArray/AutoList counts with server counterpart/legacy-byte tests. Keep UI allocation cache identity as a scoped candidate requiring call-site and pool-bound tests. None justifies a mechanical warning sweep or a claim that remaining x64 runtime behavior is safe.
