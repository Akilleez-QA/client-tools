# Native47 component gate: locally frozen, not run

Three prospective v120 AMD64 Debug objects only: actual invocation_guard.cpp, changed file_channel.cpp and ClientMilesPipe.cpp, copied byte-for-byte from callback-reentry47/portable-composition-v2. Every copied source/header is checked against composition-freeze-v2 SHA `9e7ba0585236311cdaf0bbecd2da9fa8365a92a468b5f04213c3b4ad1d3093ea`. Tests and portable test runners are excluded. The closure includes real metadata_wire/session-version/codec source dependencies for identity only; they are not compiled or linked in this three-object gate. No previously built object is reused, avoiding a false linked-composition claim.

Fresh proposed destination C:/native47-components. After root authorization only:
`C:/ci-dpvs-review/python/python.exe C:/native47-components/run-native.py --approved-compile-only`.

Input29 manifest `3414158ffd2ec9d6d9ba5d123b417eb13f54fe89b76ec1e850f9494cede82ffb`.
Runner `ec1de45d21fe028e3f241e3563099ae411b937ec123548a8706dba5aa30fa34e`.
Exact flags.json inherited unchanged from native46: actual v120 AMD64 /W4 /WX /EHsc /MTd /Od /Ob1 /RTC1, same modern-TU flags/definitions, no extra includes/macros. Forced guard requires actual _MSC_VER1800 and _WIN64. No fake Windows header, portable TLS substitution or fabricated calling-convention definition enters staging. MSVC therefore selects the authored __declspec(thread) branch.

Required raw symbols: invocation-guard defines Scope constructor/destructor and requireForwardAllowed and references `_tls_index`; file-channel references Scope construction/destruction/admitted/violated; client-pipe references requireForwardAllowed. Every object must be actual COFF0x8664, contain no AIL undefined dependency and include no SDK/Mss.h, engine source/STLport or snapshot headers. Native46 compiler/dumpbin/vcvars identities are pinned and compared to the selected tools. All inputs/tools are hashed before/after; system-header hashes remain single-time compile observations. Stop first unexpected failure, preserve logs and do not retry or suppress warnings.

No VM action has occurred during this preparation. Object/PDB artifacts remain private if a gate is later approved; curate raw command/log/include/symbol evidence. No linking, executable, SDK load, engine/Audio/custom allocator workload or product changes. Portable47's preserved first link failure and second portable result are separate evidence and do not prove these real MSVC object properties.
