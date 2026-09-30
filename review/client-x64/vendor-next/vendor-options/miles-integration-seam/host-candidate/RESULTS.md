# Original-Miles scalar host candidate

Current dispatcher candidate is v3; the parent strengthened its preflight failure-output oracle without changing dispatch code (see ../parent-review15/). In v3: five confirmed Audio borrowed-sample uses now accept parent-guarded aliases. Native x86 Debug/Release build and 28 safe preflight checks per configuration pass; vendor DLL stays unloaded. Current exact source identities and logs are under [native-v3](native-v3/). Earlier v2 eight-check results and exact input hashes remain preserved under [native-v2](native-v2/). Neither run invokes Miles or validates playback.

## Historical v1: superseded compile-only source

The following v1 paragraph describes the preserved [historical source](history/v1/host_dispatch.cpp), not the current candidate.

Native VS2013/v120 x86 Debug and Release compile exit0. Source SHA2567a499c2dda34557c24691dfc0f0fd05b80cf94be0dd511286fd755f916b8ba7c. Actual original Mss.h is included privately; every supported arm calls its declared SDK function. Object symbol inspection finds exactly39 original Miles imported functions in each configuration, equal to SUPPORTED.md; no exported client ABI or placeholder function definitions. No link/run/playback or device operation performed.

Historical v1 scope: `dispatch` is an internal host component. Its Resolver must bind to the transport-owned live kind/slot/generation registry; unvalidated input cannot become a vendor pointer. It rejects nonzero unused scalar words, unexpected masks/payloads/callback/resource fields and invalid resource resolution before any vendor call. Session initialization, API lifecycle correctness, frame decoding, lane/lease and callback admission are explicit caller preconditions, not solved by this switch. Resource destruction/creation is absent. Samples are owned-only; borrowed alias support is deliberately not advertised until parent-stream lifetime is integrated. No caller may claim a complete AIL backend from these39 arms.

Out-parameter fields reflect actual SDK writes; absent requested outputs remain protocol-zero and are not advertised as SDK values. Signed32 and float32 use bit copies. All22 other function opcodes return Unsupported before invocation. Lock/unlock/preferences/startup/shutdown/string/memory/callback/speaker-pointer and lifecycle operations remain outside this advertised subset. Those must gain actual implementations/contracts before a complete client shim can exist; there is no link-satisfying facade here.

Next gate: attach real resource registry and transport admission; independently review field arity/kinds against API-MAP; then use a real initialized original-vendor fixture for allowed ordinary calls. This packet proves compilation/import binding only, not effect, fidelity, threading, state validity or a runnable client. Parent owns further integration.

## v2 narrow review repairs and safe preflight

Original v1 compile/import evidence above retained. At v2 the host rejects nonzero offsets even for empty unused spans. Public wrapper initializes Result then stores every returned DispatchStatus in transport_status, so Unsupported/InvalidFields/InvalidResource cannot leave a success0 reply. Reverb map uses dry/wet exclusively. Concrete RegistryResolver binds real typed live registry; borrowed aliases remain rejected.

Nativev120 x86 Debug/Release compile and link against genuine repository Mss32.lib with delay-load support. Eight rejection/status checks each pass: unknown/unsupported opcode, null/unregistered resource, both noncanonical span offsets, unused argument word and invalid output mask. GetModuleHandle reports vendor DLL absent before and after; no genuine vendor function or playback executes. No fake vendor symbols are linked. Both current objects retain exactly39 realSDK imports. native-v2 contains logs, explicit import/sourcehash manifest and results. This does not upgrade39 operation semantics to runtime-tested.

FP fidelity gate: original SWG caller control word can change PC24→PC64 with collision/Direct3D timing; fresh host state can differ. Raw floatbits preserve arguments only, not SDK's caller x87/MXCSR-dependent computation. Paired actual-engine/host observations remain necessary. No blanket precision setting or vendor monkeypatch applied.

## Callback exclusion gate (source evidence, not runtime confirmation)

Windows Mss.h also defines DEFAULT_ALP=NO for AIL_LOCK_PROTECTION (18); Audio does not set that preference, and its runtime value is unobserved. Therefore the comment is not evidence that suspension is active. The original Mss.h callback documentation states that MSS callback threads suspend the application thread that called AIL_startup. Original Audio EOS code mutates game-owned Sound2d/maps directly. Moving the DLL into a helper would change which startup thread could be suspended; identical callbacks and lower transport latency alone would not preserve that exclusion. Before an EOS frontend exists, observe whether the actual original runtime uses this mechanism on the exercised sample/stream paths and establish which game-state access relies on it. No SuspendThread workaround, unconstrained forwarded callback, or queue-based equivalence is assumed.

## v3 borrowed alias boundary

Exactly five arms now accept an OwnedSample-or-BorrowedSample mask; the other sample arms remain OwnedSample-only. RegistryResolver passes the actual handle kind to the reviewed parent-aware registry, never relabeling an alias. The 28-check native preflight covers stable alias identity, allowed and disallowed masks, rejected start_sample on an alias, unused arguments for all five arms, parent closing and retirement, plus the original eight rejection cases. Valid marker addresses are used only to test registry binding; all dispatches with these markers are required to reject before invoking the vendor. Both objects still import the same 39 real SDK functions. Alias acceptance for valid vendor calls is compile-tested only, not runtime-tested.

The parent-aware registry preserves lookup lifetime, not callback quiescence or cross-stream vendor-pointer uniqueness. A stream whose underlying sample changes is rejected by the registry; actual original-runtime behavior for that case remains unmeasured.

## Parent preflight strengthening

The same28 rejection cases now require every reply byte except transport_status to be zero, starting from poisoned output. NativeWin32Debug/Release pass; removing only dispatch result clearing makes both negative controls exit1 at the first case. No vendor call executes. Exact inputs/results are under ../parent-review15. A stale native Python alias and wrong negative-control variable name caused setup failures before the successful build; both logs are retained.
