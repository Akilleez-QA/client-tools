# Plain native60 — direct x64 source reference, incomplete

Source-only: no compiler, tests, SDK library, DLL, runtime, engine allocator workload or product change. The possessed SDK header is read for declarations, not copied. No native64 SDK library exists here; this candidate supplies no stand-in and cannot establish native64 runtime fidelity.

Exactly50 additional plain public operations are defined. They cover direct scalar/driver controls, sample allocation/playback/settings, streams including borrowed stream sample identity, file_type/file_error and WAV_info projection. Header, nine52 startup functions, text retention, native startup calls and private fatal boundary are copied unchanged. Three declarations deliberately remain without definitions: set_file_callbacks, register_EOS_callback, register_stream_callback. Typed state/producer lifecycle is not implemented by pointer casts or null stubs. This is therefore not a complete linkable facade for Audio.

## Source shape

- plain_operations.cpp implements50 public names, using the actual52 immutable reporter boundary and C++ exception translation. It checks only the public WAV_info nonnull-result precondition. Other native values, nullable getter outputs, zero/null native results and float arguments pass through unchanged; no result is synthesized from private failure.
- private/native_calls60.h is a plain private declaration seam. native/native_calls60.cpp invokes exactly50 corresponding AIL exports against real SDK declarations, with per-function type assertions and primitive-type assertions. Opaque object handle reinterpretations preserve native object identity without dereference, owned/borrowed registration, or function-pointer casting. Sample/stream lifetime validity and ownership obligations remain the caller's native contract.
- WAV_info uses actual AILSOUNDINFO locally. It returns the actual signed status and writes exactly format/bits/channels/dataLength/rate/samples/blockSize only after nonzero status. Ordinary zero result leaves caller output unchanged. No vendor pointer, channel mask, initial pointer or binary structure layout crosses the public boundary.
- Header constants used by this subset are asserted against possessed SDK values, including room/file/error/state/seek constants.52's unchanged native TU covers startup preference/speaker values. The declarations retain signed milliseconds/offsets and exact floating/scalar argument types from the reviewed38 family.

Each public wrapper calls a separate ordinary C++ private delegate through the52 guard; the SDK TU forwards directly. No unreachable extern-C setter catch like55 is introduced and no exception model/warning policy is weakened. Engine/SDK exceptions and fatal reporter behavior retain52's limits; this is not SEH recovery or a teardown policy.

## Evidence and proposed next gate

source-manifest.json pins9 candidate files; provenance.json identifies six unchanged52 files plus three new60 files and reviewed38 source references. native60.patch contains all new-source additions. expected-imports.json lists exact anticipated50 `__imp_AIL_*` symbols for native_calls60.cpp and no SDK imports for the public wrapper. These are expectations, not observed object imports. No compile has occurred. Existing52/54 receipts do not certify60.

Review typed calls, handle identity preservation, failure guards and WAV projection first. A separately approved actual-header x64 object gate should then check the exact50 imports and type assertions without linking a library, plus wrapper references to all50 private delegates and52 failure policy. It must retain the first failure, rather than adjusting signatures or suppressing warnings during the gate. Any portable scripted-call test would be explicitly value/guard evidence and must never pose as a native64 library.

Normal callback registration/quiescence, complete shutdown and public adoption remain outside this source slice. Native lock/unlock here forward directly; they do not claim the temporary pipe already implements those semantics.
