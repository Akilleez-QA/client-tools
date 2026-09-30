#!/usr/bin/env bash
# Private prefix only; never configure the host audio device. Assets/runtime remain private.
set -eu
cd "$(dirname "$0")"
export WINEPREFIX="$PWD/wine-prefix"
export WINEDLLOVERRIDES='winepulse.drv=d;mscoree=d;mshtml=d'
export ALSA_CONFIG_PATH="$PWD/alsa-null.conf"
export WINEDEBUG=-all
wine reg add 'HKCU\Software\Wine\Drivers' /v Audio /d alsa /f
# Exact original DLL/plugins and source-hashed probe must already exist in this private prefix.
timeout 20 wine "$WINEPREFIX/drive_c/vendor-miles-probe/probe.exe" 'C:\vendor-miles-probe\Mss32.dll' 'C:\vendor-miles-probe\sample.wav' 'C:\vendor-miles-probe\sample.mp3'
