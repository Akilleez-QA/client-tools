# Allocator statistics/null package: bounded independent review

Reviewed `1f8f341aab958ac13f04b070bb6575be0af36091..0c09740e0ca44fbf1428eeba779ac06824e69075` in client-pr-next-pcre-count. No blocking finding in this pass. This is independent of preparation of these three commits, but not blind: I prepared the preceding size package and share the historical allocator/context evidence with the parent task.

Identity: all added/removed lines match original cf82805a9, 45fae5093 and fcf54ab3f exactly; Myers counts are 15 source files, +85/−65. No implementation changes, tests, builds or runtime were performed during review.

Checked getter declarations/definitions and the repository's 36 references to current/maximum byte getters. Win64 ByteCount is uint64_t; Win32 retains unsigned long. Snapshots and accumulators use the widened type; signed delta consumers cast operands before subtraction and match PRId64. Unsigned diagnostics cast to uint64_t with PRIu64; free-pattern addresses use void* with %p. Skeletal allocation tallies explicitly clamp decreases before unsigned accumulation. No omitted incompatible getter consumer was found in the inspected tree.

The retained int MiB display/GC values are bounded by the allocator's signed-int aggregate-MiB accounting in the prerequisite; this is not a general uint64-to-int conversion guarantee. The GC threshold multiplies after widening. Live-byte signed delta conversions remain within the allocator's representable region-total bound; lifetime cumulative totals and allocation-count exhaustion are not newly proved safe.

Null handling: MemoryManager's null-zero return precedes metadata lookup; null-positive now defaults owner=0/leakTest=false and leaves its prior untracked scalar policy intact. Nonnull metadata/copy/free paths are unchanged. XML and OCI null-positive hooks call their existing new[] allocation functions, matching their delete[] frees; they do not silently allocate in the CRT or reinterpret array ownership. No exception/failure policy is replaced.

Evidence/body review: the draft correctly distinguishes seeded-counter small-allocation diagnostics from resident multi-GiB heaps, 32 consumer compilations from Viewer/Maya source review, and 16 null-path TU compilations from runtime acceptance. The published null record confirms diagnostic tracking/scalar/guard variants and OCI-specific configuration limits. The draft does not claim an exact-base rebuild, live GC or null lifecycle success. The prohibited allocator/Audio fault workload was not run.

Residual scope: existing concurrency, counter lifetime limits, OCI runtime availability and complete allocation lifecycle remain outside this review. No additional verification campaign is requested by this finding-free pass.
