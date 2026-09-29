# Fresh product link proof

Tool revision `58ecb70c4a6317d4ac6a54ff8853c1ffac5737b2`, based on PR22
`46a56f6a`, compared with stock `94945103`. Source archives and commands are in
[run.json](run.json). A new empty directory received only the stock source
archive; no prior objects or diagnostic sources were copied into it.

Native VS2013 Win32 Release rebuild and candidate relink passed with zero errors.
Warnings are retained in [before.log](before.log) and [after.log](after.log).
Both product executables are 29,016,064 bytes. [Comparison](comparison.json)
shows full equality after normalizing COFF/export/debug timestamps and PDB age.
No instruction bytes or PDB GUIDs are normalized. Diagnostic markers are absent.

[Committed rebuild and verifier tools](https://github.com/Akilleez-QA/client-tools/tree/58ecb70c4a6317d4ac6a54ff8853c1ffac5737b2/tools/test-link-inputs)
require a licensed VS2013/SDK environment. This is native VM evidence, not hosted
CI. PR22 remains the original one-file cleanup; tools are published separately.
Debug/Optimized cleanup and further Release removals are not covered.
