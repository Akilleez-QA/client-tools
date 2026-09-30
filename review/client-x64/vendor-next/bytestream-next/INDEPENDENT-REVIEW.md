# Independent bounded ByteStream review

Reviewed candidate worktree versus d0fea5bc7 on 2026-09-30. Read-only production review. No blocking defect found in the changed paths; this is not native runtime acceptance.

## Arithmetic and ownership

`put` checks incoming > UINT_MAX−size before source access or ownership changes. Small growth slack doubles only capacities below4096, so that multiplication cannot overflow; the following addition falls back to exact required capacity if slack cannot fit. Read checks subtract only after position<=logical size, including LP64 unsigned-long read requests.

Replacement Data is scoped until allocation and both copies finish. Old Data stays alive through copying an aliased source. Valid source subranges of initialized old bytes cannot overlap the append destination when storage is reused; changing memcpy to memmove is unnecessary for that contract. Arbitrary source ranges extending into spare capacity or outside a valid object remain caller errors. Shared reserve detaches before modification, preserving other streams. The only reAllocate callers retain newSize>=current logical size; no shrinking-copy overflow found.

Failure before publication leaves put/reserve fields and old reference intact. Temporary pooled storage may be deleted rather than returned on allocation failure, which is acceptable because pooling is optional. The destructor pool insertion catch releases the mutex and deletes the rejected entry. No new throwing operation was found between acquiring that lock and entering push_back's catch. Existing refcounts are non-atomic and function-local pool initialization is not a new cross-thread guarantee; do not claim shared-stream thread safety.

## Deliberate semantics and limits

- Empty bound iterator zero-byte get now succeeds consistently; null unbound get still throws, null advance(0) is preserved. This is an explicit policy change, not byte-format change.
- Stale positions beyond current logical size reject. This **does not detect iterator invalidation generally**: clear at position0, or clear followed by refill beyond the old position, remains readable. No generation field exists. Narrow the phrase “stale iterator after clear rejects.”
- `clear` retains basic failure semantics as documented; it is not transactional rollback.
- Existing Archive.h string and nested ByteStream decoders, and UnicodeArchive.cpp, consume raw pointers before calling advance. New advance checks do not prevent their earlier out-of-bounds read on malformed input. These are separate pre-existing caller checks, not a reason to broaden this patch or claim packet validation complete.
- Nested object/delta transaction safety remains outside this patch. No native allocation-failure injection or pool-allocation-failure runtime test was performed.

## Added small independent execution

`independent-small-probe.cpp` compiles the actual candidate ByteStream.cpp and genuine server pthread ArchiveMutex.cpp, no replacement allocator/mutex, with host g++ -m32/-m64. Both execute **18 checks, zero failures**. All buffers are initialized and small; no dangerous stock run, huge allocation or simulated corruption.

Checks: partial self-append while spare capacity exists; shared-storage source alias while detaching; content preservation on shared reserve; ULONG_MAX read rejected before writing target or advancing iterator; exact read-to-end; reader of a different shared stream remains valid when another clears; shared clear-and-reuse preserves the original stream. Logs `independent-small-{32,64}.{build,run}.log`.

These supplement the author's checks, not duplicate native MSVC evidence. Exact final candidate still needs bundled-STLport/v120 native runs and matching server mirror verification before integration claims. Source review supports the exception guarantee but does not substitute for exercising failure points.
