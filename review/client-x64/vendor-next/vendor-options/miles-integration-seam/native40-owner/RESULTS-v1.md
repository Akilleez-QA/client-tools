# Native40 runner startup failure preserved

The approved invocation failed at the sibling symbol_parser import before any compiler invocation. Raw Python traceback in native-evidence-v1/04-native-matrix.log reports ModuleNotFoundError. Staging verified all21 input files including symbol_parser.py; its absence from Python import search is the concern, not a missing staged file. Embedded guest Python commonly isolates sys.path; this cause remains an inference until its path configuration is read. No repair or retry occurred.

Zero of five objects were attempted. The reused-owner precheck was not reached because the import precedes it; do not claim native40 revalidated owner39. No results/results.json was created. Collection independently rehashed all21 staged inputs with no changes and retained before/after manifests; object count0. Curated ZIP SHA256 b9617bf48b560afb89bdfc7c3b259354d4fbc68c6731d8c215ed33c0224cc52a. The outer command log records runner exit1 and completed evidence collection.

Native39 raw parser-oracle failure stays preserved. Local parser tests and source correction remain separate evidence, not a completed native gate. No compiler, link, engine runtime, SDK load or custom allocator workload occurred. All source inputs remain unchanged; compiler/tooling work has stopped.
