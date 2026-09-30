# Server semantic mirror

Applied only ByteStream.cpp/.h to previously clean local server fork. Same algorithms as accepted client isolated candidate; preserved uint32_t readSize/targetSize API and Data::size, server mutex include spelling, exception/cstdint includes, nullptr comment/string. Both candidates use pointer-width sentinel. No commits/pushes.

Existing server wire runner:19/19 on -m32 and20/20 on -m64. MissionListResponse remains explicitly not run without full same-ABI libraries. Same85 bounded initialized-storage probe passes each ABI with server's actual pthread mutex and uint32_t read API. Probe uses only small sizes, no ULONG_MAX truncation or mismatched-width assertion. Arithmetic-only81pair experiment remains separate from actual buffer allocation tests.

Source/diff identity: server-mirror-manifest.json, server-candidate.patch. git diff --check clean. Remaining client/server differences were inspected and match preserved pre-existing width/include/comment differences. No AutoDelta or raw-pointer packet decoder changes; no generic transaction guarantee.
