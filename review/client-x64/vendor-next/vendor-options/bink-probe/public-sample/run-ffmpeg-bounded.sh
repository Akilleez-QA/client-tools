#!/usr/bin/env bash
set -euo pipefail
cd /home/akilleez/Work/client-wire-validation/vendor-options/bink-probe
umask 077
# Follow-up bounds decoding by stopping after the fourth selected output (frame 32).
# Conversion, alpha, and frame selections are unchanged; initial output/log retained.
timeout 60 ffmpeg -nostdin -threads 1 -i private/public-sample/logo_legal.bik -an -frames:v 4 -vf 'trim=end_frame=32,scale=in_color_matrix=bt601:out_color_matrix=bt601:in_range=tv:out_range=pc:flags=bilinear,format=bgra,select=eq(n\,0)+eq(n\,7)+eq(n\,15)+eq(n\,31)' -fps_mode passthrough -pix_fmt bgra -f rawvideo private/public-sample/ffmpeg-bounded.bgra > public-sample/logs/ffmpeg-bounded.log 2>&1
