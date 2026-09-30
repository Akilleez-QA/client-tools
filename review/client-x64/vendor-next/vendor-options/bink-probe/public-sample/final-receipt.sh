#!/usr/bin/env bash
set -euo pipefail
cd /home/akilleez/Work/client-wire-validation/vendor-options/bink-probe
/home/akilleez/Work/swg-source-vm/winbuild/winps.sh - < public-sample/final-receipt.ps1 > public-sample/logs/final-vm-receipt.json
chmod 700 private/public-sample
chmod 600 private/public-sample/*
