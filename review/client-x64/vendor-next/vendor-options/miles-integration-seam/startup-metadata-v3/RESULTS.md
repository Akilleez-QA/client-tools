# Startup metadata revision 3: bounded repairs verified

This is an experimental component, not a production Miles backend or complete bridge. Revision 2 is preserved at `../startup-metadata-candidate/frozen-v2-review.tar`, including the weak directory oracle and incorrect preference-mutation prediction. No v2 result was rewritten.

## Changes

- Directory request bytes are copied into explicit `SessionInputs` storage before the vendor call. Stable list entries retain those bytes until after shutdown, including failed response construction. The fixture declares the owner before its Session, so destruction happens after shutdown. The owner caps cumulative logical payload bytes at `MaxFrameBytes`; allocator capacity and RSS are not measured. Its `Bytes` argument must refer to a valid readable allocation. No generic pointer-provenance check or thread safety is supplied.
- Requests use `MaxFrameBytes - 136`; replies use `MaxFrameBytes - 128`. Tests now encode and decode an exact-capacity request with frame-relative text offset 136, then reject cap+1 in both encoding and component validation. These large strings are pure codec inputs and never reach Miles. Arbitrary vendor directory lengths remain unproven.
- Runner cleanup independently attempts owned-prefix Wine termination, owned-module unload, default capture and result writing. A kill timeout cannot skip the remaining attempts. Optimized Python is rejected before any prefix, sink or vendor activity, so receipt assertions cannot disappear under `-O`.
- The directory oracle now observes distinct valid `.` and `miles` inputs directly, copies their responses immediately, resets to `.`, and then dispatches `miles`. If the direct responses do not discriminate the paths, the fixture stops before startup. The cleanup banner reports which calls actually ran instead of always sounding successful.

## Results

| Observation | Debug | Release |
| --- | --- | --- |
| Native v120 Win32 portable component | 39/39 | 39/39 |
| Native v120 x64 portable component | 39/39 | 39/39 |
| Native v120 genuine x86 host compilation | clean `/W4 /WX` | clean `/W4 /WX` |
| Original DLL, private Wine/null sink, no playback | 33/33, exit 0 | 33/33, exit 0 |
| Wrong valid path mutation (`miles` forwarded as `.`) | 32/33, exit 1 | 32/33, exit 1 |

The mutant fails the directory response comparison. Both mutated runs still restore the preference and invoke normal shutdown. They are expected discrimination failures, not successful functionality.

Two pure Python cleanup tests pass: an injected Wine termination timeout still attempts unload and saves its error; three injected cleanup errors still reach receipt writing. Both runner entrypoints reject optimized execution with exit 1 before side effects. These use injected Python functions, not vendor or engine fault injection.

Raw directory observations: `.` returned a nonnull empty string (one NUL byte); `miles` returned seven bytes including NUL. These are same-vendor return-text observations, not a documented non-mutating directory-state query. The wrong-path control proves this oracle detects that particular forwarding error; it does not prove all omitted-call or stale-return variants.

Preference reads and valid writes remain source-shaped: mixer 64, fragment values 16 and 64 with previous values 8 and 16, followed by restoration. Speaker outputs remained stereo (2) from distinct valid direct/candidate sentinels. No sample, stream, callback, playback, media parsing or engine startup was performed. The referenced known PCM hash remains a runner setup identity only; it is not used by this test.

## Attribution

The first v3 matrix is preserved under `evidence-native-v3`, receipt `7ff029db134f9960330d76cfab67b6ee5073a388fc15bef4a8caddd364ebd004`. The accurate cleanup banner and input-span comment required a fresh v3b build before genuine execution.

Executed v3b receipt: `8c188c5531f30f6a13e2f256e42707279ce485a62b5f75f22865e0ffbf8263d9`.

- Debug PE: `bf9fbb4b436022baa5fad3378784cbdf0841aa63e284d6dabed8a970cbf18385`
- Release PE: `086130a8ef54f38c97389c4b95a8a7a680e06112cfdc64015fe1ed30be3df9a9`

Wrong-path build receipt: `90801dc2e5c09723119953f3b024309df258590c278685734a1d5b8befeee768`. Only its private `metadata_host.cpp` substitutes the valid path `.` at the redist SDK call; the builder changes only output location and the host-only matrix. Production candidate files remain unchanged.

Build receipts record input/header/tool/library identities before and after compilation, exact commands and exit codes, and PE hashes immediately after successful link. Runners verify pinned receipts and selected PE hashes before execution. These are trusted local receipts, not cryptographic signatures or proof against a concurrent malicious filesystem writer.

## Limits and corrections

The v2 preference mutation demonstrated readback failure only. Its previous-value prediction was wrong and is not repeated here. The directory mutation is separate evidence.

SessionInputs ownership is explicit, but a future bridge must ensure this owner really survives vendor shutdown. This candidate does not provide that complete lifecycle, concurrency, lane or last-error ordering. Output text is copied, but future client-visible string lifetime remains an integration responsibility. Registry stale/wrong-kind/cross-session coverage was not expanded in this slice.

Cleanup logs establish that restore and shutdown calls were invoked and the owned sink was unloaded; they do not establish every internal SDK resource was destroyed. Both positive and mutant runs recorded no cleanup errors and unchanged desktop audio defaults. ALSA control-device lookup diagnostics remain visible in raw logs and were not suppressed.

Only source, text logs, receipts and summaries belong in the review packet. Original DLL, SDK, plugins, media, PE binaries and private Wine prefixes remain private. No product files, commits, pushes or GitHub actions were made.
