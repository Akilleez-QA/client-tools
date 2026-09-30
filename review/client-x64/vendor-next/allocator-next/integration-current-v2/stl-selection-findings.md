# STLport selection: scope and native evidence

Candidate detached worktree `client-stl-integration` is based on `085f77cc7` and preserves the committed LCD import. Five files: common x64 import, renderer-deps.props, new dependency-build.props, new client-runtime-deps.props, dependency README. No commit or binary in candidate.

## Root and ABI mode

Immutable91dc Release and Debug both reach the actual SwgClient linker, then extract x86 `stlport_vc71_stldebug_static.lib(locale_impl.obj)` and fail LNK1112. Full directive census covers63 actual archives in each configuration; the only STLport default name is `stlport_vc71_static.lib`. `config/stl_select_lib.h` emits that pragma. This corrects any earlier broad claim that bundled STLport has no autolink. The existing renderer macro is not changed in this repair.

`stl_user_config.h` leaves `_STLP_DEBUG` opt-in. `src/vc_common.mak` explicitly distinguishes DEBUG_static (/MTd) from STLDEBUG_static (/MTd plus _STLP_DEBUG). Actual consumers request the ordinary static ABI in both configurations; no consumer preprocessor definition is modified. Existing builder supplies all33 authentic TUs, matching /MT or /MTd and /Zc:wchar_t-. No new allocator or SDK stub.

## Scope

Factor common verified source-build settings/target into dependency-build.props. Renderer-specific genuine SDK checks remain before PrepareForBuild and the shared dependency build (including direct Link invocations). SwgClient x64 prepends real configuration-owned stlport.lib, removes the one known explicit STL-debug input, ignores exactly the observed legacy static autolink name. Other input order, directories and defines remain unchanged. Win32 imports neither new policy nor builder.

## Evidence

- `integration-stl-audit-v1/{Release,Debug}-directive-inventory.json`:63 archives per configuration; hashes and names recorded.
- `stl-props-eval-v1`:16/16 native metadata evaluations. `comparison.json` proves exact one-entry replacement and default override on SwgClient x64; SwgClient Win32 and Direct3d9 bothABIs unchanged. Last source adjustment only adds shared-build validation hook, preserving direct-Link SDK checks; metadata unchanged by construction.
- `stl-selection-link-v3`: exact91dc linker command replay, with changed provider selection, /VERBOSE:LIB and private output/PDB/importlibrary/map only. Real Release provider SHA d1033755c4f08ed35d4fe83fafac3adacbbd9911bbacba207227eb14fc3727a4; Debug d1b03fb0e401d88a17abb0fce7b49eae4343545afde82b9d526b05585ba01805. Both stop at x86 vivoxSharedWrapper_{Release,Debug}.lib(vivox.obj); Debug identifies sUnloadVivoxDLL from CuiVoiceChatManager.obj. This is progress beyond firstSTLblocker, not a completed link or complete symbol match proof. Provider lookup is observed; linker stops before complete archive resolution.
- v1 forensic replay failed before linking (LNK1171) because a32bit crosslinker was given amd64host DLL paths. Preserved; v2/v3 use matching x86_amd64 vcvars. v3 prepends provider, matching candidate metadata.

No full executable or native gameplay acceptance. Existing runtime tests of the actual source-built STLport through allocator/renderer/LCD fixtures remain bounded to those fixtures. Independent critic requested and reviewing this candidate.
