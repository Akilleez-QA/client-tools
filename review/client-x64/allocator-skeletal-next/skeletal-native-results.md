# Skeletal hard-kernel verification

Native VS2013 v120, Debug/Release, Win32 stock and candidate, x64 candidate.
No commits or product overlays performed in this lane.

## Evidence boundary

`run-skeletal-hard.py` compiled the complete actual candidate TU for Debug and Release on
both platforms. Its standalone link failed on genuine renderer dependencies,
including ShaderPrimitive and Graphics. This remains a failed whole-TU link at
`C:/skeletal-hard-v1-agent` and `C:/skeletal-hard-Debug-v1-agent`; it is not counted as a runtime pass. Stock x64
failed on its original inline assembly as expected.

`extract-skeletal-kernels.py` then selected exact unchanged source slices for
real data definitions, work structure, and the hard SSE kernels. All actual
headers remain, including the production 64-byte PoseModelTransform. No fake
allocator, fake headers or replacement symbols were supplied. Only a namespace
closure/using directive joins the selected ranges. `skeletal-slices-manifest.json`
records full-source and slice hashes and original line ranges. This is kernel
coverage, not whole-renderer integration coverage. Genuine core libraries and
source-built STLport resolve used dependencies; library hashes are in results.

The first slice run stopped on the map binding guard because Release inlined
the x64 wrapper. Version 2 uses volatile function pointers in the probe to retain
both kernel entry points, without editing their instructions. Original failed
runs remain intact. `skeletal-hard-probe-v1.cpp` preserves the original probe.

## Native results

`C:/skeletal-slices-v3-agent` and its downloaded ZIP are the final packet.
Version 2 remains preserved. Version 3 adds initially unmasked exception controls
to alternating finite normal-kernel cases; nonfinite cases stay masked.

| Configuration | Stock Win32 | Candidate Win32 | Candidate x64 | Stock/candidate value and bound differences |
|---|---:|---:|---:|---:|
| Debug | 2,688 records | 2,688 records | 2,688 records | 0 |
| Release | 2,688 records | 2,688 records | 2,688 records | 0 |

Candidate Win32 record files equal stock byte-for-byte. All runs report zero
canary, input preservation, iterator advance or full MXCSR restoration failures.
The sampled exceptional-input category also matches, but this does not establish
general NaN payload equivalence. Stock x64 rejects inline assembly on both configs.

## Prospective corpus and acceptance

The dimensions were fixed before execution: two hard kernels (normal, normal+
dot3), seven counts (0,1,2,7,8,9,65), source/destination alignment 0 or 4 modulo
16, two valid stride/offset layouts, three categories and 16 MXCSR combinations.

- Caller-shaped category: signed axis-permutation matrices plus translations,
  unit-axis normals/tangents, finite positions, flips +1/-1.
- Bounded finite stress category: deterministic finite matrix/vertex values.
- Exceptional category: signed zeros, denormals, infinities and NaNs, reported
  separately rather than assumed a valid rendering input contract.
- Real matrix W row stays (0,0,0,1); matrix and work storage remain aligned16.
- Output position@0 and normal@12. Normal-only stride24 or64; dot3 stride40 with
  offset24, or stride64 with offset32. SourceVector remains36 bytes and dot3 16.
- All four rounding modes, FTZ on/off, DAZ on/off. Alternating pre-existing
  sticky bits require exact restoration, not just restoration of control bits.
- Every output byte outside intended fields has a sentinel. Inputs and matrices
  are hashed before/after; work iterator advances and four-lane bounds are checked.
- Comparator requires exact record count, input identity, zero internal failures,
  and no finite-category differences; all exceptional differences remain recorded.

## Limits

No render dispatch, soft/multi-transform skinning, GPU upload, complete frame,
performance or lifecycle validation. Output source-aliasing is outside the observed
caller contract and was not tested. Sentinels detect writes, not speculative reads;
no guard-page proof of source read boundaries is claimed. The finite normal-kernel cases alternate fully masked and unmasked caller
exception controls; dot3 cases use masked controls. No deliberate exception
trap or signal-handler recovery is tested. The matrix W constraint is taken
from the actual PoseModelTransform constructor/identity paths, not arbitrary4x4.
No conclusion about SseMath's separate legacy register-clobber defect transfers
to these kernels: these original kernels directly match the candidate here.
