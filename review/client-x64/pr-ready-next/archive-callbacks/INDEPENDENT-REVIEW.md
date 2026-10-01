# Independent review — archive callback indices

No introduced blocker found. Reviewed master 949451032647e45e42c3aaef3f41b132c8af36e3 to e26bdd9b2fa64d0ef46e6af9aab328deb18c29a5 by explicit refs. Four files, +12/−10. All candidate hashes match the receipt and added/removed lines exactly match original 966365f945cd928dd4d0426b674f5a8563cc9fc4.

Master AutoDeltaVector already declares and invokes its member callbacks with unsigned int indices. On the intended MSVC Win32/x64 targets, uint32_t is that unsigned-int type, so the new declarations/definitions match the existing pointer-to-member signatures. CreatureObject registers attributesOnSet through setOnSet; GroupObject registers all four insert/erase functions through the corresponding vector setters. The bodies, registration, object ownership, value-reference parameters and serialization are unchanged. Explicit stdint.h includes supply the new spelling. Win32 size_t was already unsigned int; x64 now uses the archive's fixed-width index instead of native pointer width.

No wire-PR or other new source dependency is needed. This is a source API correction, not a claim that arbitrary 32-bit integer typedefs have interchangeable function types on every compiler. The PR expressly confines its type assertion to Windows MSVC and accurately labels the checkpoint as historical integrated evidence without a dedicated callback/gameplay or exact-master build claim. No evidence wording blocker found.

Only this report was written. No source edits, tests, builds, runtime, remote actions or descendant agents. Public URL reachability was not rechecked.
