# PCRE 4.1 upstream corpus coverage

Native v120, genuine integrated candidate libraries in Win32/x64 Debug/Release, plus original repository Win32 archive with both driver configurations. All source and provider identities remain in integration manifests. No production files or settings changed for these runs.

## Corpora and oracle

Upstream RunTest.in selects input1 (ordinary Perl-compatible), input2 with -i (API/errors/internal diagnostics), input4 (UTF8 matching), input5 (UTF8 diagnostics). Expected outputs are shipped testoutput files, with only CRLF→LF conversion for initial exact comparisons. These files contain 5,728 input lines, not 5,728 independently counted checks. Test3 skipped: exact POSIX fr locale not established.

## Preserved failures and driver adaptation

Version1 ordinary corpora ran; UTF8 corpora aborted on all six builds including stock. Upstream pcretest prints Unicode via fprintf(...,%n,...), disabled by the modern CRT. Version2 enables _set_printf_count_output(1) only in the diagnostic driver for trusted fixed upstream formats. No parser or game policy changes. Original results preserved in pcre-corpus-v1.zip.

Version2 uses default 1 MiB stack reserve / 4 KiB commit. Actual Win32 SwgClient Release and Debug PE headers have exactly those values; game project and available x64 link responses contain no /STACK override. All six drivers match those values. The x64 Debug corpus2 process exits 0xC00000FD (stack overflow), near the pattern on input line718: 269 repeated digit capturing groups followed by a word group and backreference270. Buffered output does not establish whether compile or match exhausted the stack. This is a real bounded difference, not hidden as a skip. Game stack occupancy/thread context may differ.

## Results

| Run | Stock Win32 both | Candidate Win32 both | Candidate x64 Release | Candidate x64 Debug |
|---|---|---|---|---|
| v2, 1 MiB, corpora1/4 | exact | exact | exact | exact |
| v2, corpus2 | exact | exact | only17 Study size changes | stack overflow |
| v2, corpus5 | exact | exact | only5 Study size changes | only5 Study size changes |
| v3, diagnostic8 MiB, all4 corpora | exact | exact | complete, metadata only | complete, metadata only |

Version3 was declared beforehand in CORPUS-STACK-PLAN.md: only driver linker /STACK:8388608,4096 changed, uniformly for all six variants. All24 corpus processes exit0. All matching/error/UTF8 outputs agree with upstream; x64 corpus2 has17 and corpus5 has5 Study size=40→48 lines, and those are the only differing bytes after newline conversion. Raw differing outputs are retained, with explicit metadata-only comparison in corpus-differences.json. This is expected pointer-layout size metadata, not an algorithm mismatch. The8MiB result does not repair or waive the production-default1MiB Debug stack limitation. No production stack increase proposed.

## Scope

Broader evidence than a single UTF8 character smoke, but not universal regex equivalence, locale coverage, game-thread stack acceptance, or a full client run. The same unmodified libraries are used throughout. PCRE4.1's own doc/pcre.txt describes recursive matching stack limitations. No unsupported modern PCRE options were added.

Primary CRT and linker references:
- https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/set-printf-count-output?view=msvc-170
- https://learn.microsoft.com/en-us/cpp/build/reference/stack-stack-allocations?view=msvc-170

Full raw packets: pcre-corpus-v1.zip, pcre-corpus-v2.zip, pcre-corpus-v3.zip (private local binaries included; do not publish wholesale). Publish text logs/JSON only.

## Smallest next-power-of-two follow-up
Version4 uses2MiB reserve /4KiB commit only in diagnostic drivers, prospectively declared. All24 processes exit0. The exact same17+5 Study size lines differ on both x64 configurations; all remaining output bytes match. This is the smallest increased reserve tested, not a measured minimum. Original1MiB failure remains.

First-party caller scan (git grep pcre_compile/pcre_exec in src/engine and src/game): game Scene animation filter and Mount name lookup, NpcEditor file filtering, shared TemplateDefinitionFile filtering. Game parsers are registered by SwgCuiConsole and SwgCuiChatWindow and call PCRE synchronously. Thread.cpp:76 uses _beginthreadex with stack_size0; executable reserve would cover main/default-reserve threads, not another tool executable or explicitly sized third-party stacks. This source trace does not prove exact game call-depth budget.
