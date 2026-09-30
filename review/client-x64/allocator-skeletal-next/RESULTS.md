# Checked allocator sizing and x64 hard skeletal kernels

Published production commits on `integration/client-x64-next`:

- `03fafe0cc`: checked allocator sizes and bounded preallocation regions.
- `3c172d1b1`: x64 hard skeletal SSE kernels, original Win32 assembly retained.

| Native VS2013 check | Result |
| --- | --- |
| Allocator boundary, tracking enabled | 21/21 per Debug/Release × Win32/x64 |
| Allocator boundary, product untracked layout | 21/21 per configuration |
| Actual allocator regression, tracking enabled | 2568/2568 per configuration |
| Diagnostic 1 MiB region limit, actual 3 MiB preallocation | 12/12 per configuration |
| Skeletal whole source compilation | Both ABIs, Debug and Release pass |
| Exact skeletal kernel comparison | 2688 records per build; zero sampled output/bounds differences |

Skeletal comparison uses original Win32 assembly as oracle, Debug/Release stock and candidate Win32 plus candidate x64. It checks output sentinels, input preservation, iterator movement and complete MXCSR restoration. Source slices come from the actual hashed translation unit and use its real layouts; they are not a complete renderer. The standalone whole-TU link failures are preserved.

Allocator invalid requests use actual FatalException support, verify the expected diagnostic and no new region, and preserve the old realloc payload. Boundary arithmetic is exercised without reserving gigabytes. The region test lowers its diagnostic maximum to exercise the real OS loop with small allocations; it does not prove giant reservations succeed. The first tracked boundary run preceded only the final alignment assertion and whitespace cleanup; untracked, stress and region runs use the final source.

## Evidence

- [Allocator sizing audit and limits](allocator-size-audit.md)
- [Skeletal tests and limits](skeletal-native-results.md)
- [Native logs, test sources, manifests and comparison records](native-and-reproduction.zip)
- [Separate statistics and null-realloc findings](statistics-and-null-audit.md)

The ZIP excludes executable/library/PDB files and environment dumps. Runners retain original experiment paths for provenance; rerunning requires the genuine v120/SDK/dependency setup described in the preceding [allocator/math packet](../allocator-math-next/RESULTS.md). This is an evidence packet, not yet a standalone CI runner for all these native tests.

Aggregate allocator statistics above 4 GiB and tracked `reallocate(NULL)` remain open. No full x64 client link, GPU rendering, representative scene, or live mixed-width acceptance is claimed.
