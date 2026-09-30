from pathlib import Path
import os,shutil,subprocess,json
out=Path('C:/warning-fixes-format-v2');out.mkdir(exist_ok=False);rows=[]
for config in ['Release','Debug']:
 for platform in ['Win32','x64']:
  name=config+'-'+platform;d=out/name;d.mkdir();bat=Path('C:/vendor-reachability/trackir-candidate-v2')/name/'env.cmd';p=subprocess.run(['cmd','/c',str(bat)],stdout=subprocess.PIPE,timeout=60);env=dict(os.environ)
  for l in p.stdout.decode(errors='replace').splitlines():
   if '=' in l and not l.startswith('='):k,v=l.split('=',1);env[k.upper()]=v
  cl=shutil.which('cl.exe',path=env['PATH']);cmd=[cl,'/nologo','/W4','/WX','/EHsc','/MTd' if config=='Debug' else '/MT','/Od' if config=='Debug' else '/O2','C:/vendor-reachability/crash-format-probe.cpp','/Fo'+str(d/'probe.obj'),'/Fe'+str(d/'probe.exe')];p=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60);(d/'build.log').write_bytes(p.stdout);r=dict(name=name,compile=p.returncode)
  if not p.returncode:p=subprocess.run([str(d/'probe.exe')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=10);(d/'run.log').write_bytes(p.stdout);r.update(run=p.returncode,output=p.stdout.decode())
  rows.append(r);print(r)
(out/'results.json').write_text(json.dumps(rows,indent=2))
