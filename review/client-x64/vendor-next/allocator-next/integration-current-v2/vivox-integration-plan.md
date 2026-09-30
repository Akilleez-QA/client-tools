# Prospective Vivox source-build integration

Separate root from STLport provider selection. Base on that committed head when parent supplies it.

- Extend the existing authenticated local dependency builder's stable output set from jpeg.lib/stlport.lib to also vivoxSharedWrapper.lib. One authentic source TU, no generated implementation or import stub.
- Include wrapper source/headers and bundled Vivox SDK headers in cache input identity. Keep compiler/SDK fingerprints and checkout/platform/config ownership, lock, all-or-nothing manifest publication. Validate the exact output-name set.
- Compile original Vivox.cpp with VIVOX_VERSION=3 (actual CuiVoiceChatManager consumer's explicit setting), ordinary STLport, /Zc:wchar_t-, /MT Release or /MTd Debug. No _STLP_DEBUG and no provider-code edits. Preserve warnings rather than disable a class globally.
- Append the real archive to SwgClient x64 and remove only legacy explicit vivoxSharedWrapper_Debug/Release names (case variants from actual metadata). Leave other vendor libraries and all Win32 policy unchanged.
- All consumers use one stable output inventory; avoid optional two-output/three-output calls invalidating each other's shared cache. Renderers may compile one extra small TU, but do not link it.
- Native all4 source compiles already pass. Re-run actual builder targets fresh/cache and evaluated metadata with integrated recipe; forensic Release link already resolves every wrapper symbol and progresses to other real dependencies.
- Runtime still dynamically loads vivoxsdk.dll, imports original API, and uses original shutdown behavior. No compatible x64 runtime/service is supplied or proved by the wrapper build. No feature removed and no replacement SDK assumed.
