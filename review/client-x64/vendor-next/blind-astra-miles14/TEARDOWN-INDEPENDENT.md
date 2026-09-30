# Independent teardown ownership assessment

2026-09-30. **Nonblind follow-up**, separate from the frozen opening and callback/FPU addendum. One bounded source/artifact pass. No fixture, allocator workload, game or vendor binary was executed; no fault was reproduced; no product source was changed. `objdump` only decoded existing executable bytes. I did not read `TEARDOWN-SOURCE-REVIEW.md`, its proposed patch, or synthesized results. No descendant agents.

**Conclusion:** The supplied evidence locates the failure in the engine allocator's previous-block coalescing check, but does not identify the allocation or ExitChain owner being freed. I found no specific source defect that can honestly be named as this fault's cause. Several tempting explanations are contradicted or materially weakened by the actual source and linked image. The smallest missing discriminator is the original fault context plus the active ExitChain entry; if those establish a callback-owned pointer, its allocation/free history is then needed. Broad allocator experiments, changing ownership families, disabling cleanup, or adding a missing thread-removal call will not answer that question.

## Exact evidence identities

Source **S**: `/home/akilleez/Work/swg-source/client-build-next`, HEAD `49d0eeed4ddaa177d7a93ea396c37c3d9b9942da`.

Evidence **F**: `/home/akilleez/Work/client-wire-validation/vendor-options/miles-engine-fixture`.

| Artifact | SHA-256 |
|---|---|
| `F/probe.exe` | `1d8fc2c767bd67cb82fb9fa4393d7ebba1c9f39557ac15c67636159e96ea8298` |
| `F/probe.map` | `d9d5a4b1be7596bec2f9471f13e8427126db7b940c5e76dc150b9a472ac87b1b` |
| `F/probe.cpp` | `390c2ac04ec54c77964db5c41df2b382a69815a5a03463acad4a5fe31fffb2c2` |
| `F/run-v3/engine-baseline-1.log` | `58d96b839dd2b34efb3d21ce4f8ab5c8de0b52fba995f798e8d545d2c8a0f9c8` |
| `F/native-evidence.zip` | `00add3edf6cbe7410b4ea34d6ccd517364c1737051ede893cc35f16c4fc3388a` |

The v3 deployed `private-prefix-engine-v3/drive_c/engine-private/probe.exe` is byte-identical to `F/probe.exe`. Archived probe source/map match the loose copies. Archived `real-input-hashes.json` source hashes for Audio, Sound2d, SetupClientAudio and Sound2dTemplate match S. It also records hashes for the Release libraries, including sharedMemoryManager `4f1fd9649d8ecb521d90cc98b9ffc0b0cf30396d18f64e836b2e3d1956019035`, sharedFoundation `a8a77bc2f9a0c1d30d9daf7b96db25edaca474d684eafe47d061d8bb27852345` and sharedUtility `cb4e1fb728c6622eab766ab30bc06de21bcd7fbfc05141f0292e77f985500d2c`. Those identify inputs; I did not rebuild the archives to certify every translation unit.

The executable is a native Win32/v120 PE, but **v3 execution was under Wine** (`run-v3/commands.json:48–50`). The text label `NATIVE_EXCEPTION` must not be read as evidence of a native-Windows runtime reproduction.

## What failed, precisely

`run-v3/engine-baseline-1.log:114–119` shows expected playback completion, `stage remove`, then access violation at image address `00421494`, base `00400000`, and only `FRAME 004050A4`. `probe.map:1368` maps `MemoryManager::free` to `00421460`; the next symbol starts at `004214f0`.

Static disassembly of these exact executable bytes gives:

```
0042146d mov esi,[esp+0xc]       ; userPointer
00421471 add esi,0xfffffff0     ; allocation header = userPointer - 16
0042147c or byte ptr [esi+8],1  ; mark this block free
00421492 mov eax,[esi]          ; previous block pointer
00421494 test byte ptr [eax+8],1; FAULT: previous block's free bit
```

This matches `S/src/engine/shared/library/sharedMemoryManager/src/shared/MemoryManager.cpp:1477,1548,1578–1586`, specifically `block->getPrevious()->isFree()`. It establishes an invalid previous-block dereference at the point of failure. It does **not** distinguish a foreign pointer, interior pointer, repeat free, overwritten block header, or earlier allocator/link corruption.

The lone reported frame is inside the fixture's own exception handler (`probe.map:6190` starts `traceException` at `00405050`). `probe.cpp:20` calls `CaptureStackBackTrace` from the handler and logs neither `ContextRecord` registers nor exception access details. Consequently the frame is not evidence naming the original deleting callback. `writeMiniDumps=false` at `probe.cpp:25`; I found no existing `.dmp`, `.mdmp` or core in this fixture tree.

## Ownership hypotheses checked

**1. Global new/delete provider mismatch is not demonstrated.** `probe.map:1353–1357` resolves scalar new, scalar delete, array new and array delete to `sharedMemoryManager:OsNewDel.obj` at `00420e30`, `00420e70`, `00420e90`, `00420eb0`. The matching source is `S/.../sharedMemoryManager/src/win32/OsNewDel.cpp:89–136,199–210`. `_malloc` and `_free` resolve independently to LIBCMT (`probe.map:2014–2015`). This is a legitimate two-family arrangement when callers match ownership. A broad claim that “the fixture linked CRT new with engine delete” conflicts with these provider records. A particular foreign pointer passed to engine delete is still possible, but requires that pointer's history.

**2. DataTable's mixed allocation families are paired in the inspected code.** Under `S/src/engine/shared/library/sharedUtility/src/shared/`, `DataTable.cpp:543,591` allocates the cell slab with malloc; `92–105` explicitly destructs cells then frees the slab. Placement construction is supported by `DataTableCell.h:24`. Cell strings use `new char[]` and `delete[]` (`DataTableCell.cpp:74–104`). Other DataTable members use new/delete (`DataTable.cpp:31,108–115`). Thus the existence of malloc in DataTable does not establish the observed engine-free mismatch.

Audio owns its music table directly (`S/src/engine/client/library/clientAudio/src/win32/Audio.cpp:1345–1349,1445–1448`), rather than acquiring that pointer from DataTableManager. DataTableManager closes a table by erasing its map entry then deleting it (`DataTableManager.cpp:93–112`), and removes remaining tables before destroying DataTableCell's pool (`44–62`). I found no automatic double ownership of Audio's music table in these paths. Corrupted data or a different call path remains possible, but the v3 log does not identify any table as the failing allocation.

**3. File caching is not an accidental fixture-only switch.** The fixture uses setupToolData then sets `m_allowFileCaching=true` (`probe.cpp:29`). Product `ClientMain.cpp:244–247` uses setupGameData then also sets it true. Both setup helpers initially set false (`SetupSharedUtility.cpp:76–85`). CachedFileManager registers its cleanup when caching is enabled and owns its filename array with delete[] (`CachedFileManager.cpp:135–170`). There is no basis here to remove caching as a teardown fix. The fixture additionally supplies required support assets; their existence is not proof that their allocations own this fault.

**4. Bootstrap differences exist, but do not explain this instruction yet.** Product and fixture install thread/debug before foundation, then file/math/utility/random before audio. Product uses D_game and full game subsystems; fixture uses D_console and a small audio loop. Product sets an allocator limit in WinMain (`S/src/game/client/application/SwgClient/src/win32/WinMain.cpp:118–121`), whereas the fixture does not. But MemoryManager lazily initializes on the first allocation (`MemoryManager.cpp:1196–1199,605–639`), so missing an explicit allocator construction is not itself an initialization defect.

Product calls `SetupSharedThread::remove()` after foundation removal (`ClientMain.cpp:384–385`); fixture omits it. That is a concrete fixture cleanup omission, but this fault occurs **inside** the preceding foundation removal. Adding the later call cannot repair the earlier invalid header dereference. Scoping fixture-owned objects before engine teardown is also sensible hygiene, not a demonstrated fix for the observed address.

**5. Release configuration is consistent where evidence exists; comprehensive ABI identity is not established.** Archived `compile-command.json` uses `/MT`, `/O2`, `/Gy`, `/Zc:wchar_t-`, `WIN32`, `NDEBUG`, `DEBUG_LEVEL=0`, `_USE_32BIT_TIME_T=1`; `build.py:9–15` derives includes and definitions from the actual Release Audio command. `FirstClientAudio.h` includes the shared foundation and memory headers; `Production.h:12–16` maps DEBUG_LEVEL=0 to PRODUCTION=1. The linked ExitChain allocates a 20-byte Entry, consistent with its Release layout (disassembly `0041a043`; `ExitChain.h:34–43`). Its allocator free lacks the Debug-only consistency checks (`MemoryManager.cpp:1479–1483`), matching the actual short free body. A debug-named library in a broad dependency list does not prove that its members were extracted or controlled allocation. No relevant mixed-Debug/Release ABI defect was established in this pass.

## Why ExitChain ownership cannot be recovered from this log

`SetupSharedFoundation.cpp:294–296` invokes `ExitChain::quit`. `ExitChain.cpp:194–211` removes an entry from the list, calls `entry->function()`, and **then separately deletes the Entry itself**. Therefore even “fault during ExitChain” has two fundamentally different allocation owners.

The exact linked dispatcher calls the callback at `0041a12c` and frees the entry through scalar delete at `0041a138` (return `0041a13d`). All equal-priority callbacks execute in reverse registration order (`ExitChain.cpp:118–126`); `SetupClientAudio::remove` is registered after installing Audio (`SetupClientAudio.cpp:28–40`). Its body first removes SoundTemplateList, then Audio, then SoundId (`44–48`), each with multiple deletes. No before/after callback log exists in v3, and Release disassembly contains no such logging. Static order identifies candidates but cannot tell how many entries completed before the fault. Enabling a Release config debug flag alone will not restore compiled-out entry logging.

## Minimal diagnostic observation plan — not executed or authorized by this memo

1. **First seek an already-captured original exception context or debugger dump outside this packet.** Required fields: exception access address/type, EIP/ESP/EBP/EAX/ESI/EDI, bounded stack bytes and readable bytes around the user pointer/header. The existing handler output cannot reconstruct them retrospectively.
2. **For this exact image, the missing context would immediately classify the free path.** At `00421494`, `[ESP+0xc]` is userPointer, ESI is userPointer−16, EAX is the alleged previous block, and `[ESP+8]` is the immediate return address. Return `00420e80` means scalar delete; `00420ec0` means array delete. In those wrappers, `[ESP+0x14]` at the fault is delete's caller return. If it equals `0041a13d`, this is deletion of the ExitChain Entry itself. Read the still-readable Entry's function/name fields at userPointer+4/+8 and map the function. These offsets apply only to this hashed binary and fault instruction, not a rebuilt variant.
3. **If the free originates inside a callback**, identify the active ExitChain Entry/function and deleting caller, then the object/member being released. A minimal future diagnostic capture would retain a fixed-size, preallocated entry record at callback entry/return and before Entry deletion, together with the fault context. Do not allocate or use complex logging inside allocator hooks. This observation proposal does not authorize rerunning the previously rejected workload; a separately approved diagnostic opportunity is required.
4. **Only then identify allocation family/history.** An engine-looking header cannot prove origin. Track the identified pointer's allocation, returns and prior frees through its concrete source path. For a DataTable, distinguish the slab (CRT), cell string (engine array), member container/table (engine scalar), and any pool object. For an Entry, `ExitChain::add` calls the same engine scalar new (`0041a045 -> 00420e30`) and records function/name; a foreign-provider theory would then need contrary pointer evidence. Release `DO_TRACK=0` (`MemoryManager.cpp:51`) means no allocation-owner stack can be assumed recoverable from this header.

This plan separates callback-owned free, Entry free, and allocation family before proposing a repair. Until those discriminators exist, modifying DataTable ownership, allocator coalescing or cleanup ordering would be speculative. The missing post-foundation thread removal can be recorded as a fixture completeness issue, but must not be presented as fixing this fault.
