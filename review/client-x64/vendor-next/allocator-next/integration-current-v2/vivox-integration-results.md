# Genuine Vivox wrapper build integration candidate

Three files in detached client-vivox-integration, based0d2f8c168: build.py, client-runtime-deps.props, README. No source SDK implementation or runtime feature changes. Candidate hashes in vivox-candidate-manifest.json.

The existing builder builds the original Vivox.cpp (VIVOX_VERSION3, matching CuiVoiceChatManager.h) as a stable third output, with SDK/header source digests in cache identity. All three archives must exist and match the exact output-name set for reuse. Ownership/locking remains intact;12 existing ownership tests pass. No additional network downloads or binaries enter Git.

Native evidence:
- Unchanged original Vivox.cpp compiles/archives in all4 configurations, with actual SDK and STLport headers, matching CRT/wchar settings (vivox-wrapper-source-v1). Warnings retained.
- Actual integrated MSBuild sourcebuild target passes fresh/cache for x64 Release andDebug (vivox-props-target-v1), each83 commands:80 source TUs plus3 archives. Owner/manifests/commands/logs retained. Qtools restored.
- Native metadata16/16. SwgClient x64 removes exactly2oldwrapper case variants per configuration and adds1real archive; all remaining input order, directories, defines and defaultlibs unchanged. Win32 and renderer metadata entirely unchanged (vivox-props-eval-v1/comparison.json).
- Private final-link replay uses the integrated builder's actual STLport and wrapper archives plus genuine LCD/UTF8-enabled PCRE/XML providers. Release resolves all wrapper/STLport/LCD/PCRE/XML references and stops with exactly60 unresolved Miles imports. Debug firststop remains old x86 VideoCapture_debug.lib. This is mixed-snapshot diagnostic evidence against the immutable91dc consumers, not a complete current-head client build. R source/outputs unchanged.

The wrapper still dynamically loads vivoxsdk.dll and uses the original imported API and shutdown behavior. No compatible x64 SDK DLL, provider ABI/service availability, voice login, device behavior or gameplay is proven. Building the real wrapper is not a substitute for those dependencies.
