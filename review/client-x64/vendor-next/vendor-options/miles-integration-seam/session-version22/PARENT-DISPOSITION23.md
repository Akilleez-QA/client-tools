# Parent disposition of the module-identity finding

The revision21 review identified a real API-contract gap: a basename query did not establish that the original SDK macro selected the held module. Revision22 removes that mechanism. The adapter now passes its supplied HMODULE directly to LoadStringA. Parent inspected the small implementation and checked source archive, build receipt and runtime-results hashes against the published identifiers. The independent senior23 reviewer repeated only the portable tests; existing native observations remain a shared evidence family.

The finding is closed for basename selection within this adapter. Its caller must still verify and hold the module. The two identical resource mappings demonstrate operation outside the normal basename namespace, not a wrong-version distinction between different DLLs. This does not supply integrated module ownership or a complete client backend. Keep revision21 and its finding intact.

Research supporting the correction: Microsoft GetModuleHandleA documentation states selection is unspecified with duplicate basenames; LoadLibraryA documents first-loaded basename matching; LoadStringA accepts the explicit module handle. See revision21/PARENT-DISPOSITION22.md for the research record. The new implementation avoids the ambiguous lookup rather than adding a general loader framework.

Next use is a separate, bounded framed startup experiment. Product49d0 stays unchanged and the failed original-engine teardown baseline stays failed. No vendor, engine or allocator workload was executed by this parent inspection.
