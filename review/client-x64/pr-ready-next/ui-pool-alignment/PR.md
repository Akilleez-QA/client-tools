# Preserve natural alignment in the UI pool stride

The UI pool rounds each block using a four-byte alignment. On x64, a size_t header followed by an ordinary eight-byte-aligned UI object can consequently place alternating blocks at misaligned addresses. Use sizeof(size_t) in the existing stride formula: Win32 retains four-byte alignment; x64 gets eight-byte alignment. Allocation policy and header size are unchanged.

This master-based package changes one production line (+1/-1), with no build, test-tool, or dependency changes. The resulting manager source is byte-identical to the previously reviewed candidate at `2a06b9dcb08d0ba0c090536f34e27cfcaeaa12f5`.

[Recorded native evidence](https://github.com/Akilleez-QA/client-tools/blob/3d2107ff7ede73ee7afa7643cd24f56947c1c1a2/review/client-x64/vendor-next/ui-alignment-next/CANDIDATE.md) reports 3,129 checks per v120 Win32/x64 Debug/Release configuration, using the actual UI allocator and UIButton/UIPage/UIText layouts. The exact repository fixture/runner results are in the [native text packet](https://github.com/Akilleez-QA/client-tools/blob/3d2107ff7ede73ee7afa7643cd24f56947c1c1a2/review/client-x64/vendor-next/ui-alignment-next/native-repository-v4-text.zip).

Those runs use an explicitly recorded integrated MemoryManager/core/STLport dependency closure, not a fresh build of this master-based branch. The snapshot-dependent harness is not imported here. No new tests or native builds were run during packaging. The evidence covers the measured natural eight-byte alignment requirement, not arbitrary 16-byte-aligned subclasses, allocation overflow, large free-list keys, or complete UI lifecycle behavior.
