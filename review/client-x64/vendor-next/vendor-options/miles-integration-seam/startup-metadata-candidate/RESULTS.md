# Startup metadata — bounded experimental result

The isolated component implements five missing operations: get/set preference, last-error text, redist-directory text, and the client's exact speaker-configuration shape. No product or frozen bridge component was changed.

| Check | Result |
| --- | --- |
| Portable wire/ownership/rejection checks, v120 Win32/x64 Debug/Release | 30/30 each |
| Genuine original DLL, x86 Debug/Release under private Wine/null sink | 31/31 each |
| Valid-value mutation, requested16 mapped to64 | 30/31 each, expected exit1 |
| Preference restoration and normal shutdown | completed on positive and negative runs |
| Default audio sink/source | unchanged; only owned private sink removed |

## Supported API scope

- Get preference IDs1 (`DIG_MIXER_CHANNELS`) and42 (`DIG_DS_MIX_FRAGMENT_CNT`). Set only ID42 to16/64, matching the actual two Audio.cpp callers. Unsupported IDs/values reject before dispatch. The fixture restores the saved original value directly; this is a control operation, not a generic setter claim.
- Preference values preserve signed host32 bits; portable preparation rejects values outside signed32 and result decoding sign-extends to64. Negative/boundary values were codec checks, not arbitrary vendor preference writes.
- Last-error and redist results are immediately copied into owned byte vectors. Result.null_mask bit0 means a null text pointer with no payload. Nonnull empty text is one NUL byte. Null representation is proven by helper/golden-byte checks; a genuine null return was not observed. Genuine empty text and independence from later `AIL_set_error` calls were tested.
- Speaker configuration accepts mask8 only: physical/logical/falloff pointers are null, channel-spec is valid. The return vector pointer is ignored, never serialized or falsely reported as null. Other presence patterns reject.
- Unused fields are zero or rejected; transport status remains separate from genuine SDK return bits. Text exceeding the maximum reply payload is an explicit transport failure after the call, not a fabricated SDK result or rollback claim.

### Caller lifetime precondition

The caller must keep the redist input bytes alive through the vendor's possible use, conservatively through original `AIL_shutdown`. The fixture does this with a session-long string. Mss.h alone does not establish that the vendor copies its directory argument, and this component does not own a session path store. Passing a transient receive-frame pointer and destroying it after dispatch is therefore **not established safe**. Returned text ownership is separate and is implemented here. A later integrated host must retain the input or independently establish the SDK copy contract.

## Actual original-DLL observations

The literal `miles` directory referenced the existing private plugin directory copied into the disposable prefix. Its returned text was nonnull and7 bytes including terminator. Mixer preference was64. Fragment setting16 read back16 with previous8; setting64 read back64 with previous16. The saved8 was restored before shutdown.

The genuine idle stereo driver reported channel-spec2. The direct control started from valid mono sentinel1 and the dispatcher from valid5.1-discrete sentinel96; requiring stereo2 prevents a no-write/default-value false pass. The three omitted outputs remained omitted in the actual call. No sample, playback, callback or stream was created.

The direct control and dispatcher use the same original DLL and driver environment. This is a **same-vendor oracle**, not independent engine/fidelity evidence. Fixture-only direct calls include redist priming, startup, preference save/restore/readback, valid error-string setup, driver opening, speaker control and shutdown.

## Discrimination and preserved failure

A private mutation maps the valid requested16 to64. Actual readback became64, causing the selected check to fail in both configurations. Both runs retained their30/31 result and exit1, restored the preference and shut down normally. No invalid media, allocator fault or engine teardown was introduced.

The first native attempt failed `/WX` at the test macro's `do/while(0)` constant-condition warning, before any runtime. A normal check function replaced only that test wrapper. `evidence-v1-failed/` preserves the diagnostics.

## Build-to-runtime identity

The positive receipt pin is `d7826e5c760214ebe251bd000b3b561ba610b21cf8780092e92bfeac7d45b016`; the mutation pin is `1dc1db6fcdc560b17e38331c35d73c5a83a6c174c25fafc616219a34e95528ba`. The builder reuses revision4 header/tool discovery and records pre/post sources, reached headers, tools and candidate libraries, exact commands/exit codes and immediate output PE hashes. The runtime scripts verify the pinned receipt and selected PE bytes before copying/executing them; they do not infer build provenance from current source hashes after execution. The test launchers were run with ordinary Python, with assertions enabled.

The positive Debug/Release PE hashes are respectively `35c9ea4c9f6bdbb7a0bc76036952b0d2a49de713025c3535c0c6d7c1db472b1d` and `86fc1c6767bc0c502d72996a01350687b86536724887bf369fbe3c2b3b363043`. Original private DLL hash remains `0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe`.

Curated `evidence-v2/` and `evidence-mutation-v1/` contain text receipts, commands and logs. Private executables, DLLs, plugin directory and Wine prefixes are excluded. A WAV hash appears in the reused setup record, but no media file was passed to this fixture or parsed; it is not media-coverage evidence.

## Remaining limits

Only the tested `miles` directory behavior is established; generic path-length behavior is not. The C-string copier trusts a valid SDK C string and does not prove readable memory or synchronize concurrent vendor writes. Client shadow-pointer lifetime, session ownership, full transport integration and concurrent last-error/preference ordering remain outside this component. The two getter output masks not used by Audio and the speaker vector return remain unsupported.

`AIL_MSS_version` / SessionVersion is deliberately absent from this five-operation packet. Native Windows device behavior, playback, callbacks, stream I/O, engine shutdown and full-client fidelity remain untested. This candidate is not a replacement export DLL or an adopted game backend.
