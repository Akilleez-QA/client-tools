# Sample host source and portable result

Implemented two isolated overlays on the exact frozen live27 source composition: ResourceRegistry reservation/publication/cancellation and actual Backend allocation/query/end/release integration. Allocation tracking is prepared before vendor work; native success immediately enters a stack PendingSample owner, then allocation-free publication transfers tracking to the registry. A null vendor result cancels unpublished storage. Release invokes the SDK before retiring identity. Confirmed shutdown retires the driver and invalidates its tracked sample children. Existing driver opening now reserves before vendor work too.

The pre-frozen portable gate passed first invocation with strict C++11 warnings and ASan/UBSan. Tests cover unavailable reserve storage before simulated side effects, no-allocation publication/cancellation/retirement, exact-registry token binding and consumed-token rejection, cancellation, parent validity, stale generations, vector relocation, 256 sequential cycles with capacity2, generation exhaustion and existing borrowed alias invalidation. These tests execute authored registry code only, with inert local addresses. They do not invoke or mock the vendor SDK or prove actual host execution.

Source archive SHA256: `050fa0df52f6a81f529aa701307219c25a801bfd0133cc655b853a740fedbffc`.
Manifest SHA256: `70d84b2f848bbcc234fc0f7c69dd5f80f0e72effee614d160b539e7623c0a836`.
Portable receipt SHA256: `35bd8857d3f07f0314a628b636dd5a0230cc47151e6f4ed4858b6638f46c8b94`.

No VM/native/vendor/engine execution occurred. Actual Backend source awaits v120 compilation and original-DLL evidence in a separately reviewed composition with repaired client sample-pipe29. Native-sample27 declares the source operations; no borrowed stream sample is created by this Backend. Named binding/rebinding, playback, EOS and callback registration remain absent. There is no callback-quiescence claim. Memory exhaustion closes the host path before vendor allocation, while the remote client observes channel uncertainty; this is not graceful resource-exhaustion recovery or complete fidelity.

The legacy registry insert API remains for prior, noncomposed users; all owned samples allocated by THIS Backend use parent-required reservation. Registry identities are session-private; session/coordinator binding remains outside the registry. Slots are reused, with the original finite slot/generation namespace retained and no cumulative lifetime cap added.
