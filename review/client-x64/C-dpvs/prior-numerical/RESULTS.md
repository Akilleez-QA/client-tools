# Exact production-file candidate recheck

Native Windows v120 run `20260929-075041-626`. No production edits by this check.

The copied production `dpvsMath.cpp` has SHA-256 `81b7be9b2dd448e3c45643e80942016e8ee9e1b22dce63a138e3c0a19b8605c6`. Its bytes still matched the working source at comparison time. The fixtures include that file unchanged, compile x64, and link the existing isolated candidate's 69 other DPVS objects. This is not a full-client run or a test through the integrated project DLL.

Both build/link/run results are zero:

- Broad probe: 38,880 rows, zero oracle failures.
- Caller-shaped probe: 11,978 rows, zero raster oracle failures.

**Every numerical row is identical to the prior held double-repair x64 run.** Against the preserved native Win32 PC64 assembly reference, the broad suite differs only in 15 min/max signed-zero rows; dot and raster outputs match. The caller-shaped suite retains exactly one one-ULP dot difference, triangle 299 / offset 4 (`b2762091` versus `b2762092`), both negative. No sampled caller classification or raster difference remains.

Raw output, exact sources, hash, scripts, binaries, compiler/link logs, status records and `comparison.json` are retained. The original PC64 reference logs retain raw `fnstcw=037f` and assembly dispatch metadata. This confirms the exact production-file candidate reproduces the prior measured result; it does not expand the earlier fixture coverage or establish universal numerical/visibility equivalence.
