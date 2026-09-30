"""Frozen authored-registry checks only; no VM, SDK or vendor execution."""
from pathlib import Path
import hashlib,json,subprocess,shutil,os
b=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((b/'source-manifest.json').read_text())
for n,v in m.items():
    if h(b/'prepared'/n)!=v:raise RuntimeError('frozen source mismatch '+n)
out=b/'evidence-v1';out.mkdir(exist_ok=False)
private=b/'private-test-v1';private.mkdir(exist_ok=False)
compiler=Path(shutil.which('g++')).resolve()
result={'scope':__doc__,'compiler':{'path':str(compiler),'sha256':h(compiler)},'checks':[],'manifest':h(b/'source-manifest.json')}
try:
    command=[str(compiler),'-std=c++11','-Wall','-Wextra','-Werror','-pedantic','-fsanitize=address,undefined','-fno-omit-frame-pointer','-g',str(b/'prepared/sample-host29/registry_test.cpp'),'-o',str(private/'registry-test')]
    for name,args in [('compile',command),('authored-registry',[str(private/'registry-test')])]:
        (out/(name+'-command.json')).write_text(json.dumps(args,indent=2)+'\n')
        env=os.environ.copy();env['ASAN_OPTIONS']='detect_leaks=1:halt_on_error=1';env['UBSAN_OPTIONS']='halt_on_error=1'
        r=subprocess.run(args,capture_output=True,timeout=60,env=env)
        (out/(name+'.log')).write_bytes(r.stdout+r.stderr)
        result['checks'].append({'name':name,'exit':r.returncode})
        if r.returncode:raise RuntimeError('first failure '+name+'; no retry')
    result['stable']=all(h(b/'prepared'/n)==v for n,v in m.items())
    if not result['stable']:raise RuntimeError('inputs changed')
except Exception as error:result['failure']=str(error)
result['passed']=not result.get('failure') and result.get('stable',False)
(out/'receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':result['passed'],'receipt':h(out/'receipt.json'),'failure':result.get('failure')},indent=2))
raise SystemExit(not result['passed'])
