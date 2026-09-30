# Independent pretest review86 and saved85 attribution

Source/evidence inspection only. No runner, compiler, test, VM, SDK/engine runtime, linker, Git or product operation was executed. Only this review was added. **No blocking selection, merge or runner defect found in this scope.**

##85 same-experiment evidence

Read portable-registry85/evidence-v1 build/run logs and receipt. Build log is empty; compile_exit and run_exit are0; each of six frozen markers appears once and the raw run log reports185 assertions. The actual saved command uses strict Clang C++11 warnings-as-errors, ASan/UBSan and no recovery. All seven frozen inputs still match, and the receipt reports no changed inputs. Test source uses actual83 registry/header with local object addresses only; assertions cover the declared parent/reservation/alias/cascade/capacity/generation behavior. There is no fake registry or SDK. This is an audit of the root's same single run, not an independently repeated experiment or additional runtime corroboration. It does not exercise Backend, vendor operations or quiescence.

## Exact86 composition

Recomputed all74 composition manifest entries and all71 native inputs without mismatch. IDENTITIES.json's composition, input, remote-runner and local-orchestrator hashes all match actual files: composition5fc0e0d0…a8f63c, input4c92251e…1a883e, runnerf30dbcbd…8cf4d, local7bd084c0…013bb.

Compared current86 candidate directly with77: exactly the six stated paths change. Core.cpp, Core.h and Session.h are exact81; Backend and registry are exact83. Public wrapper is exact81 plus only80's six-line guarded file registration insertion, preserving the actual supplied pointers and inherited one-time/non-null/private-root-pin limitations. Public header is exact70. Staged production bytes match the86 snapshot. Independently enumerated wrapper Core references equal the frozen53-name delegate list. No competing public implementation or test supplier is selected.

## Dependency selection and prospective oracles

Walked quoted includes from all35 prior selected sources against the actual86 tree, rather than trusting selection.json. No include-edge change relative to native77's recorded local closures exists. Selecting source-changed OR any transitive-header-changed reproduces exactly28 entries in the same order:14x86 and14AMD64. Every omitted unit and its local dependency closure is unchanged:

- x86: call_context, host_dispatch, coordinator, invocation_guard.
- AMD64: failure_boundary, coordinator, invocation_guard.

No affected registry/Session/private-header consumer was missed. These seven are omitted, not rebuilt or silently linked from77. The first selected unit is real x86 host.cpp/Backend, not a synthetic registry anchor. The only changed AIL expectation is its prior five names plus open_stream, stream_sample_handle and close_stream. Other selected unit metadata/import sets are unchanged. The actual selected public wrapper expects53 delegates plus fatal/reentry dependencies. Required LiveChannel/runtime/worker/mapper references and rejection of canonical fallback remain.

Read the complete remote runner and local orchestration plus diffs from77. Remote changes are fresh destination/approval token,28/14 cardinality and scope; compile flags, strict diagnostics, tool checks, include boundary checks, symbol parser, actual COFF validation, before/after input/tool/reused-snapshot checks and first-failure behavior remain. The local driver pins the new hashes/path, still archives71 inputs plus manifest, refuses an existing destination or active compiler, invokes once, and curates only text/identity evidence. No link or target execution is present. SDK is private/reused35; no new SDK body is copied into candidate. System headers remain single-time observations, not falsely post-attested. The stale runner comment mentioning73 registry is provenance wording only; actual per-unit hashes select83.

Approval would authorize only the stated object experiment.85 does not prove83's Backend ordering;86 object success would not execute81 snapshots, file callback installation, streams or lifecycle. EOS, locks, remaining image/version work, callback quiescence and paired normal teardown remain outside this gate. No86 compile pass is claimed before execution.
