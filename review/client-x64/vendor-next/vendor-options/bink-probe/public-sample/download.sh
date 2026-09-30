#!/usr/bin/env bash
set -euo pipefail
cd /home/akilleez/Work/client-wire-validation/vendor-options/bink-probe
umask 077
curl --fail --location --proto '=https' --max-time 60 --max-filesize 1048576 --dump-header public-sample/logs/download-headers.txt --output private/public-sample/logo_legal.bik https://samples.ffmpeg.org/game-formats/bink/logo_legal.bik
sha256sum private/public-sample/logo_legal.bik
ffprobe -v error -show_format -show_streams -of json private/public-sample/logo_legal.bik > public-sample/ffprobe.json
ffmpeg -version > public-sample/logs/ffmpeg-version.txt
