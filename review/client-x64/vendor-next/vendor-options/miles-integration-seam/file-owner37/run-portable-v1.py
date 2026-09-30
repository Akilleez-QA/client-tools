#!/usr/bin/env python3
"""One frozen portable strict ASan/UBSan gate; stop first failure, no retry."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
D=Path(__file__).resolve().parent;C=D/'candidate';OUT=D/'portable-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((D/'candidate-manifest-v1.json').read_text())
for n,v in m['sha256'].items():assert sha(D/n)==v,n
OUT.mkdir(exist_ok=False)
files=['transport-candidate/codec.cpp','file-channel26/file_channel.cpp','session-file-admission34/coordinator.cpp','file-owner36/session_file_owner.cpp','file-owner36/portable_job.cpp','file-owner36/tests.cpp','file-owner36/test_allocators.cpp']
command=['g++','-std=c++11','-Wall','-Wextra','-Werror','-pedantic','-g','-O1','-fno-omit-frame-pointer','-fsanitize=address,undefined']+[str(C/n) for n in files]+['-o',str(OUT/'owner-tests')]
r={'scope':'portable scripted platform only; no engine/vendor/VM','command':command,'manifest_sha256':sha(D/'candidate-manifest-v1.json')}
p=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(OUT/'compile.log').write_bytes(p.stdout);r['compile_exit']=p.returncode
if p.returncode==0:
 env=dict(os.environ,ASAN_OPTIONS='detect_leaks=1:halt_on_error=1',UBSAN_OPTIONS='halt_on_error=1:print_stacktrace=1')
 r['test_command']=[str(OUT/'owner-tests')];r['sanitizers']={k:env[k] for k in ['ASAN_OPTIONS','UBSAN_OPTIONS']}
 p=subprocess.run(r['test_command'],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(OUT/'run.log').write_bytes(p.stdout);r['run_exit']=p.returncode
r['sources_unchanged']=all(sha(D/n)==v for n,v in m['sha256'].items());r['passed']=r['compile_exit']==0 and r.get('run_exit')==0 and r['sources_unchanged']
(OUT/'results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));sys.exit(0 if r['passed'] else 1)
