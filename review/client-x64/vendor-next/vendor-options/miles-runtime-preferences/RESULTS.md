# Original Miles startup preference observation

Native Windows, VS2013/v120 Win32. All three fresh processes loaded the original SWG Source v3 DLL, started Miles, read both preferences, shut it down and unloaded normally. No driver, callback or audio device was opened.

| Initial mode | Raw x87 word during load/startup/read/shutdown/unload | Lock protection (18) | Mutex protection (44) |
|---|---|---:|---:|
| Inherited | 027f | 0 | 1 |
| Explicit PC24 | 007f | 0 | 1 |
| Explicit PC64 | 037f | 0 | 1 |

MXCSR remained 00001f80. Each process restored its original027f word before exit. This observes that the matching Windows-header preference defaults hold after startup for this DLL. Startup does not itself normalize these three caller precision modes in this experiment.

It does **not** establish preferences after driver/device/plugin creation, absence of all suspension paths, callback synchronization, worker FPU state, the real game's state at a Miles call, PCM equivalence or a working helper. No production precision or locking policy was changed. The failing real Audio/Sound2d teardown baseline was not run.

DLL SHA256: `0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe`. Exact probe/compiler/header/executable identities in native-identities.log; raw state records in three mode logs; structured extraction in results.json. Scratch was removed after observation. Initial compile failed on SDK-private YES/NO macro expansions before any execution; original source and failure retained under compile-attempt-v1. The corrected probe compares explicit predeclared0/1 values, without modifying vendor preferences.

Context reviewed2026-09-30: [Microsoft controlfp_s](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/controlfp-s?view=msvc-170) and [versioned control87 documentation](https://learn.microsoft.com/en-us/previous-versions/e9b52ceh(v=vs.140)) distinguish x87 and MXCSR controls. [RAD development history](https://www.radgametools.com/msshist.htm) spans different releases; it does not establish this7.2a binary's behavior. Direct observations above control the narrower conclusion.
