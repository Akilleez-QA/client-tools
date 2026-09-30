# LCD build integration candidate

Source worktree: `/home/akilleez/Work/swg-source/client-lcd-integration`, detached at `91dc05e8bebe0881d0540e74d4c53de909feb876`. Four candidate files only: common x64 props import, LCD props, SHA validator, dependency README. No vendor binary, device installer, feature replacement or commit.

## Native import-placement evidence

`lcd-props-actual-v1/results.json`: 8/8 actual MSBuild evaluations succeed (baseline/candidate × Release/Debug × Win32/x64), using the actual candidate common props import position on the isolated Q checkout. An audit-only target records effective Link metadata. `comparison.json` shows Win32 inputs and directory lists unchanged; x64 input lists unchanged and only the official SDK directory prepended. The candidate x64 validator was explicitly invoked and succeeded. Temporary Q source files were restored in the runner's finally block. The active R integration build has no LCD candidate.

This is metadata/SDK identity evidence, not a full-client link. Existing peer evidence links all 16 genuine LCD wrapper TUs against the real SDK and real allocator/Foundation/STLport in four configurations; physical display/buttons/hotplug and missing-driver startup remain untested.

## Provider contract

`SwgLogitechLcdSdkDir/Lib/x64/lglcd.lib`, genuine legacy API archive SHA256 `a48539793ceb80d68df27d5e913fc2d977d142a4e8e5cfb36d80725c034d17c4`. Existing `lgLcd.lib` link input retained. External SDK extraction is documented; build does not download/install it. Missing or nonmatching archive fails early. No assumptions about modern Logitech API interchangeability.
