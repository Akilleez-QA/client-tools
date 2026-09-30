# UI pool natural-alignment candidate

2026-09-30. Detached throwaway `client-ui-alignment-candidate` at `91dc05e8b`.

Production change: only `s_alignment = 4` to `s_alignment = sizeof(size_t)` in UiMemoryBlockManager.cpp. SHA-256 of candidate source: `356655d354091bb3d4851e40c9b30811d3676eab2c1b1ad9190b36ba119b28fa`.

Native original evidence: `native-candidate-v2.zip` (SHA-256 `76f0c04f2a35ae8b576940d78859cf2e72e936ad439760a007def875d4ac8b02`). ZIP integrity checked. Actual candidate TU passes 3,129 checks on each of Debug-Win32, Debug-x64, Release-Win32 and Release-x64, v120 and bundled STLport. Fresh manager allocation bound in each link map. Supporting TUs UiReport and UILowerString are real production code; genuine minimum-block MemoryManager/core objects and libraries are explicitly hashed. This dependency set combines known snapshots and is not a full-client final-head test.

The first attempt failed to link because the actual UI headers require UILowerString's real cache initializer; the final test compiles that TU rather than replacing it. Original exact-stdout gating rejected Debug's existing numeric MemoryManager shutdown summary. Final gating allows only that specific numeric line, exact PASS count, zero exit and actual map binding. Failures remain in the private VM directories.

The fixture has 3,072 pure small-size arithmetic checks and 57 actual allocator checks using native UIButton/UIPage/UIText sizes/alignment. Four raw allocations, measured stride, frees and reuse per type. No UI object is constructed, payload accessed or old malformed allocation executed. Header alignment follows from user address minus sizeof(size_t). Not a broad allocator canary/overflow or lifecycle test.

One line preserves the entire Win32 stride formula. On x64 it restores eight-byte headers/objects for the measured types. It does not provide a generic sixteen-byte allocation contract. Independent critic accepts that boundary and found no demonstrated sixteen-byte UI consumer; future/unchecked derived classes are not proven by this sample. int map key, arithmetic overflow, allocation failure and debug-counter width stay separate.

Repository test is under tools/test-ui-memory. Runner takes real evaluated definitions/include dirs and explicit library/object inputs, hashes them, compiles actual TUs and checks architecture/map/output. Build dependencies are prerequisites, not auto-generated; this limitation is documented. Repository runner validation is recorded separately in native-repository-v3.zip: exact repository runner passes all four configurations. Packaging attempts v1/v2 failed before compilation (copied-script default path and unresolved project-relative include inputs); both were corrected without changing the fixture or production code.

Final fixture adds `_MSC_VER == 1800` compile guard. Exact guarded fixture and unchanged repository runner pass all four again; complete downloaded/integrity-checked evidence is `native-repository-v4.zip`.
