# Native86 observed results

The single authorized compile-only invocation passed all 28 new v120 objects: 14 x86 (COFF 0x14c) and 14 AMD64 (0x8664). Each recorded compiler exit is 0, with no /W4 /WX diagnostic. No link or execution occurred.

The actual public-wrapper symbol listing contains all 53 expected private Core delegates. The actual x86 host anchor adds AIL_open_stream, AIL_close_stream and AIL_stream_sample_handle imports to its existing startup/shutdown/driver/sample imports. Exact per-unit SDK import sets and required private dependencies passed; these are object dependency observations, not vendor behavior tests.

All 71 staged input identities match before/after records. The reused35 snapshot has all 9,536 recorded entries unchanged; pinned tools also match before/after. System header hashes were observed once per reached compilation and are not a before/after system-header attestation. The seven unchanged units excluded by the source/header closure were not rebuilt. External engine worker implementation remains unlinked.

Evidence: native-evidence-v1/curated/results/results.json, per-unit raw commands/compile logs/symbol listings/actual-includes.json, and curated before.json/after.json. Curated archive SHA-256: 4aea849150a0931db8ed7ceb20bd31324a7cf902d959e560cbf1d6281bebded2. Input manifest: 4c92251e90452ef7bbb65722b74224d19f0cd4ebe8b18bdd2566e67caa1a883e. Runner: f30dbcbd7eea61c1f33e86c34ddc53f6b4dcff434dade44d7e57c2e41ad8cf4d.

This gate does not establish SDK callback effects, stream/EOS quiescence, clean shutdown, Audio adoption, or an operational paired executable. Nine public exports remain absent. Portable85 and portable87 are separate bounded tests, not execution of this native graph.
