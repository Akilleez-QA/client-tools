# Native plain54 gate proposal — local preparation only

No VM staging, compiler, linking, test execution, SDK load or product edit. Parent must review this runner/freeze before authorizing one invocation. Four new AMD64 v120 objects are proposed, stopping on the first compile, diagnostic, identity, include or symbol concern. Never retry in the same gate.

## Frozen sources and actual objects

Only the six production files pinned in52 source-manifest-v1 are copied under inputs/candidate. No portable test/provider, compatibility macro, fake SDK or allocator test TU is included. The public header includes corrected51 seek constants. The authored engine_plain_probe uses actual FirstSharedFoundation plus that single plain ClientMiles.h, native-shaped extern callback references and startup declarations. It does not use actual Audio.cpp bodies, represent an Audio adoption patch or link any engine code.

1. candidate/plain_startup.cpp — actual retained text snapshots and public startup wrappers. Required undefined native-call startup and private guard/fail symbols; no AIL imports in this outer TU.
2. candidate/private/failure_boundary.cpp — actual reporter/fallback implementation; required abort reference, no AIL imports. The object is never executed.
3. candidate/native/native_startup_calls.cpp — actual private SDK delegate/static assertions; genuine possessed Mss.h from the reused35 snapshot. Require exactly eight UNDEF imports: AIL_startup, shutdown, get_preference, set_preference, last_error, set_redist_directory, open_digital_driver, speaker_configuration. SDK version macro legitimately references Windows resource functions, not AIL_MSS_version. Other CRT/Windows imports are retained in the full raw dump; no SDK function is called by this gate.
4. engine_plain_probe.cpp — header compatibility in engine/STLport environment. Require public startup and set_file_callbacks undefined references; no AIL import. Extern callback symbols are authored shape references, not actual Audio callback symbols/bodies.

All compile commands use /c /W4 /WX /EHsc /Y- /showIncludes and a forced actual _MSC_VER1800/_WIN64 assertion. Modern units use /MT /O2 /DWIN32 /D_WIN32_WINNT=0x0601; only the native delegate gets SDK include path. Engine probe reuses the35 Debug-x64 audited Audio definitions/include paths and cwd, plus its original /MTd /Od /Ob1 /RTC1 /Zc:wchar_t- /Zc:forScope /GR /Gy /fp:precise /Gm- /Zi /FC. No warning suppression or dialect substitution.

## Reused inputs and include attribution

Fresh target is C:/native-plain54. Reuse C:/native-file-callbacks35 explicitly; no new SDK/snapshot copy. Verify its existing input-manifest identity13a7272cdf84d617ea82f70481da686ea4abefc8e198e77e9f3d501f6fc9538a and all9536 listed file hashes before and after the invocation. Require possessed Mss.h966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e. Pinned cl/dumpbin/vcvars paths/hashes are copied from35 receipt and verified before/after; resolved tools must match. Check no active cl.exe without killing processes.

Engine actual includes get hashes and raw indentation ancestry. Compare canonical paths and hashes against35 actual engine-header includes. SDK and private adapter headers are forbidden in engine probe. Require STLport presence, unchanged baseline overlap and attributable new paths: authored forced guard/plain facade, or descendants of that facade. Any unexpected new ancestry is a stop/report concern. Do not reject extensionless VC headers globally; inherited35 CRT/C++ headers are legitimate if hashes match. Removed35 file-callback-specific headers need not appear. This is header compatibility only. System headers are hashed at each compile observation, not blanket before/after attested; staged source/full reused snapshot/tool checks are separately before/after.

## Proposed transfer and invocation after approval

Stage only input-manifest.json, run-native54.py and inputs/ into a freshly created C:/native-plain54; preserve the existing35 tree. Reuse the reviewed transfer method with an existence check. Invoke once using C:/ci-dpvs-review/python/python.exe C:/native-plain54/run-native54.py --approved-compile-only. The embedded Python sibling parser path is explicitly inserted. The runner verifies inputs before compiling and creates results only if absent.

Curate authored sources and text commands/logs/results/actual include ancestry and symbols. Keep SDK, snapshot, objects/PDB private. Capture before/after product HEAD/status separately during any authorized execution. Raw failures remain unchanged; a failure in an oracle is not silently turned into a compiler failure/pass. No claim here concerns caught exceptions, termination behavior, native SDK availability, startup behavior or ABI beyond the observed object checks.
