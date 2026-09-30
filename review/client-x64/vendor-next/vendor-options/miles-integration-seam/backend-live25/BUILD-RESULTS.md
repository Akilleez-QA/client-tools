# Native build checkpoint

The single Release x86 host/x64 facade pair compiled and linked on the first attempt in C:/backend-live25. Both header-discovery and compile steps exited0, all recorded sources/headers/tools/libraries and build helpers remained unchanged, and no unrecorded link libraries were observed. No PE was executed. Four authored Python files passed syntax parsing; the runtime runner remains unexecuted.

| Artifact | SHA256 |
|---|---|
| source-v1.tar,41 manifest members | e62d6ce7f94aa60c6845b000e1743f4d349e2419b5998214fddebd8f2e0a9243 |
| source-manifest.json | 03d9f012227013bbd5a07c59b346f4d2a1a268b88b337ca9eb2489a37c8c4f81 |
| evidence-native-v1/receipt.json | 26a06500ce4c6df80786dfd7bc2861ec989aa566afc298ed04ef6b700c102849 |
| private x86 host, PE0x14c | d147e02d5ae34e3efc3a69fdff3adf456f530efbc792932ac2872315dc0c6274 |
| private x64 controller, PE0x8664 | f6bcfb37abe4dabd6da5a0fc5d5228cd802a3c4e2b5417cae0f14434d059fda5 |

`evidence-native-v1/local-binding.json` records receipt verification against the externally captured pin and copied private PEs. All41 current source-manifest members were rechecked unchanged. The evidence directory retains the exact native commands and logs; SDK bodies and executable binaries are excluded from the evidence archive.

The separate `backend-zero-startup25` ASan/UBSan test observed startup0 mapped faithfully, followed by local WrongState refusals for shutdown and close; only one channel request occurred and finish was never called. This documents the known missing graceful-close path, without inferring SDK shutdown policy. Its result SHA256 is8ab5e117db4b61a2206843bcca1f330794cdedc9d16fe8879e285a5457e8f851. Frozen23/24 source remains unchanged.

Delivery state: built. Live outcome: unobserved. The strongest supported claim is that the frozen facade24 can be linked into this experimental two-process startup composition. Parent review controls the remaining one-run, exact23-request live gate. No native x64 vendor implementation was linked or executed; Bink's same-process real-driver binding, startup0 recovery, callbacks, playback and whole-client fidelity remain outside this result.
