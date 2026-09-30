# Native38 owner gate: first-object compile failure

One approved runner invocation reached the owner TU and stopped on v120 error C2899 at session_file_owner.cpp:12: `typename cannot be used outside a template declaration`. The redundant typename precedes std::aligned_storage in the concrete FileRecord definition. Compiler exit2; the five remaining objects were not attempted. Zero objects were produced. No warning suppression, source repair, retry, linking or runtime occurred.

The actual include trace contains no forbidden SDK/engine/STLport headers. Since compilation failed, no owner COFF/import observation exists, and no claim is made about actual-job, file-channel, codec, Coordinator or host-context native compilation in this gate. Frozen input manifest19 entries and runner matched before execution and all19 hashes remained unchanged afterward.

Curated text ZIP SHA256: `adcf5ed61948890ab5842ddc901013ddc902f4066f30546410300b11323f7ef5`. Raw expanded command, compile log, actual includes, failed results and before/after input identities are under `native-evidence-v1/curated`. System headers were hashed during compilation only; no before/after header attestation. The staging Python tarfile future-default warning is separate from the compiler error.

The previous portable37 pass remains valid within its portable scope and did not establish v120 syntax compatibility. A separately reviewed successor can remove the redundant typename without changing the storage type/expression. This result is preserved; no successor or rerun is included here. Current job still uses canonicalServices. Product49d0 remains clean, and no engine, custom allocator workload, DLL load or native execution occurred. Compiler/tooling work is stopped.
