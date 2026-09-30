# Genuine legacy LCD wrapper link

2026-09-30. No production edits or commits.

| Native v120 build | 16 original wrapper TUs | Real allocator bridge | Complete link | Executed |
|---|---:|---:|---:|---|
| Win32 Release | compiled in lcd-legacy-v2 | 0 | 0 | no |
| x64 Release | compiled in lcd-legacy-v2 | 0 | 0 | no |
| Win32 Debug | compiled in lcd-legacy-v2 | 0 | 0 | no |
| x64 Debug | compiled in lcd-legacy-v2 | 0 | 0 | no |

`results-v4.json` records input hashes and outcomes. `evidence.zip` retains commands, logs and link maps, including failed runner attempts. All original wrapper objects are supplied directly, not selected piecemeal from an archive. The probe constructs a real CEzLcd but is **not run**. Genuine low-level SDK libraries match target architecture. Each map contains `MemoryManager.obj` and the real `OsNewDel` provider; x64 maps resolve `lgLcdUpdateBitmap` and `lgLcdSetAsLCDForegroundApp` to `lgLcd:lgLcd_LIB.obj`.

Allocator source is the actual minimum-block candidate used in `C:/allocator-minimum-v1`, separately compiled with its real candidate header. It contains no fixture main or substitute allocator. DebugHelp and InstallTimer objects are genuine separately compiled implementations from that same accepted probe, and the remaining providers are actual built SWG libraries plus genuine v120 STLport. No symbols were invented to complete the link. This does not claim that all prerequisite product fixes are committed.

The v120 STLport replacement requires suppression of old vc71 automatic library names, as in the existing renderer dependency work. This is isolated diagnostic link configuration, not a proposed new allocator or SDK wrapper.

## Failed attempts retained

- v1: launching `cl` from Python without an absolute executable path failed before compilation.
- v2: path separator mismatch prevented replacing the old probe command; requested allocator object was missing. No valid link result.
- v3: Python/cmd quoting made cl see a quoted filename as a literal extension, warning that no action was performed; allocator object missing. Exit code alone did not establish compilation.
- v4: write an actual `.cmd` file, normalize source paths, compile the real source bridge and require the subsequent full link. All four succeeded. Existing minimum probe source was unchanged; the failed v2 command only recompiled that scratch probe object.

## Remaining acceptance

Production props still need explicit architecture-selected SDK path, early missing-provider failure and evaluation against actual executable target. No full SwgClient link is claimed. No LCD manager service, physical device, foreground/priority arbitration, reconnect or button test has run. Preserve these tests for hardware acceptance; do not substitute the modern high-level API because it omits explicit foreground/priority controls used by the original wrapper.
