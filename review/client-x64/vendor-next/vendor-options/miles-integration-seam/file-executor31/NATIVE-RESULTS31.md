# Step31 first native failure — preserved without retry

The single authorized 20-object gate stopped at its **first** compilation: Debug|Win32 `EngineFileWorker.cpp`, compiler exit 2. The remaining **19 objects were not attempted**. No object was generated, so this gate establishes no COFF-machine result, x64 compile result, link result, or runtime behavior.

Raw diagnostics:

```
EngineFileWorker.cpp(33): error C2220: warning treated as error - no 'object' file generated
EngineFileWorker.cpp(33): warning C4512: 'MilesFileExecutor30::EngineFileThread': assignment operator could not be generated
```

The new Thread subclass contains a reference member (`owner`) and omits a declared assignment operator. This is a new candidate-source warning promoted by the unchanged Debug `/WX` flags, not an inherited engine baseline warning. The existing engine member-function Thread wrappers explicitly declare private copy/assignment operations; that is a source lead for a future separately authorized correction, not a repair performed here. The native input tree, driver and candidate sources remain unchanged; no flags were relaxed and no compile was retried.

The attempted TU consumed 232 headers. The recorded include-boundary check passed: engine STLport was present and modern file26/transport headers were absent. MSVC reported `_MSC_FULL_VER=180040629`. Modern adapter TUs, Release and x64 remain uncompiled by this gate.

Before/after checks match all **9,547 staged input entries**, including the frozen runner. These are staged-source/input identities. Actual include hashes were recorded during compilation, but system headers were **not** rehashed afterward; no before/after system-header attestation is claimed.

- Input manifest: `3296557d7c2c18c6b69f83a973fcdb93d8d318b20bbaf4ec0bea3bef9bbe8be7`
- Runner: `1080278829ce9798deae25a15338e81417ec2e349ddbe05f3105897434d86481`
- Curated text ZIP: `b4cb5302bef4ccbcd60dbea26eca8063d183a909d52b022eb826172672b24d06`

`native-evidence-v1/curated/results/results.json` retains the one attempted record and expected matrix count 20. The adjacent raw command, compile log, actual-include hashes and compiler guard are preserved. Curated evidence contains eight text files, no SDK snapshot, object or PDB. Private source/snapshot staging stays private. The staging-only Python tarfile DeprecationWarning is also retained in the orchestration log and is unrelated to C4512.

Product remains clean at49d0. No engine Thread change, product adoption, link, DLL invocation, generated-code execution, Audio/ExitChain workload, fault injection or runtime occurred. VM compiler/tooling work has stopped.
