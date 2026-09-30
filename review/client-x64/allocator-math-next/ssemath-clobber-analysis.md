# Native SseMath register-lifetime contradiction

Evidence read: `Release-stock-disassembly-v2.txt` and `Debug-stock-disassembly-v2.txt`, dumpbin 12.00.40629 production.obj observations from C:/ssemath-next-v3. This is the stock TU, not the intrinsic candidate. Parent controls binary identity and execution; this is a source/disassembly critic, not a separate native rerun.

## Confirmed instruction chain

Release `rotateScale_l2p` and `rotateTranslateScale_l2p`: offset 0x08 MOVAPS loads transform row0 into xmm0. Offsets 0x16, 0x22 and 0x2f MOVSS subsequently load source x, y and z into xmm0. The memory-source MOVSS clears the upper lanes. Offset 0x60 MULPS xmm3,xmm0 therefore multiplies the source vector by [source.z,0,0,0], not by row0. The position phase of both skin functions has the same sequence. The normal phase overwrites xmm0 again with sourceNormal.z before its MULPS (skinAdd offset0x119 and0x139). The observed X is consequently source.x*source.z*scale, rather than the intended affine first-row result. This agrees exactly with the finite sample recorded earlier.

Debug is independently broken differently: its source x/y/z assignments use integer registers, but the scratch w=1 assignment loads 1.0 through xmm0 at offset0x79. `rotateScale` loads 0.0 at the same offset. MULPS at0xa4 uses [1,0,0,0] or [0,0,0,0]. The second skin phase reloads1.0 at0x263, then consumes it at0x27d. Neither Debug nor Release preserves the register's assumed cross-block lifetime.

This establishes a legacy mixed-inline-assembly/C++ register-lifetime defect for the inspected native v120 builds. It is distinct from x64 addition reassociation or x87 precision. Source comments that say rows survive are not a contract with compiler-generated code between asm blocks. Other residual differences, flags, NaN payloads and rounding still need separate assessment; this finding does not bless the entire intrinsic candidate.

## Minimal actual-TU discriminator

`ssemath-clobber-probe.cpp` uses diagonal(2,3,4), translation(10,20,30), position(2,3,5), normal(7,11,13), weight0.5 under nearest/masked exceptions. No large range or inexact input is needed. Predicted values:

| output | intended row arithmetic/x64 candidate | observed-code prediction Release Win32 | observed-code prediction Debug Win32 |
|---|---|---|---|
| translate | (7,14.5,25) | (5,14.5,25) | (1,14.5,25) |
| rotate | (2,4.5,10) | (5,4.5,10) | (0,4.5,10) |
| skin position | (7,14.5,25) | (5,14.5,25) | (1,14.5,25) |
| skin normal | (7,16.5,26) | (45.5,16.5,26) | (3.5,16.5,26) |
| add position, initial(1,2,3) | (8,16.5,28) | (6,16.5,28) | (2,16.5,28) |
| add normal, initial(4,5,6) | (11,21.5,32) | (49.5,21.5,32) | (7.5,21.5,32) |

The probe prints bits and exits zero for an observation, never claiming equality. Run it with actual stock Debug/Release and x64 candidate production.obj plus the same genuine link dependencies. A further causal control is a diagnostic copy of stock with each matrix/scale load moved into the assembly block that consumes it, after scratch preparation, reloading again for normal; preserve the unmodified stock alongside it. Such a control is not a proposed unreviewed Win32 production change.

## Caller boundary

Recursive source search for all four arithmetic method names found no uses outside SseMath.cpp/.h in this checkout. Searches for SseMath:: show only canDoSseMath callers in Transform.cpp and SoftwareBlendSkeletalShaderPrimitive.cpp. Therefore no gameplay failure is established for these four APIs, and neither Transform's own matrix assembly nor skeletal's hard-vertex assembly is implicated by this result. Link-map/disassembly retention and representative native client scenes remain distinct checks. Do not emulate the bug on x64 by default; also do not silently change Win32 under a migration claim. Keep a separate compatibility decision with the evidence attached.

## Authored diagnostic control

`diagnostic-register-reload-SseMath.cpp` is generated from the saved stock file and explicitly is NOT a stock reference. Its manifest records both SHA256 digests. At all six `mulps xmm3,xmm0` blocks it reloads the three matrix rows and the scale immediately before consuming them, using eax without disturbing the ebx scratch base. No C++ runs between these reloads and the packed multiplies. All original global scratch, output scalar expressions and fourth-lane calculations remain. This specifically tests the register-clobber hypothesis; it does not repair scratch concurrency. The x64 candidate's local scratch avoids the original shared-global race but that is not a tested concurrent-behavior claim.

Fourth-lane flags and optimizer elimination remain separate: the normal uses w=1 and drops that result lane, while rotate uses w=0. A compiler may omit unused intrinsic lanes. Even if the register-reload reference agrees on finite values, compare MXCSR and retain differences rather than treating them as equal. All production source stayed unchanged while authoring this control.

## Native observations collected

`C:/ssemath-clobber-v1-agent` reused the production objects from the diagnostic matrix, compiled the tiny probe with their recorded v120 flags, and linked actual objects/CRT without symbol stand-ins. All six executions completed. Local `ssemath-clobber-v1-agent/prediction-check.json` confirms every printed value exactly matches the prospective table above, binding each log digest and production-object digest. The Win32 candidate means the untouched Win32 branch of the candidate file, not the corrected reload control.

`reload-control-v1-results.json` and its Debug/Release comparison JSONs contain the separate 33280-case control matrix per build. Categories 0 (caller-shaped inputs), 1 (bounded finite), 2 (subnormal), 3 (extreme), and 5 (discarded lane) have no recorded value or MXCSR differences between the diagnostic Win32 reload control and x64 candidate in either configuration. Category4 exceptional values differ: Debug3156 records/9699 value words; Release713 records/1650 value words. MXCSR words match. These are recorded exceptional differences, not dismissed as equivalent NaNs.

The driver returns nonzero because its inherited unchanged-Win32 comparison sees the diagnostic reload control differs from the original. That is expected for the experiment but remains its literal outcome; the original stock-versus-candidate failure packet is intact. Finite intended-arithmetic agreement does not imply stock behavior preservation, thread-safety proof, exceptional equivalence or gameplay coverage.
