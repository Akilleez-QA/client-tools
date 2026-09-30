# Corrected complete-Sources Link task

The isolated v1 target omitted WinMain.obj. v2 includes all actual product source objects (ClientMain.obj, FirstSwgClient.obj and WinMain.obj) plus SwgClient.res. No production sources or provider policy changed between probes. Baseline still fails LNK1181. Candidate reaches LNK1120 with exactly60 unresolved symbols, all __imp_AIL_ Miles imports; externalCommandHandler is resolved. Both native MSBuild tasks exit1, no executable run. This is still isolated task evidence, not a full current-head product build.
