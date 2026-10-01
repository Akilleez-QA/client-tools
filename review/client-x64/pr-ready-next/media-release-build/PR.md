# Build matching Release Miles/Bink development components

Add `--configuration Release` while retaining Debug defaults and output paths. Use the matching engine configuration and static CRT, isolate Release outputs, enable PipeBinkVideo for Release-x64, and name the selected game SwgClient_r. The project requires matching pipe/worker archives and isolated Audio/Graphics libraries.

Base: Bink game selection `abe067bcc70fffd397ff4de531943400c38a7caa`; this already includes the Miles selection and Bink host/session prerequisites. The original build commit is kept whole: 3 build files +30/-19, followed by README +27/-9 (Myers). There are no production C/C++ changes. The existing development relink tool remains Debug-only.

The [original checkpoint](https://github.com/Akilleez-QA/client-tools/commit/33efad160379912308171fbbb0e3cab54eddd523) records a full integrated Release-x64 rebuild with 0 errors and 3274 warnings, 20616 source/build inputs unchanged across the build, and strict Debug/Release host plus Release pipe/worker builds. These are recorded historical results, not a fresh exact-base build of this split branch.

Packaging verified the unchanged original build hunks and clean whitespace. No new builds/tests/runtime were run. Matching genuine providers and the separately enumerated full-client dependencies remain required; an archive existence check alone cannot prove its configuration or ABI. No SDK assets are included and no new runtime/fidelity claim is made.
