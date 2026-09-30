# Binding probe 30 — source-only precommit

No compiler, VM, PE, vendor, audio runtime or playback has been invoked in preparing this package. A later parent review must separately authorize the one build; a successful build is not permission to run. No production replacement or product edit.

## Fresh source scope

Verified the actual product checkout `/home/akilleez/Work/swg-source/client-build-next` at HEAD `49d0eeed4ddaa177d7a93ea396c37c3d9b9942da`, and checked its Audio.cpp against `git show` for that commit before implementation. Current getSampleTime begins at 4427, binding at 4449, release only in success branch at 4455. Buffered sound/music begin at 5328/5348 and bind on the same retained handle at 5338/5358, after stop/end on reuse. These agree with the earlier review's older snapshot behavior; line references above supersede that snapshot. The baseline helper's failure-path handle leak is not copied: this probe always releases its one allocated sample during normal completion or C++ failure cleanup.

## Fixed question and sequence

Can the exact original x86 DLL accept repeat PCM binding on one allocated sample and recover by binding known-valid B after a zero-return unsupported-format bind? This is state characterization with all inputs alive. It cannot answer whether an obsolete/failed input may be freed or whether failure preserves the old binding.

One startup, driver open at 22050/16/stereo, and one HSAMPLE allocation. Bind A1 → B1 → A2 → F → B2-after-F. A/B/A/B success must be nonzero raw S32, never normalized to 1. Query only after their observed successful binds; initialize outputs to -19001/-19002 and log signed values plus raw 32-bit hex. Precommitted expected total milliseconds are 1000/2000/1000/2000, current 0; stop at a mismatch without changing expectations. End after each successful query; release once and shutdown once on normal completion. No start/stop/resume/playback or callbacks.

A: canonical full 44-byte-header PCM WAV, mono S16, 22050 Hz, 22050 silent frames, 44144 total bytes. B: same with 44100 frames, 88244 bytes. F: full A-size bounded RIFF/WAVE with fixed format tag 0x7fff replacing PCM tag 1. It is an unsupported-format candidate, not guaranteed to fail by documentation. F must return exactly 0. If accepted, classify failed prerequisite and stop; no alternate tag, truncation or retuning. No query/status/end is issued after an observed zero F result; the next SDK operation is the known-valid B bind (last-error was copied immediately after F). If F unexpectedly succeeds, failure cleanup may end and release that allocated sample, without querying it.

Every bind is immediately followed by AIL_last_error and copying into an already allocated 8192-byte owned record, before any subsequent SDK operation. Log nullness, termination, byte count and hex; successful binds may leave stale error text, so text is observational, not an independent pass criterion. An oversized message is a stopped prerequisite, not a truncation silently treated as complete. All three full image buffers and independent suffix arrays are allocated before startup and live unchanged through sample release and vendor shutdown, including exception cleanup. No page protection, buffer mutation, free/reuse test, allocator fault injection, borrowed frame pointer or artificial image-retirement policy.

## Source and future build boundaries

`source-manifest.json` hashes probe, plan, pins and build helpers. `source-v1.tar` freezes those exact bytes and the manifest. `FREEZE-v1.json` pins both. Parent review must approve those exact hashes. No repair/retry may overwrite v1.

`build-once.py --approved-build-only` is prepared for a separate Windows parent-approved build. It checks pinned source/SDK/import hashes and uses copied existing build-receipt helpers. A new exclusive `native-build-v1` directory permits only one CL invocation, Release v120 x86 with /W4 /WX /showIncludes, including link against the possessed original API import library. No preceding compiler discovery or second configuration, no PE execution. It records actual include paths/hashes after the one compile; this is not a claim that unpinned system headers were independently hashed before compilation. Native compile correctness remains unverified now.

## Future runtime proposal, not authorized

Parent must inspect the build receipt and dumpbin imports before authorizing a separately pinned bounded runner. Verify original DLL SHA-256 from input-pins.json, exact staged path and matching loaded import module; stage only owned probe files/original runtime into a fresh private prefix and route audio to an owned null sink. Use a single process invocation with a short fixed timeout (suggest 15 seconds), no retries, no visible desktop takeover, exact command and complete stdout/stderr/exit receipts. No runner is supplied or launched in this source task. Do not use a newer bundled DLL as a substitute. The executable receives exact-original-dll-path and private-redist-directory arguments and checks the imported module path before startup; the runner must enforce the external binary hash pin. Runtime module/plugin identity and shutdown logs are required.

Retain exact raw outputs even when a precondition fails. A pass requires all four successful binds and exact expected query outputs, F=0, B recovery, release-returned and shutdown-returned, exit 0. This does not establish failure rollback, buffer-retirement boundaries, arbitrary format/codec behavior, asynchronous safety, playback fidelity or full client/host integration. Binder memory reclamation remains blocked on applicable contract or further separately reviewed evidence.
