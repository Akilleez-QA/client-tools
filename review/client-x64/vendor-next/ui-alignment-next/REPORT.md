# UI pool alignment read-only spike

Native v120 compile-only fixture reads class sizeof/__alignof constants from its COFF .layout section. No executable linked/run; no UI objects constructed or potentially misaligned storage accessed. Actual ui project metadata, bundled STLport, real headers. C:/ui-alignment-readonly-v3; native-layout.zip. PE machine332=Win32,34404=x64. V1 quoting issue and v2 v120 rejection of __alignof abstract types retained; final abstract alignment slots0 mean unmeasured, not actual zero alignment.

| Class | Win32 Debug size/alignment | Win32 Release | x64 Debug | x64 Release |
|---|---:|---:|---:|---:|
| UIButton |348/4|344/4|504/8|496/8|
| UIPage |300/4|296/4|456/8|448/8|
| UIText |424/4|420/4|616/8|608/8|

UIBaseObject exposes inherited class operator new through UI_MEMORY_BLOCK_MANAGER_INTERFACE. Its static manager is declared with8MiB pool granularity. Derived ordinary UI classes use it. Four other concrete pool-manager implementations occur for rectangle styles, packing location/size information, and widget boundaries; no __declspec(align), alignas or __m128 found in this UI source scan, which is not a proof about all future/externally derived classes.

## Root cause

Default PASS_THROUGH_TO_GLOBAL_MEMORY_MANAGER=0, no project override found. Each fresh pool allocation uses floor((size+sizeof(size_t)+4)/4)*4; user pointer is raw+sizeof(size_t). On x64 each measured size multiple8 yields size+12. Consecutive blocks alternate raw offsets0,4 modulo8. Second header itself is a misaligned size_t; second user pointer likewise4mod8. E.g Release UIButton496 =>stride508, user offsets8,516,1024; second516%8=4. This is ordinary HUD-size behavior, independent of the separate huge-size int-key narrowing.

Win32 measured classes require4alignment; oldstride size+8 and header4 satisfy it. Passing through to malloc would give each raw allocation a correctly aligned base, and raw+8 is8aligned onx64, so it avoids this particular alternating-stride issue. It still does not guarantee16alignment and changes allocation policy/performance; do not use pass-through as a silent fix.

Microsoft's VS2013 malloc reference confirms base alignment8 onWin32/16 onx64: https://learn.microsoft.com/en-us/previous-versions/visualstudio/visual-studio-2013/6ewkz86d(v=vs.120) (searched2026-09-30). Offset/stride destroys a stronger base guarantee.

## Narrow candidate options, not implemented

A. Set pool alignment to sizeof(size_t): remains4Win32, becomes8x64. Existing formula then yields size+16 for measured x64 classes, preserving every8aligned header/user offset. Minimal fix for current observed8alignment contract; explicitly not support for over-aligned classes. Keep header size unchanged. Test all sizes1..boundedlimit with address arithmetic and measuredclass layouts; Win32 formula identical.

B. If a generic16aligned x64 allocator contract is required, both header span and stride need16 rounding. Changing only s_alignment to16 leaves user=raw+8 and still violates16. This is a wider storage/free-header design change, with a separate reason required; current classes do not establish necessity.

Neither option fixes integer overflow in requested-size additions, int size-bin narrowing, allocation failure handling, pool granularity recursion, or Debug byte counters. Keep those findings separate and avoid claiming complete allocator safety. Parent review before production changes.
