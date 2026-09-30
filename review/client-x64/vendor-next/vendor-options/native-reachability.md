# Native vendor reachability — 2026-09-30

Outcome: all 24 actual translation units preprocessed and compiled successfully with VS2013, using the saved project defines/include paths and real source/headers. Six TUs × Win32/x64 × Debug/Release. No production edits, macro overrides, stubs, or product output writes. The driver is `run-reachability.py`; `native-v1/results.json` records source/audit digests and statuses; command files, .i files, real .obj files and dumpbin output preserve the sensors.

This is compile/object-reference evidence, not a full link or runtime observation. The driver deliberately disables PCH, and has no production optimization switch; undefined references therefore establish emitted source dependencies, not that the final optimized executable keeps every section. Stock existing guards were unchanged.

| Family | Native observation in all four combinations | Consequence |
|---|---|---|
| Browser manager/widget | Manager install body becomes empty; widget implementation absent. No undefined Mozilla references in either object. | The unusual `#if DEBUG=0` excludes these implementations under the actual compiler/defines. No claim about other call paths or linking unused libMozilla project. Restoring browser would be new functionality relative to these guarded builds. |
| TCG manager | Undefined actual libEverQuestTCG init, callbacks, launch/update functions in all four objects. | Wrapper is genuine compile/link dependency. Source separates init (save configuration) from SWGTCG.dll load in launch. Runtime service/launch reachability still not measured. |
| LCD | Undefined CEzLcd constructor/init/update/foreground/button methods in all four objects. | Real dependency, consistent with startup initializeLcd and default enabled config. No hardware availability implied. |
| Capture | Debug SwgVideoCapture references real VideoCapture encoder functions and Debug CuiIoWin references VideoCapture::SingleUse::run. Neither Release object has these vendor references. | Debug dependency is real even though user-facing capture commands are disabled. Do not classify it as Release runtime blocker from library-list names alone. |

Raw extracted references: `native-v1/vendor-references.json`. All sources are from C:/client-next-build; matching local source identity can be checked from recorded hashes before transferring a conclusion to another head.

POODO boundary: requested question is compiled reachability versus stale names. Rival was that source guards were misread by Linux inspection; native preprocessing discriminates it. A complete executable member map remains needed to establish final linked dependency closure. Parent owns independent integration/runtime lane; no additional child worker created to avoid overlapping that ownership.
