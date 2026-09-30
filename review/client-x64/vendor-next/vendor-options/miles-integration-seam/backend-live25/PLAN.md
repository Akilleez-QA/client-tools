# Facade live composition 25 — pending execution gate

2026-09-30, recorded before runner implementation. Parent directs preparation only. Do not build or execute this live gate until the parent reviews the plan/source and explicitly authorizes it after CLI review reconciliation. Freeze backend-boundary24 and startup23 unchanged. No product edits, new pipe-drain23 integration, playback, callbacks, streams, samples, Audio/ExitChain, fault injection, vendor/SDK publication or commit/push.

The intended experiment is one Release x64 facade controller linked from frozen24 plus the original x86 startup23 host linked against the possessed Mss32 import library. Use exactly the original DLL SHA0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe and SDK header SHA966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e. This adds the reviewed source facade to the previously observed live path; it does not qualify an x64 vendor DLL or full replacement.

## Evidence, research and choice

Inspected frozen startup23 runner/build/cleanup helpers, facade24 composition source and source manifest. Facade source archive9a020d7a4af3419726ffbcbcf3193cca8890c51b0ea1980ebc7c4a22c7d78761 compiled but its live composition has not executed. Startup23 runtime resultbc8a6a32adc18fcc214d6c528d40ec301d3b90e8c3dfc191f58904fb0bd344d8 supplies the matching-state oracle/history, not a success claim for this gate.

Research retrieved2026-09-30: [Python subprocess](https://docs.python.org/3/library/subprocess.html) distinguishes timeout from child termination and supplies explicit process/session management; [wineserver manual](https://manpages.debian.org/bookworm/wine/wineserver-stable.1.en.html) identifies WINEPREFIX-scoped kill and wait. These platform/project contracts inform cleanup; actual exit/defaults observations remain required. Existing parent assignment waives redundant questions. This worker is already a delegated spike; independent CLI review belongs to the parent, not another spawned worker.

Topology: frozen source selection → native receipt/PE identities → exact original module → one private Wine/null sink →23 frame/admission/oracle observations → bounded process cleanup and defaults. Strong rival: the facade compiles but changes ordering, value ownership or error handling in the actual process path. Exact request/admission traces and the same direct host oracle discriminate this rival. Zero-startup is a separate pure mapping question, not permission to induce a real vendor failure.

Exactly20 paths considered: (1) execute now rejected by gate; (2) prepare then parent review selected; (3) recompile both frozen Release sides selected for one receipt; (4) splice unrelated PE receipts rejected; (5) private original DLL selected; (6) simulated vendor rejected; (7) global Wine/default changes rejected; (8) owned cloned prefix/null sink selected; (9) integrate pipe-drain23 rejected as extra variable; (10) frozen Endpoint selected; (11) broaden samples/playback rejected; (12) exact23 no-sample sequence selected; (13) omit negative probes rejected; (14) keep probes fixture-private selected; (15) automatic runtime retry rejected; (16) preserve first failure selected; (17) parent-only process timeout insufficient; (18) owned process-group plus prefix-scoped server cleanup selected; (19) real zero-startup fault injection prohibited; (20) separate test-only zero-result mapping selected. The selected scope does not saturate callback, media or whole-client behavior.

## Prospective source/build/runtime contract

`build-facade25.py` will compile only a Release Win32 host and x64 controller under unique C:/backend-live25, reusing revision4 receipt mechanics. Source, transitive header, selected compiler/linker/library and helper hashes are checked before/after; PE hashes/machines are captured immediately. No native x64 implementation is linked into the controller, and no PE is executed by the builder. Every compile/identity discrepancy exits nonzero. A fresh source manifest/archive pins all selected files, including the runner and its imported helper.

After separate authorization and successful build, `run-facade25.py` requires the externally captured receipt SHA. It checks the actual local imported receipt/cleanup helpers and its own source against receipt entries before import, validates exact staged PEs and original DLL/plugins before launch, then performs one30-second controller run with no retry. It retains logs, encoded reply sizes/SHA256/scalars/text, exact host admission trace and actual owned-result checks. The private prefix and uniquely named null sink are the only runtime configuration changes; default sink/source must remain unchanged.

Exact request order and expected status:

| ID | Operation | Expected |
|---|---|---|
|1|Hello|0; private bootstrap|
|2|SessionVersion|0; actual `7.2a` plus NUL|
|3,4|set_redist_directory dot, miles|0; nonnull empty then `miles/`|
|5|malformed redist text|3 before metadata dispatch|
|6|startup|0 transport, actual vendor nonzero|
|7,8|get preferences1,42|0; signed actual values|
|9,10|last_error first/changed|0; controlled owned snapshots|
|11,12|set42=16, get42|0; previous/readback|
|13,14|set42=64, get42|0; previous/readback|
|15|unsupported negative preference|3 before vendor|
|16|get42|0; still64|
|17|open22050/16/stereo/flags0|0; nonnull real driver|
|18|speaker mask24|3 before vendor|
|19|speaker unregistered driver|2 before admission/vendor|
|20|speaker mask8|0; actual spec2|
|21|shutdown|0; restore prior preference first, retained path bytes8|
|22|get42 after shutdown|4097; no vendor call|
|23|SessionClose|0; private ordered teardown|

Expected host admission ordinals:0..17 for requests1..18, then17,18,19,19,20. The host's independent fixture remains the direct original API/resource oracle. Facade values are checked by frozen24's controller. The runner additionally verifies exact23 frame and host records, matching opcode/status/value/text lengths, selected actual text/scalars, no failure marker and orderly host completion. The initial fragment value is compared relationally, not replaced with a fabricated constant. No unsupported negative value reaches the vendor.

Success requires the exact count/order/status/oracles, controller0, unchanged staged input/plugin hashes, no emergency cleanup, successful bounded cleanup, no owned sink remaining and unchanged defaults. Termination attempts each live owned process group (TERM then KILL with bounded waits), then prefix-scoped wineserver kill and wait; independent sink/default cleanup and durable result writing still occur after errors. Cleanup failures force nonzero exit. Preserve first failure and do not retry. The process-tree procedure is a bounded experiment, not universal fault recovery.

## Separate zero-startup supplement

New sibling backend-zero-startup25 uses frozen facade24 with a test-only framed Channel returning one valid startup0 reply. Prediction: startup returns0; shutdown and private Session.close reject WrongState without sending another request; Channel.finish is not called; scope destruction abandons the channel. This records the known missing graceful-close behavior, not correct SDK shutdown semantics. No frozen code change or vendor/allocator fault workload is needed or authorized.

Highest possible claim after the future live gate: frozen facade24 preserves the selected startup23 no-sample behavior through the original DLL under this exact environment. It cannot establish Audio policy, startup0 recovery, callback/TreeFile progress, Bink real-driver binding, native x64 vendor availability or full replacement. At preparation handoff the live outcome remains unobserved; parent/user controls execution.
