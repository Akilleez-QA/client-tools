# Dependency output ownership candidate

Implemented only in `/home/akilleez/Work/swg-source/client-deps-owner-review`, base `6776d2054410e7bb3b986161070b34280cf4b682`. Remote inspected locally: `https://github.com/Akilleez-QA/client-tools.git`. No main-checkout edits, commits, pushes, PRs, upstream operations, native jobs, VM access, or Q/R use. Browser/TCG/normal voice deprecations and all vendor/runtime implementation remain untouched.

## Finding and repair

Original `tools/build-client-deps/build.py:66` checked owner equality only when `owner.json` existed; line 69 then wrote an owner unconditionally. Consequently an absent owner adopted existing output, and a matching owner was needlessly rewritten. This is a source/control-flow finding, not a renderer-runtime finding.

Candidate `tools/build-client-deps/build.py:27` adds `ensure_owner`, called under the existing lock at line 87 before `build` at line 88. Only absence permits considering adoption, and every directory entry except the caller's `.build-lock` blocks adoption. Existing unowned files and directories are preserved. Existing invalid JSON, incomplete owner objects, unreadable records and differing owners fail. A matching owner returns without rewriting anything, retaining retry of same-owner interrupted builds.

New ownership uses exclusive creation of `owner.pending`, writes JSON, flushes and fsyncs the file, closes it, then replaces `owner.json` in the same directory. Failed writes/publication propagate and prevent build entry. Abandoned staging files block later unowned adoption; there is deliberately no automatic cleanup of them. README lines 17 and 19 document ownership/retry policy and bounded tests. The production change is 21 added helper lines and replacement of the original four-line owner block with one call.

## Independent challenge of conclusions

- A directory containing only an empty subdirectory is not empty; tested rejection. Hidden entries and pending files also reject. A dangling `owner.json` symlink is discovered by directory enumeration after its read reports absence; tested rejection without unlinking it.
- An incomplete owner must not become adoptable: empty/truncated JSON and valid JSON with incomplete/wrong structure all reject unchanged. Partial staging writes, fsync failure and rename failure also reject and block retry without a valid owner.
- Requiring a completion manifest would prevent valid interrupted-build recovery. The helper deliberately accepts an exact matching owner with partial outputs and missing completion manifest; the unchanged build function remains responsible for cache verification and rebuilding.
- Merely extracting a helper would not prove entry ordering. Tests call actual `main()`, parsing arguments, taking/releasing its directory lock and checking ownership before a mocked build boundary. Both unowned output and publication failure prevent that boundary from being reached. A simulated boundary failure leaves valid ownership and allows retry.
- This retains the existing cooperative `.build-lock` trust model. It is not protection against a separate process ignoring the lock, malicious symlink replacement, or forged owner records. Existing readable matching owner symlinks are not newly forbidden. No new crash/power-loss durability claim is made: the staged file is fsynced, but directory metadata is not fsynced. Native Windows filesystem behavior and concurrent lock waiting were not rerun.
- Changing the builder hash intentionally invalidates prior cache identity; source inspection confirms the original identity logic, compiler recipes and publication of dependency outputs are unchanged. No cache-reuse/runtime claim follows from this inspection.

## Existing evidence and source identities

Read, without executing, these existing records under `/home/akilleez/Work/client-wire-validation/allocator-next/`:

- `build-client-deps-proposal.md`: original dependency identity/offline/provider scope and limits. It is a proposal, not the final command-line interface.
- `stlport-build-plan.md`: original bundled-source recipe and corrections; it explicitly separates compilation from runtime evidence.
- `renderer-integration-results.md`: historical integration summary and limits.
- `renderer-integration-worker-v4/candidate-hashes.json`: historical builder/README identities match this checkout's original bytes exactly.
- `test-deps-builder.py` and `deps-builder-tests-v2/results.json`: historical recorded native parallel/cache/header-failure/archive/owner-mismatch checks. Those checks did not test missing-owner adoption of nonempty output. They were not rerun or reinterpreted as candidate validation.

Also read `/home/akilleez/Work/client-wire-validation/vendor-options/primary-research.md` for original-provider/fidelity limits. No external research links were fetched or used to make new API claims.

`source-identities.json` preserves base revision, full checkout path, original/candidate changed-file SHA256 values, hashes for the 450 local source/header inputs selected by the builder, JPEG archive pin, unchanged renderer property-sheet hash, and exact paths/hashes of the six allocator evidence records above. The external JPEG archive and Windows compiler/include trees were not read anew; their existing identity collection is unchanged. `original/` saves the base builder and README; `candidate/` saves all three candidate files.

The `_STLP_DONT_FORCE_MSVC_LIB_NAME` claim is present in external `allocator-next/renderer-integration-results.md` under Current native results, and the macro is present at `tools/build-client-deps/renderer-deps.props:11`. Repository search found no occurrence in the bundled `src/external/3rd/library/stlport453` tree, nor in the owned builder/README. Thus the claimed bundled macro behavior is not supported by this source inspection. The external report and property sheet are outside the authorized edit scope and remain untouched. Recorded historical link observations alone do not establish that this macro caused them.

## Validation and limits

`python -B -m unittest discover -s tools/build-client-deps/tests -v`: **12 passed, 0 skipped**, exit 0 on Linux Python 3.14.7. First local test iterations exposed test-harness errors (duplicate Mock name argument; overbroad Path.open interception), corrected before the passing run. There were no native failure reproductions. Tests use disposable local temporary files and controlled Python exception injection.

Saved `candidate.patch` passed `git apply --check`, then was applied to fresh temporary copies of the base files. All three applied-file hashes matched the candidate hashes; all 12 tests passed there too. `git diff --check` passed. Exact final test output: `tests.log`; structured results: `test-results.json`.

Function tests execute the real ownership helper. Entry tests substitute only the module-local Windows platform gate, expected hash for an inert archive fixture, and the native build boundary; the fixture is never extracted or executed. These are ownership/control-flow tests, not a fake compiler, successful library build, renderer link, rendered-frame result, JPEG behavior check or original SWG runtime fidelity proof. Python 3.8 and Windows execution were not tested. The existing native VM was not used.

Changed-file SHA256 values (also `changed-file-sha256.json`):

```
0cd163f465c3d1f7f36a8b249658a4df3200519beff1627d31be5005b0b5ecd7  tools/build-client-deps/build.py
10c02cc5efb585efebc0cc9d8f3a3c7a2a25aba4797cf0530a93966eff24cda3  tools/build-client-deps/README.md
3ecffac855e57ef3f45266612738d9746203ba8c19c39f43a7c37bf94df072b9  tools/build-client-deps/tests/test_owner.py
```
