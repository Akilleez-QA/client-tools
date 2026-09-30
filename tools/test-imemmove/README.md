# Checked int-length memmove helper

From a VS2013 developer prompt matching the requested architecture, using Python 3:

```
python tools/test-imemmove/run.py --checkout . --bits 32 --configuration Release --out <new-directory>
python tools/test-imemmove/run.py --checkout . --bits 64 --configuration Release --out <new-directory>
```

The probe includes the checkout's real `FirstSharedFoundation.h`, which supplies the real `Misc.h`, platform types and fatal macros. No headers, fatal functions or providers are replaced. Release runs 30 checks: forward/backward overlap, disjoint regions, identical regions and zero length with valid pointers, each through the int helper, CRT size_t function pointer and ptrdiff_t expression. Expected bytes come from a separate pre-copy snapshot; destination return identity and the entire buffer are checked. No negative sizes or null pointers execute.

`--configuration Debug` compiles the actual Debug header and call expressions to an object only. It does not link fake DebugFatal functions or claim initialized-engine Debug runtime behavior. Release uses the real header's Release policy; Debug is explicitly defined for the Debug compile.

For a separate checkout at upstream `94945103`, run the same tool with `--baseline`. Original Win32 Release must pass the same 30 checks. Original x64 can be checked with `--baseline --expect-ambiguity`: only a failed compile containing exactly the two expected C2668 memmove error locations (the real helper delegation and probe ptrdiff_t call) is accepted as the predicted negative control. Additional, missing, duplicate or unrecognized error diagnostics fail; Windows paths are normalized and source line anchors must be unique. No failed build is executed. This demonstrates the observed overload failure, not all compiler diagnostics or all engine callers.

Outputs must be fresh. The runner records commands, source/compiler/included-header hashes, build/run logs and strict results. Any unexpected compile, runtime result, count or missing input fails the process. Actual caller translation-unit builds require the original project metadata and its dependency environment; they are separate evidence, not supplied or silently assumed by this compact header test.

Run `python tools/test-imemmove/test_diagnostics.py` for 14 safe text-only classifier tests, including mixed expected/unrelated errors and incidental memmove text. They do not compile malformed C++ or execute a failed baseline.
