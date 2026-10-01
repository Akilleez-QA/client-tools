# Preserve native Miles widths and Audio diagnostic arguments

The Audio file callbacks and their bookkeeping used 32-bit handles where the Miles SDK declares pointer-width `UINTa`. Carry that type through callback declarations/definitions, the file map, next handle and debug tracking. Open status remains separate from the output handle; seek offsets and read counts retain their existing SDK types.

Read the mixer-channel preference into `SINTa`, reject values outside `int` before narrowing, and retain `size_t` for container-count diagnostics. Pass `c_str()` to the three speaker `%s` diagnostics instead of passing `std::string` through varargs.

Three source commits change only `Audio.cpp` (+28/−24), based directly on master `949451032647e45e42c3aaef3f41b132c8af36e3`. Head: `0699bd3d9b08998cb731d6ac7655681f3d003e6d`. Every added/removed line matches original commits `d0fea5bc79`, `25f7fff28d` and `681f337c3f`; no manual context adaptation was needed. No facade, pipe, backend-selection, TLS-lifetime or vendor-distribution changes are included.

Existing evidence:

- [Native callback results](https://github.com/Akilleez-QA/client-tools/blob/f2b8cbc8e93d5937edd743dbf76437e424f3ff7a/review/client-x64/vendor-next/audio-next/RESULTS.md): actual source compilation across Win32/x64 Debug/Release, real TreeFile callback slices with 18/18 Release and 20/20 Debug checks, and original x64 callback-type compile failures. Debug x64 evidence includes the separate allocator minimum-block repair.
- [Preference/count results](https://github.com/Akilleez-QA/client-tools/blob/f2b8cbc8e93d5937edd743dbf76437e424f3ff7a/review/client-x64/vendor-next/allocator-next/integration-current/audio-narrowing-plan.md): four native clientAudio project rebuilds passed with the separate Archive narrowing repair. SDK-type arithmetic checks cover representable limits; they do not exercise vendor returns or Audio's fatal path.
- [Original speaker diagnostic repair](https://github.com/Akilleez-QA/client-tools/commit/681f337c3f0064b831c4fd0ba10935daeaf024f5): all three string arguments are changed to character pointers, whose storage remains alive through the logging full expression.

Those native results belong to the recorded integrated source/dependency snapshots, not a fresh build of this master-based package. No builds or runtime tests were repeated during packaging. This is the native Audio prerequisite for the later facade adaptation, not a working x64 vendor runtime or complete audio qualification.
