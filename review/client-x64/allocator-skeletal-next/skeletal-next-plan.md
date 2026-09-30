# Skeletal hard-vertex x64 candidate — prospective plan

Scope: only SoftwareBlendSkeletalShaderPrimitive.cpp. Parent controls native VM tests and commits. The 21 compiler diagnostics originate in its two `_asm` blocks; no corresponding server file exists. User intent is an actual x64 client with unchanged features; compile success alone is not acceptance. Existing context waives redundant clarification. Win32 assembly must remain verbatim.

Observation: hard vertices use only their first transform, aligned column-major 4x4 PoseModelTransform, 36-byte SourceVertex and 16-byte Dot3Vector. Work structure contains pointers and grows on x64. Assembly position grouping is `(c0*x+c1*y)+(c2*z+c3)`, normal/dot3 grouping is `(c0*x+c1*y)+c2*z`. Bounds use MINPS/MAXPS with old bound as second operand. Selected MXCSR exception masks and FTZ are enabled inside the loop then full original CSR restored. Output writes are exactly 24 bytes position/normal, optionally 16 bytes dot3 including flip; caller stride can be larger. Prefetch is a hint only, with no valid basis for a performance equivalence claim.

Research gate, 2026-09-30: queried Microsoft intrinsics availability and Intel MINPS/MAXPS/FTZ behavior. Microsoft x64 intrinsic list confirms packed load/add/multiply/min/max and MXCSR support; Intel instruction reference confirms the second operand matters for NaNs and signed zero. Sources: https://learn.microsoft.com/en-us/cpp/intrinsics/x64-amd64-intrinsics-list ; https://cdrdv2-public.intel.com/774492/325383-sdm-vol-2abcd.pdf ; https://www.intel.com/content/www/us/en/docs/dpcpp-cpp-compiler/developer-guide-reference/2024-2/set-the-ftz-and-daz-flags.html . These support semantics, not v120 code generation or game-level equivalence. Existing scalar fallback uses different association/bounds and cannot be assumed identical.

Exactly 20 materially distinct paths considered before selection:
1. Instruction-shaped x64 SSE intrinsics.
2. Compile existing scalar fallback and measure it as a rival.
3. External MASM x64 kernels.
4. Shared portable scalar algorithm with explicit intermediate rounding.
5. Dispatch both ABIs to intrinsics (would change Win32).
6. Defer kernels and leave x64 build blocked.
7. Use DirectXMath adapter (new dependency/behavior).
8. GPU skinning replacement (architectural scope change).
9. Preserve two duplicated intrinsic kernels.
10. Share a templated hard/dot3 intrinsic loop.
11. Share only packed-vector arithmetic helpers.
12. First establish input layout/stride contracts without source edits.
13. Native actual-TU finite differential corpus.
14. Native adversarial nonfinite/denormal corpus with differences retained.
15. End-to-end representative animated scene comparison.
16. Page-guard and output-sentinel memory probe.
17. MXCSR save/restore and rounding-mode probe.
18. Disassembly review for packed order and eliminated lanes.
19. Remove prefetch hints and measure performance separately.
20. Preserve prefetch schedule using pointer-width arithmetic.

Decision: combine 1, 10, 12–18 and 20. Keep x86 assembly untouched, select x64 with _M_X64. Typed source/transform/output pointers avoid hard-coded pointer-width offsets. Preserve packed association, second-operand bounds, all four lanes and full CSR restoration. Native expected result is exact finite output equality, intact sentinels and restored CSR; exceptional differences are recorded separately. Reversal condition: any finite mismatch, missing real-TU binding, unexpected memory write, or failed state restore. No proof from source review alone. Parallel parent/Transform agent owns neighboring math; this agent owns this file and diagnostic append probe only.
