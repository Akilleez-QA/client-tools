# Network candidate reproduction: prospective contract

Parent PLAN.md owns framing, research gate, options and orchestration. POODO applies here to the authorized execution slice; no new stage decision or descendant agents. This worker was already fan-out allocated; no capacity allocated for descendants.

Input v1: a393d1233aada331f99d4edb50f678e8c186fff2, base 949451032647e45e42c3aaef3f41b132c8af36e3. Native Windows VM, Visual Studio 2013 v120 x86/amd64, Debug/Release. Runner source and all directly/indirectly used headers hashed; output directories must not exist.

Prediction: 40 actual-header include-order combinations compile and run 21 bounded raw Winsock/IOCP checks each; 20 x86 reverted-header controls also compile/run and 20 x64 reverted-header controls fail width/redefinition checks. Three full production TUs (Sock, TcpClient, TcpServer) compile in four configurations. Each TCP full-TU copy with only its key declaration reverted compiles on x86 and fails the actual GetQueuedCompletionStatus signature on x64. All unexpected outcomes fail aggregated command status.

Strongest rival: raw API probe is correct while changed production IOCP declarations remain wrong or the branch cannot compile independently. Actual-TU compilation and independent key reversions discriminate this. Raw API probes never establish production TCP runtime behavior.

Known potential contradiction: parent observed common Misc.h memmove ambiguity on the clean base in another TU. First run must retain this unmodified failure. A later run may use the explicit four-file common-header prerequisite only through a parent-prepared stacked branch, with its own identity and output directory. No header skips, stub declarations, silent overlay or dependency edits.

Oracle: compiler/API declarations for type mismatch; probe.cpp exact byte equality, key equality including high x64 bits, 21 observed checks. Compile-only source adaptation derives includes/definitions from Win32 project, disables PCH and removes _USE_32BIT_TIME_T only for x64. It is not an x64 project configuration or full library/client build.

Stop/rollback: Any unexpected compile/run outcome retracts that scope's pass claim. Keep raw failure and diagnose; preserve all attempt outputs. No production edits, commits, pushes or publishing in worker scope. Next prerequisite owned by parent. Runtime bounds: each probe <=15 seconds; receive/completion <=3 seconds. No synthetic handles passed to Winsock and no network destinations except loopback.
