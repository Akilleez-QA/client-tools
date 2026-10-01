# Exact-candidate Win32 production consumers

Candidate `3b00af6296e9d3631cd3e068d4a0c31499a9756a`, based on upstream
`949451032647e45e42c3aaef3f41b132c8af36e3`; production patch remains four files,
+7/−7. This supplements the existing header regression and strict negative controls.

A complete Git archive of the candidate was built with native VS2013 v120,
using its original Release|Win32 projects and repository dependencies. All
20,505 archive files were checked against the candidate Git blobs and the build
manifest; the recorded inputs matched before and after the build. No source,
header or project-configuration substitutes were used. Parent verification
inspected the worker's raw evidence; it was not a second native build.

| Actual library | Changed caller compiled | Errors | Warnings |
|---|---|---:|---:|
| sharedFoundation | Md5.cpp | 0 | 0 |
| sharedFile | Iff.cpp | 0 | 0 |
| clientGame | TCPQueue.cpp | 0 | 5 |

The five clientGame warnings are one Game.cpp C4067, two deprecated networking
API C4996 warnings, and two LNK4221 empty-object warnings. They remain in the
raw logs. This is library build coverage, not a full client link or runtime test.

## Reproduction

Use the complete candidate checkout, VS2013 v120 and its normal SDK installation.
For each of the three projects below, run the native MSBuild 12 executable with
`/t:Build /p:Configuration=Release /p:Platform=Win32 /p:BuildProjectReferences=false
/nologo /v:normal`, plus fresh, separate `/p:OutDir=<output>/` and
`/p:IntDir=<output>/` values. Do not reuse object files from another checkout.

- `src/engine/shared/library/sharedFoundation/build/win32/sharedFoundation.vcxproj`
- `src/engine/shared/library/sharedFile/build/win32/sharedFile.vcxproj`
- `src/engine/client/library/clientGame/build/win32/clientGame.vcxproj`

The exact executed command arrays and unedited native logs are in
[native-text.zip](native-text.zip). [Results](exact-results.json),
[artifact hashes](exact-artifacts.json) and
[source verification](parent-verification.json) describe the recorded run.
Private compiled libraries and SDK files are not included.

## Failed prerequisite attempts and remaining scope

The earlier 275-file header-fixture checkout was insufficient for production
library builds: Win32 returned 17 errors and 12 warnings from missing repository
dependencies. That attempt remains a failure, not a compiler-regression result.
Supplying the complete exact candidate produced the builds above.

The original project has no Release|x64 configuration: attempting it returns
MSB8013. The separate x64 build-configuration work remains a prerequisite for
whole-library x64 builds. Existing native x64 header tests and the separately
identified mixed-development caller tests keep their narrower scope. No
initialized-engine Debug runtime, invalid-buffer equivalence or full client
acceptance is established here.
