# Miles upgrade boundary

The game-facing boundary is a small native-Miles-shaped C++ API. It carries sample/stream operations, signed scalar values, float values, nullable output pointers and opaque handles. Pipe sessions, request IDs, leases and process control stay private. A later native same-version library selects direct forwarding behind this boundary; gameplay code does not adopt an IPC API.

```text
clientAudio → ClientMiles operations → selected implementation
                                      ├─ Native: actual Win64 Miles declarations → native library
                                      └─ Temporary: private pipe → x86 host → original Miles DLL
```

The native library is unavailable. The native branch above has real object-compilation evidence, not a successful link or runtime. It contains real unresolved Miles imports, not a fabricated import library or stand-in implementation. Its compatibility target is the possessed 7.2a header; a different licensed SDK version still requires signature and behavioral qualification.

Borrowed stream samples use the same opaque `Sample*` type as allocated samples, matching how SWG uses Miles. Ownership remains different: release allocated samples, never release a stream's borrowed sample; stream close invalidates the borrowed identity. The five SWG shared controls use their existing names. There is no second borrowed-audio interface or runtime plugin system.

## Current evidence

- Common-handle native compilation: all11 enumerated AMD64 delegate, caller, signature-contract and pipe objects pass against the real header. Exact native import sets5/19/9 and six borrowed-caller references are recorded in borrowed-native33. No native64 library or playback ran.
- Temporary allocation lifecycle: sample-live31 passed780 actual original-DLL requests, including257 allocations,256 explicit end/release cycles and shutdown with one live allocation. This is not playback coverage.
- Nineteen owned-sample playback controls now have private pipe implementations in playback-pipe34. Its930 scripted checks cover encoding/decoding and error/output handling under ASan/UBSan. Actual vendor effects and native compilation of this new slice are not yet established.
- Named-file characterization: binding-probe30 successfully reused one actual sample A/B/A, rejected an unsupported WAV tag, and recovered with B. Nonempty last-error text persisted after success, so the scalar return decides success. All buffers stayed alive through shutdown: this proves no retirement boundary.
- File execution remains an integration candidate. The extracted Audio bodies compiled in eight real product-object checks. Subsequent strict Debug worker gates exposed nonassignable-type warnings; failed records and narrow corrections remain separate.

## Remaining obligations

The pipe still needs proven file-image ownership and retirement, live stream/borrowed-proxy handling, callback registration and completion ordering, engine file execution and shutdown, Bink's real-driver relationship, and representative audio/gameplay acceptance. No cumulative sample cap, one-bind rule, silent fallback or fabricated success is an acceptable substitute. Production checkout remains49d0, with unresolved real Miles imports.

The temporary host can be removed only after a native backend supplies the full used interface and passes the same behavior/ownership tests. Compile compatibility and using the original mixer do not establish100% experience or timing equivalence.
