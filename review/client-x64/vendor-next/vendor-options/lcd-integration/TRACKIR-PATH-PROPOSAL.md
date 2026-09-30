# Bounded TrackIR path construction

The candidate's x64 filename adds two characters to an existing unchecked strcat path. Keep the selected name and signature/profile/API behavior. At the registry read in ClientHeadTracking::install, reserve `strlen(ms_npClientLibrary) + 2` bytes from the passed capacity: one slash and one NUL. This is also necessary because the existing RegistryKey::getStringValue writes an additional terminator at `dest[valueSize]`; passing the entire backing buffer permits a one-byte overflow for a full-sized registry result.

With backing buffer N, DLL name length D, pass B=N-D-2 to getStringValue. Even a non-NUL registry result of exactly B bytes is terminated within the backing buffer, then the slash + D bytes + final NUL fit exactly (N bytes total). Explicitly verify `strlen(libraryName) <= B` before append. Both selected filename lengths must be checked against N before subtracting if not compile-time arrays.

This is a local capacity fix, not a shared registry rewrite. The wrapper's getValue still FATALs on RegQueryValueEx failure including ERROR_MORE_DATA, so too-long registry data does not become a graceful fallback. A fully graceful path would require a separate bounded read/API failure policy; do not claim it here. Keep current empty/default path behavior and normal successful path unchanged.

Boundary discriminator: for each actual DLL name, backing buffer guard canaries; path lengths 0, B-1, B including unterminated B-byte input; append must yield exact name and terminating NUL without touching canaries. B+1 is rejected before append. Real TU preprocessing/compilation all four configurations must be rerun because the source hash changes. No registry writes or device bypass required.

## Candidate implemented and tested

Actual ClientHeadTracking.cpp candidate SHA256 `95778fa3a4e2bb2c6ebd8c8932e6dc01bbc760bb20a4561fe64330229d13552c`. Native v120 preprocess/compile both phases exit 0 on Win32/x64 Debug/Release. Header layout comparison remains matching. `trackir-candidate-v2-results.json` records the exact source/audit hashes. `git diff --check` passes.

The separate synthetic path arithmetic probe uses the real 512-byte capacity constant (Os.h), both DLL names, 0/B−1/B/B+1 lengths and backing canaries; 80/80 checks on each ABI/configuration. It intentionally does not load a provider or query/write the registry. It does not establish that Windows registry errors recover gracefully. Source is `trackir-path-boundary.cpp`; results `trackir-boundary-results.json`.
