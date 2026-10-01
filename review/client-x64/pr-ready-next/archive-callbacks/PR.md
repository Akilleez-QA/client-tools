# Match game archive callback indices on x64

Change the five CreatureObject/GroupObject archive callback declarations and definitions from `size_t` to `uint32_t`. On Windows x64, `size_t` is wider than the archive callback's existing `unsigned int` parameter, so the member-function pointer types do not match. The callback bodies and serialization remain unchanged.

One source commit on master `949451032647e45e42c3aaef3f41b132c8af36e3`: four files, +12/−10, no tooling. The exact original patch is retained. No wire-PR prerequisite is required: master's `AutoDeltaVector.h` already declares the same unsigned-int callback contract; `uint32_t` matches it on the intended Windows MSVC targets.

[Historical source/build checkpoint](https://github.com/Akilleez-QA/client-tools/blob/56ecc29fc95c62d10241b6cac0d8d9e713961db1/review/client-x64/allocator-math-next/RESULTS.md) identifies original commit `966365f945cd928dd4d0426b674f5a8563cc9fc4`. It is integrated evidence, not a fresh build of this master-based branch or a dedicated callback/gameplay test. No builds or runtime were repeated during packaging; this change alone does not qualify the full x64 client or wire compatibility.
