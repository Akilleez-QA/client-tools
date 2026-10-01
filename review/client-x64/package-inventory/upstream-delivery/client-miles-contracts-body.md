Adds the SDK-header-free ClientMiles declarations, explicit little-endian frame codec, generation-bearing resource registry, owned replies, metadata/buffer formats and EOS completion/consumption validation. The private paired protocol remains version 3, with resource kinds through File; this does not alter the SWG network protocol.

This source-only package adds 17 production files (+1248/−0). Review base: `949451032647e45e42c3aaef3f41b132c8af36e3`; head: `8ebfbe2c8b8f7efa72250558ea45cba208c43f6f`. It starts directly from maintained master.

The unchanged EOS protocol test is included (+111 lines). The master base has no wire-compatibility workflow, so its original CI hunk is deferred until that prerequisite exists.

Introduced files match their pinned pre-Bink blobs byte-for-byte except the standalone comment clarifications in `ClientMiles.h` and `protocol/miles_wire.h` from foundation 1. Existing notices are preserved; all non-comment source lines are unchanged. [Historical core checkpoint](https://github.com/Akilleez-QA/client-tools/commit/d1c5903de35586dc8cfb0939a5da1756cca43179) records their source provenance; the per-file receipt retains exact revision/blob/SHA-256 identities. Later Bink and game-selection edits are not imported.

These foundations are dormant: no existing project, game backend selection, build script or workflow changes are included. The unchanged complete build entry points arrive only in step 7 after the source closure exists. The existing portable EOS test passes **298 checks** on this exact branch using Clang with AddressSanitizer and UndefinedBehaviorSanitizer on Linux. This checks completion/consumption message validation with the isolated source closure; it does not run the engine, vendor DLL or pipe transport. Other integrated evidence remains historical. This branch does not independently enable audio or establish callback fidelity, shutdown behavior or heap safety.

Reproduce the portable protocol check from the repository root:

```sh
clang++ -std=c++11 -Wall -Wextra -Werror -fsanitize=address,undefined \
  tools/miles-bridge/tests/eos_protocol.cpp \
  tools/miles-bridge/src/eos/eos_protocol.cpp \
  tools/miles-bridge/src/wire/codec.cpp -o /tmp/miles-eos-protocol
/tmp/miles-eos-protocol
```

[Exact source identities, review boundaries and available results](https://github.com/Akilleez-QA/client-tools/blob/1aa5f76ced9f11bcbe9c0d4263d67e5dd07c6455/review/client-x64/pr-ready-next/miles-contracts/RESULTS.md).
