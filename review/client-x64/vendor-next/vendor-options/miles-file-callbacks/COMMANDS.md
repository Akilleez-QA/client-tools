# Exact command record

All local writes used this directory. Read-only discovery also inspected the
specified predecessor and review files, the existing winps/winssh wrappers, and
original DLL. Initial discovery tried a nonexistent /home/akilleez/Work/swg-source/src/
header path; no source was changed. Header was then copied from the established
native C:/vendor-miles-probe/Mss.h. An initial overly broad file search was truncated;
the required predecessor documents and sources were subsequently read directly.

Native transport (existing key and wrapper; no mappings changed):

```bash
scp -q -i /home/akilleez/Work/swg-source-vm/winbuild/ssh/id_ed25519 -P 2223 -o UserKnownHostsFile=/home/akilleez/Work/swg-source-vm/winbuild/ssh/known_hosts builder@127.0.0.1:C:/vendor-miles-probe/Mss.h Mss.h
/home/akilleez/Work/swg-source-vm/winbuild/winps.sh - < build.ps1 > native-create.log 2>&1
scp -q -i /home/akilleez/Work/swg-source-vm/winbuild/ssh/id_ed25519 -P 2223 -o UserKnownHostsFile=/home/akilleez/Work/swg-source-vm/winbuild/ssh/known_hosts probe.cpp Mss.h build.cmd builder@127.0.0.1:C:/miles-fcb-20260930-a/
/home/akilleez/Work/swg-source-vm/winbuild/winps.sh 'cmd /c C:\miles-fcb-20260930-a\build.cmd; exit $LASTEXITCODE' > compile-1.log 2>&1
scp -q -i /home/akilleez/Work/swg-source-vm/winbuild/ssh/id_ed25519 -P 2223 -o UserKnownHostsFile=/home/akilleez/Work/swg-source-vm/winbuild/ssh/known_hosts builder@127.0.0.1:C:/miles-fcb-20260930-a/probe.exe probe.exe
```

`build.cmd` contains the exact v120 x86 /MT /O2 /W4 compile. Compilation succeeded
with only two fopen deprecation warnings. No native playback was attempted.

First run: `python run.py > run-1.log 2>&1`, using now-preserved `run-initial.py`.
Copied ../miles-realtime/wine-prefix using `cp -a --reflink=auto` to
private-prefix-fcb-a. Created swg_fcb_0d924b17a4b5 (module536870916). Preflight
failed before Wine/probe launch; full assertion and cleanup failure preserved.
Explicit cleanup: `pactl unload-module 536870916 > cleanup-initial.log 2>&1`.
Module IDs were recycled by the server: same numeric ID on retry is not a shared
resource; sink names differ.

Corrected preflight/cleanup and reused only that owned, not-yet-launched prefix.
Second run: `python run.py > run-2.log 2>&1`. Full exact subprocess argv sequence
in run-b/commands.json, plus run.py for process environment, file copies and
timeouts. Sink swg_fcb_04c7f5ed1826, sink index16954. No media captured.

Analysis: `python analyze.py` -> analysis.json and hashes.json.
Cleanup and native source/binary/compiler SHA256:

```bash
/home/akilleez/Work/swg-source-vm/winbuild/winps.sh - < cleanup-native.ps1 > native-hashes-cleanup.log 2>&1
```

Local prefix and exact private DLL/PCM/executable retained for parent review;
its wineserver stopped. Native scratch folder removed. Original/shared paths
were read-only. No R:/Q: changes, production changes, game, commits or uploads.
