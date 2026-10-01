# Support Windows x64 byte-order conversions

MSVC x64 rejects the naked inline-assembly implementations of `htonl`, `ntohl`, `htons` and `ntohs`. Use the corresponding 32-bit and 16-bit byte-swap functions under `_M_X64`; preserve the Win32 implementation and public signatures. The production change is one file, +26 lines; regression tooling and CI are separate commits.

**Prerequisite:** [client imemmove PR #25](https://github.com/SWG-Source/client-tools/pull/25). This fork package is based on its submitted head `a7954b5e7`. An independent master submission must wait for or reconcile that dependency; the aggregate master diff currently includes the prerequisite.

The actual production translation unit passes 166,631 input cases in both directions in Win32/x64 Debug/Release. The native VS2013 run and [hosted MSVC matrix](https://github.com/Akilleez-QA/client-tools/actions/runs/36829714456) each meet all ten expected outcomes: four candidate passes, two original Win32 passes, two original x64 assembly compile failures, and two deliberate no-swap failures. The fixture also verifies production symbol binding and object architecture. [Earlier commands and evidence](https://github.com/Akilleez-QA/client-tools/blob/e515a78f54abf71bf677fd6f9e46dcc9ba662bfb/review/client-x64/pr-ready-next/byteorder/REPRODUCTION.md) are retained.

The first hosted run passed the conversion cases but failed its negative-control classifier on modern compiler parser cascades. The correction recognizes only the observed code/location pairs in the pinned original source, still rejects unrelated build errors, and passes 30 classifier checks. That failed run remains preserved.

The standalone link suppresses an unused legacy STLport default-library directive; it supplies no replacement headers, allocator or STL implementation. This establishes bounded conversion behavior, not a complete library/client build or packet/gameplay behavior.
