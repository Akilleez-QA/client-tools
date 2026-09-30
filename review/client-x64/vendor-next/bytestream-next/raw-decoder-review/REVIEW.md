# Raw archive decoder preflight review — 2026-09-30

Read-only inspection after ByteStream client8d9010900/server7131fd38 repair. No malformed raw-pointer decode was executed, no production edits.

## Active sites

| Decoder | Header | Access before checked advance | Preflight today |
|---|---|---|---|
| Archive.h `get(ReadIterator&, std::string&)` | uint16 byte count; sentinel65535 followed by uint32 | constructs string from raw pointer and declared byte count | absent; header reads checked, pointer starting position checked, payload extent not checked |
| Archive.h `get(ReadIterator&, ByteStream&)` | uint32 byte count | target.put(raw pointer,declared bytes) | absent; target append arithmetic checked, source payload extent not checked |
| UnicodeArchive.cpp `get(ReadIterator&, Unicode::String&)` | uint32 code-unit count | target.assign(typed pointer,typed pointer+count) | absent; multiplication and payload extent only encountered after typed-pointer assignment |

ByteStream constructor from ReadIterator copies source.getSize(), so its raw access is bounded by actual remaining size; not the same declared-length issue. Archive writers from ByteStream/ReadIterator likewise use actual remaining size. Historical src/solaris/Archive.cpp contains raw string code but is not in active archive Windows vcxproj; do not conflate it with the current inline overloads. UnicodeArchive.cpp is explicitly compiled by unicodeArchive project. ChatOnRequestLog's Archive::get(ChatLogEntry&) calls the string/Unicode overloads through actual member types, demonstrating network-message reachability; this is not a claim that every network entry point has been mapped.

## Narrow proposed repair

Use existing `source.getSize()` preflight rather than a new public helper/API for just three sites:

- string and ByteStream: after reading the length header and **before any target mutation/raw payload access**, throw existing `Archive::ReadException` if declared bytes > source.getSize(). Then perform current copy and advance.
- Unicode: before multiplying or constructing a typed end pointer, compare declared units > source.getSize()/sizeof(Unicode::unicode_char_t). This ensures product fits remaining unsigned-int byte extent. Compute explicit unsigned-int byte count only after that bound.
- Handle zero units/bytes explicitly so an empty payload does not form a range by arithmetic on a null pointer. String/Unicode clear; ByteStream append-empty leaves its contents unchanged, preserving append semantics.

Header bytes remain consumed on rejection under this minimal policy. A temporary ReadIterator could instead make iterator advancement atomic, but that is a separately chosen stronger behavior, not necessary for payload bounds. Destination retains previous contents when preflight rejects. Allocation failures inside assignment/append follow those containers' contracts. Outer message may already have changed earlier members: no full decoder transaction or retry guarantee.

## Unicode alignment deserves explicit treatment

Unicode::unicode_char_t is unsigned short (2bytes on both Windows ABIs); raw payload can follow an odd number of preceding bytes. Existing reinterpret_cast-and-dereference therefore assumes alignment. Prefer a suitably sized temporary Unicode::String and a bounded byte copy through source.get into its contiguous storage, then swap/assign, if actual legacy STLport storage guarantees are confirmed. Otherwise keep alignment as an explicit separate issue rather than claiming preflight fixes it. This is not a proposed reinterpret_cast to a wider pointer.

## Related writer boundary, separate decision

Unicode writer checks code-unit count with ArchiveCount::fromSize<unsigned int>, then calls target.put(source.data(),size*sizeof(unit)). That count check does not ensure the **byte** count fits ByteStream's unsigned-int API. Need count<=UINT_MAX/sizeof(unit) before multiplication and before header publication if repairing the writer. No massive string is needed to test the arithmetic helper; do not fabricate a giant object or pass a truncated ULONG_MAX and count it as coverage.

## Prospective bounded acceptance

Candidate only, all backing buffers fully initialized and small. Valid empty, one-character, embedded zero, multibyte Unicode code units, short/long string boundary headers, and exactly remaining bytes preserve legacy bytes/values. Place Unicode after a one-byte prefix to exercise alignment handling if included. For rejection tests after preflight exists, declare one byte/unit beyond remaining in a small buffer and require ReadException **before target changes**, explicitly record header-consumed iterator position. Test incomplete headers through existing checked scalar reads, and a nonempty destination ByteStream to preserve append semantics. No unsafe old-code execution. Existing wire suites and both native widths remain required. Nested message partial-state behavior stays separately documented.
