# Four query output stores: bounded static review 33

**No output-seeding defect was found for normally returning calls on valid live/bound handles in the possessed DLL.** All four routines overwrite each requested output; none reads its prior contents. Initializing private output locals to zero therefore does not change these native results. Equal output pointers finish with the second output's value because the DLL writes first then second. Passing one shared local pointer preserves that ordering.

This is evidence about these functions and this DLL, not approval of the complete pipe implementation or a runtime test.

## Exact scope and identity

Read-only disassembly on 2026-09-30, GNU objdump 2.47. No vendor execution, build, VM, playback or changes to frozen source/reports. Raw vendor disassembly is private under `output-static33/private/` (directory mode 0700); this report contains only identities, offsets and findings.

- Possessed `Mss32.dll`: `/home/akilleez/Work/swg-source-vm/client/SWGSource Client v3.0/Mss32.dll`; SHA256 `0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe`.
- Possessed Miles 7.2a `Mss.h`: SHA256 `966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e`. Output declarations are at lines 4580–4586, 4752–4754 and 5204–5206.
- Private evidence manifest SHA256: `ee11031b3bf64701a16e142e40d70ab173756a2a89c1979ef66edfa40efe6762` (`private/SHA256.json`).
- All addresses below are RVAs relative to PE preferred base `0x21100000`.

Preconditions: a valid nonnull native sample handle with valid bound state, or successfully opened live stream; each requested output is writable storage for its declared S32/F32 type. Outputs may be null individually or may equal each other. Output memory aliasing the vendor's internal handle fields, stale handles, concurrent destruction, damaged state and faults/nonreturn are outside this finding. No requirement to start playback is introduced.

## Per-function findings

| Function/export RVA | Store path | Result |
|---|---|---|
| `AIL_sample_volume_levels`, `0x16930` | Left store `0x1699c` from sample field `+0x64`; right store `0x169b0` from `+0x68` | Both requested F32 outputs written; right wins if aliased. |
| `AIL_sample_reverb_levels`, `0x169d0` | Dry store `0x16a59` from `+0x70`; wet store `0x16a6d` from `+0x6c` | Both requested F32 outputs written; wet wins if aliased. |
| `AIL_sample_ms_position`, `0x1cab0` | Calls core `0x2e890`; total store `0x2e9a5`, current store `0x2e9ed` | Both requested S32 outputs written; current wins if aliased. |
| `AIL_stream_ms_position`, `0x1cbc0` | Calls core `0x11950`; total store `0x11a02`; current stores `0x11a12` or `0x11a4c` | Both requested S32 outputs written; current wins if aliased. |

Volume and reverb have no intervening semantic callees: after checking the handle and each output pointer, they load sample state and store it. There is no output-content load or branch on an output's previous value.

Sample milliseconds computes a rate through ADPCM, processor, or ordinary format branches; each converges at `0x2e957` before the two pointer-conditional stores. The ordinary format helper `0x2e4d0` returns a scalar and receives no output pointer. The processor property call at `0x2e937` receives a separate stack temporary initialized to `-1`, not either caller output. Provided that call returns normally, the two outer stores still occur. This does not certify every processor's numerical result, arithmetic validity or termination. The PCM path has no provider callback in that rate branch.

Stream milliseconds similarly converges from its rate branches. Even its explicit zero-rate case writes a value (`1`) to each requested output; it does not leave the caller's seed untouched. For nonzero rate, current position comes from scalar `AIL_stream_position` at `0x1bf90`, whose core `0x11640` was also inspected. That function can return a scalar sentinel on a state branch; the outer milliseconds routine still calculates and stores a result. It receives the stream handle only, never either caller output pointer. Its nested sample queries use separate internal stack storage. No interpretation or normalization of those scalar/signed results is justified by this review.

## Boundary cases and implication

The DLL deliberately contains null-handle guards. Null sample in volume or sample milliseconds, and null stream in stream milliseconds, leave requested outputs unchanged. Null sample in reverb instead writes zero to requested outputs. These guards are concrete observations, but the header alone does not establish null handles as supported API use. They are not a valid-handle defect in a pipe that resolves only live nonnull handles. If a future facade explicitly promises native null-handle behavior, output seeding would need separate treatment for the three no-write cases.

Nullable output pointers are directly supported by the inspected branches. Zero initialization of omitted private locals is immaterial provided omitted outputs are not written back. On local/transport failure the facade must continue preserving caller storage; this native-store finding does not review that path.

Optional export tracing was not exhaustively inspected; the ordinary semantic paths and direct callees above are the basis of the result. The evidence supports closing the proposed initial-output-value concern within the stated valid-handle scope. It does not widen the existing runtime approval or prove whole-pipe integration readiness.
