# LoginClusterStatus fixture handoff — 2026-09-30

Implemented and executed nine new bounded wire fixtures in the disposable detached checkout
`/home/akilleez/Work/swg-source/client-login-wire-probe`, based on
`d0fea5bc79fc0ee31cd38fdc9122dbb18574f3c0`. Only five files under
`tools/test-wire-compatibility` changed. HEAD and recorded production source hashes are unchanged.
No commit, PR, push, production serializer edit, main checkout write, VM access or installer action.

## Observed results

| Run | Runtime PASS | Width check | FAIL | SKIP notices | ABSENT notices | Runner/runtime exit | Total |
|---|---:|---:|---:|---:|---:|---|---|
| Original `94945103` Win32 oracle | 55 | 1 | 0 | 1 | 1 | 0 / 0 | 56/56 |
| Candidate Win32 | 58 | 1 | 0 | 2 | 0 | 0 / 0 | 59/59 |
| Candidate Win64 | 65 | 1 | 0 | 0 | 0 | 0 / 0 | 66/66 |
| Private native-size encoder control Win32 | 58 | 1 | 0 | 2 | 0 | 0 / 0 | 59/59 |
| Private native-size encoder control Win64 | 62 | 1 | 3 | 0 | 0 | 1 / 1 | 63 pass, 3 fail |

The three intentional failures are first element encode, second element encode, and combined
message encode. Each uses real serializers with only the private negative-control field write
changed. Stock literals are always decode inputs; no corrupted array count or string length is
fed to the decoder. The mutant writes `onlinePlayerLimit` as native `size_t` (4/8 bytes), retaining
the original decoder. This is a synthetic discriminator, not adopted PR21 code.

Exact SKIP text and the single allowed stock ABSENT notice are enforced. A separate replay of
recorded raw runtime output through the actual verdict block passed 14/14 enforcement cases,
including missing fixture output, malformed/unknown/duplicate absence, wrong/missing/duplicate
skip, explicit failure, NOT RUN and nonzero exit. This replay is verdict testing, not additional
serializer runtime evidence (`enforcement.log`, `check-enforcement.py`).

## Oracle and boundary

Original `949451032647e45e42c3aaef3f41b132c8af36e3` shared sources were exported by `git archive`
to `oracle94945103`; no extracted historical candidate was treated as authoritative. Literal
bytes were independently transcribed from its LoginClusterStatus/Archive/AutoByteStream source.
Its actual Win32 implementation then passed the literals. Candidate output was not used to
generate expected bytes. The source evidence and initial SHA256 manifests preserve this lineage.

Records are 50 and 53 bytes: 41 fixed bytes plus addresses `alpha.swg` and `b.example:42`.
The bounded message is 109 bytes: u16 registered-member count 1, u32 array count 2, both records.
The empty bounded message is six bytes. All 14 decoded fields are checked, including population
-1/INT32_MAX, timezone INT32_MIN/-3600, high unsigned IDs/limits, port boundaries, enum endpoints,
and opposing boolean flags. Exact exhausted iterators and an untouched three-byte sentinel are
checked. List size is at most two. Existing string escape-boundary fixtures remain in the suite;
LoginClusterStatus itself does not test giant addresses or malformed input.

**This proves bounded serializer compatibility, not a complete packet.** Real LoginClusterStatus
constructors register the real AutoArray; real AutoByteStream and record Archive put/get execute.
The explicitly documented GameNetworkMessage constructor shim omits command CRC registration,
and MessageBase initializes type to zero. No serializer is stubbed. Actual command header, real
base construction, transport framing, dispatch, live server/client interoperability and a proposed
12-field legacy variant remain outside this proof.

## PR21 observation

The available local non-git PR21 snapshot retains the stock LoginClusterStatus widths and
signedness. Its admin/secret fallback checks remaining bytes in the whole iterator, so a 12-field
multi-record variant could consume next-record ID bytes as flags. That is a boundary/versioning
issue by source inspection, not a demonstrated LoginClusterStatus width defect. No runtime claim
about such a server format is made. See `pr21-observation.md` and the hashed source copy.

## Execution and actual compilation

Tool versions: Clang 22.1.8, MinGW GCC 16.2.0, with full version outputs in `tool-versions.json`.
All Win32 runs use `--wine-arch win64` with `WINEPREFIX32=/home/akilleez/.wine-swg64` to run real
32-bit PE executables using existing WoW64 support. Win64 uses that existing default prefix.

Each candidate/mutant build compiled 27 linked translation units and five syntax-only units.
The stock oracle compiled 26 linked units (no ArchiveCount/count_sites) plus five syntax-only
units. `compiled-TUs.json` in each run directory lists exact paths, SHA256, modes and exits.
`commands-<bits>.jsonl` preserves all actual compiler/linker/Wine commands, full captured raw
stdout/stderr and exits. `staged-source-<bits>.json` hashes shared sources after documented syntax
shims; it is input identity, not a claim that every file ran. The linked fresh executables are retained.

The new production TU is `sharedNetworkMessages/src/shared/clientLoginServer/LoginClusterStatus.cpp`.
Its inline field serializers reside in LoginClusterStatus.h; actual array and primitive serializers
come from AutoByteStream.h and Archive.h. The new harness TU is `login_cluster.cpp`. Existing
serializers, runtime glue and syntax-only coverage are preserved. Compiler/linker exits were zero
for every completed matrix run; no compile-only result is counted as a runtime fixture.

Reproduce from the authored checkout:

```sh
WINEPREFIX32=/home/akilleez/.wine-swg64 python3 tools/test-wire-compatibility/run.py --bits 32 --wine-arch win64 --require-current-coverage --artifacts NEW_CANDIDATE32_DIR
python3 tools/test-wire-compatibility/run.py --bits 64 --require-current-coverage --artifacts NEW_CANDIDATE64_DIR
WINEPREFIX32=/home/akilleez/.wine-swg64 python3 tools/test-wire-compatibility/run.py --bits 32 --wine-arch win64 --root /home/akilleez/Work/client-wire-validation/login-cluster-next/oracle94945103 --artifacts NEW_ORACLE32_DIR
```

The control runs use `--root .../login-cluster-next/wrong-width` with the corresponding ABI flags.
Use fresh artifact directories so earlier evidence is preserved.

## Failures preserved and resolved

Initial builds accidentally listed LoginClusterStatus.cpp twice; linking rejected duplicate
symbols. The duplicate OPTIONAL_SOURCES entry was removed, with raw failed attempts retained as
`*-initial-link-failure`. An initial int64 member-width control did not compile because Archive
has no matching int64 overload; `wrong64-int64-compile-rejected` retains it. That attempt is not
runtime evidence. The later safe encode-only native-size control compiled and produced the
predeclared Win32-pass/Win64-three-failure outcome. No unresolved environment blocker remains.

## Parent review deliverable

- `login-cluster-fixtures.patch`: complete patch including the new file.
- `commit-ready-manifest.json`: base revision, exact five-file hashes and patch hash.
- `patch-apply-check.txt`: clean base export accepted `git apply --check`; applied files matched
  the authored files byte for byte, entirely in the evidence directory.
- `results.json`, raw `.log`/`.exit` files and per-run compiler artifacts: observations.
- `initial-*`, `source-evidence`, `final-status.txt`, `diff-check.txt`: scope and identity evidence.
- `critic-review.md`: independent opening source review and subsequent fixture critique;
  same model/source family, not independent runtime corroboration.

`delivery_state`: built and checked, uncommitted.
`outcome_state`: passed for the declared bounded fixture surface; negative control rejected as predicted.
`highest_justified_claim`: stock-source Win32 literals and candidate Win32/Win64 serializers agree
for these bounded cases; the suite detects an injected native-width field-write regression.
`required_runtime_observation`: none for this bounded task. Complete packet/live-client acceptance
would require a separately authorized integration test.
`who_controls_next_test`: parent/user for review and any future x64 integration or upstream proposal.
