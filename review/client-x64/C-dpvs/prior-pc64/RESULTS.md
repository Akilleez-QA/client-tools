# Native Windows PC64 numerical comparison

Run: `20260929-074318-657`, Windows VM, VS2013 v120. Diagnostic-only; no production source edits, commits or pushes.

## Reference and provenance

The reference is the existing DPVS Win32 **assembly**, forced to PC64 and round-to-nearest. Each Win32 executable logged raw `fnstcw=0x037f` after setting the mode and rejects a different precision/rounding field. Native assembly logs report `assembly=1`, `cmov=2`; scalar controls report `assembly=0`. This is a deliberately selected native Windows reference, **not a measurement of native SWG runtime state**. The parent task is tracing runtime state separately.

All builds use `/O2 /Ob1 /fp:precise /EHsc /MT`. Each executable substitutes one math translation unit into the existing isolated candidate's 69 other DPVS object files. They do not link the newly integrated project DLL. Three source variants are copied unchanged from the prior investigation and hashed in `source-hashes.txt`: original math; held pairwise-double dot/exact-double-product raster repair; held pairwise-float dot/exact-double-product raster repair. PC64 selection and raw-mode logging change only the fixture. Both Win32 scalar and x64 scalar were run for every variant.

The complete build scripts, sources, compiler/link logs, executables, raw outputs and status records are retained in the original local experiment archive. This published excerpt bundles the report and comparison JSON, not that full archive. `analyze.py` produces `comparison.json`; it checks the row counts and that caller plane/camera bits are identical across comparisons.

## Broad suite: 38,880 rows per executable

Counts compare against original Win32 assembly under PC64. The Win32 scalar control gives exactly the same comparison counts as x64 for each variant.

| x64 implementation | Dot output bits differ | Dot sign/zero classifications differ | Raster rows differ | Other differences |
| --- | ---: | ---: | ---: | --- |
| Original scalar | 4,680 | 703 | 2 | 15 min/max signed-zero results |
| Held double repair | 0 | 0 | 0 | 15 min/max signed-zero results |
| Held float/PC24 repair | 4,368 | 199 | 0 | 15 min/max signed-zero results |

The original scalar exits 3 because of two exact-product raster oracle failures. The original Win32 assembly and both repaired scalar variants exit 0. Exit zero does not require identical dot sign: the pre-existing broad dot oracle is a magnitude/error-bound test; the separate comparison explicitly reports sign and zero changes.

These new 703 changes belong to this **PC64** run. The earlier PC53 experiment independently also had 703; the earlier PC24 experiment had 504. Equal counts do not merge their provenance.

## Caller-shaped suite: 11,978 rows per executable

There are 3,584 dot rows (512 normalized triangle planes × 7 camera offsets) and 8,394 raster rows. Plane/camera bit patterns are identical for each paired comparison. Raster scales are 8 (default half-resolution scale × 16) and float `16 * 0.45`, approximately 7.2.

| x64 implementation | Dot output bits differ | Dot sign/zero classifications differ | Raster rows differ |
| --- | ---: | ---: | ---: |
| Original scalar | 3,583 | 1,442 | 702, all at scale 7.2 |
| Held double repair | 1 | 0 | 0 |
| Held float/PC24 repair | 3,582 | 1,089 | 0 |

The remaining double-repair difference is preserved: triangle 299, offset index 4 produces Win32 `0xb2762091` versus x64 `0xb2762092`, a one-ULP difference with both values negative. This is direct evidence that the sampled pairwise-double replacement is **not universally bit-identical to PC64**. No classification difference occurs in these sampled caller inputs; that does not establish all near-boundary decisions are preserved.

All original Win32 reference variants produce identical rows, confirming the held source repairs did not change the assembly branch. Scalar repaired runs pass the raster oracle; original scalar runs report 702 raster oracle failures.

## Assessment and limits

The held double repair is substantially closer to the selected PC64 reference than either the original scalar code or the PC24-tuned repair in these two fixtures. The raster prediction holds for these inputs. There is already one measured numerical difference in the caller-shaped dot output, so no exact-equivalence claim is appropriate.

This comparison alone does not authorize choosing PC64 as the native client reference or promoting a repair. It does not test actual ground-scene visibility, live native Windows FPU state, alternate rounding/precision transitions, all invalid/overflow/NaN/subnormal inputs, or performance. The 15 min/max signed-zero differences remain visible in the report. No blanket epsilon was introduced. Production repairs remain held pending runtime interpretation and assessment.
