# Disabled browser build graph cleanup

At the immutable integration snapshot, both Win32 configurations link with no
Mozilla namespace references in 64 archive symbol tables or the three executable
objects. Original-input `/VERBOSE:LIB` logs load no members from the wrapper or
five SDK archives. Current SWG Source README and historical disabling commits,
verified independently by the parent, establish disabled browser as intentional.

The isolated proof removes only SwgClient's solution dependency and its explicit
browser inputs: libMozilla, nspr4, plc4, profdirserviceprovider_s, xpcom, xul.
Debug did not explicitly list libMozilla; Release did. Other eight solution tool
dependencies remain. No source module, feature define, include or SDK file changed.
Both solution builds/relinks pass, and the entire Win32 Release and Debug product
executables are equal after normalizing only COFF/export/debug timestamps and
PDB age. PDB GUID, paths and all executable sections remain compared. Raw logs,
commands, originals, candidate files and comparison JSON are in
`mozilla-link-proof-v2`. Initial v1 stopped before omission when an assertion
noticed nine solution dependencies rather than one; its source was restored.

Local production candidate mirrors this edit for Debug/Release on both ABIs.
Optimized is deliberately left alone because it has no equivalent link proof.
The generic generator's closure parser now returns 66 projects, excluding Mozilla;
eight other tool dependencies remain. It contains no hardcoded closure count.
The generator is a historical bootstrap from a pre-generation base; rerunning it
on that historical base would overwrite subsequent project refinements (including
previous renderer changes). That is not a valid verification of today's follow-up
commit. Keep that limitation explicit instead of adding a browser policy to the
architecture generator. A fresh native x64 build is still needed to expose later
link dependencies. This evidence does not demonstrate startup or live gameplay.
