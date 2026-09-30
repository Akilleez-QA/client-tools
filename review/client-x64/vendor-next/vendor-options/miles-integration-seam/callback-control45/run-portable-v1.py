#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, os, subprocess, sys
D=Path(__file__).resolve().parent; C=D/'candidate'; O=D/'portable-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((D/'candidate-manifest-v1.json').read_text())
for n,v in m['sha256'].items():
 if sha(D/n)!=v:raise RuntimeError('identity mismatch: '+n)
O.mkdir(exist_ok=False)
files=['transport-candidate/codec.cpp','file-channel26/file_channel.cpp','session-file-admission34/coordinator.cpp','file-owner36/session_file_owner.cpp','file-owner36/portable_job.cpp','callback-control45/host_association_mapper.cpp','callback-control45/tests.cpp']
cmd=['g++','-std=c++11','-Wall','-Wextra','-Werror','-pedantic','-g','-O1','-fno-omit-frame-pointer','-fsanitize=address,undefined']+[str(C/f) for f in files]+['-o',str(O/'control-tests')]
r={'command':cmd,'manifest_sha256':sha(D/'candidate-manifest-v1.json'),'scope':'real mapper, owner, coordinator, file adapter and codec; scripted worker/job only; no native ABI/runtime'}
p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180);(O/'compile.log').write_bytes(p.stdout);r['compile_exit']=p.returncode
if not p.returncode:
 env=dict(os.environ,ASAN_OPTIONS='detect_leaks=1:halt_on_error=1',UBSAN_OPTIONS='halt_on_error=1:print_stacktrace=1')
 p=subprocess.run([str(O/'control-tests')],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=30);(O/'run.log').write_bytes(p.stdout);r['run_exit']=p.returncode
 r['sanitizers']={k:env[k] for k in ['ASAN_OPTIONS','UBSAN_OPTIONS']}
 expected=['forward-before-ACK join and distinct wire/local IDs','ACK-before-forward join','unsolicited callback during unrelated command','idle callback open-close lifetime','causal/session/lane/lease validation','unsupported lock actions rejected before admission','reverse replay before and after ACK','early/stale/duplicate/peer-intake ACK rejection','uncertain file execution retains forward and callback pins','reverse storage capacity fails before second file admission','malformed frame rejected']
 lines=p.stdout.decode(errors='replace').splitlines();r['expected_scenarios']=expected;r['all_scenarios_present']=all(lines.count('PASS '+x)==1 for x in expected)
r['sources_unchanged']=all(sha(D/n)==v for n,v in m['sha256'].items());r['passed']=not r['compile_exit'] and r.get('run_exit')==0 and r.get('all_scenarios_present',False) and r['sources_unchanged']
(O/'results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));sys.exit(0 if r['passed'] else 1)
