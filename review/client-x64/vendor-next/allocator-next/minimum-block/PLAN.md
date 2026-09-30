# Minimum block invariant

Prediction, before native candidate execution: every non-sentinel allocated or free block must be large enough to contain the real FreeBlock type. The current source computes a 48-byte small allocation and permits a 48-byte split remainder on product x64, whereas the rounded free-node footprint is 64 bytes. This is a source/layout finding, not a reproduced crash. The separate CLI fault-reproduction request was rejected by its safety filter and will not be retried.

Candidate floors allocated sizes at cms_freeBlockSize and adds that same floor to the split condition while retaining the old condition. Win32 size/split decisions should be unchanged. Validate compiler-reported sizes, bounded size arithmetic, then candidate-only allocate/free/reallocate and block-chain invariants using actual MemoryManager plus the existing native core libraries. The test will not execute the old invalid allocation sequence. Keep untracked production definitions; tracked coverage is separate.

Oracle: native structure sizes, documented allocator invariants and preserved payload bytes. Bounds, exact check counts, source hashes and exit codes are recorded. Debug/Release on both architectures use VS2013. Successful candidate tests do not establish a whole-client heap proof or characterize the unrelated Audio startup failure until that fixture is relinked consistently.
