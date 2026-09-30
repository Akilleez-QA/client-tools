# SessionVersion22 targeted correction

Revision22 removes the adapter's basename identity assumption. `queryCurrentDll` now calls `LoadStringA(currentDll, 1, text, 256)` directly on the caller's held, externally verified original module. It contains no SDK header, `GetModuleHandle`, `LoadLibrary`, version constant or SDK macro. Resource-read failure returns false without changing the frame. The portable query/result/consumer implementation and tests are byte-identical to revision21.

This changes the host implementation while preserving the observed `Audio::getMilesVersion` result contract. The original private SDK macro remains only in the native comparison fixture, under the explicit single-normal-basename setup where its earlier evidence was valid. Its private body is not copied or published. No AIL export is defined or emulated.

## Native results

All eight v120 builds passed `/W4 /WX`, with unchanged recorded source/header/tool/library identities and no uncovered observed library-search paths. All twelve runtime launches exited zero. PE and both original DLL-copy hashes matched before and after every run. The actual launcher hash is checked against its frozen build receipt; it ran under Python `-O`. A wrong external receipt pin was rejected before runtime-directory creation or PE launch.

| Native surface | Debug | Release |
| --- | --- | --- |
| x86 portable wire controls | 600/600 | 600/600 |
| x64 portable wire controls | 600/600 | 600/600 |
| Direct adapter and resource controls | 32/32 | 32/32 |
| Same controls with poisoned compile-time string | 33/33 | 33/33 |
| x64 consume normal host response | 606/606 | 606/606 |
| x64 consume poisoned host response | 606/606 | 606/606 |

For both normal and poisoned builds, the adapter and original macro returned **7.2a**, five bytes including NUL, producing a 133-byte canonical reply. Setting `MSS_VERSION` to `SV21_COMPILE_TIME_POISON` changed neither result. Normal module and later resource mappings were released before the final x64 file-backed response consumption.

The missing-resource control used the valid probe executable's own HMODULE, whose resource-1 query returned zero. The adapter rejected it and retained the exact prior frame. Null handle and invalid request also retained that frame. A zero API return is deliberately rejected, including the indistinguishable empty-resource case; no empty string is fabricated as successful output. The verified original version resource is nonempty.

## Duplicate-basename evidence and its boundary

After the single-module macro comparison, the probe unloaded the normal Miles DLL. It mapped two hash-identical original DLL copies from distinct absolute paths using `LOAD_LIBRARY_AS_DATAFILE_EXCLUSIVE | LOAD_LIBRARY_AS_IMAGE_RESOURCE`. Both filenames were `Mss32.dll`. The returned resource handles were distinct, `GetModuleHandleA(MSSDLLNAME)` found no normal module, and queries through both supplied handles produced the recorded resource result. The mapping flags avoid additional normal DLL initialization; the preceding macro fixture still performed ordinary DLL attach/detach.

This control exercises resource queries without the normal basename namespace. Revision21's basename check would reject those states. The two copies contain identical strings, so this is **not** a distinct-version wrong-module discrimination test and does not reproduce the old review finding as a native wrong-version failure. The source/API contract establishes the narrow identity property: the adapter passes its supplied `currentDll` directly to `LoadStringA` and never resolves a name. Its caller must verify that handle's file identity and hold it throughout the call; concurrent unload and product loader ownership remain outside this component.

The direct adapter and original macro share Windows' resource API and the same private DLL. Their equality is a fixture-path comparison, not independent vendor corroboration. The compile-time poison rejects constant substitution; source inspection rejects a hardcoded observed version.

## Identities and preservation

- Frozen source: `source-v1.tar`, SHA-256 `74edc78ad96434eb6daf44b584a66096c037462370cbba1f4e75059c67e4f01c`.
- Native build receipt: `evidence-v1/build-v1/receipt.json`, SHA-256 `b278f8582d5f5d6d4d77d3b8436403668f909a39331470d1f31e15b05c78e30e`.
- Runtime results: `evidence-v1/runtime-v1/results.json`, SHA-256 `fe65820abe560d592c9304967809187b17273f01be8d3e01d7c54f83a82d000d`.
- Text-only evidence archive: `evidence-v1.tar`, SHA-256 `e4e736a4c30479534bfd3dbe94c8f72f2453624f1d2246cca4586bedbaa5b1ee`.
- Both original private DLL copies: SHA-256 `0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe`.
- Fixture-only SDK header: SHA-256 `966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e`.

| PE | Build-time SHA-256 |
| --- | --- |
| x86 Debug wire | 0ab68e02851c21888100080933b0b75d0156484686bfa27d4ddcde575178ee53 |
| x86 Debug host | 9490814ef19f57041dffed98faeecb4e8d392ad16a906a2a7d88d17e484f2e3c |
| x86 Debug poison | 28858548804dc04c15b907709dc32c724994bba36e749c366cd8586efdcbd718 |
| x64 Debug wire | 7ed93b1bfdd14678fdd5534b100ec9af75738777acef8198a2d9c8c4b03e40cc |
| x86 Release wire | cc301d77c558a2bca5b84adca9eb0299eedcfabbf1c8385b2d35d02b47cbdf33 |
| x86 Release host | aca09a60e79d70ab1a0ac17f429b800e3c2412dab627f707d5bf86ae74cb9869 |
| x86 Release poison | 3fbe5c005f4c32a009383c98be3edf5bf0a3e119a8bc0827ba216b0ff385d742 |
| x64 Release wire | d69daf940d17f73656bb1c38afa91da2616079de4f00fe229f8c9a56ddd9b3dd |

Native private staging is `C:/session-version22`. Vendor DLLs and PEs remain there. Local receipts/logs contain no vendor binaries or SDK macro body. `collect_evidence.py` and final documents were added after the frozen build snapshot solely for collection/handoff. Current source matches the native receipt. Revision21's source-v2 manifest, final native receipt and runtime-results hashes were rechecked unchanged. Its senior22 finding and restricted prior evidence remain preserved rather than rewritten.

## Handoff boundary

P1–P5 passed on the named native artifacts. Parent review determines disposition of the earlier finding; this packet supplies a targeted design correction and evidence. No product, frozen protocol/codec, previous revision, upstream repository or PR was changed. No Audio install, Miles startup, device, playback, vendor allocator or engine fixture was run. No general loader framework was added.

`delivery_state`: built and checked.

`outcome_state`: passed for held-handle resource-query, resource-failure preservation, basename-independent resource mappings and file-backed x64 copy tests.

`highest_justified_claim`: the new adapter directly reads the supplied held module's resource-1 text, matches the original macro's 256-byte output on the exact DLL, and preserves owned/validated wire copying without basename lookup.

`required_runtime_observation`: actual client use over integrated live transport with module/session lifetime and failed-response policy. None remains for this bounded component's planned probes.

`who_controls_next_test`: parent integration agent; independent review is pending separately.
