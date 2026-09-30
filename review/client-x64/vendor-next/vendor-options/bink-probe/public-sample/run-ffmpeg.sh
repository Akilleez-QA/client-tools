#!/usr/bin/env bash
set -euo pipefail
cd /home/akilleez/Work/client-wire-validation/vendor-options/bink-probe
umask 077
# Exact predeclared conversion and selections, only input/output paths differ.
timeout 60 ffmpeg -nostdin -threads 1 -i private/public-sample/logo_legal.bik -an -frames:v 32 -vf 'trim=end_frame=32,scale=in_color_matrix=bt601:out_color_matrix=bt601:in_range=tv:out_range=pc:flags=bilinear,format=bgra,select=eq(n\,0)+eq(n\,7)+eq(n\,15)+eq(n\,31)' -fps_mode passthrough -pix_fmt bgra -f rawvideo private/public-sample/ffmpeg.bgra > public-sample/logs/ffmpeg-decode.log 2>&1
