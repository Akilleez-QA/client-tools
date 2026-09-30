# Independent pretest review66

One P2 oracle gap should be corrected before the first gate. No compile/test/runtime was executed and no frozen input was edited. Verified33 inputs against freeze.json SHA256 `ff2dd4b918f175203455673e8dd0e1a83c7aa7900d5ad6b21f950d04a3edc3e5`; actual ClientMilesPipe.cpp and source-only LiveChannel copy are byte-identical64. Only this report was added.

## P2 — legal pair masks use the production helper as their own oracle

The pair loop in tests.cpp calls `checkPure(..., MilesWire::validPairMask(mask))`, then skips negative-mask cases based on the same helper. Session::validateReply itself uses that helper. Thus the required acceptance set0/1/2/3/7 is not independently asserted despite being stated in PLAN.

Concrete false-pass: if validPairMask regresses to accept8, the mask8 zero-result case expects true and the validator returns true. The subsequent omitted-output mutations are still rejected by the separate omitted-output checks, so they do not expose that illegal-mask acceptance. No execution is needed to trace this shared-oracle path.

Use an independent explicit expected set/table for masks0–8 in the test and use it for the branch as well; optionally assert production validPairMask equals that independently specified value. Preserve the initial unrun freeze and review the new freeze before executing. This is a test-oracle finding, not a production64 defect.

## Lifetime and reachable behavior

The placement Session is genuinely constructed in alignas(Session) static byte storage. Its destructor is not registered as an automatic/static Session destructor and is intentionally never invoked. The test clears actual driver/SampleState heap owners before normal exit; the private callback shared_ptr is empty, and no worker, callback/file record or Endpoint exists. I found no concrete UB or unavoidable allocation leak in this setup. This is synthetic object-lifetime management, not production teardown evidence. Exceptions on failed checks return nonzero; the prospective runner must retain that first failure.

Direct tests exercise actual validator code and actual opaque proxy list definitions. They cover all four pair opcodes, live-parent lookup, parent echo, initial null alias, stable/changed/null-after-live alias, cross-parent duplicate alias and allocation duplicates. They do not execute stream facade operations through an actual host, and the direct validator cases assume their documented prior generic decoding. There is no false claim that these synthetic owner rows are reachable from the incomplete selected host's current stream routing.

The scripted Channel's normal/refusal/malformed calls do reach actual Session::request and actual sample_ms_position. It uses actual codec and coordinator methods; expected failures cannot easily hide a prior CHECK failure because completion/observation counters, output sentinels, uncertainty and retained coordinator state are checked afterward. Failure-case snapshots exclude only the expected uncertainty flag. SessionFiles readiness's requestPins value proves retention of that registration's admission pin; it is not a separate assertion of every handle in the coordinator's private resource vector.

The scripted success path explicitly observes PendingCallback, acknowledges and completes before returning to real output stores. That proves this scripted ordering with the real coordinator, not actual Runtime::returned or concurrent ACK scheduling. The latter are absent from the stub by design. Likewise the source oracle checks lexical ordering in the immutable actual LiveChannel copy; it is not a CFG proof and could not validate an arbitrary edited transport merely by finding those strings. The independent64 source review is therefore a necessary companion, as the plan states.

## Runner scope

The runner freezes inputs, creates exclusive evidence, bounds oracle/compile/test subprocesses, stops on the first failure and requires each of five scenario markers once. The proposed program has one normal execution, no process-fatal destructor workload and no engine/vendor execution. ASan/UBSan and leak detection are enabled. No sanitizer result or compilation success exists yet; strict compiler acceptance and runtime assertion reachability remain future evidence. The normal final assertion count is printed by the program but not independently required by the runner; the present five markers and zero exit are its explicit scenario contract, not exhaustive coverage.

Known coverage limits are not new source defects: actual Windows Runtime/Endpoint execution, live host stream routing, file installation/TLS, shutdown and failure quiescence are outside this gate. This review is a separate same-model-family source inspection sharing the parent framing, not runtime corroboration or operational approval.
