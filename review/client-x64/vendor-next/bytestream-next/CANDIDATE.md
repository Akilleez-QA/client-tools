# Isolated candidate, not integrated

Worktree `/home/akilleez/Work/swg-source/client-bytestream-candidate`, detached base d0fea5bc7. Only ByteStream.cpp/.h changed; no production-main/server edits. candidate.patch and candidate-manifest.json record the review artifact.

Public functions, field types, and class layout unchanged. Existing valid serialization bytes remain unchanged. Read errors use existing ReadException. Append totals exceeding unsigned-int capacity throw length_error before source access/ownership mutation. Allocation failures propagate bad_alloc. No throwing destructor/pool-return claim relies on ignoring pooling failure: pool insertion catches exceptions, releases lock, deletes that optional pooled object.

Read compatibility: reads/advances outside logical size now reject; stale iterator after clear also rejects instead of underflowing. Null iterator get remains an error; null iterator getSize/getBuffer remain0/null; advance(0) remains a no-op. Bound empty/end iterator zero-byte get now consistently succeeds without touching a null buffer (previous behavior depended on allocated Data). This deliberate correction needs parent approval in review.

Ownership: replacement storage is scoped with std::auto_ptr (available in this bundled STLport/v120 era, unlike std::unique_ptr). Allocate and copy before publishing fields; valid self-append source remains alive through copy. Constructor reuses put. Existing spare capacity/pool retained; shared storage detached before modification. Retention-limit setter publishes limit only after required reserve. clear retains its existing basic rather than strong failure semantics.

Review can split into (1) arithmetic and logical-read bounds; (2) storage ownership publication with optional-pool exception cleanup and pointer-width sentinel. The pool cleanup is required for safe dereference/destruction in the latter, not justification for changing broader pool architecture. Nested AutoDelta state transactions are untouched and remain open.

Acceptance so far: actual candidate client ByteStream with real server pthread mutex passes85 small initialized-storage checks on host -m32/-m64 (candidate only, no dangerous stock reproduction). This includes self-append, copy-on-write, reserve, read-to-end, stale iterator,16 ordinary small pool/detach cycles. Initial attempt using nonexistent client Linux mutex failed before compilation, preserved. Final-source portable PE wire fixtures passed50/57 (candidate-final-wire32/64.log). Actual native v120 ByteStream and real Windows ArchiveMutex compiled in all four configurations with bundled STLport; initial standalone link blocked on genuine custom MemoryManagerNotALeak allocation dependency. Runtime native integration is pending the verified allocator/core link set, not counted as a pass. No allocation-failure injection or huge allocations. Arithmetic-only guard81pairs separately checked.

Remaining evidence: native v120 actual archive TU with bundled STLport on both ABIs; final-head existing wire fixtures; same narrow server mirror and Linux fixture run; reviewer assessment of documented zero-length policy and caller assumptions. Full message/object rollback, thread-safety of shared streams, pool-allocation fault execution and live networking are not claimed.

Raw-buffer decoder limit: Archive::get(ByteStream&) copies a declared size directly from getBuffer before advance; this candidate does not preflight those callers. ReadIterator bounds do not establish all archive decoding safety. Keep separate review.

## Native final validation

Exact candidate ByteStream and Windows ArchiveMutex compiled and linked with native VS2013 v120 and bundled STLport in Debug/Release × Win32/x64. All four executables pass85 bounded checks, exit0, PE architecture correct, linker map binds ByteStream::put to candidate0.obj. Final portable wire reruns pass50/57.

Initial v1 compile succeeded all4 but standalone link lacked SWG custom MemoryManagerNotALeak operator new. v2 binds the same genuine minimum-block MemoryManager object, DebugHelp/InstallTimer objects and full core/STLport link set as independent LCD-v4 tests. This is a recorded mixed dependency snapshot, not a full-product build or allocator leak-free guarantee. Hashes per object/library are in native-v2.zip verified-results.json; original dependencies remain untouched.

Initial v2 verifier required stdout exactly one line and rejected Debug memory-manager shutdown summary even though checks/exit passed. Separate verify-native-v2.py reruns the same binaries, requires exactly one85-check success line and0 exit plus correct map binding; allows only the known numeric MM::remove diagnostic in Debug. Original results/logs preserved. This oracle adjustment does not hide assertion failures/crashes.

No native fault injection, oversized buffers, or deliberately failing old-memory paths were executed. Exception guarantees are source-reviewed, not allocation-failure runtime tested. Parent/independent critic review remains before any integration; shared-server mirror has not been made.
