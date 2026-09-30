# Facade live composition 25

The single authorized Release run passed on its first attempt with Python assertions disabled (`python -O`). The pinned x64 facade controller and original x86 Miles host completed exactly 23 framed requests, with matching controller/host order, opcodes, statuses, admission ordinals, reply extents, scalar values and owned text. No retry or source repair was needed.

Observed actual values were version `7.2a`, startup 1, initial preferences 64/8, fragment readbacks 16/64 and stereo speaker spec 2. Redist results were nonnull empty text and `miles/`; the two controlled last-error strings remained distinct owned snapshots. The five private negative probes rejected malformed redist text, unsupported preference, unsupported speaker output mask, unregistered driver and a post-shutdown call before adapter dispatch. Retained directory bytes remained 8 through actual vendor shutdown. The fixture restored the original fragment preference before shutdown.

Both owned process handles had already exited 0 when cleanup started. The prefix-scoped server cleanup returned without errors, owned children were reaped, the uniquely named null sink was absent afterward, and default sink/source were unchanged. Staged DLL, PE and plugin identities remained unchanged. A separate postcheck reverified all 41 frozen source members and all 16 supplemental zero-startup inputs. Logs and parsed records preserve the actual outputs; all 23 encoded replies retain byte counts and SHA256 attribution.

| Evidence | SHA256 |
|---|---|
| source-v1.tar | e62d6ce7f94aa60c6845b000e1743f4d349e2419b5998214fddebd8f2e0a9243 |
| evidence-native-v1/receipt.json | 26a06500ce4c6df80786dfd7bc2861ec989aa566afc298ed04ef6b700c102849 |
| evidence-runtime-v1/results.json | 9f42056eaa0adf4ea2ea7d0c99da4d9ca039534ff1a58d0b0ef86e9518fe24fc |
| evidence-runtime-v1/invocation-and-postcheck.json | 66886ffc3ec5d255f688c9a02005baa9af4e7b33d46b43b0dc750e7a3184d334 |

The original DLL SHA256 is 0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe. The x86 host SHA256 is d147e02d5ae34e3efc3a69fdff3adf456f530efbc792932ac2872315dc0c6274; the x64 controller SHA256 is f6bcfb37abe4dabd6da5a0fc5d5228cd802a3c4e2b5417cae0f14434d059fda5. The revision 4 receipt binds their native build inputs and immediate PE identities. Runtime checked named imported helpers before import and launch; this is not universal runtime provenance.

The separate pure zero-startup supplement documents the existing missing graceful-close behavior: startup 0 returns 0, then shutdown and close refuse locally; no finish call occurs. It does not infer SDK shutdown policy. Composer and direct parent/senior reviews were reconciled for the successful path. Grok timed out 124 without output and supplies no clearance.

Delivery state: built and checked. Outcome state: passed for this exact no-sample composition. The strongest claim is that frozen facade 24 preserves the selected startup 23 behavior through the original DLL in this private Wine/null-sink environment. This live gate uses only the nine-operation startup facade. The separate native-startup25 eight additional delegates remain compile-only and were not part of this runtime. No native x64 vendor implementation was linked or executed. No Audio/ExitChain, sample, playback, callback, stream or fault workload ran. Product adoption, startup 0 recovery, Bink's same-process real-driver binding, pipe-drain integration and whole-client fidelity remain unproven. The parent controls the next development gate; this result completes only the bounded experiment.
