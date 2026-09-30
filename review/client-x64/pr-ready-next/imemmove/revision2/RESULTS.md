# Strict negative-control classification

Reviewed candidate: `3b00af6296e9d3631cd3e068d4a0c31499a9756a`, based on `94945103`. The tooling follow-up changes run.py and README.md and adds test_diagnostics.py after `5219952`. Production commit `9eadbbb` and probe.cpp are unchanged. The committed tool bytes match the final native-tested inputs; no upstream activity occurred.

The old gate searched the entire output for unrelated tokens. The replacement parses complete MSVC error records and requires exactly two C2668 memmove ambiguities: the actual normalized Misc.h delegation location and probe.cpp ptrdiff_t call. Their line numbers come from unique anchors in the actual input files. Wrong files (including same basenames elsewhere), lines, codes, functions, missing/duplicate records, additional compiler/linker/fatal errors and unparsed error text are rejected. A zero compiler exit is also rejected for this expected-failure control. English diagnostic spelling is selected by VSLANG=1033; different diagnostic formats fail closed rather than being classified as expected.

## Verification

- `python tools/test-imemmove/test_diagnostics.py`: 14 safe text-only tests passed. They include both reviewer counterexamples, normalized path spelling, order variation, missing/duplicate errors and fatal/linker failures. No malformed C++ or invalid runtime input was used.
- Native VS2013 eight-outcome matrix rerun with exactly the revised runner: all expected outcomes passed. Candidate Win32/x64 Release and original Win32 Release each passed 30 valid-buffer checks. Candidate Debug on both ABIs and original Win32 Debug compiled successfully. Original x64 Debug/Release each returned compiler exit2 with exactly the two expected error records and were never executed.
- The earlier original x64 raw logs also satisfy the new classifier; this separate reclassification does not substitute for the native rerun.
- `git diff --check` passed.

Final run.py SHA-256: `a617ca35eb6ee0eb08b73853c2ac79de97e1c49f88631a306861fddad7dc01e3`. All eight native result files record that exact runner hash. `source-manifest.json` hashes the final tools; `outcomes.json` summarizes actual compile exits and runtime counts. `native-text.zip` contains commands, input/compiler/included-header identities and logs without compiled binaries. Original revision1 evidence remains unchanged. The native recipe uses the same genuine frozen repository inputs in private C:/pr-imemmove18-v2; no active build tree or mapping changed.

Scope remains valid-buffer Release helper/CRT behavior and Debug object compilation. No initialized-engine Debug runtime, invalid-input behavior, full client link or whole-branch x64 build is claimed. The unchanged caller-TU results from revision1 remain supplemental because their other headers/configuration inputs came from existing development checkouts; no caller rerun or stronger dependency claim is added here.
