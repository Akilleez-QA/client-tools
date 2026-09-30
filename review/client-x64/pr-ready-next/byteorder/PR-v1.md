# Use byte-swap intrinsics in the Windows x64 ByteOrder implementation

The Windows byte-order functions use x86 inline assembly, which MSVC cannot compile for x64. Select the corresponding 16-bit and 32-bit byte-swap intrinsics under `_M_X64`; keep the Win32 assembly unchanged.

Production diff: one file, 26 added lines. No project configuration changes or full-client build claim.

## Validation

Prior native VS2013 testing of the same production patch compiled the actual ByteOrder translation unit with repository headers: 166,631 input cases in both directions per Win32/x64 Debug/Release executable. The original Win32 implementation passed; original x64 compilation failed on assembly; a no-swap mutation failed the oracle.

The isolated branch has not yet rerun that matrix. The previous runner depends on local build-metadata paths, so it is not yet a self-contained reproducer from this branch. These are preparation gaps, not completed validation.
