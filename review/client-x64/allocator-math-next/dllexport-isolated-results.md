# DllExport isolated native results — 2026-09-30

Observed native VS2013/v120 builds using the real project in an isolated copy, no live checkout edits or output overwrites. Evidence directory: `dllexport-isolated-worker-v1/`. Candidate source SHA256 `a7693a71dc53f38efcffaa761553763680976a40c4421ad44465057f7abbbb9f`; saved HEAD stock SHA256 `3655aea2678e156ddcff550edc85797ca9beb0ba9f5338c314ad8af5a86382f4`.

| Artifact | Debug Win32 | Release Win32 | Debug x64 | Release x64 |
|---|---:|---:|---:|---:|
| Candidate actual project compile/link |0|0|0|0|
| Saved stock source compile/link |0|0|not run|not run|
| Candidate exported names |79|79|79|79|
| Win32 decorated exports equal stock |yes|yes|N/A|N/A|

`run-dllexport-isolated.py` copies real vcxproj, resolves relative read paths against original project, points only its source to immutable scratch snapshot, and overrides object/PCH/PDB/DLL/import/map/BSC output paths. Actual logged CL/link output paths are within `C:/dllexport-isolated-worker-v1`; this run does not modify `C:/client-next-build`. Additional library search paths point at real STLport builds; no fake symbol library or substitute allocator was added. Project's own pre-existing DllExport export-template implementations are compiled as intended; they are not used as a runtime allocator oracle.

`owner-contract/` records actual Direct3d9 MemoryManagerHook compilation in Debug/Release x64 with saved project metadata and real headers, then real dumpbin symbol comparisons against actual MemoryManager.obj from product tree and new DllExport DLL export tables. Both comparisons pass with these exact decorated names:

- `?allocate@MemoryManager@@SAPEAX_K0_N1@Z`
- `?free@MemoryManager@@SAXPEAX_N@Z`

Consumer snapshot SHA256 `f6b326c9398f76658908539cb6d4b781fd03fd5d87d3ee0349936de9badad3fb`. Comparator `compare-allocator-symbols.py` requires both allocate/free families, provider definitions and matching template exports; no missing symbols. This establishes observed symbol contract for those objects, not final renderer link, SwgClient exported implementation, delay-load redirection or allocator runtime behavior. Existing parent allocator probes remain separate evidence.

## Renderer closure and unresolved external coverage

Solution explicitly declares each of Direct3d9, Direct3d9_ffp and Direct3d9_vsps depends on DllExport; DllExport has no solution dependency section. This small build-graph closure is not a complete runtime dependency closure. Renderer project explicitly links libjpeg, Win32 ODBC/multimedia, delayimp, dxguid, d3d9, d3dx9, ddraw and dxerr9; it searches bundled DirectX/libjpeg/STLport Win32 directories and delay-loads DllExport.dll. x64 SDK/import selection and actual libjpeg architecture still need real renderer link evidence. Parent is handling renderer builds; this lane did not run them.

Separate runtime LoadLibrary sites from bounded audit include Bink, Vivox, EverQuestTCG and head-tracking DLL. Their startup/feature conditions and x64 vendor binaries remain unresolved here; DllExport's success does not clear them. No vendor stub, feature removal or new replacement recommended.

Delivery state: built and symbol-checked. Outcome: passed only listed native builds/Win32 export identity/x64 object contract. Required next observations: full renderer link and real runtime export resolution; parent controls these. No commits, pushes or PRs.
