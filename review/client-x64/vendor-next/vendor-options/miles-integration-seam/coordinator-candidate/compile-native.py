from pathlib import Path
import subprocess,json,tarfile
r=Path('C:/miles-coordinator-v1');r.mkdir(exist_ok=True)
with tarfile.open('C:/miles-coordinator-input-v1.tar') as t:t.extractall(r)
results=[]
for arch in ['x86','amd64']:
 for cfg in ['Debug','Release']:
  o=r/(arch+'-'+cfg);o.mkdir(exist_ok=True)
  flags='/nologo /EHsc /W4 /WX '+('/MTd /Od' if cfg=='Debug' else '/MT /O2')
  cmd=o/'build.cmd';cmd.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\nif errorlevel 1 exit /b 1\ncl '+flags+' '+str(r/'coordinator-candidate/coordinator.cpp')+' '+str(r/'coordinator-candidate/coordinator_test.cpp')+' /Fe'+str(o/'probe.exe')+'\n')
  p=subprocess.run(['cmd','/d','/c',str(cmd)],cwd=o,capture_output=True);(o/'build.log').write_bytes(p.stdout+p.stderr)
  e=dict(arch=arch,cfg=cfg,build_exit=p.returncode);results.append(e)
  if p.returncode==0:
   p=subprocess.run([str(o/'probe.exe')],cwd=o,capture_output=True,timeout=20);(o/'run.log').write_bytes(p.stdout+p.stderr);e.update(run_exit=p.returncode,text=p.stdout.decode(errors='replace'))
(r/'results.json').write_text(json.dumps(results,indent=2));print(results)
