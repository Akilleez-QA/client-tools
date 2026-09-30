# Native runtime prerequisites at 49d0eeed4

Read-only PE header and native VS2013 dumpbin inspection; no DLL or executable was loaded. The source head is 49d0eeed4ddaa177d7a93ea396c37c3d9b9942da. The full product still does not link because of Miles; this is not startup acceptance. Hashes, machine identifiers and complete import tables are retained in inventory.json and the per-file text logs.

All 12 generated DLL outputs are AMD64: six renderer variants (gl05/gl06/gl07, Debug/Release), two DPVS DLLs, two XML DLLs, and two DllExport build templates. No generated DLL in these scanned output directories is I386. DPVS and XML import only KERNEL32; these builds use static CRTs.

Renderers normally import d3d9.dll, d3dx9_43.dll, DDRAW.dll, KERNEL32.dll and USER32.dll. DllExport.dll is a delayed import: Direct3d9/src/shared/SetupDll.cpp:36–52 redirects it to GetModuleHandle(NULL). The generated DllExport DLL is an import-library template, not a runtime provider to copy beside the game. The final host export bindings remain untested because no valid x64 client executable exists.

Native System32 d3d9, DDRAW, KERNEL32 and USER32 exist and are AMD64. d3dx9_43.dll does not exist there. This does not exhaust all possible application-local search paths; a future runnable package must supply the official matching x64 DirectX runtime or install it before launch. No SDK or system files were changed.

There is no dev/x64 staging directory. The renderer project keeps PostBuildEventUseInBuild=false on both Win32 and x64, so its copy command is not executed. Graphics.cpp:191–220 loads .\gl05/06/07_{r,d}.dll relative to the working directory. An intentional runtime staging layout is therefore still required. The XML DLL exists in each source-built provider directory, but was not copied to the product output because its AfterLink target did not run after the failed link. DPVS likewise needs the correct configuration staged under its shared dpvs.dll basename.

The repository's dynamically loaded vendor files were inspected separately: binkw32.dll, mss32.dll and vivoxsdk.dll are I386. Bink also imports mss32.dll. Vivox additionally imports its own old audio/network providers. Their availability is distinct from the 60/61 final Miles static-import failures and cannot be inferred from successful wrapper compilation. Detailed startup gating belongs to the independent source audit.

Runner v1 failed before dumpbin because of command-shell quoting; v2 failed tool lookup because duplicate PATH casing selected the inherited path. v3 uses a real vcvars batch and its complete fresh environment, then resolves dumpbin absolutely. Only v3 provides the inventory evidence.
