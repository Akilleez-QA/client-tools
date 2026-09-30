# Source map

All product paths below are relative to the read-only checkout
`/home/akilleez/Work/swg-source/client-build-next`, commit
`49d0eeed4ddaa177d7a93ea396c37c3d9b9942da`. Line numbers refer to the unmodified
source. [source-manifest.json](source-manifest.json) records SHA-256 hashes.

| Source and lines | Concrete constraint on the adapter |
|---|---|
| `src/engine/client/library/clientAudio/src/win32/Audio.cpp:88,113,123` | FileMap is `std::map<UINTa, AbstractFile *>`; one original map and a counter initialized to zero. |
| `Audio.cpp:234–237` | Four original callback declarations are file-local `static`; their definitions later omit `static` but retain that linkage. A different translation unit cannot legitimately call them by an extern declaration. |
| `Audio.cpp:1289–1293` | Original Miles startup precedes registration of all four original callback addresses. Proposed patch leaves the registration intact. |
| `Audio.cpp:3936–3965` | Global `once`; nonmain-thread lazy install; `TreeFile::open(name, PriorityAudioVideo, true)`; map insert and counter increment on success; zero out key on failure; boolean outcome returned as U32. Status distinguishes successful key zero from failed open. |
| `Audio.cpp:3968–4004` | Original close resolves key, calls `close`, deletes the object, erases the map entry, and updates debug bookkeeping. Missing key has debug diagnostics and no new return status. |
| `Audio.cpp:4007–4059` | Seek maps 0/1/2 to AbstractFile origins, passes signed offset via Windows `long`, ignores `seek` boolean, and returns `tell()` as S32. Invalid origin is fatal for a live key; absent key defaults to zero plus debug diagnostics. |
| `Audio.cpp:4063–4098` | Read calls `AbstractFile::read(buffer, bytes)` with U32 bytes into an `int` parameter, then converts signed `bytesRead` to U32. Missing key returns zero plus debug diagnostics. |
| `Audio.cpp:1418–1443` | Shutdown clears installed state before actual `AIL_shutdown`; the remaining file map is only warned about afterward. |
| `src/external/3rd/library/miles/include/Mss.h:1245–1283` | Windows U32/S32 are unsigned/signed int; UINTa uses the Windows target's pointer width. Local header uses fixed 32-bit values and uintptr_t, verified by proposed adapter assertions. |
| `Mss.h:5218–5242` | Windows `MSS_FILE` is char; exact open/close/seek/read callback typedefs and seek origin constants are 0/1/2. |
| `src/engine/shared/library/sharedFile/src/shared/TreeFile.cpp:84–181` | Live configuration establishes SKU/priority paths, trees, TOCs, absolute and cache search nodes. Calling the existing TreeFile keeps that state in the game. |
| `TreeFile.cpp:198–215` | TreeFile removal clears cached files and deletes search nodes; adapter admission must end in the correct lifetime order. |
| `TreeFile.cpp:505–600,661–666` | Normalization expects sufficient output storage and is run against the original filename in a fixed `Os::MAX_PATH_LENGTH` buffer. The transport must preserve original bytes and validate extent, not normalize independently. |
| `TreeFile.cpp:668–704` | Preloaded cache lookup transfers its file pointer by setting the cache entry to null, then returns that existing file. Opening elsewhere or copying the cache would not preserve this behavior. |
| `TreeFile.cpp:711–740` | Current search-node order and deletion marker decide which file opens; requested priority is forwarded to each node. Cache mutex does not serialize the entire open or Audio's map. |
| `src/external/ours/library/fileInterface/src/shared/AbstractFile.h:28–43,68–86,109` | Seek-origin/priority enums; tell returns int; seek uses int offset and bool result; read returns int with int count; close is void. |
| `src/engine/shared/library/sharedFoundation/src/win32/PerThreadData.cpp:125–133` | Installing the subsystem installs primary-thread TLS. |
| `PerThreadData.cpp:137–172,175–227,297–312` | Subsystem removal requires other threads to finish; threadInstall(false) allocates Data/Gate and writes TLS without the already-installed check; threadRemove owns removal. This does not prove a valid new callback lane. |
| `PerThreadData.cpp:67–79,460–462` | Access requires installed subsystem and per-thread TLS; read gate comes from that thread's Data. |
| `src/engine/shared/library/sharedFile/src/shared/FileStreamer.cpp:208–242` | Threaded reads enqueue a request using the caller's TLS gate and wait for it. The original callback has a real blocking/thread-state dependency. |
| `src/engine/client/library/clientAudio/build/win32/clientAudio.vcxproj:31–55,106,339–360` | Configurations produce a StaticLibrary; the public include path already exists; existing headers are listed for project organization. Current local namespace entries require no DLL export macro. New header project-list registration can remain optional future IDE bookkeeping. |

Existing candidate references, read only:

- `ARCHITECTURE.md`: same-stack versus unsolicited callbacks, unresolved callback
  scheduling, original TreeFile ownership and original-engine lifecycle gate.
- `protocol-candidate/API-MAP.md`: opcode 28 registers four callback tokens; final
  paragraph records exact file callback signatures.
- `protocol-candidate/CONTRACT.md`: reverse file operation results, checked
  session/generation identity, valid-zero original file key and thread context.
- `protocol-candidate/miles_wire.h`: File resource kind and FileOpen/FileClose/
  FileSeek/FileRead control identifiers; no implementation added here.
- `transport-candidate/resource_registry.h:34–36,104–110`: rejects null local
  pointer storage. A local key of zero must live inside a non-null owned record
  if this registry is reused; it cannot be cast to the registry pointer.

The protocol prose saying the host owns all real file addresses must not be
read as moving TreeFile objects into the host. In the reverse design, original
AbstractFile objects and their map stay client-owned; the host owns only its
local callback token binding. The seam makes that distinction explicit.
