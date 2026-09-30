# Original client file callback seam, candidate 20

2026-09-30. Product reference: `49d0eeed4ddaa177d7a93ea396c37c3d9b9942da`.
Review artifact only. The product checkout is unchanged. Following the user's
existing authorization for native source work, the full original and patched
Audio.cpp now compile to objects with native Windows v120 in Win32/x64
Debug/Release. No executable was linked or run, and no allocator, engine,
vendor, codec, device, transport, or fault workload was executed.

[`Audio-file-callbacks.patch`](Audio-file-callbacks.patch) adds one explicit
client-local interface, declared in
[`ClientAudioFileCallbacks.h`](ClientAudioFileCallbacks.h). The patch adds the
header to clientAudio's normal public forwarding-header layout, includes it in
`Audio.cpp`, and defines four wrappers immediately after the existing callbacks.
Each wrapper calls exactly one original callback in that same translation unit.
The original four callback bodies, static linkage, registration call, map,
counter, thread-install flag, and file ownership remain intact. No copy of any
file callback or filesystem implementation is added. The future reverse-RPC
dispatcher includes this header and calls these ordinary C++ entry points only
after it has admitted the request onto an appropriate client execution context.

```cpp
// Client-local calls after admission; these are NOT a network message layout.
ClientAudioFileCallbacks::OpenResult opened =
    ClientAudioFileCallbacks::open(originalNameBytes);
if (opened.callbackResult != 0) {
    // Bind opened.handle to a fresh session/generation File identity.
    // opened.handle.value == 0 is a valid successful open.
}
```

The wrapper type has no implicit conversion to `bool` or `void *`. Its
`uintptr_t` value represents the original `UINTa` map key in this client only.
The public API deliberately returns open status and the local handle separately;
it cannot be installed as a Miles callback table. Actual Miles callback calling
conventions remain on the original functions. The patch does not replace
`AIL_set_file_callbacks` with macros or connect the host.

`clientAudio.vcxproj` builds a static library; existing `Audio.h` has no export
decoration. These externally linked namespace functions therefore need no DLL
export macro for the current client-local link. Listing the new header in the
VCX project's `ClInclude` items is optional IDE organization for a future
integration; its include path already exists and no new translation unit is
needed. The candidate deliberately does not expand the project-file patch.

| Original callback, Windows ABI | Proposed client-local C++ entry |
|---|---|
| `U32 __stdcall fileOpenCallBack(char const *, UINTa *)` | `OpenResult open(char const *)` |
| `void __stdcall fileCloseCallBack(UINTa)` | `void close(LocalFileHandle)` |
| `S32 __stdcall fileSeekCallBack(UINTa, S32, U32)` | `int32_t seek(LocalFileHandle, int32_t, uint32_t)` |
| `U32 __stdcall fileReadCallBack(UINTa, void *, U32)` | `uint32_t read(LocalFileHandle, void *, uint32_t)` |

The wrappers convert scalar values, never cast function pointers or alias a
`uintptr_t *` as `UINTa *`. Compile-time checks in the proposed `Audio.cpp`
addition bind scalar width/signedness and seek origins to its real SDK types.
Those checks have now compiled in the full Audio.cpp against the pinned real
SDK/engine headers on all four native configurations. The earlier standalone
type-only checks remain narrower evidence; see
[compile plan and results](COMPILE-PLAN.md).

## Future reverse-operation handoff

This is the concrete handoff shape for the existing FileOpen/Close/Seek/Read
controls in `protocol-candidate/miles_wire.h`. It is not an implemented dispatcher
or a revision to their codec. [Source map](SOURCE-MAP.md) records the evidence.

| Admitted reverse operation | Single original invocation | Required reply/ownership handling outside the seam |
|---|---|---|
| FileOpen: original NUL-terminated filename bytes | `open(name)` | Preserve `callbackResult` in unsigned return bits. Publish a non-null wire File identity only on success, including local key zero. A failed open's local zero is not a live file. |
| FileClose: session/kind/generation-checked File identity | `close(binding.local)` | Preserve the original void result. After already-admitted file operations finish, invoke close exactly once and retire the binding after return. |
| FileSeek: File identity, signed 32-bit offset, unsigned origin 0/1/2 | `seek(binding.local, offset, origin)` | Preserve the signed 32-bit result in the existing wire representation; do not use the ignored `AbstractFile::seek` boolean as the callback result. |
| FileRead: File identity, unsigned 32-bit request count | `read(binding.local, localBuffer, requested)` | Preserve unsigned callback result bits and exactly that many initialized bytes when the result is within the request/buffer bounds. Keep staging storage alive until the original call returns and transfer owns the returned bytes. |

The client owns the wire-identity-to-local-key binding. The x86 host owns its
own local Miles `UINTa` token-to-wire-identity binding; it never receives the
client's key or `AbstractFile *`. The existing `ResourceRegistry` stores non-null
`void *` and rejects null storage. Casting the original local key into that
registry would lose valid handle zero. If reused, its stored pointer must refer
to a stable, separately owned `FileBinding` record containing `LocalFileHandle`,
with the record pinned until retirement. A typed registry with an independent
occupied flag is another possible future implementation; neither is supplied
here. No raw key becomes an address.

Reserve binding/token capacity before opening where possible. If a successful
open cannot be published, a locally tracked rollback must call the original
`close` on the same approved lane exactly once. It must not delete an
`AbstractFile` itself, invent an open-failure callback result, or forget a local
handle because the wire reply failed. Once a reply may have escaped, do not
retry the side-effecting open/close; resolve the failed session's ownership.
That disconnect cleanup is an unresolved coordinator contract, not implemented
by this header.

Filename validation must preserve exact bytes and the terminating NUL; do not
normalize, case-fold, transcode, or resolve host paths first. The real TreeFile
already normalizes and chooses mounts, deletion markers, and preloaded files.
`TreeFile::open` uses a fixed `Os::MAX_PATH_LENGTH` local buffer while its
normalizer assumes sufficient output capacity. A future decoder needs a
source-compatible validated filename extent, not a silent truncation. An
over-limit request is an explicit unsupported transport condition until the
actual caller contract is established.

The adapter exposes the full original U32 read signature. Internally the game
passes it to `AbstractFile::read(void *, int)`, so the first admitted domain must
fit nonnegative signed `int` and a real staging allocation. A request above that
domain must fail explicitly before invocation; it must not be narrowed or
reported as EOF. This is a bounded experimental domain, not a claim of complete
U32 read support. Do not split one SDK read into several original callback
invocations merely to fit a 1 MiB frame; chunking a completed byte transfer must
retain the original single read operation. Large-result transfer is still
unimplemented.

The original read callback casts its `int` result to U32. If a negative result
becomes a large unsigned value, preserve the raw result for diagnosis and stop
that transport operation rather than copying outside the buffer or clamping to
zero. The existing protocol's successful-read rule (`actual <= requested` plus
exact bytes) cannot represent that as an ordinary successful byte reply.
This is an explicit compatibility limit to resolve, not a fabricated vendor
error. Signed seek offsets/results, including negative values, remain signed
through the local entry point and retain their bits at the existing codec.

## Required thread and lifetime contracts, still unresolved

1. **Execution context.** The adapter runs on its caller's thread and keeps the
   original callback body on that stack. It does not choose a lane. Causally
   related callbacks require an evidence-backed waiting-client route; worker
   callbacks need an independently live route even when no client call is
   waiting. Source-thread/causal identity cannot be guessed from an active
   request. No generic receiver-thread, frame-only pump, or thread-pool policy
   is established by this patch.
2. **TLS installation.** Original callbacks share one `static int once`, not a
   per-thread guard. The first nonmain callback calls
   `PerThreadData::threadInstall(false)` and clears that flag; subsequent
   nonmain threads do not receive installation. Preinstalling a new worker and
   leaving `once` true also is not an established solution:
   `threadInstall(false)` allocates a new Data/Gate and overwrites its TLS slot,
   rather than behaving as an idempotent ensure-installed function. The initial
   main thread already has engine TLS and skips this branch. Any new worker
   route needs a separately reviewed thread/TLS ownership change and teardown
   policy; this patch leaves the original flag untouched. FileStreamer uses
   the caller's TLS gate while waiting for reads, so TLS is operational state.
3. **Serialization and reentry.** `s_fileMap`, `s_nextFileHandle`, debug maps,
   the global `once`, and each file's position are not protected in the
   callbacks. TreeFile's cache mutex does not protect them. The coordinator
   must prove ordering/non-overlap with every original callback entry, including
   any direct in-process caller. Merely adding an adapter-only mutex does not
   cover the original registration path, or prove compatible ordering. Nested
   operations on a live file and close races need exact pins/order; the seam
   has neither a scheduler nor a lock.
4. **Progress.** A pending vendor call can need this service while a Miles lock
   scope is active. Transport progress must continue while the original client
   callback waits in FileStreamer. Do not hold a transport mutex or assume
   main-thread execution can always be deferred. Interaction with unsolicited
   EOS/reentry and shutdown is unmeasured.
5. **Close and shutdown.** Only the original close callback owns
   `AbstractFile::close`, `delete`, and map erasure. Close must run after prior
   admitted reads/seeks finish; local file/binding and staging storage remain
   pinned until completion. Keep TreeFile, FileStreamer, TLS and callback
   admission available for legitimate callbacks during Miles shutdown.
   `Audio::remove` sets `s_installed = false` before `AIL_shutdown`, so an
   `isInstalled()` check alone would wrongly reject needed shutdown callbacks.
   FileMap debug warnings after shutdown are not a cleanup or quiescence
   mechanism. Host death and unknown close outcome need one explicit client
   owner and a no-future-use proof before cleanup.
6. **Identity lifetime.** Wire session/generation invalidation is separate from
   native Audio keys. The original counter has no reset/wrap/collision guard
   here and insertion success is not checked; the bridge must not claim its
   generations solve native wrap. Reinstall/restart and maximum open-count
   contracts remain unresolved. No reset or new file map is added.

The small patch is ready to review as a source integration point. Running it
through reverse RPC remains gated on these contracts and the clean original
engine lifecycle baseline described in the architecture proposal.
