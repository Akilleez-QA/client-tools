# Renderer dependency integration candidate — uncommitted

Exact eight candidate file hashes in `renderer-integration-worker-v4/candidate-hashes.json` match the Linux working tree after native verification. No product VM checkout or its outputs were changed. No commits/pushes.

## Candidate scope

- New `tools/build-client-deps`: native v120 builder, renderer-only property sheet, README.
- Existing shared x64 sheet imports that sheet only for the three renderers.
- Three renderer project files: Debug/Release x64 provider names/paths only. Win32 conditioned XML groups compare exactly with HEAD.
- Central renderer header: `_M_X64` selects genuine June2010 DxErr API; Win32 original remains.

No second x64 generator. No binaries/vendor packages/scratch paths in production files. Existing DllExport ProjectReference stays.

## Current native results

`renderer-integration-worker-v4/results.json`: Direct3d9, ffp, vsps × Debug/Release all compile/link0, using the exact candidate builder/props/project changes. Private actual DllExport project copies are built through preserved ProjectReference semantics before renderers; no prebuilt DllExport injection in v4. Source include locations and all outputs are relocated solely for isolation. Scratch TargetPath/name overrides produce MSB8012 warnings; they do not establish production deployment correctness.

`/VERBOSE:LIB` logs show generated jpeg.lib/stlport.lib; all six logs have no old stlport_vc71 name, and no bundled x86 library directories. Actual Debug renderer object `/directives` dump has no old STLport request. `_STLP_DONT_FORCE_MSVC_LIB_NAME` disables only that legacy automatic naming for x64. Real Windows SDK and DxErr providers remain, with inherited Windows system libs intact.

Incremental test copies JPEG headers privately (no product mutation), changes one public header comment, and rebuilds all three Debug renderers. First rebuild regenerates both libraries; next two verify cache. All three rerun link and change the final DLL timestamp, exit0. `incremental-results.json` records this bounded header-to-library-to-consumer rebuild.

`deps-builder-tests-v2/results.json`: two simultaneous clean invocations produce one actual build and one verified cache hit, both0. Public header content mutation invalidates cache and rebuilds. A deliberate header `#error` returns failure while preserving the prior completed libraries and manifest. Bad archive hash is rejected even when cache exists; cross-checkout output reuse is rejected. First test-driver v1 failed before building because cmd mklink treated a forward-slash path as an option; v2 uses Windows Path spelling.

Missing SDK run reports the intended DXSDK_DIR diagnostic before renderer compilation. The independent DllExport reference may compile before the renderer PrepareForBuild target; it does not require DxErr. This is not a promise of zero build activity on configuration failure.

## Critic findings and fixes

- MSBuild12 lacks EnsureTrailingSlash: v2 failure independently observed/preserved. Current sheet derives an internal path using an ordinary separator, never writes back to an immutable command-line property.
- Earlier v1 failed because overriding SwgClientDepsDir prevented in-place normalization and concatenated Debugstlport.lib. Separate derived path fixes it.
- Legacy STLport pragma and old search paths were real: current candidate suppresses the pragma with upstream's configuration macro and removes those x64 renderer directories. Provider tracing above supplies actual evidence.
- Cache identity covers source/public header/builder content, actual compiler INCLUDE tree content, compiler executable/frontend DLL content and output library hashes. CRT libraries are selected later by the consumer link, not embedded in these object archives.
- Cache is explicitly private to one checkout/platform/configuration, enforced by owner.json. It is not a concurrent cross-checkout immutable artifact store. Inputs must not be edited during active builds. Lock protects dependency publication; bounded waiting supports same-input parallel targets. Manifest publishes last; a failed build blocks Link.

## Limits

This proves isolated actual project/reference builds, the sampled dependency mutation/incremental behavior, and fault handling. It does not establish a full parallel solution build, production deploy/copy behavior, a new Win32 binary regression build after this candidate, screenshot runtime output, DLL allocation lifecycle or Direct3D device creation. Win32 source/XML paths remain unchanged by inspection. Earlier JPEG ABI/sample and 39-code DxErr results are documented in vendor-source-results.md; do not generalize them to every codec path or HRESULT.
