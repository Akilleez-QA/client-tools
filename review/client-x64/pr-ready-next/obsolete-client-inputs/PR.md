# Remove unused browser build inputs and disabled capture polling

Remove SwgClient's Mozilla solution dependency and stale browser link inputs, including the remaining Optimized-Win32 entries. Remove the nonproduction capture poll and unused include whose start/stop/configuration and parser paths were already disabled upstream. Keep the browser/capture implementations and other tool dependencies.

Base: x64 projects `5b558625c0c42a7d2b1dcce67fb80e0200f53850`, which already incorporates the published link cleanup. Three unchanged root-cause patches: 2 build files +5/-6 and 1 production file -5 (Myers). This package has no Miles/Bink dependency.

Historical evidence is scoped to the original integrated snapshots:

- [Browser cleanup](https://github.com/Akilleez-QA/client-tools/commit/94a81438c4c442f21105a58047c82d34e04c9cb4): Win32 Debug/Release relinks match after normalization of timestamps and PDB age; code, PDB GUID/path remain compared. Other tool dependency edges are retained.
- [Optimized follow-up](https://github.com/Akilleez-QA/client-tools/commit/d36090a8cec01785b25bcb9608473a8b1b770c18): native project evaluation preserves other ordered inputs; full Optimized linking was not verified.
- [Disabled capture poll](https://github.com/Akilleez-QA/client-tools/commit/4d4d03aac3329ae56d16fbe564c6da844af7d1ab): four native CuiIoWin compilation configurations passed; Win32 Debug relinks resolved. The historical x64 diagnostic used inherited /FORCE and is explicitly not link-success evidence.

Selected source/build changes match the originals and whitespace checks pass. No builds/tests/runtime were rerun for this package; these records do not establish an exact-base full-client build or live-game equivalence.
