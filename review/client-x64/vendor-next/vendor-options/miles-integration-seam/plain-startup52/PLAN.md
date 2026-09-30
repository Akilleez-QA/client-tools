# Plain startup adapter 52 — implemented source, uncompiled

This new snapshot implements exactly nine operations behind the corrected51 v2 plain header: startup, shutdown, get_preference, set_preference, last_error, set_redist_directory, MSS_version, open_digital_driver and speaker_configuration_spec. All other declarations in the copied common header remain unimplemented by52, including file registration, EOS and sample/stream methods. The complete header is copied byte-for-byte from51 v2 as requested; this preserves common opaque identities and the corrected FileSeekBegin/Current/End constants without implying a complete adapter.

No compiler, portable/native test, SDK call, process-failure path, engine, VM or product workload has run. There is no runner in this snapshot. Existing product49d0 and earlier snapshots are unchanged. No SDK implementation body is copied; the native file includes the private selected Mss.h and invokes its real symbols/macro.

## File boundaries

- candidate/ClientMiles.h: unchanged corrected51 v2 public declaration proposal; stdint.h only, no owned standard-library object or public exception class.
- candidate/plain_startup.cpp: actual nine public definitions, private snapshot/input ownership and a single shared catch boundary instantiated by every public function.
- candidate/private/failure_boundary.h/.cpp: composition-only plain reporter binding and nonreturning fallback. Not included by the public header.
- candidate/private/native_startup_calls.h: nine statically linked private calls, no runtime function table, plugin or backend-selection protocol.
- candidate/native/native_startup_calls.cpp: actual direct native definitions with SDK signature/type/value assertions. Full pointer-sized preferences and driver arguments forward unchanged.

The small static private-call seam permits a later portable gate to link a clearly scripted supplier against the **real public snapshot/failure implementation**. Production must link the native source; the public header exposes no test hook or supplier selection. No scripted supplier exists in this snapshot, and a portable supplier would never be claimed as SDK evidence.

## Text and input ownership

last_error and set_redist_directory each return a separate adapter-owned snapshot. Nonnull native text is fully copied into a replacement string before swapping it into private retained storage. A genuine null returns null; a genuine empty string returns a nonnull empty string. Calling the other text function does not overwrite a snapshot. The next call to the same function or completed shutdown invalidates it, as accepted in51. This is the adapter's deliberate retention contract, not an assertion about undocumented vendor-pointer lifetime.

TextStorage is allocated lazily **inside** the public catch boundary, so no modern-library global constructor can throw before containment. The plain global pointer and reporter pointer have constant zero initialization. Neither text function requires startup to have returned: pre-startup redist/error calls use actual native operations, with private retention already available. startup returning zero does not automatically destroy storage or synthesize shutdown.

Before set_redist_directory calls the SDK, it completes a private input string copy and inserts its stable list node. Prior directory nodes remain stable until actual shutdown returns. This reuses native24's conservative retained-directory behavior. Null directory input follows native24's explicit invalid-argument policy; it is not presented as evidence of native null/reset semantics. Actual Audio passes the nonnull literal "miles". A result-copy failure after the setter may follow a vendor effect; it retains the directory and terminates through the private failure path rather than retrying or fabricating null/empty.

shutdown calls the native shutdown first, then releases private text/directory storage. If the native call throws, the fault path is nonreturning and storage remains retained. This ordering is source behavior, not a proof of vendor quiescence. The composition must keep reporter code/context available and serialize text/lifecycle access; no native thread-safety or actual composed owner is supplied here. Callers also obey the public snapshot invalidation/synchronization contract. No mutex is held across SDK calls and no SDK callback scheduling is introduced.

## Version and native scalar semantics

MSS_version requires a nonnull destination and positive int32 capacity. It then invokes the selected SDK macro directly with those arguments. It does not initialize the buffer, substitute a version, interpret empty output as a fault, or return an invented success status. The actual Windows macro at private Mss.h:4286–4296 performs a resource query and writes an empty string on its module-load-failure branch. Other macro output/termination semantics remain the macro's; the wrapper does not claim stronger guarantees. The actual Audio call uses a256-byte buffer (Audio.cpp:2468–2471). No macro body is reproduced here.

Preferences preserve intptr_t/SINTa values and any uint32 preference number rather than the temporary pipe's get1/get42/set42 restrictions. Driver opening forwards frequency/bits/channels/flags without stereo-only restrictions, range normalization or a null-as-fault rule. Speaker spec uses the same private MSS_MC_INVALID initialization and sole channel-spec output as native24, then returns that native scalar after normal completion. No exception path returns that initialization value as a fallback.

## Private exception and fatal boundary

Composition calls ClientMilesPrivate52::bindFatalReporter once, before any public operation—including pre-startup text/version calls—and before concurrent access. The reporter remains immutable through adapter use; null/duplicate binding is a fault. Public functions check the binding before native work. The plain reporter takes numeric reason and borrowed diagnostic text only, synchronously; it must consume/copy text within that call.

Every public definition invokes guarded with captures that contain only plain scalar/pointer inputs. The complete private work occurs inside guarded's try: reporter check, allocation, SDK call, conversions, snapshot publication and shutdown cleanup. std::exception and all other C++ exceptions are contained there. The failure routine invokes the engine reporter in its own catch-all and unconditionally calls std::abort if the reporter is absent, returns or throws. Thus a genuine adapter fault cannot return a normal null/zero/empty result or leak a modern exception into the engine. No abort path has been executed in this task.

Actual SDK values—zero startup, null driver, null/empty text, wide preferences—return normally. No runtime success claim follows from these source paths. The boundary is C++ exception containment, not a claim to catch/recover Windows structured exceptions or corrupted memory. Reporter integration with a real engine fatal facility, thread/lifecycle serialization, the actual STLport include boundary and native symbol/type checks still require separately reviewed composition/compile evidence.

## Source provenance and remaining gate

The public header parent is public-surface51/source-manifest-v2.json. Native24's direct startup/preferences/driver/speaker logic and retained-directory strategy are retained in narrower files; its public OwnedText/Failure return boundary and its extra nonempty version check are deliberately removed according to51's accepted contract. Static assertions inspect the possessed SDK declaration types; they are authored assertions, not executed verification. source-manifest-v1.json records all authored inputs and hashes; provenance-v1.json records parents/private SDK identity only, no SDK contents.

PROPOSED-TESTS.md supplies the deterministic prospective portable oracles and failure-process design. Root source review precedes any test authoring/freeze/run. No full adapter, actual engine inclusion, linked Miles64 client or gameplay result is claimed.
