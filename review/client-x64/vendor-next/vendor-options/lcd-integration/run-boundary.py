from pathlib import Path
import subprocess,os,shutil,json
root=Path('C:/vendor-reachability');out=root/'trackir-boundary-v1';out.mkdir(exist_ok=False);results=[]
for name in ['Release-Win32','Release-x64','Debug-Win32','Debug-x64']:
 d=out/name;d.mkdir();v=subprocess.run(['cmd','/c',str(root/'trackir-candidate-v2'/name/'env.cmd')],stdout=subprocess.PIPE,timeout=60);env=dict(os.environ)
 for l in v.stdout.decode(errors='replace').splitlines():
  if '=' in l and not l.startswith('='):k,val=l.split('=',1);env[k.upper()]=val
 cl=shutil.which('cl.exe',path=env['PATH']);cmd=[cl,'/nologo','/EHsc','/MTd' if name.startswith('Debug') else '/MT',str(root/'trackir-path-boundary.cpp'),'/Fe'+str(d/'probe.exe'),'/Fo'+str(d/'probe.obj')];v=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60);(d/'build.log').write_bytes(v.stdout);r=dict(name=name,compile=v.returncode)
 if not v.returncode:
  v=subprocess.run([str(d/'probe.exe')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=30);(d/'run.log').write_bytes(v.stdout);r.update(run=v.returncode,output=v.stdout.decode())
 results.append(r);print(r,flush=True)
(out/'results.json').write_text(json.dumps(results,indent=2))
