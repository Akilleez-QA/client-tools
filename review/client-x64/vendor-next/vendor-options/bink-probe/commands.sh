#!/usr/bin/env bash
# Reproduction; local-only. Run from client-wire-validation. No product changes.
set -euo pipefail
probe=vendor-options/bink-probe
winps=/home/akilleez/Work/swg-source-vm/winbuild/winps.sh
key=/home/akilleez/Work/swg-source-vm/winbuild/ssh/id_ed25519
known=/home/akilleez/Work/swg-source-vm/winbuild/ssh/known_hosts
python "$probe/extract.py"
objdump -p '/home/akilleez/Work/swg-source-vm/client/SWGSource Client v3.0/binkw32.dll'
ffmpeg -version
ffmpeg -hide_banner -decoders
"$winps" 'New-Item -ItemType Directory -Force C:/vendor-bink-probe | Out-Null'
scp -q -i "$key" -P 2223 -o "UserKnownHostsFile=$known" "$probe"/{probe.cpp,driver.cpp,build.cmd,verify_vm.py} "$probe"/private/{bink.h,radbase.h,binkw32.dll} builder@127.0.0.1:C:/vendor-bink-probe/
timeout 120 "$winps" 'cmd /c C:/vendor-bink-probe/build.cmd'
timeout 65 "$winps" '& C:/ci-dpvs-review/python/python.exe C:/vendor-bink-probe/verify_vm.py'
# Not executed: no movie found. Predeclared FFmpeg comparator command, kept fixed:
# timeout 60 ffmpeg -nostdin -threads 1 -i "$probe/private/movie.bik" -an -frames:v 32 -vf 'trim=end_frame=32,scale=in_color_matrix=bt601:out_color_matrix=bt601:in_range=tv:out_range=pc:flags=bilinear,format=bgra,select=eq(n\,0)+eq(n\,7)+eq(n\,15)+eq(n\,31)' -fps_mode passthrough -pix_fmt bgra -f rawvideo "$probe/private/ffmpeg.bgra"
