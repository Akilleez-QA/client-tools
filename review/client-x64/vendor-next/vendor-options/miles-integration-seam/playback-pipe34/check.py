"""Scripted real framing only; no native SDK, vendor or engine execution."""
from pathlib import Path
import hashlib,json,subprocess,shutil,os
b=Path(__file__).resolve().parent;stage=b/'private-source-v1';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((b/'source-manifest.json').read_text())
for n,v in m.items():
 if h(stage/n)!=v:raise RuntimeError('frozen source mismatch '+n)
out=b/'evidence-v1';out.mkdir(exist_ok=False);build=b/'private-build-v1';build.mkdir(exist_ok=False)
cc=Path(shutil.which('g++')).resolve()
sources=['playback-pipe34/test.cpp','backend-boundary24/pipe/ClientMilesPipe.cpp','transport-candidate/codec.cpp','startup-metadata-v4/metadata_wire.cpp','session-version22/session_version.cpp']
flags=[str(cc),'-std=c++11','-Wall','-Wextra','-Werror','-pedantic','-fsanitize=address,undefined','-fno-omit-frame-pointer','-g']
result={'scope':__doc__,'compiler_sha256':h(cc),'source_manifest':h(b/'source-manifest.json'),'checks':[]}
try:
 for label,args in [('compile',flags+[str(stage/n) for n in sources]+['-o',str(build/'test')]),('scripted',[str(build/'test')])]:
  (out/(label+'-command.json')).write_text(json.dumps(args,indent=2)+'\n')
  env=os.environ.copy();env['ASAN_OPTIONS']='detect_leaks=1:halt_on_error=1';env['UBSAN_OPTIONS']='halt_on_error=1'
  r=subprocess.run(args,capture_output=True,timeout=60,env=env);(out/(label+'.log')).write_bytes(r.stdout+r.stderr)
  result['checks'].append({'name':label,'exit':r.returncode})
  if r.returncode:raise RuntimeError('first failure '+label+'; no automatic rerun')
 result['stable']=all(h(stage/n)==v for n,v in m.items())
 if not result['stable']:raise RuntimeError('source changed')
except Exception as error:result['failure']=str(error)
result['passed']=not result.get('failure') and result.get('stable',False)
(out/'receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':result['passed'],'receipt':h(out/'receipt.json'),'failure':result.get('failure')},indent=2))
raise SystemExit(not result['passed'])
