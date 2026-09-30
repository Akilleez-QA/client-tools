from pathlib import Path
import hashlib,json,subprocess,shutil,os
b=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((b/'source-manifest.json').read_text());stage=b/'private-source-v1'
for n,v in m.items():
 if h(stage/n)!=v:raise RuntimeError('source identity mismatch '+n)
out=b/'evidence-v1';out.mkdir(exist_ok=False);build=b/'private-build-v1';build.mkdir(exist_ok=False)
cc=Path(shutil.which('g++')).resolve();r={'scope':'portable authored thread helper only','compiler_sha256':h(cc),'manifest_sha256':h(b/'source-manifest.json'),'checks':[]}
try:
 commands=[('compile',[str(cc),'-std=c++11','-Wall','-Wextra','-Werror','-pedantic','-pthread','-fsanitize=address,undefined','-fno-omit-frame-pointer','-g',str(stage/'call_context.cpp'),str(stage/'test.cpp'),'-o',str(build/'test')]),('scripted',[str(build/'test')])]
 for name,args in commands:
  (out/(name+'-command.json')).write_text(json.dumps(args,indent=2)+'\n')
  env=os.environ.copy();env['ASAN_OPTIONS']='detect_leaks=1:halt_on_error=1';env['UBSAN_OPTIONS']='halt_on_error=1'
  p=subprocess.run(args,capture_output=True,timeout=60,env=env);(out/(name+'.log')).write_bytes(p.stdout+p.stderr);r['checks'].append({'name':name,'exit':p.returncode})
  if p.returncode:raise RuntimeError('first failure '+name+'; no retry')
 r['stable']=all(h(stage/n)==v for n,v in m.items())
 if not r['stable']:raise RuntimeError('source mutated')
except Exception as e:r['failure']=str(e)
r['passed']=not r.get('failure') and r.get('stable',False);(out/'receipt.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'passed':r['passed'],'receipt':h(out/'receipt.json'),'failure':r.get('failure')}));raise SystemExit(not r['passed'])
