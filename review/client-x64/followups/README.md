# CI and reproducibility follow-up

## Current observations

- Client wire PR23 head `e6738a9f5`: [fork Actions](https://github.com/Akilleez-QA/client-tools/actions/runs/36548947196) passed50/50 Win32 and57/57 Win64. Exact-head checkout, fresh fixture executables, logs and SHA metadata are automatic. StrictCI mode rejects missing helpers; stock-oracle reducedcoverage mode remains explicit. [Logs](client-wire/) record the identical commit's earlier validation run36548590751.
- DPVS PR24 head `ebce07521`: [native reproduction report](dpvs/RESULTS.md), [source and commands](https://github.com/Akilleez-QA/client-tools/tree/ebce07521eba3b4c92eccf5aaf3bdcb3d6f475c4/tools/test-dpvs). Allfour DLL configurations and freshly compiled probes passed. Hostedv120 CI remains a separate gap. The original five production commits are unchanged.
- Server production head `8e57911e`: [fresh twoABI validation](server/RESULTS.md). No cached build outputs, no new client/gameplay session; RELEASE uses C++-O0. Database fixtures, clusterhealth/restart/shutdown and listed native regressions passed.
- Server CI branch `25816f10`: [portable Actions](https://github.com/Akilleez-QA/src/actions/runs/36549084361) passed bothABIs. [Legacy fullbuild](https://github.com/Akilleez-QA/src/actions/runs/36549084466) passed, including Clock, OsFile, DebugHelp and Miff against its fresh 32-bit build. PR35 now includes these CI changes plus a documentation-only follow-up at `6b998f6f`. Its [portable rerun](https://github.com/Akilleez-QA/src/actions/runs/36550577907) and [full-build rerun](https://github.com/Akilleez-QA/src/actions/runs/36550577889) both passed.

- Link cleanup: [fresh native product rebuild and relink](link-proof/RESULTS.md) passed normalized whole-executable equality. Rebuild and hardened verifier tools are published separately from PR22.

## Review map and remaining work

[Tracked acceptance follow-ups](ACCEPTANCE.md) retain the unclosed requirements.
[Server dependency assessment](server-dependency-plan.md) separates src23's vendor import from the smaller handwritten changes; it proposes no blind cherry-pick split and rewrites no history.

The first client CI run exposed a coverage-policy issue: stock comparisons may
legitimately report absent helpers, but current-headCI must reject them. The
strict mode was added and a real stock-code negativecontrol failed as required.
The first legacy serverCI attempts exposed an imagearchitecture assumption and
an Oracleheader searchpath omission; those failedruns remain available.
Reusable PE verifiers were challenged with malformed metadata pointers into
instructions. Hardened verifiers reject those spans; actual comparison results
remain bounded to the recorded binaries and permitted metadata fields.

No fullx64client link, nativeGPU FPU tracing, or new gameplay acceptance is implied.
