# Debug x64 callback fixture startup failure

The original failure remains in v2/v3. It was not an audio callback failure: execution had not reached SetupSharedFile or the callback checks.

Diagnostic v4/v5 adds only a vectored exception observer returning EXCEPTION_CONTINUE_SEARCH. It never handles or suppresses exceptions. The original exception is access violation c0000005, read at address 0x8; SetupSharedFoundation's unhandled filter then reports ExceptionHandler invoked and causes breakpoint exit0x80000003. Debug Win32 still passes20/20.

The genuine linked map and captured stack show:

SetupSharedFoundation::install → MemoryManager::registerDebugFlags → DebugFlags::registerFlag → DebugFlags::insert → STLport vector<Flag>::insert/_M_insert_overflow/_M_clear → scalar operator delete → MemoryManager::free.

v4 failure RVA0x4140e is the `mov rax,[rax+8]` in the Debug chain assertion; allocatedBlock->getPrevious() is null. This explains why the final Fatal output alone was insufficient to diagnose it. It does not establish where corruption began without a controlled change.

## Discriminator

Both private relinks use the same v5 callback object, same genuine dependency libraries and same matching InstallTimer object. Only the allocator's minimum allocation/free-remainder rule differs:

| Allocator | Source SHA256 | Result |
|---|---|---|
| Candidate minimum64 bytes on x64, with minimum64 split remainder | 172dcd8958b78af24ef4b08f1f0a2409e89ae81665fb2ef6717b9a24d161467f | Debug x64 setup + real TreeFile callbacks20/20; exit0 |
| Same source with only the two minimum-size edits reverted | 37a389eb8f7a713248ec2cc63bca7248dc421546bfb6b69007f7e1406813feb1 | SetupFoundation AVread0x8 returns before callbacks; exit0x80000003 |

This isolates the fix from the concurrently changed ByteCount/InstallTimer interface. It agrees with the separate allocator invariant probe: an x64 free node is56 bytes rounded64, so an allocated32-byte block or a48-byte split remainder cannot safely become a free node. No Audio.cpp backend changes, fake symbols, skipped initialization or exception bypass were used.

The old Foundation/MemoryManager library hashes were identical between v3 and v4 (625f2653bd701d40c0753d2cf1589b7440338c3f3700c156eb0d9975d0e43eae and a6f7763184c98451c0347f0cbdbbff564c6d42418a1ae441b15ad6f99dc2c239 respectively). Some unrelated libraries had rebuilt, so these runs are not advertised as a single frozen full-product snapshot. The controlled relinks bind the new allocator directly and use identical remaining objects.

Evidence: audio-debug-investigation.zip; runners relink-minimum.py and relink-minimum-control.py. VM dirs C:/audio-callbacks-minimum-v1-agent and C:/audio-callbacks-minimum-control-v1-agent retain executables and maps. This is callback fixture verification, not an x64 Miles runtime or full client acceptance result.
