# Scoped x64 executable stack reserve candidate

Candidate detached worktree client-stack-reserve-candidate at a21af1630. Only Link.StackReserveSize=2097152 conditioned on ProjectName SwgClient AND Platform x64. Existing common sheet is imported only by generated x64 projects. No StackCommitSize edit, no Win32 or renderer/library setting.

## Basis
Actual original Win32 client Release/Debug executable PE headers reserve1MiB/commit4KiB; project/link responses show no /STACK override. Genuine candidate PCRE4.1 all4 native corpora were measured under default1MiB, diagnostic8MiB, then prospectively declared next-power-of-two2MiB. The only process failure remaining after trusted-driver %n adaptation is x64 Debug testinput2 stack overflow at1MiB. All24 processes complete at2MiB as at8MiB; exact matching/UTF8/error output agreement, apart from separately retained17+5 Study size40→48 metadata lines. No claim2MiB handles every pattern or exact game call-depth budget.

## Native scope check
16/16 actual project evaluations exit0: baseline/candidate × SwgClient/Direct3d9 × Win32/x64 × Debug/Release. Baseline reserve/commit fields empty. Candidate only x64 SwgClient gets2097152; commit remains empty everywhere. This uses identical candidate metadata injected after Cpp.targets without changing active product source or mappings. It proves native metadata condition behavior, not exact final import ordering or a linked game PE. Those remain to check in the next immutable product build. Initial attempts used an absent per-session R mapping (and first renderer path was wrong); their failed logs are retained on VM, then physical project paths succeed.

## Runtime scope and tradeoff
Scene animation filtering and Mount lookup call PCRE synchronously through game console/chat command parsers. sharedThread/src/win32/Thread.cpp:76 passes stack_size0 to _beginthreadex. Executable stack reserve governs initial thread and default-reserve threads. The change adds1MiB virtual address reservation per such thread; it does not double initial physical commitment, whose4KiB default remains unchanged. It does not cover another tool executable (NpcEditor/TemplateDefinition consumers), externally explicit-sized threads, or guarantee all untrusted regex patterns. No parser algorithm/restriction or provider change.

## Primary documentation
https://learn.microsoft.com/en-us/cpp/build/reference/stack-stack-allocations?view=msvc-170
https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/beginthread-beginthreadex?view=msvc-170

Parent review required before integration; no commit or product source edits by this agent.

## Actual-position follow-up completed
Frozen a21af1630 project and all relative props copied into separate baseline/candidate private trees. Commonprops remains at original import position before Microsoft.Cpp.targets; only metadata reporting is injected afterward.8/8 evaluations pass. Both candidatex64 configurations reserve2097152; all other cases retain empty/default reserve. A minimal main-return0 nativev120 executable is then linked using only the evaluated stack settings: candidatex64PE2MiB reserve/4KiB commit; other6PE1MiB/4KiB. This closes import-position/property and linker encoding questions, not full-client linkage or runtime acceptance. Actual-position input manifest records all copied file digests; no active product tree/mapping changes.
