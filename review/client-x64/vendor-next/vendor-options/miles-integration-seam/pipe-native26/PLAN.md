# Prospective pipe-native26 native object-only gate

Status: prepared for parent review; no VM staging or native compilation authorized by this document. Root must approve the frozen plan/script/source identities first. No vendor/Wine/game/engine runtime, product edits, linking, import-library creation, fake library or substitute Miles implementation is permitted.

## Inputs and composition

Original source is pinned by pipe-startup26's source manifest 09d5d3c749d4e2ac8e431c1d44788ae69804a1c9cfff5e5abb80be285db23bcf. The three already-reviewed frozen26 patches are applied with zero fuzz only to a NEW local staging tree, never to frozen23/24/25/26 or product49d0. Quoted includes for the new host anchor and live channel are added as explicit pinned original inputs. Record original and applied hashes separately. Package only authored source/patches/text; the private Mss.h stays at its existing VM path and must hash to 966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e.

If approved, stage the frozen composed archive beneath a fresh C:/pipe-native26. Native source root there contains seam-relative paths. Use existing private Python and v120 vcvarsall.bat through the established transport. The new driver requires an explicit --approved-compile-only argument. It does not invoke frozen native25's old manifest/driver against modified source. That staged driver includes the expected-header correction but is itself only retained as a source input; the new gate implements the same nonempty/exact-Mss.h requirement directly.

## Exact compile scope

For each group run /Zs /showIncludes first, then /c /showIncludes with /nologo /W4 /WX /EHsc /MT /O2 /DWIN32 /D_WIN32_WINNT=0x0601 and actual SDK include directory. No warning disable, fake declarations or narrowed linker trick. Preserve first failing diagnostics and stop later groups on failure.

- x86 group (vcvarsall x86): pipe-native26/native/host_composition.cpp and **host-candidate/host_dispatch.cpp explicitly**. The anchor calls actual staged Backend::execute, which includes the seven-op whitelist delegating to actual MilesHost::dispatch. It uses existing common helpers and contains no main/runtime fixture. The old23 23-request fixture and old linker source list are not used.
- amd64 group (vcvarsall amd64): staged backend-boundary24/pipe/ClientMilesPipe.cpp and pipe/LiveChannel.cpp; pinned backend-boundary24/native/native_miles64.cpp; staged native-startup25/native/native_startup25.cpp; the SAME fixed native-startup25/sample/install_order.cpp; native-startup25/tests/portable_contract.cpp. Pipe and direct native adapters are separate object files only; they are intentionally not linked together.

The actual v120 architecture guards and native static_asserts must pass, including exact four callback typedefs, signed/unsigned pointer-sized types, fixed stereo == MSS_MC_STEREO, and SDK signatures. Sample callbacks remain unresolved for the pipe: no pipe callback definition is added.

## Receipt/oracle

Require actual SDK identity before discovery and a nonempty discovered-header set containing the exact expected private Mss.h for BOTH compile groups. Every discovered non-system source header under the staging root must appear in the frozen composed source manifest; capture all discovered header and compiler/tool hashes around object compilation. Record exact compile/dumpbin commands, diagnostics, source/builder before/after and actual output COFF identities. Compilers from actual vcvarsall are used; require expected architecture via COFF values and guarded sources rather than an assumed filename.

Required outputs: 2 x86 objects with machine 0x14c and 6 x64 objects with machine 0x8664. Inspect symbols without executing objects:

- x86 host_dispatch.obj: all seven corresponding unresolved decorated AIL import references.
- x86 host_composition.obj: unresolved actual MilesHost::dispatch reference, demonstrating composition calls the dispatcher rather than supplying a duplicate implementation.
- x64 ClientMilesPipe.obj: seven public facade definitions and no defined ClientMiles::set_file_callbacks.
- x64 native_startup25.obj: all eight actual SDK imports unresolved (seven mapped operations plus file callback registration).
- x64 install_order.obj: unresolved ClientMiles::set_file_callbacks; no linked test substitute.

No .exe/.dll/.lib output is permitted. A symbol check proves object references/definitions only, not linking or behavior. Retain receipts even if discovery, compile or symbol checks fail; do not repair frozen sources in place. Package only source/text evidence, never objects, private SDK/header/tool contents or executable outputs.

Passing would establish compilation of this composed source slice for the two real ABIs with actual header evidence. It would not establish host runtime admission, callback safety, vendor float/room behavior, complete install support, driver-provider expansion, startup/shutdown cleanup, Bink binding or full client adoption. No vendor run follows automatically.
