# First real Miles IPC slice: no playback

**Open contradiction, 2026-09-30:** Astra source review found the claimed 32-KiB aggregate payload-copy bound undercounts temporary copies inside RetainedBuffers::stage. Upload, sealed copy, stage candidate and map/pair copy coexist: at least 36,080 payload bytes for the 9,020-byte fixture. The earlier budget claim is retracted; the runtime observations below did not measure or validate that bound. A bounded repair and new evidence are pending. This is not an observed buffer overflow.

The isolated candidate passed in Debug and Release. A native v120 x64 controller launched a native v120 x86 host, sent 21 framed requests over private named pipes, and received results from the genuine original Miles DLL. Both programs ran under a disposable Wine prefix with a private clocked null sink. This is a component result, not a native Windows device run or a game backend.

| Observation | Debug | Release |
| --- | --- | --- |
| Controller and host compile, `/W4 /WX` | both clean | both clean |
| Exact framed requests | 21 | 21 |
| Genuine startup / named-image bind | 1 / 1 | 1 / 1 |
| Initial duration / position | 204 ms / 0 | 204 ms / 0 |
| Volume getter after framed setter | 0.25 / 0.75 | 0.25 / 0.75 |
| Rate getter after framed setter | 11,025 | 11,025 |
| Duration after rate change | 407 ms / 0 | 407 ms / 0 |
| Released sample token | rejected, status 2 | rejected, status 2 |
| Real shutdown and child exit | completed / 0 | completed / 0 |

Initial rate was 22,050 Hz. A separate fixture-only sample in the same host was bound directly to the same retained valid bytes and underwent the same state changes; its real getters matched the target sample's dispatched results. These direct control calls are distinct from the 21 IPC requests. Neither sample was started, no callbacks were registered, and no stream was opened.

## Boundary and lifetime

The controller and host authenticate the connected child's PID on both pipes. The host checks its server PID when the API succeeds. The full random 128-bit nonce crosses the Hello payload and is checked independently of the coordinator's 64-bit incarnation. Requests are strictly sequential with one active correlation; this does not establish scheduling, fairness, callback affinity, or concurrent intake behavior.

One registry supplies lifecycle handles, sealed-upload identity and scalar dispatch resolution. Pointer values are not serialized. The positive image is exactly 9,020 bytes and is checked against its prospective SHA-256 before any vendor bind. Only one bind attempt is accepted. The attempted 32-KiB payload-copy accounting includes upload, sealed image, retained image and suffix but misses a staging copy; see the open contradiction above. Framing/metadata are separately bounded, not part of a proved process-memory ceiling. The retained image survives sample release and actual `AIL_shutdown`. No additional `AIL_close_digital_driver` is inserted into this success path. The upload copy is released after samples, while the vendor-bound retained copy stays alive through shutdown.

The lifecycle calls, direct control sample, upload handler and named bind are fixture glue, not additions to the existing 39-arm dispatcher. The real getter/setter arms use that dispatcher. Existing coordinator admission/completion is used only for the admitted synchronous operation; no vendor success is inferred from coordinator completion.

## Handler field audit before execution

| Operation | Wire fields used | Genuine signature boundary |
| --- | --- | --- |
| startup, shutdown | none | `S32` startup result preserved; shutdown has no return |
| open driver | v0 frequency, v1 bits, v2 channels, v3 flags | `U32`, `S32`, `S32`, `U32`; fixture restricts 22050/16/stereo/0 |
| allocate / release | Driver / OwnedSample target | native pointers resolved locally; nullable allocation preserved |
| named bind | sample target, sealed-buffer resource, suffix text, v0 size, v1 block | exact 9020-byte `U32` size and signed block 0; NUL-terminated `.wav` suffix |
| volume setter / getter | two float bit patterns / output mask | actual float values; real getter outputs encoded |
| rate setter / getter | signed 32-bit rate / signed result | fixture values 22050 and 11025 are representable |
| duration getter | output mask 3 | two signed 32-bit outputs encoded as bit patterns |
| end sample | sample target | real vendor operation, never playback start |

Unused values/resources/spans are rejected; codec validation precedes handlers. Fixture-only transport statuses 4 (invalid state) and 5 (direct-control mismatch) are not promoted as a finalized public protocol. The stale-token negative is rejected before a vendor call.

## Evidence and limits

`evidence-v2/` contains exact native commands, compile logs, all component source hashes, controller/host runtime logs, original private input hashes, binary hashes and defaults-before/after. Endpoint, codec and registry hashes match the independently tested Endpoint v5 manifest. The failed v1 compile remains preserved privately: it found three fixture compilation issues, not vendor or product failures.

The loaded DLL path was verified in each host log; its private input SHA-256 is `0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe`. The PCM SHA-256 is `ad880479382433a16f99e60d5d5248c30446a44ccc692bfaabb1d012c607a7a9`. DLL, SDK, media, native binaries and disposable Wine prefixes are private and excluded from the evidence packet.

Both runs preserved default audio sink/source and unloaded only their owned sink. ALSA emitted hardware-control lookup diagnostics; the genuine driver opened successfully through the selected private sink. These diagnostics remain in the logs.

Not established: playback, EOS/reverse I/O callbacks, streams, scheduling or lock behavior, restart/recovery, general media support, native Windows device fidelity, full 39-arm coverage, production backend adoption, or complete x64 client operation. A passing bounded sample does not establish 100% game fidelity.

## Deliberate defect discrimination

A private copy swaps the two valid arguments at the genuine sample volume setter. Both configurations observed the reversed real values, returned fixture mismatch status 5, and the diagnostic controller exited 1 as expected. The controller explicitly recognizes this expected failure so it can finish all 21 requests and normal sample release/shutdown before exiting; it does not recategorize the swapped behavior as successful functionality. Both hosts exited normally. No malformed vendor input, playback or callback was introduced.

The unmodified positive source remains unchanged. `evidence-mutation-v1/` contains raw failures, actual mutant build manifests and a provenance note: the initial runtime script's source field recorded the unchanged candidate, while its executable hashes and the native build manifest correctly identify the mutant. That raw record is preserved; the script has been corrected for future use. Defaults were unchanged and the private sink was removed in both mutation runs.
