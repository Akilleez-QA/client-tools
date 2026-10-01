# Opt in to the development x64 Miles process boundary

Connect the real Audio bootstrap to the existing pipe facade and engine callback worker under `ClientMilesDevelopment=true`. Keep ordinary direct-Miles selection unchanged. The selected path retains template/cache dependencies through paired shutdown, verifies normalized module paths, and uses a windowless helper with normal-size command IO.

The property sheet isolates Debug-x64 clientAudio outputs and requires explicit matching pipe/worker libraries. The receipt-checked relink tool reuses real existing archives; it does not constitute a full source rebuild.

Dependency base: `6b94c184f4659da10cf067e7495d8655da6959ed`, the explicit joint prerequisite of [Miles build/Audio](https://github.com/Akilleez-QA/client-tools/commit/afe844818e86b24313a9e940d4723a02f7262ae8), [x64 native providers/link policy](https://github.com/Akilleez-QA/client-tools/commit/5292d6fd8d07cd1d8f93091e57b1ca468c7b5833), and [FileManifest ownership](https://github.com/Akilleez-QA/client-tools/commit/514498397a9ead2518ab11d5894a785ef877b82d). Those prerequisite changes are excluded from this review diff.

Production: 9 files, +195/-22; build tooling: 5 files, +270/-6; README: +28/-5 (Myers). Six source/build commits preserve the selected original added/removed lines; one documentation commit replaces historical diary hunks with scoped usage notes.

Existing integrated build/runtime observations remain pinned to the [original checkpoint](https://github.com/Akilleez-QA/client-tools/blob/a68ceb4280ca59af5317f3ad5c6de8a3e0a87314/tools/miles-bridge/README.md). Packaging checks verified exact selected changes and whitespace; no builds/tests/runtime were rerun. This branch has no CI workflow. A complete client still needs the separately packaged x64 source fixes and obsolete browser/capture build-input cleanup. Release selection and Bink rendering are outside this change; this is not standalone full-client qualification.
