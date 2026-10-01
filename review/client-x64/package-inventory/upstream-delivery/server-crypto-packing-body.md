Draft pending the existing [server CI repair (#38)](https://github.com/SWG-Source/src/pull/38). The source change applies independently to `master`; this PR does not duplicate that workflow repair. Master’s inherited workflow has a known clone/checkout failure and is not evidence about this candidate. No successful upstream CI run or complete Windows server build is claimed.

Scope MSVC x64 C4103 suppression around the crypto PCH's vendor includes, preload `deque` and `memory` inside that scope, and restore the warning state afterward. No packing pragma, global warning policy or crypto algorithm is changed; the guard leaves Linux and Win32 behavior unchanged.

One original commit, **one header, +11/−0**, directly above upstream `master`. `FirstCrypto.h` has the same baseline on master and PR35, and the final header matches the maintained server counterpart. The large Crypto++ vendor refresh on the `64-bit-types` line is not a source prerequisite for this wrapper change and is not imported.

The [original record](https://github.com/Akilleez-QA/src/commit/78ec0f03f48cc6a71730ca8fcdf5ec3546c3a8d8) attributes historical layout, `/WX` and warning-restoration controls to the client. Complete server vendor trees differ between master and PR35, so matching the wrapper does not establish matching included libraries, layouts or native server behavior. This package makes no server compilation, ABI or cryptographic correctness claim from those client results.

No new build, tests, runtime or branch-head CI were run during packaging. The source delta and final header match the reviewed fork draft; its CI-only prerequisite is excluded. No SDK contents, binaries or vendor source refresh are included.

[Review packet and exact source identities](https://github.com/Akilleez-QA/client-tools/blob/de951450e45a8caf37cf3b8cea691aad36c75e54/review/client-x64/pr-ready-next/server-crypto-packing/RESULTS.md).


Upstream review identity: base `7d2159a337281184d6a55db30d2bc9a4013c0e80`, head `6e258f2f2f998821a2b53888de27789a66c9c243`. Removing the CI-only prerequisite changed no production blobs or source hunks.
