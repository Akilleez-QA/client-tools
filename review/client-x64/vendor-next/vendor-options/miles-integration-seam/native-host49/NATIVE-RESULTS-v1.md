# First native host49 gate

One authorized six-object matrix passed: file_tokens.cpp, reply_transaction.cpp and file_protocol.cpp each compiled once with actual v120 x86 and AMD64 compilers. All six exits were zero, with no compiler diagnostics. Raw object machines were respectively 0x14c and 0x8664. No repair or retry occurred.

Raw command and dumpbin evidence was independently inspected. Both token objects emit ResourceRegistry reserve/publish definitions; both transaction objects reference real decodeReply/copyRead and expectFileAck/encodeFileConsumptionAck; both protocol objects define ACK functions and reference encodeCallInto. Other required decorated-symbol checks passed. These are emitted definitions/references, not a linked call graph.

All 19 frozen inputs and pinned tools remained unchanged. Curated archive SHA256: fee891200a444396afd5e2995adf054622b8c91a7d05a6a7b0075bef6d9d04c4. Raw evidence is under native-evidence-v1/curated/results. Include hashes are single-time observations; system headers were not post-hashed. Staging emitted a Python tar extraction deprecation warning; compiler logs contained no compiler warnings/errors.

No SDK headers/imports, thunk ABI, link, executable, engine or runtime gate. Objects/PDB stayed on the VM. /Ob0 is the reviewed inspection delta from native47 /Ob1.
