**No production control-word transplant is justified yet.** The evidence establishes a real difference between SWG’s evolving x87 state and the diagnostic helper’s observed state. It does not establish the state at each original Miles call, or which parts affect Miles output.

The review used main `49d0eeed4ddaa177d7a93ea396c37c3d9b9942da`. No fixture, workload, or target binary was executed.

**Source-backed boundary facts**

- Win32 `FloatingPointUnit::install()` sets x87 precision to PC24, round-to-nearest/even, and masks exceptions unless configuration enables them. It preserves other CW bits. Win32 access uses `fnstcw`/`fldcw`; it does **not** configure MXCSR. `status` and `precision` are process-wide static bookkeeping, while the hardware access operates on the executing thread. `update()` restores stored `status`, not a freshly derived value from the precision enum. [FloatingPointUnit.cpp](/home/akilleez/Work/swg-source/client-build-next/src/engine/shared/library/sharedFoundation/src/win32/FloatingPointUnit.cpp:71)
- `Os::installCommon()` records the main thread and installs FPU state. `Os::update()` reapplies desired state before processing Windows messages. This is not a guard around every Miles call. Other code executes between that update and `Audio::alter()`. [Os.cpp](/home/akilleez/Work/swg-source/client-build-next/src/engine/shared/library/sharedFoundation/src/win32/Os.cpp:218), [Game.cpp](/home/akilleez/Work/swg-source/client-build-next/src/engine/client/library/clientGame/src/shared/core/Game.cpp:1080)
- Startup order is foundation → audio → graphics. Audio sets the redistributable directory, calls `AIL_startup`, registers file callbacks, then opens the digital driver. Consequently, later DPVS PC64 observations cannot be assigned retrospectively to Miles startup. There is no explicit FPU normalization around these Audio calls. [ClientMain.cpp](/home/akilleez/Work/swg-source/client-build-next/src/game/client/application/SwgClient/src/win32/ClientMain.cpp:303), [Audio.cpp](/home/akilleez/Work/swg-source/client-build-next/src/engine/client/library/clientAudio/src/win32/Audio.cpp:1285)
- Current x64 FPU code controls MXCSR, with fixed-by-type precision and preserved exception flags. Its “control word” is not an x87 CW and cannot be copied numerically into one.

The active clientAudio include path selects `miles/include/Mss.h`, which declares **7.2a, 20-Dec-07**, rather than the adjacent 7.2e header. The product declares `Mss32.lib`; the genuine fixture’s recorded PE imports resolve 54 AIL exports through `mss32.dll`. The probes use the installed DLL identified by SHA-256 `0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe`; its embedded strings identify 7.2a. Header version alone would not establish runtime identity. [Active header](/home/akilleez/Work/swg-source/client-build-next/src/external/3rd/library/miles/include/Mss.h:31), [fixture linkage evidence](/home/akilleez/Work/client-wire-validation/vendor-options/miles-engine-fixture/RESULTS.md:9), [probe identity records](/home/akilleez/Work/client-wire-validation/vendor-options/miles-rpc-contract/run-b/results.json)

**What the measurements establish**

| Evidence | Observed state | Supported conclusion |
|---|---|---|
| DPVS transition trace | Before install `027f`; after install `007f`; first collision restore `037f`, with stored CW `037f` but enum PC24 | PC64 arose through SWG’s old-state setter behavior, not merely a startup default |
| RPC direct sample 1 | Main TID 300; EOS TID 320; both `027f/1f80` | Foreign-thread callback observed |
| RPC direct sample 2 | Main and EOS TID 336; `027f/1f80` | Caller-thread callback also observed |
| Generation direct sample | Main TID 300; EOS TID 320, between commands; `027f/1f80` | Callback state/context recorded independently of an active request |

Here `007f`, `027f`, and `037f` mean PC24, PC53, and PC64 respectively, with nearest rounding and masked exceptions. DPVS MXCSR values such as `1fa0`, `1fa4`, and `1fa5` differ from `1f80` in accumulated status flags; those differences do not establish different rounding, FTZ, or DAZ controls. [Raw DPVS trace](/home/akilleez/Work/client-wire-validation/msvc-b5bb8792/critical-review/dpvs-probe/fpu-runtime/trace/ground-transition.log:1), [RPC raw logs](/home/akilleez/Work/client-wire-validation/vendor-options/miles-rpc-contract/run-b/direct-sample-2.log:72), [generation raw log](/home/akilleez/Work/client-wire-validation/vendor-options/miles-generation-live/rawlogs/direct-sample.log:214)

Crucially, RPC logging starts at dispatch **after DLL loading, Miles startup, and driver opening**. Therefore `027f/1f80` is observed post-initialization state, not a measured untouched startup default. Direct and controlled arms share this helper implementation; their agreement does not compare against SWG’s environment. [Probe source](/home/akilleez/Work/client-wire-validation/vendor-options/miles-rpc-contract/probe.cpp:23)

The EOS-observer experiment records callback thread and timing, **not CW/MXCSR**. It demonstrates publication-delay differences but supplies no additional FPU equivalence evidence. [Observer source](/home/akilleez/Work/client-wire-validation/vendor-options/miles-eos-observer/probe.cpp:25)

**Thread context and unsupported assumptions**

The 7.2a header explicitly describes the `AIL_startup` caller as the application thread that MSS callback threads suspend. That is relevant boundary documentation, but not proof that every measured callback follows that mechanism. Thread IDs establish execution context, not CPU affinity or processor pinning. [Header comment](/home/akilleez/Work/swg-source/client-build-next/src/external/3rd/library/miles/include/Mss.h:3825)

SWG’s foreign file-callback path installs `PerThreadData`; that function establishes TLS and lifetime tracking, not FPU state. EOS directly invokes `Sound2d::endOfSample()`, including its game callback, and defers sample release. Moving that work to a receiver thread changes context even if numeric arguments survive intact. [PerThreadData.cpp](/home/akilleez/Work/swg-source/client-build-next/src/engine/shared/library/sharedFoundation/src/win32/PerThreadData.cpp:189), [Sound2d.cpp](/home/akilleez/Work/swg-source/client-build-next/src/engine/client/library/clientAudio/src/win32/Sound2d.cpp:845)

Miles mixer/codec implementation source is absent from the inspected material. No matching private symbols were established; an embedded PDB pathname is not symbols. Worker initialization, internal temporary FPU changes, and arithmetic choices remain unknown. Neither export signatures nor preserved float bits establish internal x87/SSE/integer arithmetic. A callback’s CW also does not reveal the worker’s state throughout mixing.

**Next measurable gate**

A minimal prospective discriminator is **one paired, ordinary-lifetime x86 public-API probe**, using the same original DLL, asset, driver settings, command schedule, and observer policy:

- A leaves host FPU controls untouched.
- B changes only x87 precision on the Miles-owning thread to a stated hypothesis—initially PC24 before startup, reflecting SWG installation—while leaving MXCSR controls unchanged.

Record raw CW, x87 status, MXCSR and thread ID before/after DLL loading, startup, driver opening, tested calls, and callback entry/exit. Use preallocated callback records, capture PCM, and compare getters and EOS ordering/timing separately. Let vendor workers initialize normally; do not patch or force their state. Use valid handles and normal teardown only, outside the failing engine fixture.

This pair can establish sensitivity to caller state, including effects mediated through vendor initialization. A null result remains bounded to that workload. **Before choosing any transplant policy, the missing gate is a measured original SWG→Miles boundary sequence**, including startup versus later playback and callback contexts. DPVS’s `037f` is evidence to investigate, not a universal Miles control word.