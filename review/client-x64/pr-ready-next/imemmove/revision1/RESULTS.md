# imemmove qualification

The review head is `5219952f271ed7283b9e441dea761b462495b51c`, based on `94945103`. Production commit `9eadbbb` changes four files, +7/-7 lines: rename the int-length overload to `imemmove`, convert its delegation length to `size_t`, and update five int-count calls. The following test commit adds three files and 100 lines; their bytes are identical to the native-tested inputs. The production patch is unchanged by that commit.

## Real-header native matrix

| Checkout / ABI | Release | Debug |
|---|---|---|
| Candidate Win32 | 30/30 runtime checks | object compile passed |
| Candidate x64 | 30/30 runtime checks | object compile passed |
| Original Win32 | 30/30 runtime checks | object compile passed |
| Original x64 | expected C2668 compile rejection | expected C2668 compile rejection |

These are native VS2013 runs, using the actual `FirstSharedFoundation.h`, platform/types/memory/fatal headers and `Misc.h` exported from each named Git revision. No header guard is bypassed, no Fatal function is substituted and no vendor/engine binary is linked. The real Release header disables its own Debug checks. Debug builds compile only because exercising the engine's DebugFatal dependency would require additional genuine runtime integration.

The 30 runtime checks cover five valid buffer geometries through three call forms: int helper, exact CRT size_t function pointer, and ptrdiff_t expression. Each checks the returned destination pointer and all 32 buffer bytes against a separate pre-copy snapshot. Forward overlap, backward overlap, disjoint, same-address and zero-length cases use valid pointers. No negative length, invalid pointer, allocation stress, fault workload or old x64 executable ran.

The original x64 logs identify C2668 both in original Misc.h233 and at the ptrdiff_t expression. The negative-control runner only accepts a failed compile containing C2668 and memmove; other failures fail the aggregate. All eight expected matrix outcomes returned runner exit0. Fresh output directories are required; an existing-output negative control returned nonzero without modifying its prior sentinel file.

## Production callers

`CENSUS.md` and `caller-census.txt` identify the five renamed int-count calls and remaining first-party CRT calls. The helper retains its pointer assertions; it does not validate signed lengths. External STLport pointer-difference calls remain CRT calls. Their Debug-only pointer-assertion routing can change on Win32 after removal of the int overload; unchanged invalid-input behavior is not claimed.

All three exact candidate translation units (TCPQueue, Iff and Md5) compiled in Win32/x64 Debug/Release, using existing real project compiler metadata, candidate library headers first and PCH reuse disabled. Every v2 include trace selects the candidate Misc.h. Win32 logs contain no compiler warnings; x64 has one warning each in TCPQueue/Md5 and two in Iff. This is compile-only evidence, not caller runtime testing.

The v1 caller pass selected external development Misc.h for Md5/TCPQueue. That narrower, misbound result is preserved and superseded by the explicitly reordered candidate-header v2 run. Both recipes and raw logs remain.

**Dependency limit:** caller compilation still uses remaining genuine headers, SDK paths and project flags from the existing v1/v2 development checkouts. Only the candidate library subsets in `inputs.tar` and `caller-inputs.tar` were exported from this isolated branch. These compiles are not an independent complete branch build, a full x64 client link, or evidence that all external dependencies match upstream master. The standalone header/runtime matrix does not silently depend on those development checkouts.

## Reproduction and identities

The checkout tool accepts explicit `--checkout`, `--bits`, `--configuration` and fresh `--out`; see its README. `--baseline` selects the original int overload for an upstream checkout; `--expect-ambiguity` is restricted to baseline x64 and never executes it. Every unexpected compile/run/count or missing input fails nonzero.

`source-manifest.json` hashes all four production files and the three tools. Each native header result records compiler command, compiler/probe/runner/Misc hashes and every included-header hash. `native-text-v2.zip` contains the text-only complete packet (matrix, logs, command responses and metadata identities). No compiled object, executable or SDK asset is packaged. `native-text.zip` preserves the earlier caller snapshot. Test input tar files contain only actual repository source/header exports and authored probe code; they are local provenance inputs, not required binaries or additional production changes.

Delivery: authored and checked. Outcome: observed native valid-buffer Release checks and compile discrimination passed within the named scope. Required remaining observation: actual initialized-engine Debug and game caller runtime behavior, if claimed by a future integration change. Parent controls separate independent review and any commit/publication.
