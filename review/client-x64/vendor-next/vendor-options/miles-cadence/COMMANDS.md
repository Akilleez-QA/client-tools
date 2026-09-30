# Command and evidence record

PLAN.md was written before probe creation/build/playback. Source reads covered
predecessor plans/results, realtime host/drain and runner/analysis, file-callback
probe/build/runner/analysis, and Grok vendor6. Old raw logs were re-read directly.
All new artifacts are inside this private mode0700 directory.

Native creation used the existing winps.sh wrapper with build.ps1 on stdin,
output native-create.log. scp used the established winbuild ssh key, port2223,
known_hosts and builder@127.0.0.1:C:/miles-cadence-20260930-a/ to transfer probe.cpp,
Mss.h and build.cmd. No drive remapping. Header copied from predecessor Mss.h.
Native invocation (twice):

    winps.sh 'cmd /c C:\miles-cadence-20260930-a\build.cmd; exit $LASTEXITCODE'

Outputs compile-1.log and compile-2.log. First source/binary retained as
probe-v1.cpp/exe. Final source change anchors the next 50 ms wait after getters.
Final probe.exe downloaded with the same scp transport; no native playback.
Exact compiler flags are in build.cmd.

    python vendor-options/miles-cadence/run.py > vendor-options/miles-cadence/run-1.log 2>&1
    python vendor-options/miles-cadence/analyze.py > vendor-options/miles-cadence/verification.log
    winps.sh - < cleanup-native.ps1 > native-hashes-cleanup.log 2>&1

run.py records exact subprocess argv in run-a/commands.json and specifies the
private process environment/copy operations. Its sole six-process matrix used
one unique null sink; no retries. Cleanup-native.ps1 hashes inputs/compiler/output
before removing exclusively the owned native folder. Local evidence remains.
