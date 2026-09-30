# Native47 component gate passed

One approved invocation compiled exactly three new v120 AMD64 objects: invocation_guard, file_channel and ClientMilesPipe. All exited0 with no warnings/errors, no SDK/engine/STLport include contamination and no AIL undefined dependencies. Each actual COFF machine is0x8664; independently reread object hashes match receipts.

Raw symbol evidence defines Scope construction/destruction/admitted/violated and requireForwardAllowed in the guard object, alongside an undefined `_tls_index` reference. This was the real MSVC __declspec(thread) source branch, with no substitute macro. File-channel references Scope ctor/dtor/admitted/violated; ClientMilesPipe references requireForwardAllowed. `compact-attribution.json` reparses actual logs and records exact source/object/log hashes and those symbols.

All29 staged inputs and pinned compiler/dumpbin/vcvars hashes were unchanged before/after. Raw results SHA256 `3a1b24cd677b80f266eeb07e68dfa48db7cb50f17ea788bb1af8a4915a2fe901`; curated text ZIP `2cc7d43a63539f1fd81ddf8a1c613956f5008fa8085254c2000b2df8da1cb848` contains21 files. Raw commands, compile/include/symbol logs, results and input identities remain in native-evidence-v1/curated. System headers were hashed during compilation only; no before/after system-header claim. Objects/PDB remain private.

No tests were staged or compiled, no existing objects were reused, and no linker, executable, SDK load, engine/Audio/custom allocator workload or product adoption ran. The portable47 v1 link failure remains preserved and v2's portable success remains separate evidence. This native gate establishes compilation and guard dependency placement, not operational reentry/lifetime behavior in the engine. Product49d0 remains clean and tooling has stopped.
