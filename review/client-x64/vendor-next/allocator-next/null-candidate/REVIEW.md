# Null reallocation candidate: source and compile evidence only

2026-09-30. Isolated client-null-realloc-candidate at d36090a8c. Parent review pending; no commits/push or main/server mutation.

## Exact scope

Three files,8 additions/2 deletions:

- MemoryManager.cpp: tracked metadata reads now use `allocatedBlock ? ... : default`, retaining owner0/leakTestfalse for no prior block. Array default remainsfalse. Nonnull metadata/copy/free logic is untouched. Existing earlier NULL+zero returnsNULL before these lines, unchanged.
- SetupSharedXml.cpp: NULL+positive dispatches `xmlAllocate(byteCount)` (existing new[] hook); NULL+zero and all nonnull requests still go through original reallocate. Matching xmlFree uses delete[]. This separately repairs allocation-domain intent rather than treating the core null guard as sufficient.
- OciSession.cpp: same NULL+positive rule through existing mallocHook(0,newsize), whose first argument is unused and allocation is new char[]. Matching freeHook uses delete[]. NULL+zero unchanged.

No failure-policy change: no catches, fallback CRT allocation, clamping or new return convention. Tracking caller-frame offsets and existing size/ownership metadata policy remain separate. These are legacy null-path defects, not claims that x64 introduced them.

Native compiled-copy SHA-256 (Windows CRLF; these were initially mislabeled candidate hashes):
- MemoryManager.cpp `7c3d134815065224b78c61b73f01339f20cc1749cbc547ac70901d4c26a4ecd0`
- SetupSharedXml.cpp `1937d2690b53a7614244ede81cabac296e4fc6ddc9321902b12a4b861add3973`
- OciSession.cpp `e5ce028b0e3f1494f701759a23720eb0c6c32978c60c83aae780204a460d969e`

## Native compile-only acceptance

`native-v1.zip` downloaded, includes sources/commands/logs/results.16/16 genuine v120 TU compilations exit0; COFF machines verified I386 or AMD64 as appropriate:

| TU variant | Debug Win32 | Release Win32 | Debug x64 | Release x64 |
|---|---|---|---|---|
| MemoryManager normal | compile0 | compile0 | compile0 | compile0 |
| MemoryManager tracked/scalar/guards | compile0 | compile0 | compile0 | compile0 |
| SetupSharedXml | compile0 | compile0 | compile0 | compile0 |
| OciSession | compile0 | compile0 | compile0 | compile0 |

MM and XML use actual existing product .tlog compiler commands (v1 physical source metadata Win32; v2 x64), isolated source/object/PDB outputs, genuine headers. Tracked compile copy changes only DO_TRACK0→5, DO_SCALAR0→1, DO_GUARDS0→1 to expose conditional code; its different source hash is recorded. No tracked flags are added to production.

OCI is outside current SwgClient dependency closure. It uses its genuine Win32 vcxproj definitions/include paths and bundled ora90 OCI headers; x64 diagnostic compilation drops `_USE_32BIT_TIME_T` and selects x64 compiler, not a claim an integrated OCI x64 project exists. No fake Oracle declarations or providers.

**No executable was linked or run, no allocator fault workload executed, no new null runtime probe.** This proves syntax/types/conditional build coverage, not allocation/free lifecycle behavior or runtime repair efficacy. Runtime acceptance stays explicitly unestablished under the current task boundary.

## Server counterpart, inspected without edits

server-client-compat has no corresponding custom MemoryManager.cpp. Its sharedXml SetupSharedXml.cpp uses CRT `realloc(memory,byteCount)` and xmlFree2 naming; its OciSession.cpp no longer contains this client's malloc/realloc/free hook block. Blindly transplanting the client adapter would change a different allocation domain. No server hunk proposed. That existing domain design requires its own audit if requested, not an inferred part of this client repair.

## Identity correction

The native compile script used Path.write_text on Windows, translating LF to CRLF. All three normal compiled sources match the production candidate exactly after CRLF→LF normalization; no include/content adaptation exists. source-transformations.json records both hashes and newline counts. Production hashes: MemoryManager `86675283bf63d052d5012c8f0b9c8a8a06aedaa88e6200c0e4ef45cac8c1827f`; SetupSharedXml `d10c172df4af1dc8b128bdccca12f021a1211d4509188ee11cffdb1f52531d68`; OciSession `15a64c5f40136617fea93b18d8982fddf97a9c5f4f5d0ae3eb81ef73d53db32b`. Prior native evidence is preserved.
