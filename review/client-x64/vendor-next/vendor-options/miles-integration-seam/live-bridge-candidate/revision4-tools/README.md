# Revision 4 build receipts

This revision improves the source/build/output identity record. It does not change the bridge or establish additional Miles behavior. The v3b evidence is frozen. None of the newly built v4 executables has been executed.

`build_receipt.py` creates a new output directory and builds the four native v120 configurations. For each build it:

1. Discovers the actual transitive headers using `/showIncludes /Zs` with the same configuration flags. This performs syntax checking without linking or executing anything.
2. Hashes the frozen local C++/header snapshot, discovered headers (including private SDK and compiler headers), selected compiler/linker tools and companion DLLs, and candidate default/import libraries before compilation.
3. Records exact argument vectors, working directory, selected PATH/INCLUDE/LIB environment and discovery/compile exit codes.
4. Runs the actual compile/link with `/showIncludes` and `/VERBOSE:LIB`. Immediately after a successful link, records PE machine and SHA-256.
5. Re-hashes the same inputs, rejects changed inputs, new header dependencies or unrecorded searched library paths, and records whole-matrix source/builder stability.
6. Writes a new receipt once, makes it read-only, and prints its content digest for an external trusted record. The adjacent digest file is convenient output, not an independent trust anchor.

The receipt verifier requires that external digest and validates both selected executables against their exact configuration, machine and build-time hashes. It uses the receipt's frozen input record; it never hashes current source after runtime and presents that as a build input. Staged executables may live at different paths, but their bytes must match. `launch_verified.py` defaults to verification only. Its separate `--execute --media` mode is intended only for a separately authorized runtime; that mode was not used here.

## Observed result

The fresh four-way compile matrix passed; inputs were unchanged and every observed searched library path was covered by a pre-build hash. Each configuration records 37 local source/header files. Win32 discovers 235 transitive headers and hashes 30 tool files; x64 discovers 225 headers and hashes 45 tools. Link-input snapshots contain 20 candidate libraries for the host and 19 for the controller, with observed search paths recorded separately.

Pinned receipt SHA-256:

```
2c33ad61aefc720d739b7e210680fd433ab939eb9cfe733db91bc94fc2c64569
```

| Output | Build-time SHA-256 |
| --- | --- |
| Debug x86 host | `2199e486295a921f145e71aea449710c4e45ccc6101667ddf04a37a7e9d5a8c1` |
| Debug x64 controller | `6ee25838a832706190b7b534be378a01bb98a2496375a168ad016888d9c2a784` |
| Release x86 host | `d8f8406cc6f03eeb91df43b33a441c5897a02a57040e3f39c3f54be0d7283c8b` |
| Release x64 controller | `f5d3a1ff2ca26f603a9b641961e5b8aa55efccf332b3d08511cd7ef87117da35` |

Verification-only checks accepted both real pairs without launching a process. Fourteen pure Python controls passed on Linux and the native Windows Python runtime: changed receipt, changed/missing output, wrong machine, duplicate/missing configuration, unsuccessful compilation, changed inputs/builder, missing header provenance, and separation from mutable current source. Synthetic PE headers used by those controls are never executed.

An initial tools startup attempt failed before compilation because the embedded Windows Python does not automatically include the script directory on `sys.path`. `startup-failure-v4.txt` preserves this. The v4b entry points explicitly add their own tool directory; the fresh compile matrix is identified as v4b. No earlier compile/runtime evidence has been relabeled.

## Reproduction

Use the private frozen source snapshot and genuine local SDK/import library. No private SDK, vendor binary or media is included here.

```
python build_receipt.py --source C:/frozen-source --output C:/new-receipt-build
python test_receipt.py
python launch_verified.py --receipt C:/new-receipt-build/receipt.json --receipt-sha256 <externally-recorded-digest> --configuration Debug --host C:/new-receipt-build/x86-Debug/host.exe --controller C:/new-receipt-build/amd64-Debug/controller.exe --record C:/new-verification.json
```

`evidence-native-v4b/` contains text-only receipts, commands, logs and verification records. Vendor headers/import libraries are represented by paths and hashes, not their contents. Executables and object files remain private on the VM.

## Limits

This is a trusted-builder receipt with an externally pinned digest, not a digital signature or an adversarial supply-chain attestation. It does not protect against a malicious compiler, an operator replacing both the receipt and its external trust record, or source files changed and restored between observations. The launcher checks executable bytes immediately before launch but does not provide an atomic, race-proof file-to-process binding against concurrent hostile writers. Use an isolated stable staging directory.

Header discovery records the headers actually reached by these configurations, not every possible preprocessor branch. Tool identities cover selected v120 executables and companion files; this is not a complete OS/loader attestation. An observed link-search census and pre/post library hashes bind this successful matrix, without claiming unused libraries were linked. Build paths and timestamps can change PE hashes; this is not a deterministic-build claim.

The old v3b runtime results remain attached to their old binaries and manifests. The new v4 output hashes do not retroactively strengthen them. No vendor, audio, game, playback, callback or full-client workload was run for this revision.
