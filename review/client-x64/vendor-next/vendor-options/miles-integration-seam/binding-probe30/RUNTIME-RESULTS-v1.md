# Binding probe 30: one original-DLL run

The first and only authorized run passed, exit 0. Actual v120 x86 probe against original DLL SHA-256 `0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe`, under the private Wine prefix and owned null sink. No repairs, retuning or reruns. No playback, failed/unbound-state query, page protection or engine execution.

| Bind | Raw S32 result | Total ms queried | Current ms |
|---|---:|---:|---:|
| A1 | 1 | 1000 | 0 |
| B1 | 1 | 2000 | 0 |
| A2 | 1 | 1000 | 0 |
| F, unsupported tag 0x7fff | 0 | not queried | not queried |
| B2 after F | 1 | 2000 | 0 |

All five calls used sample identity `008D3360`. Each successful PCM query was followed by end; one final release and shutdown returned. All images and suffixes remained alive through shutdown.

F's immediately copied last-error text was `Unsupported wave file format.` (29 bytes, nonnull and terminated). B2 succeeded but returned the same stale error text. This directly demonstrates why the bind result, not nonempty last-error text alone, decides success.

Observed cleanup: both owned process handles reaped, prefix-specific wineserver kill/wait returned, owned null sink absent, no cleanup errors, default sink/source unchanged, staged executable/DLL/plugin bytes unchanged. Raw probe output and durable result record are retained privately and copied into the source/text-only curated directory.

Evidence scope: this characterizes repeated same-handle PCM binding and known-valid recovery after this particular failed bind for the pinned original DLL/environment. It does not query the state immediately after F and therefore cannot prove old-binding preservation or clearing. Because every buffer remains alive, it provides no obsolete/failed image or suffix retirement boundary, no asynchronous safety guarantee, no compressed-format generalization and no playback/game fidelity approval.

Build provenance remains limited: one successful native compile+link with stable pinned source/SDK/import bytes before/after; actual system headers were hashed after compilation only.

## Durable identities

- source manifest: `491d0e204988dfc0a4e32583d74e6f2a513dce675e169bba71d63f7258e7e582`
- source archive: `4b32fa329b878630976ee6ff5c09cbb981da70376ee03a37ba21c135e5fef631`
- native receipt: `42303cb6f5fb9498a51be97e2e56e3ba78b1603248198f5bde0943ec36caa2b9`
- actual private PE: `362ae3248b3f8d6d6e287aa6fe6a53b9c8959a1cdec611bfb5e6acfa27eaa49d`
- runtime recipe manifest: `17d635166bc16fb65ee03b0c60714517db5ed3b58e36a8b284736d3a89afe0dd`
- raw trace: `4a4612a45b7822bdf5fefc79874688e606a4802883d03971899d148e4fefc9dc`
- runtime results: `0d9911279fb661ae934bfa6a95731d5c599945a2a28acabe1f3bb000f82b7083`
- curated evidence manifest: `8377a31d949e91acd3b401bb7180f3eec54cc32417e766eaca67daf0660ef732`

Private run: `/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/binding-probe30/runtime-recipe-v1/private-run-959d3f4e`. Curated directory: `/home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/binding-probe30/curated-evidence-v1`. No executable, DLL, SDK header, import library or game asset was copied into curated evidence. The downloaded PE remains private.
