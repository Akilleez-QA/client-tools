# Read-only teardown/lifetime review

2026-09-30. No further execution, allocator workload, injected fault, production
edit or assertion suppression. Examines fixture v3 and current actual source.

## Concrete fixture/product differences, with limits

1. Product ClientMain.cpp:384–385 calls SetupSharedFoundation::remove followed
   by SetupSharedThread::remove. Fixture probe.cpp:35 calls only foundation
   removal. This is a real missing cleanup stage. **It cannot explain a fault
   occurring inside the preceding foundation removal**; adding it is contract
   hygiene, not a demonstrated fix.
2. The fixture's local SoundId (probe.cpp:33) remains alive through foundation
   removal. ClientMain's gameplay call has returned and its scoped game work has
   ended before line384. A small fixture should finish its own playback-object
   scope before global teardown. However, **the suspected SoundId heap-lifetime
   cause does not hold up**: SoundId.h:46–47 contains an int and TemporaryCrcString;
   TemporaryCrcString.h owns an inline 512-byte buffer, and its destructor at
   TemporaryCrcString.cpp:62–64 is empty. It does not free a cached template or
   call Audio on destruction. Moving it into an inner scope cannot honestly be
   predicted to repair the observed free fault.
3. The fixture runs Foundation D_console, File install(false,0), a deterministic
   random seed, and a small audio-only subsystem set. Product ClientMain uses
   D_game, File install(true, actual SKU bits), compression/regex and broader
   object/game setup before audio. These are intentional headless differences,
   not proven invalid bootstrap. No source evidence yet identifies an omitted
   initialization whose cleanup dereferences the bad block. Do not add unrelated
   subsystems until that dependency is shown.
4. The fixture registers its observation-only VEH and never unregisters it.
   Store the returned handle and remove the handler after normal teardown. This
   is test-owned resource hygiene, not the cause of the earlier exception.

## Ownership paths checked

- The authored Sound2dTemplate and Iff are already enclosed in probe.cpp:32's
  inner scope, so their destructors run **before Audio::playSound**. They are not
  live across global removal. SoundTemplate::~SoundTemplate clears its list via
  real Audio::decreaseReferenceCount and deletes its actual vector. Later playback
  reloads the serialized template through SoundTemplateList. Do not retain the
  authoring template artificially to mask a possible cache-lifetime issue.
- The fixture holds no AbstractFile pointer. Actual Audio/TreeFile load and cache
  own their files/buffers. It would be incorrect to manually delete vendor or
  cache data from the fixture during shutdown.
- Real Sound2::~Sound2 releases its template (Sound2.cpp:95–102). The observed
  disappearance at epoch41 and zero sound count establish that the live Sound2d
  finished, but are not proof that every cache/option-manager object is freed.
- SetupClientAudio.cpp:39 registers one teardown callback with ExitChain.
  Its remove at44–49 calls SoundTemplateList::remove, then Audio::remove, then
  SoundId::remove. The fixture already relies on this same real callback and
  must **not** add a second manual Audio::remove/SetupClientAudio::remove call.
- Audio::remove at1377 onward stops sounds, clears sample maps, shuts down Miles,
  clears music offsets/deletes its own DataTable, deletes cache keys and sample
  bytes, clears cache and deletes the serve timer. The music table was created
  by `new DataTable`/load at1347–1349, not fetched from DataTableManager; the
  obvious “both managers delete the same music table” theory is unsupported.
- ExitChain::run at194–213 removes each entry from the list, calls its real
  function, and then deletes the entry. The observed MemoryManager::free fault
  could be inside a callback **or deleting the ExitChain entry itself**. Current
  short stack does not distinguish these. Do not name Audio::remove as the
  faulting owner merely because audio ran before shutdown.
- Link map confirms the actual global new/delete providers are
  sharedMemoryManager:OsNewDel.obj and actual MemoryManager, not test substitutes.
  No contradictory provider is established by finding CRT free elsewhere in the
  map; CRT's internal allocations legitimately use CRT free.

## Scoped proposed fixture-only correction

An unexecuted `fixture-cleanup-proposal.patch` makes playback a nested scope,
saves only the scalar result before leaving it, calls thread removal after
foundation removal, and unregisters the fixture VEH. It does not reorder real
ExitChain callbacks, free caches manually, suppress shutdown, catch/ignore the
fault, modify allocators, or claim a fix. The earlier failed evidence stays
unchanged. No rerun is proposed as a way of validating an allocator fault.

**Missing causal evidence:** which ExitChain callback (or entry deletion) owns
the failing free and which allocation family created that address. The source
review rules out the initially suspected SoundId owned-heap destructor, but does
not identify the corrupted object's origin. If further observation is approved,
use diagnostic-only source-entry tracing of the real ExitChain callback names
and existing symbolized stack facilities, not a new allocator stress/fault case.
Until then, playback evidence remains bounded and overall teardown remains failed.
