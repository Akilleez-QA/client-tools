# Revision29 portable result

First gate passed without source repairs or repeated checks: overlay apply0,
ASan/UBSan build0, scripted run0 with 1700 assertions. The count includes the
256-cycle regression and is not a measure of runtime integration coverage.
The complete native-sample27 duration helper link failed1 at the intentionally
missing set_named_sample_file symbol, as required. All captured input hashes
remained unchanged.

The real patched client Session and reply decoder ran with a scripted Channel.
Tests establish 256 sequential successful allocations/releases without cumulative
proxy growth, pre-exchange proxy and list-node allocation failure, null/refused
allocation cleanup, refused release retention, and successful/refused/unknown
shutdown with a live sample. Unknown outcomes preserve outputs and block further
requests. They do not establish actual host sample ownership, SDK cleanup,
private wire/callback generation composition, alias-output fidelity or rebind
semantics. Public pointers are invalid after release; there is no stale public
pointer ABA guarantee.

Frozen28 stays unsuitable and unchanged. Its lifetime64 rejection is independently
recorded in ../sample-pipe28/parent-lifetime-review/result.json. Revision29 replaces
that wrong requirement and its extra shutdown precondition. No complete pipe
sample backend or live readiness is claimed.

Identity:

- Source manifest: `cba0fdbed3f78e020432427bc4bd5e70202a06b9ceecba5a0397511d5944c333`
- Source archive: `216a29c37aa5203ca2bf0b800e62c26b24f31921da337ff3168b2dccbe752877`
- Pretest manifest: `991e04079b9c79622586861c048cef3f9fb4d2cf9622f40d6fab1b1836b13cdc`
- Receipt: `f5934c8ebe75f06b5ae6f4262a71ec850de677a41f10f5f8fee092baa3749d41`
