Scope MSVC x64 C4103 suppression around the crypto PCH's vendor includes, preload `deque` and `memory` inside that scope, and restore the warning state afterward. No packing pragma, global warning policy or crypto algorithm is changed; the guard leaves Linux and Win32 behavior unchanged.

One original commit, **one header, +11/−0**, above the published [master workflow repair](https://github.com/SWG-Source/src/pull/38). `FirstCrypto.h` has the same baseline on master and PR35, and the final header matches the maintained server counterpart. The large Crypto++ vendor refresh on the `64-bit-types` line is not a source prerequisite for this wrapper change and is not imported.

The [original record](https://github.com/Akilleez-QA/src/commit/78ec0f03f48cc6a71730ca8fcdf5ec3546c3a8d8) attributes historical layout, `/WX` and warning-restoration controls to the client. Complete server vendor trees differ between master and PR35, so matching the wrapper does not establish matching included libraries, layouts or native server behavior. This package makes no server compilation, ABI or cryptographic correctness claim from those client results.

No new build, tests, runtime or branch-head CI were run during packaging. PR38 supplies repaired inherited master CI; it does not qualify the Windows branch of this header. No SDK contents, binaries or vendor source refresh are included.
