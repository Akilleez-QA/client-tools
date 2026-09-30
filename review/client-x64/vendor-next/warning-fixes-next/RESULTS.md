# Two bounded warning candidates, uncommitted

POODO scope follows the immutable94a81438 warning review and parent's authorization. Client throwaway `/home/akilleez/Work/swg-source/client-warning-candidate` detached at782aed355. Matching server changes authored first in server-client-compat; preserve every unrelated difference. Separate root-cause patches and exact current file hashes in this folder. No Archive.h, UnicodeArchive.cpp, UI pool, feature or provider changes. No commits/pushes.

## Crash address

Only SetupSharedFoundation.cpp `%08x=addr` becomes `%p=addr`; ExceptionAddress is already PVOID. Both client and server counterparts changed identically. Exception-code format/labels unchanged.

Synthetic fixture extracts the exact production sprintf statement into a real Windows EXCEPTION_RECORD/EXCEPTION_POINTERS setup. Uses null,1,max uintptr and a patterned high address, without dereferencing it or crashing. Native v120 /W4 /WX Win32/x64 Debug/Release: **36/36 each**, buffer canaries intact. x64 prints1234567887654321 in full; Win32 still prints eight hexadecimal digits. This is an extracted-statement test, not a full Foundation rebuild or actual crash handler run. First probe mistakenly compiled an x64 constant in Win32's unused ternary arm and failedC4310; preserved native v1 failure, fixed probe with explicit ABI conditional; production patch unchanged.

## AutoArray/AutoList count headers

Only the two pack count assignments use `ArchiveCount::fromSize<unsigned int>` before Archive::put writes the header. Unsigned32 legacy type retained. Existing Archive.h provides the helper; no new include or unrelated cleanup. The changed expressions are identical across repos.

Actual candidate AutoByteStream.cpp/ByteStream.cpp/header, real pthread ArchiveMutex: host client **29/29-m32,30/30-m64**, server **29/29-m32,30/30-m64**. Fixtures pack0–3 actual unsigned-byte elements into real AutoArray and AutoList, compare a seeded destination to explicit little-endian legacy bytes, unpack and require full consumption. Previous client HEAD header/AutoByteStream.cpp Win32 control passes29/29 against same expected bytes. No giant allocation or fabricated container.

One check perABI exercises helper UINT_MAX acceptance. Only64-bit has an additional helper UINT_MAX+1 rejection check;32-bit prints SKIP and does not count rejection as pass. **This is not oversized-container rejection at the real pack sites.** Order of checked conversion before first header write is established by source inspection. Allocation failure during element serialization can still leave partial output. Native v120 full Archive/client matrix remains a separate integration check.

## Review scope

Root1 crash formatting: one changed line per repo.
Root2 count checks: two changed lines per repo.
`git diff --check` passes. Keep these independent; do not fold UI allocation-pool work or nested transaction changes into either.

## First-class wire regression coverage

Promoted small-container cases into existing tools/test-wire-compatibility/fixtures.cpp: AutoArray/AutoList at counts 0,1,3, 12 checks total. Each encoder appends to a seeded destination and must match literal legacy unsigned32 header/payload bytes. Each decoder reads the independent literals and must return all elements with no trailing bytes. No duplicate helper checks; strict expected common runtime count rises58→70. README updated. Workflow unchanged.

Fresh real PE builds and Wine runs: candidate Win32 **71/71**, candidate Win64 **78/78**, pristine stock949451032 Win32 **68/68**. All three runner exits0. Stock's3 known absent helper checks remain explicit omissions; no absent test counted as pass. Exact compiler commands, tested TU hashes and raw outputs in first-class-{32,64,stock32}/commands-*.jsonl; concise stdout logs adjacent. These are clang/MinGW/Wine results, not native MSVC full-client rebuilds.
