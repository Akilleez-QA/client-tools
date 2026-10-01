# PCRE capture-vector capacity regression

This checks the scene parser's capacity argument and separately exercises the correct API contract against a real PCRE 4.1 static library. It never runs the old call that advertised bytes as integer elements.

From a VS2013 developer command prompt matching the provider's architecture, with Python 3 available:

```
python tools/test-pcre-capture-count/run.py --checkout . --include-dir <directory-containing-pcre.h> --library <actual-PCRE-4.1-static-library> --bits 32 --configuration Release --out <new-results-directory>
```

Repeat with `--bits 64` and Debug/Release as appropriate. The provider must match the toolchain architecture and static CRT (`/MT` Release, `/MTd` Debug). No vendor archive, header, or binary is bundled. Obtain the original library/header from this repository's PCRE 4.1 directory, or supply an authentic source build. The runner prints the runtime provider version and records exact library, header, caller, probe, runner, compiler and included-header SHA-256 digests. Those identities describe the supplied inputs; they do not certify an arbitrary provider's provenance or prove whole-toolchain reproducibility.

The first stage is deliberately a **lexical structural assertion**, not a C++ AST check or execution of the scene parser. It binds the reviewed declaration chain, sole `pcre_exec` call and negative-result guard. An in-memory reversion to `sizeof(captureData)` must be rejected before compilation or provider execution. Changed source structure requires review of this assertion, even when equivalent.

To run only that stage on any host:

```
python tools/test-pcre-capture-count/run.py --checkout . --out <new-results-directory> --check-only
```

The provider probe uses only correctly bounded 33-element calls. Its 25 checks cover 0, 1, 10, 11 and 20 captures: expected return count (including zero when capture storage is insufficient), adjacent sentinels, whole-match offsets, no-match result, and sentinels after no match. Zero remains a successful match, consistent with the production caller. The extra-capture cases are safe provider truncation tests, not execution of the old overflowing call.

Any missing input, structural failure, build/link failure, timeout, provider failure or unexpected pass total returns nonzero. `results.json`, `build.log` and `run.log` retain results; generated binaries stay in the supplied output directory. No full parser translation-unit build, actual game command, broader regex grammar, or full client link is established by this tool.

The **PCRE caller structure** GitHub workflow runs only `--check-only` on Ubuntu: lexical caller binding and safe in-memory reversion rejection. It does not compile or execute PCRE. The genuine-provider 25-check runs are separate recorded native evidence, not hosted CI coverage.
