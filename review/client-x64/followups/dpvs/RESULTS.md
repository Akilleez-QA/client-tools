# Fresh native DPVS reproduction

Tested commit: `ebce07521eba3b4c92eccf5aaf3bdcb3d6f475c4` (C2 `14005646` plus test tooling only).
Git archive SHA-256: `0671ca8d1a3d18fe12ee4990390f74240c85627a99e48b704cd37c00bbb4683c`.

The new runner built all DLLs, all public-interface probe executables and all
numerical probe executables from the committed archive, using VS2013/v120 on
native Windows. No prior project outputs, object files or executable fixtures
were reused. The run records compiler logs, explicit process exit statuses,
archive provenance and production/harness SHA-256 manifests. Independently
compared all 165 manifest entries against the committed Git objects: exact match.

| Build | Build exit | Stress | Fixed-cost occlusion |
| --- | --- | --- | --- |
| Win32 Release | 0 | 192/192 | 64/64 |
| Win32 Debug | 0 | 192/192 | 64/64 |
| x64 Release | 0 | 192/192 | 64/64 |
| x64 Debug | 0 | 192/192 | 64/64 |

Every runtime probe exit was zero. The verifier checks sentinel visibility,
balanced callbacks, unique/in-range visible identifiers, exact expected occlusion
mask, write counts and complete sequential frame/query records.

Fresh Win32 PC64 assembly versus fresh x64 scalar probes:

- 38,880 broad records: 15 min/max signed-zero differences, no other differences.
- 11,978 caller-shaped records (3,584 dot, 8,394 raster): one negative dot value
  differing by one ULP; zero sign/zero classification or raster differences.
- Win32 raw control word `037f` and assembly dispatch were verified. x64 scalar
  dispatch and all numerical process exits were verified.

A fresh stock `949451032647e45e42c3aaef3f41b132c8af36e3` Win32 Release DLL was
rebuilt at the same absolute path. Complete normalized DLL equality passed.
Normalization is limited to parsed timestamps, CodeView GUID/age and Win32 path
capitalization, and one source-defined build-time string. Raw code sections
remain equal; no instruction differences were discarded.

Standalone `verify.py` passed on Windows and on the Linux host using the exported
logs and DLLs. This packet's `hardened/` directory contains text logs and manifests. Generated
binaries are retained locally and can be rebuilt with the committed runner;
they are not bundled in this evidence branch.

Negative controls:

- Actual C1 (`7b5c73da8`) source was rebuilt with the same fixtures. The fresh x64
  numerical probe returned 3 (`RESULT rows=38880 failures=2`), and the runner
  returned 1. The C1 scalar path cannot pass the C2 acceptance checks.
- Validator mutation tests rejected a missing stress query, extra invalid query,
  wrong visible mask, truncated numerical rows, changed dot classification,
  nonzero/missing execution status and a changed DLL instruction byte.

No production changes, no self-hosted runner registration and no hosted CI job
were added. Hosted v120 availability remains a separate prerequisite. This is
bounded regression evidence, not full-client x64 linking, native Direct3D FPU
tracing, arbitrary allocation safety or gameplay acceptance. The known FPU setter
coupling and unisolated integer-path comparisons remain documented in the harness.

The final commit also hardens PE normalization against executable metadata spans.
Eight synthetic controls passed on native Windows and the host, including forged
debug-directory/CodeView pointers into instructions, writable/executable metadata,
virtual-only ranges and truncation. The complete four-configuration matrix and
fresh baseline comparison were rerun after this hardening on the committed head.
Archive input was extracted into an empty directory; no source template overlay
was used. All 165 production/fixture/harness hashes matched the exact Git commit.
