# Add bounded Archive storage and decoder regression runners

Deliver the two regression harnesses omitted from the source-only [archive prerequisite, PR13](https://github.com/Akilleez-QA/client-tools/pull/13). Two original test commit units add **six files, +424/−0** above `085a62e3358e7b51c5198c93bb1581864020c3fb`; production and workflow files are unchanged. Fixtures, runners and READMEs are byte-for-byte copies of their original commits.

The ByteStream fixture checks logical read limits, initialized small-buffer self-append, copy-on-write, reserve and pool reuse: **85 checks per ABI**. The decoder fixture checks short/long strings, embedded zeros, byte-stream append, odd-offset Unicode, incomplete headers and insufficient payloads: **34 checks per ABI**. Rejected payload lengths preserve destinations while leaving successfully read headers consumed.

From a Linux checkout with Python 3, MinGW-w64 C++ and Wine:

```sh
python3 tools/test-byte-stream/run.py --bits 32 --artifacts artifacts/byte-stream-32
python3 tools/test-byte-stream/run.py --bits 64 --artifacts artifacts/byte-stream-64
python3 tools/test-archive-decoders/run.py --bits 32 --artifacts artifacts/decoder-32
python3 tools/test-archive-decoders/run.py --bits 64 --artifacts artifacts/decoder-64
```

Use fresh artifact directories and the README's Wine architecture/prefix options where required. Each runner compiles this checkout's real ByteStream and Windows mutex; the decoder runner also compiles UnicodeArchive. They need no integrated core/STLport providers. A failed rebuild cannot run a stale executable. Acceptance requires the correct PE machine, exit zero and exactly one expected stdout verdict; manifests retain source/tool identities, commands and executable hashes.

Historical [ByteStream evidence](https://github.com/Akilleez-QA/client-tools/blob/115d618f039a7fb36350611c104e9cb25d45e60c/review/client-x64/vendor-next/bytestream-next/CANDIDATE.md) and [decoder evidence](https://github.com/Akilleez-QA/client-tools/blob/115d618f039a7fb36350611c104e9cb25d45e60c/review/client-x64/vendor-next/bytestream-next/raw-decoder-review/CANDIDATE.md) retain the portable checks and separate native v120 provider-based qualification. The saved portable fixture hashes match this package. Their complete input snapshots predate later archive changes: the 85-check manifest differs in Archive.h/AutoByteStream.h; the 34-check manifest differs in AutoByteStream.h and the later Unicode writer guard. This is historical evidence, not a new build of this branch. Native records used their documented integrated providers and separate commands.

No builds or runtime checks were repeated for packaging, and no new CI jobs are added. These bounded fixtures do not establish allocation-failure guarantees, huge-input processing, full iterator-invalidation detection, nested-message rollback, shared-stream thread safety or full-client acceptance. Historical native link/verifier failures remain in the evidence.
