# Step29: separate legacy TLS setup from file operations

Source-only candidate against product `49d0eeed4ddaa177d7a93ea396c37c3d9b9942da`. Product checkout remains unchanged. No compiler, VM, Miles DLL, generated executable, fault injection, or Audio/ExitChain test was run.

`Audio-file-executor.patch` includes the dormant seam20 header/wrappers and the new extraction, applying directly to product49d0. `Audio-file-executor-from-seam20.patch` is the smaller incremental review diff applying after seam20. Use one route, never both. The `baseline`, `seam20`, and `candidate` directories retain exact full sources for inspection; `source-manifest.json` pins their identities.

Four file-local common functions contain the exact existing open/close/seek/read operation bodies. Existing SDK callback names, signatures, declarations and registration remain intact. Each SDK callback retains its exact old process-global-once TLS prologue, then delegates. The disabled read-callback crasher block remains in the native trampoline at its original position before TLS setup. The dormant `ClientAudioFileCallbacks` wrappers instead call the common functions directly: an admitted engine worker with TLS already installed can eventually use this seam without executing the legacy `threadInstall(false)` block a second time.

No body semantics were repaired or normalized. TreeFile priority/failure policy, map/counter ownership, successful local key zero, seek/tell behavior, raw read conversion, close/delete ordering, debug bookkeeping and fatal paths are preserved as source. Additional helper calls may change compiled stack traces/inlining; native behavioral equivalence has not been established by execution. The native global-once policy remains legacy behavior, including its limitations.

The public header contains only `<stdint.h>` and ordinary client-local declarations, with unchanged types and signatures. Its updated contract explicitly requires known installed engine TLS, engine/file lifetime, operation pins and serialization with every original callback. This patch supplies no admission check or concurrency guarantee. No worker, transport adoption, mutex, TLS probing, global Foundation change or shutdown change is included.

Run static checks with:

```sh
python3 /home/akilleez/Work/client-wire-validation/vendor-options/miles-integration-seam/file-executor29/check-source.py
```

`static-checks.json` records passing byte comparisons for every extracted operation body and legacy native prefix, unchanged registration and unrelated Audio source, unchanged public declarations, and both patches reconstructing the same candidate. The checker applies patches only in disposable private directories and uses read-only `git apply --check` on product. These are extraction/identity checks, not runtime tests.

The exact full-Audio native compile recipe is `COMPILE-RECIPE.md`. It is deliberately unrun pending parent scope/source review. Compile acceptance and later executor/lifecycle acceptance remain separate; this patch only makes the existing engine-owned-TLS path possible without changing native TLS initialization.
