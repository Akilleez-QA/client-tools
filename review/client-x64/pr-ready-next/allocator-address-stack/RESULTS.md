# Allocator owner and stack address package

Published as [fork draft #3](https://github.com/Akilleez-QA/client-tools/pull/3), above [allocator layout/order PR #29](https://github.com/SWG-Source/client-tools/pull/29). Verified base `2af9f19b502e9183731656cdaf93236faacb404e`, head `fc667f38eafbd4a2b4d50f96a31efb5cca3ef55c`: three commits, 15 production files, +346/−149, with no test/build changes. [Description](PR.md) gives the module closure, evidence and limitations; [receipt](receipt.json) records exact source identities.

Primary and separate senior-engineer source reviews found no introduced blocker in the address/signature closure. That review is source analysis, not independent runtime corroboration. Historical native results are linked from the description and matched to the applicable source hashes. No fresh isolated build or runtime run occurred during packaging.

Rebuild diagnostic and allocator consumers together: Win32 allocator owner ABI is retained, while diagnostic stack signatures/layouts change. Allocation-size checks, statistics and null-reallocation behavior remain separate packages. Historical fault limits, optional optimized frame ancestry and concurrent DbgHelp teardown remain explicit.
