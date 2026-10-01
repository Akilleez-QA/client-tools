# Compose the archive and media protocol regressions in CI

Restore the existing dependency-ownership, ByteStream, decoder, Miles callback and Bink protocol checks to the portable wire workflow. Explicit joint prerequisites supply the tested source and every runner; this delta changes only one workflow, +26/-1. SHA-pinned actions, read-only permissions, fresh builds, strict runner verdicts and retained artifacts stay in place.

The base combines Bink host/session (and its native-provider prerequisites), expanded galaxy/container wire fixtures, and standalone archive regression runners. It deliberately excludes native UI tests, which need genuine v120 engine dependencies. Pushes to this review branch run the composition automatically; the inherited master PR and integration push triggers remain. Fork drafts targeting prerequisite branches do not gain a blanket automatic test trigger.

[Exact-head hosted run](https://github.com/Akilleez-QA/client-tools/actions/runs/36850510021) passed at `505795c7dd132b88d282151d8c95de999d1f45ba`:

| Check | Result |
|---|---|
| Win32/Win64 wire fixtures | 71/71 and 78/78 |
| ByteStream | 85 per ABI |
| Archive decoder | 34 per ABI |
| Dependency-output ownership | 12 Python tests |
| Miles EOS, Bink protocol and video admission | 298 EOS, 1,047 Bink protocol and 22 admission checks under Linux ASan/UBSan |

This is fresh validation of the declared portable composition, not an MSVC build, UI allocator run, original-provider execution or complete game acceptance. The workflow does not install private SDKs or game assets.
