#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,os,subprocess,sys,time
if sys.argv[1:]!=['--approved-portable']:
 raise SystemExit('Separate approval required; no default execution')
r=Path(__file__).resolve().parent
f=json.loads((r/'freeze.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for name,value in f['sha256'].items():
 if sha(r/name)!=value:raise RuntimeError('Input changed: '+name)
out=r/'evidence-v1';out.mkdir(exist_ok=False)
command=['/usr/bin/clang++','-std=c++11','-Wall','-Wextra','-Wpedantic','-Werror','-O1','-g','-fsanitize=address,undefined','-fno-sanitize-recover=all','-fno-omit-frame-pointer','-include',str(r/'native35_compat.h'),str(r/'tests.cpp'),str(r/'tree/transport-candidate/codec.cpp'),str(r/'tree/session-version22/session_version.cpp'),str(r/'tree/startup-metadata-v4/metadata_wire.cpp'),str(r/'tree/session-file-admission34/coordinator.cpp'),str(r/'tree/callback-reentry47/invocation_guard.cpp'),'-o',str(out/'portable-reply66')]
result={'scope':'actual64 validator/types/core plus scripted Channel and unavailable Runtime substitute; no OS/engine/SDK runtime','start':time.time(),'commands':[]}
def run(argv,name,timeout):
 result['commands'].append(argv)
 with (out/name).open('wb') as log:p=subprocess.run(argv,stdout=log,stderr=subprocess.STDOUT,env=env,timeout=timeout)
 return p.returncode
env=os.environ.copy();env['ASAN_OPTIONS']='detect_leaks=1:halt_on_error=1:abort_on_error=1';env['UBSAN_OPTIONS']='halt_on_error=1:print_stacktrace=1'
try:
 result['oracle_exit']=run([sys.executable,str(r/'source_oracle.py')],'oracle.log',30)
 if result['oracle_exit']:raise RuntimeError('Source oracle failed; stop')
 result['compile_exit']=run(command,'build.log',120)
 if result['compile_exit']:raise RuntimeError('Compile failed; no retry')
 result['run_exit']=run([str(out/'portable-reply66')],'run.log',30)
 if result['run_exit']:raise RuntimeError('Test failed; no retry')
 markers=json.loads((r/'expected-markers.json').read_text());lines=(out/'run.log').read_text().splitlines()
 result['markers']={m:lines.count(m) for m in markers}
 if any(v!=1 for v in result['markers'].values()):raise RuntimeError('Scenario count failed')
except Exception as e:result['failure']=repr(e)
finally:
 result['changed']=[n for n,h in f['sha256'].items() if sha(r/n)!=h]
 result['end']=time.time();result['passed']=not result.get('failure') and not result['changed']
 (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
raise SystemExit(0 if result['passed'] else 1)
