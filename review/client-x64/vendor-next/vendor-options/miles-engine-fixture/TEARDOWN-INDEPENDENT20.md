# Independent teardown diagnosis: exact missing observation

2026-09-30. Source HEAD `49d0eeed4ddaa177d7a93ea396c37c3d9b9942da`;
retained `probe.exe`, `probe.map`, `probe.cpp`, native build-command archive,
`run-v3/engine-baseline-1.log`, RESULTS and TEARDOWN-SOURCE-REVIEW reviewed.
No fixture execution, allocator/media workload, product edit, or push.

**No root-cause repair is demonstrated by this retained evidence.** There is,
however, a specific diagnostic defect: the VEH captures its own current stack,
not the interrupted context. The only retained frame is conclusively the return
from that capture call. Repeating callback-name logging alone would still not
identify the failing allocation. The missing observation is the original x86
CONTEXT plus the first six stack words and the block header at the fault.

## What the executable actually proves

All addresses below are preferred-image VAs for this exact retained executable;
the log confirms actual image base `00400000`. They are not inferred addresses
from a different build.

* `00405050` is `traceException`. At `0040509e` it calls the imported
  CaptureStackBackTrace. The saved `FRAME 004050A4` is its return instruction,
  inside the VEH. It is **not** a MemoryManager caller, corrupted return address,
  or a shutdown callback. No crashing-thread registers, stack bytes, or accessed
  address were printed. `writeMiniDumps=false`; the run-v3 evidence inventory
  contains no dump.
* `MemoryManager::free` begins at `00421460`, pushes ESI and EDI, calls the mutex,
  then loads its userPointer and subtracts 16 into ESI. At `00421492`, EAX becomes
  `[ESI]`, the previous-block pointer. At `00421494`, the failing instruction is
  `test byte ptr [EAX+8],1`. Thus the predecessor pointer is unusable for reading
  its flags. The current header was readable, and its flags were writable just
  before the fault. This is compatible with a corrupt header, non-engine/interior
  pointer, or stale/double free; it does not choose among them.
* This Release free does not retain a trustworthy allocation owner or check
  whether the block was already free. Before faulting it has already set the free
  bit and changed counters. A dump at this instruction cannot recover the
  original free bit and must not use those counters as a pristine pre-free state.

## Precise recovery recipe for an existing dump/context

These offsets follow the retained instructions, not x86 frame-pointer heuristics.
Let S be **ContextRecord->Esp at EIP 00421494**, not the VEH's ESP.

| Observation | Meaning at this instruction |
|---|---|
| Context ESI | alleged allocated-block header, userPointer minus 16 |
| Context EAX | alleged previous-block header |
| `[S+0]`, `[S+4]` | saved caller EDI, saved caller ESI |
| `[S+8]` | return address from MemoryManager::free |
| `[S+12]` | original userPointer |
| `[S+16]` | array argument |
| `[S+20]` | owning delete return address, **if** `[S+8]` is one of the wrapper returns below |

The scalar delete wrapper at `00420e70` calls free and returns at `00420e80`;
the array delete wrapper at `00420eb0` returns from free at `00420ec0`. Neither
adds a saved-register frame. Therefore `[S+20]` directly identifies the owning
delete call for either path. Other direct free callers require their own decoding.

Useful independently recovered owning return sites:

| Return site | Ownership discriminator |
|---|---|
| `0041a13d` | ExitChain::run deleting its entry after the callback |
| `00411c5f` | SoundTemplateList::remove deleting anonymous-container object |
| `00411cee` | SoundTemplateList::remove deleting named-map object |
| `00411d5c` | SoundTemplateList::remove deleting binding-map object |

ExitChain's indirect callback call is at `0041a12c`, with return `0041a12e`.
Finding that return deeper in an interrupted stack establishes callback ancestry,
but does not identify the callback on its own. If the immediate owner is
`0041a13d`, `[S+4]` and `[S+12]` should both identify the Entry; its Release fields
are next/+0, function/+4, name/+8, priority/+12, critical/+16. This distinguishes
entry deletion from callback execution without relying on a complete unwind.
If entry deletion fails, the callback may already have completed: naming it as
the bad free would be wrong.

The decisive minimal retained observation would therefore be EIP/ESP/EAX/ESI,
the exception's read address, six stack DWORDs, and readable bytes around
userPointer-16. Prefer a pre-existing dump if one is found elsewhere. None was
present in the named run-v3 evidence. A future authorized diagnostic would capture
the supplied ContextRecord, not merely call CaptureStackBackTrace again. This
report does not run or authorize such a diagnostic.

## Destruction order and startup

ExitChain::add inserts before existing equal-priority entries; ordinary priority
is zero. SetupClientAudio installs ConfigClientAudio, SoundId, Sound2, Sound2d,
Sound3d, SoundTemplateList, and Audio, then adds its own remove callback last.
Among the audio callbacks the resulting order is SetupClientAudio removal,
Sound3d removal, Sound2d removal, Sound2 removal, ConfigClientAudio removal.
Sound2d::remove additionally clears index pools and deletes its MemoryBlockManager;
Sound3d::remove deletes its MemoryBlockManager. Those later owners remain
possible even after successful Audio removal.

The binary confirms SetupClientAudio::remove (`00405580`) calls
SoundTemplateList::remove first (return `00405585`), Audio::remove second (return
`0040558a`), then tail-jumps to SoundId::remove. Consequently silence after
"stage remove" does not establish that Audio::remove was reached.

MemoryManager is a static in OsNewDel.cpp, with dynamic constructor/destructor
symbols `004037e0` and `00464ab0`. Its allocate path also initializes it lazily.
It is not an ExitChain removal callback. Foundation::remove calls ExitChain::quit
while main is still active, before normal CRT global destruction. There is no
source basis for a theory that ordinary CRT destruction already removed the
MemoryManager before this free. A missing explicit MemoryManager::install in the
fixture is likewise not a demonstrated startup defect.

The author's Sound2dTemplate and Iff end their scope before playback. SoundId's
TemporaryCrcString uses inline storage and its destructor does not free an engine
object. Ending that scope before shutdown is reasonable hygiene but cannot be
presented as a fix for this observed invalid predecessor.

## STL and allocator ABI checks

The map includes `stlport_vc71_stldebug_static:dll_main.obj`, but that filename
alone is not evidence of the causal ABI mismatch. The fixture uses retained v120
Win32 `/MT`, `/DNDEBUG`, `/DDEBUG_LEVEL=0`, `/Zc:wchar_t-` and the actual STLport
include directory. It does not substitute MSVC STL at its public engine boundary.

Crucially, disassembly of retained `__stlp_chunk_malloc` (`00401db0`) shows a call
at `00401db9` to `00420e50`: the engine's `operator new(size_t,
MemoryManagerNotALeak)`. The selected small-node allocation/deallocation pair
`00402040`/`004020d0` uses the same free-list base `0049bac0`, 8-byte classes, and
the same lock helpers. Thus the tempting theory that this selected STLport chunk
allocator obtains CRT malloc blocks and hands them directly to engine free is
contradicted by the executable for this path.

SoundTemplateList removal also preserves the distinction between pooled tree
sentinels and whole container objects: its 20/24-byte sentinel deallocations call
STLport `_M_deallocate` at `004020d0`; the container-object deletes call the
engine scalar delete at `00420e70`. There is no demonstrated sentinel-to-global-
delete mismatch in those instructions. This is a scoped check, not a proof that
every linked library/object has a consistent ABI.

## Decision

Do not change global allocation providers, reorder Audio teardown, retain an
otherwise-dead SoundId, or add unrelated bootstrap subsystems on this evidence.
The next observation must establish the original free's pointer and owning return
site. The exact offsets above reduce that requirement to a small context record;
symbolizing `00421494` again cannot supply it. Playback completion remains useful
bounded evidence, but teardown and the original-engine baseline remain failed.
