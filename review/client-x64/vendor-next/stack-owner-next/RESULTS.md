# Ordinary DebugHelp frame-order observations

Actual DebugHelp.cpp SHA256 `6b1b596c275b243dc9a8be788cf87b613c937f42b1ca41db5f5689e4a64094de`, identical to current client source, compiled and linked on native v120 with genuine existing headers/core libraries. Four build/run pairs exit0. Debug `/Od /MTd`, Release `/O2 /MT`; symbols enabled. Private C:/stack-owner-{Debug,Release}-v1; no product source or R/Q mapping edits. Main executes only two normal named chains and stack captures. Real core bootstrap executes ordinary initialization; no explicit MemoryManager allocation/owner/null/free/fault workload is tested.

Return addresses are captured directly using `_ReturnAddress` in leaf, middle and outer. Retained middle/outer have post-call volatile side effects; all three marked noinline. Tail-eligible middle has no operation after the call. The driver records raw stack addresses, return addresses and equality indices; it is an observation probe, not an allocator correctness assertion.

| Configuration | Retained leaf/middle/outer return slots | Tail-eligible slots |
|---|---|---|
| Win32 Debug |2/3/4|2/3/4|
| x64 Debug |2/3/4|2/3/4|
| Win32 Release |2/3/not found|2/3/not found|
| x64 Release |2/3/4|2/2/3|

In x64 Release the tail-eligible leaf/middle captured return addresses are equal: that middle frame was eliminated. Win32 Release fails to recover the outer return address despite the retained noinline calls, illustrating an optimized x86 walk limitation; raw evidence is retained, not repaired with different flags. These observations refute an unconditional claim that the x64 walker always inserts one extra frame relative to Win32 at capture entry. They do not establish stable fixed indices under arbitrary optimized call chains.

## Owner source interpretation, not exercised

Current Windows default DO_TRACK is0. Optional allocation tracking records explicit supplied owner at slot0 and, for DO_TRACK>1, captures stack addresses using OFFSET3 and stores owners[i+3] for i=1 onward. Explicit setOwner uses OFFSET2 and stores owners[i+2] for i=0 onward. reallocate preserves prior owner0 (or0) as the owner argument to allocate; its deeper recorded frames are newly captured, not a copy of the original allocation chain. These paths have different call shapes, so ordinary probe indices alone cannot prove their intended logical owners match or justify changing offsets.

No source repair proposed from this evidence. An owner contract must name intended frames and account for optimized/inlined/tail-eliminated callers; do not treat DO_TRACK>1 metadata as validated by this test. All raw addresses, build commands, maps, code/binary/provider hashes are in stack-owner-evidence.zip (text-only archive).
