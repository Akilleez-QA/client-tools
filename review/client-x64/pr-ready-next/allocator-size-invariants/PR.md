# Check allocator sizes and preserve the minimum free-block representation

The allocator accepts `size_t` requests but stores block and region sizes as signed `int`. Validate requests before narrowing, rounding, updating statistics or taking the allocation lock; use the existing fatal-error policy for unrepresentable requests. Large preallocations become multiple bounded regions instead of one truncated region. The size cap also respects the requested-size tracking field when enabled.

On x64, a small allocated block or split remainder could be smaller than the free-list node it must hold after release. Require both to fit `cms_freeBlockSize`, retaining the existing subdivision condition. The prior untracked x64 layout could produce 48-byte blocks for a 64-byte aligned free node.

Two source-only commits change `MemoryManager.cpp` (+70/−29 in GitHub’s diff), stacked on `review-ready/client-allocator-address-stack` at `fc667f38eafbd4a2b4d50f96a31efb5cca3ef55c`. The prerequisite is not part of this review delta.

Existing native v120 evidence:

- [Checked-size results and limits](https://github.com/Akilleez-QA/client-tools/blob/2a1ff9279341516cce2746889b29cbc6a0e8a788/review/client-x64/allocator-skeletal-next/RESULTS.md): Debug/Release × Win32/x64, 21/21 boundary checks in tracked and untracked layouts, 2568/2568 tracked regression checks, and 12/12 reduced-region preallocation checks per configuration.
- [Minimum-block results](https://github.com/Akilleez-QA/client-tools/blob/f2b8cbc8e93d5937edd743dbf76437e424f3ff7a/review/client-x64/vendor-next/allocator-next/minimum-block/RESULTS.md): 1622/1622 checks per configuration using the untracked product layout, including block sizes, payload preservation and allocation/free/reallocation cycles.

These results used recorded integrated source/dependencies, not this newly stacked branch. The original source changes are reproduced exactly; no builds or runtime tests were repeated during packaging. The first tracked boundary snapshot preceded the final alignment assertion and whitespace cleanup. Region tests lowered the region maximum to exercise real small allocations; they do not prove multi-gigabyte reservations succeed. The minimum-block matrix does not establish tracked-layout or whole-client heap safety.

Aggregate byte statistics, full-width free-pattern diagnostics and tracked null-reallocation metadata are separate follow-ups. This package does not claim those issues are fixed or provide a complete x64 allocator build.
