#!/usr/bin/env bash
set -euo pipefail
cd /home/akilleez/Work/client-wire-validation/vendor-options/bink-probe
umask 077
winps=/home/akilleez/Work/swg-source-vm/winbuild/winps.sh
key=/home/akilleez/Work/swg-source-vm/winbuild/ssh/id_ed25519
known=/home/akilleez/Work/swg-source-vm/winbuild/ssh/known_hosts
"$winps" 'New-Item -ItemType Directory -Force C:/vendor-bink-probe/public-sample | Out-Null'
scp -q -i "$key" -P 2223 -o "UserKnownHostsFile=$known" public-sample/{probe-public.cpp,driver-public.cpp,build-public.cmd,verify-public.py} private/public-sample/logo_legal.bik builder@127.0.0.1:C:/vendor-bink-probe/public-sample/
timeout 120 "$winps" 'cmd /c C:/vendor-bink-probe/public-sample/build-public.cmd' > public-sample/logs/build.log 2>&1
timeout 150 "$winps" '& C:/ci-dpvs-review/python/python.exe C:/vendor-bink-probe/public-sample/verify-public.py' > public-sample/logs/verify-vm.log 2>&1
scp -q -i "$key" -P 2223 -o "UserKnownHostsFile=$known" 'builder@127.0.0.1:C:/vendor-bink-probe/public-sample/verification.json' public-sample/
scp -q -i "$key" -P 2223 -o "UserKnownHostsFile=$known" 'builder@127.0.0.1:C:/vendor-bink-probe/public-sample/decode-*.raw' 'builder@127.0.0.1:C:/vendor-bink-probe/public-sample/frame-*.bgra' private/public-sample/
