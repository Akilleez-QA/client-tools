#!/usr/bin/env python3
"""Authorized portable coordinator state tests only; no engine/vendor/VM."""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'portable-v1';OUT.mkdir(exist_ok=False)
records=[]
for name,source in [('resource-regression','resource_regression_test.cpp'),('session-files','session_files_test.cpp')]:
 command=['g++','-std=c++11','-Wall','-Wextra','-Werror','-pedantic',str(ROOT/'coordinator.cpp'),str(ROOT/source),'-o',str(OUT/name)]
 p=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (OUT/(name+'-build.log')).write_bytes(p.stdout)
 record={'name':name,'build_command':command,'build_exit':p.returncode};records.append(record)
 if p.returncode:
  (OUT/'results.json').write_text(json.dumps(records,indent=2)+'\n');raise SystemExit(p.returncode)
 command=[str(OUT/name)];p=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (OUT/(name+'-run.log')).write_bytes(p.stdout)
 record.update(run_command=command,run_exit=p.returncode,executable_sha256=hashlib.sha256((OUT/name).read_bytes()).hexdigest())
 print(p.stdout.decode(),end='')
 (OUT/'results.json').write_text(json.dumps(records,indent=2)+'\n')
 if p.returncode:raise SystemExit(p.returncode)
