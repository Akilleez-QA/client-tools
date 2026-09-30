# Independent parser integration review

2026-09-30. Read-only review of client-parser-integration source, native results and original client configuration. No VM mutation. No production blocker found in the scoped provider builder. Final MSBuild integration evidence remains necessary as already planned.

## Verified choices

- PCRE is actual4.1, pinned archive, generated header checked against original repository header. SUPPORT_UTF8 is explicit, and native smoke asserts UTF8=1,newline10,linksize2 before ordinary and UTF8 matching. Earlier no-UTF8 candidate is not the proposed integration. This is not a modern PCRE substitution.
- libxml uses actual2.6.7, not bundled older2.4.28. Source header comparison records43 normalized-identical headers; generated xmlversion configuration is the known exception. The provider flags match the checked-in libxml-configure-win32.bat exactly for ftp/http/html/c14n/docb/iconv/sax1/legacy and Debug/Release CRT/memory/XML debugging. Removing obsolete /OPT:NOWIN98 is a toolchain adaptation, not a removed parser capability.
- XML remains DLL/import ABI. Actual sharedXml project includes2.6.7 headers and uses imported xmlFree data; changing to static declarations would be a different repair. Smoke assigns XML allocator hooks, creates/parses/dumps/frees documents and calls imported xmlFree. The caller CRT owns allocations through passed function pointers; keeping an authentic DLL preserves that contract.
- SwgClient-only import occurs in generated x64 props. Win32 production providers are untouched. BeforeTargets=Link plus failed Exec should stop Link; AfterTargets=Link copies the matching DLL. The named old dependency replacement preserves unrelated libraries. Exact evaluated Link metadata and copy execution are still build-agent checks, not inferred final-link proof.
- Missing/mismatched archives fail before output creation; isolated output ownership rejects other checkout/configurations and unowned contents. Directory lock is released on exceptions; a killed process leaves a lock requiring investigation, rather than silently reusing output. No fallback to old provider on failed build is coded.

## Decision-relevant limits

1. **Do not equate smoke hooks with the game allocator lifecycle.** The smoke uses CRT callbacks; actual SetupSharedXml.cpp uses new[], delete[], DuplicateString and MemoryManager::reallocate. The known null/array ownership audit is independent and not repaired or exercised here. This does not invalidate import-data/callback ABI evidence, but full client setup/parse/shutdown still needs its own result.
2. **Publication is not a transactional directory switch.** Individual os.replace calls publish three products before manifest publication. An interrupted publication can leave an old manifest with some new files. The current MSBuild invocation fails and must not continue to link; a later normal invocation rebuilds every provider. External manual consumers must not trust an old manifest after failure, and parallel consumers of a directory across revisions remain unsupported as documented. No observed stale-provider success; this is a limitation rather than a reason to redesign the bounded builder.
3. **DLL deployment is part of acceptance.** A successful smoke runs next to its own DLL; a successful import-library link alone does not establish the final SwgClient output directory has that DLL. Require the planned evaluated-property/copy test, including DLL hash and architecture, before describing integrated deployment as proven. Failed linking leaves any prior executable/DLL on disk; do not run those and label them the failed build's output.
4. **Feature and header evidence is bounded.** PCRE smoke is one UTF8 expression, not an exhaustive corpus. Original libxml Release intentionally disables the debug features present in the repository's Debug-generated xmlversion header; this mismatch is baseline configuration, not introduced here. Keep existing report distinction rather than silently claiming every header macro matches both builds.

## Verdict

Suitable for parent integration review once the planned real MSBuild target-order/replacement/copy checks pass. No demand for a generic caching/publication overhaul or parser version upgrade. Native4/4 builder success and the15 resolved symbols are separate evidence; neither is a full-client XML lifecycle or gameplay pass.
