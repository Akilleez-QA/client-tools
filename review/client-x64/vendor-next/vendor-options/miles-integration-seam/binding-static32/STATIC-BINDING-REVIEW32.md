# Original DLL binding ownership: bounded static review 32

The possessed DLL does **not** preserve the previous binding when a normal named WAV bind reaches unsupported-format rejection. It initializes the handle, including replacing its source-buffer descriptors, before rejecting the format. Successful PCM binding stores an address inside the caller's image; it does not copy that PCM payload. A subsequent bind removes the previous descriptor array. These are direct control/dataflow findings, not a proof that every vendor thread or provider has relinquished every reference.

This materially narrows the missing implementation decision: old-binding atomicity must not be promised as native behavior. Repeated PCM replacement has a concrete descriptor retirement mechanism. Generic codec retirement and asynchronous quiescence remain unproved by this bounded review.

## Identity and scope

Read-only static inspection on 2026-09-30 using GNU objdump 2.47 and a small local PE export parser. No DLL execution, build, VM, playback, protection changes, fault tests or proprietary downloads. No product or frozen-candidate edits. Raw disassembly is retained only in the mode-0700 `private/` directory, excluded from this report. Do not curate that directory into public evidence.

- DLL: `/home/akilleez/Work/swg-source-vm/client/SWGSource Client v3.0/Mss32.dll`; SHA256 `0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe`.
- PE32 preferred image base: `0x21100000`. All offsets below are RVAs, independent of load relocation.
- Possessed `Mss.h`: SHA256 `966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e`; header identifies Miles 7.2a. The declarations/comments do not establish rebind failure atomicity or a general retirement guarantee. Prior bounded local documentation search found no usable lifetime manual; no new manual is being asserted here.
- Private raw-evidence manifest `private/SHA256.json`: SHA256 `d65dff1e5ecdbf7d3bf72c2a472d6d0f9fa50514387c1d38d38168242f6c299c`.

The reviewed path is ordinary RIFF PCM WAV with nonempty `.wav` name/suffix, and the otherwise valid WAV with unsupported format tag used by probe30, when no registered provider handles that suffix/tag. A provider that handles `.wav` can select another path. VOC, ID3-adjusted compressed files, arbitrary codecs, allocation failure, callbacks, active playback and all mixer threads are outside a completed proof.

## Auditable path identities

| Export | RVA | Internal path followed |
|---|---:|---|
| `AIL_set_named_sample_file` | `0x14b50` | named dispatch `0x2b5f0` |
| `AIL_set_sample_file` | `0x149c0` | file dispatch `0x2b440` |
| `AIL_init_sample` | `0x148f0` | initialization `0x2cab0` |
| `AIL_set_sample_buffer_count` | `0x17260` | descriptor replacement `0x2e640` |
| `AIL_WAV_info` | `0x1d170` | WAV parsing `0x29c40` |
| `AIL_set_sample_address` | `0x150e0` | address installation `0x2cca0` |
| `AIL_release_sample_handle` | `0x14860` | release `0x2ca50` |

PCM setup is internal RVA `0x29fb0`; suffix provider lookup is `0x25370`, calling registry search `0x34d0` and suffix matching `0x3400`. Names are export identities where present; internal labels describe observed operations, not recovered vendor symbols.

## Image lifetime and failure semantics

1. **Binding mutates first.** Named dispatch calls initialization at `0x2b698`, before suffix-provider lookup and `.WAV` fallback. File dispatch initializes again at `0x2b464`, before WAV parsing and format acceptance. Initialization marks the sample's driver status entry, disconnects processor stages, resets scalars and calls buffer-count replacement at `0x2caef`. The latter frees the previous array at `0x2e657`, clears the sample's array pointer, allocates a replacement and zeroes its entries. Hence even rejection need not leave the old binding or settings intact. Buffer replacement allocation failure is also not an atomic rollback; no fault experiment was performed.

2. **PCM is borrowed, not copied.** WAV parser `0x29c40` records the data chunk's interior address in its caller-provided info structure at `0x29d47`. In this binding call the info structure is on the file-dispatch stack. PCM setup calls address installation at `0x2a026`. Its core writes the incoming address into the first descriptor at `0x2cca7`, writes the byte length at `0x2ccb0`, and clears subsequent descriptors. The caller must keep the full owned image alive while it is the bound source. Ordinary A/B PCM replacement has no cumulative image list in this direct path: initialization removes A's descriptors and setup installs B's address.

3. **Unsupported-tag rejection is destructive to the old direct binding, but does not install F.** After WAV parsing, format dispatch rejects neither the RIFF container nor the data chunk itself. For a tag other than the direct supported cases it asks for a provider at `0x2b53d`. A zero provider branches at `0x2b546` to error and zero return at `0x2b4ee`. The intervening image-derived addresses are in stack-local WAV info; the address-installation call at `0x2b553` is bypassed. Thus, on this exact branch, F is not installed in the sample descriptor, and A's old descriptor has already been removed. This is not a claim about all reasons for a zero return.

4. **Generic failure can occur after image installation.** If the format provider exists, the path installs the incoming data address at `0x2b553`, then sets a processor and converts its `-1` result to bind return zero at `0x2b563–0x2b569`. Named suffix-provider dispatch similarly installs an image address at `0x2b750` before its processor-result checks. The reviewed caller path contains no rollback after those checks. Even without proving which provider can produce that result in a real run, this ordering defeats an unconditional source-level assumption that failure occurs before image publication. Pending ownership must survive until that path's cleanup/retirement is resolved.

5. **Release removes the direct array and invokes cleanup.** Release marks the driver status entry at `0x2ca61`, invokes an optional driver callback at `0x2ca82`, calls processor cleanup at `0x2ca89`, frees the descriptor array and clears its pointer at `0x2ca96–0x2ca9b`, then frees other sample-owned work arrays through `0x28fb0`. This direct path does not free the caller's image. The indirect callback/provider cleanup implementations and every potential thread-held reference were not traced; release's global quiescence is not newly proved here.

## Suffix and concurrency boundary

The named path reads the suffix for matching and passes it to registry lookup. Registry search gets provider properties through an indirect call, then passes the caller suffix to local matcher `0x3400`. In the reviewed registry call sequence the indirect provider-property call is not given the caller suffix; the matcher reads it synchronously. No direct store of the suffix into sample state was found in these routines. This supports a synchronous suffix-use inference for the examined path, not a whole-binary no-escape theorem: wrapper tracing, deeper string helpers and every indirect path were not exhaustively audited. Retaining the tiny owned suffix alongside its image is the simple conservative implementation choice.

Export wrappers call conditional mutex helper `0x1090`; its import calls are `CreateMutexA` and `WaitForSingleObject`, with `ReleaseMutex` in the wrapper exit. This is real serialization machinery, but its enabling global and participation of every consumer were not proved. Do not equate an observed lock with a completed asynchronous lifetime proof.

## Consequence for the pipe implementation

For the examined native PCM/rejection path, “failure preserves the previous native binding” is incompatible with the DLL. Preserve caller outputs on *transport/local preparation error*, and report native bind return separately; do not describe a native zero as restoring the previous audio state. Probe30's F returned zero with an error, while B2 returned one with the same stale error. Success must follow the signed API return; `last_error` is diagnostic text, not a success predicate.

A small owner prepared before the call remains appropriate: current and pending images/suffixes stay alive during native binding; commit uses allocation-free moves. The direct PCM path supplies evidence for replacing the previous descriptor, but this review alone does not authorize dropping all prior owners for generic providers or active playback. Failure owners cannot be retired solely because return is zero. An implementation claiming all supported Audio formats still needs the relevant provider cleanup and consumer synchronization paths, or a version-specific vendor contract. Accumulating every failed image forever or imposing a one-bind cap is not an acceptable substitute.

The next useful static step is narrow: identify the actual processor/driver configuration used by the target host, trace the exact cleanup callbacks and PCM consumer locking, then decide whether that closes the old-address escape set. If the scope includes compressed sources, separately follow those actual providers; PCM reasoning does not cover them. No additional runtime measurement is authorized or performed by this report, and a successful query after replacement would still not prove absence of dormant references.
