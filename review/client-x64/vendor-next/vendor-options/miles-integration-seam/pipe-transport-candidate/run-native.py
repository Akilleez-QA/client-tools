from pathlib import Path
import subprocess,tarfile,json
r=Path('C:/miles-pipe-transport-v1');r.mkdir(exist_ok=True)
with tarfile.open('C:/miles-pipe-input-v1.tar') as t:t.extractall(r)
results=[]
for cfg in ['Debug','Release']:
 for arch in ['x86','amd64']:
  out=r/(arch+'-'+cfg);out.mkdir(exist_ok=True)
  flags='/nologo /EHsc /W4 /WX /D_WIN32_WINNT=0x0601 '+('/MTd /Od' if cfg=='Debug' else '/MT /O2')
  sources=' '.join(str(r/f) for f in ['pipe-transport-candidate/endpoint.cpp','pipe-transport-candidate/fixture.cpp','transport-candidate/codec.cpp'])
  cmd=out/'build.cmd';cmd.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\nif errorlevel 1 exit /b 1\ncl '+flags+' '+sources+' /Fe'+str(out/'fixture.exe')+'\n')
  p=subprocess.run(['cmd','/d','/c',str(cmd)],cwd=out,capture_output=True);(out/'build.log').write_bytes(p.stdout+p.stderr);results.append(dict(arch=arch,cfg=cfg,build_exit=p.returncode))
 if all(x['build_exit']==0 for x in results if x['cfg']==cfg):
  out=r/('amd64-'+cfg)
  try:
   p=subprocess.run([str(out/'fixture.exe'),str(r/('x86-'+cfg)/'fixture.exe')],cwd=out,capture_output=True,timeout=90)
   (out/'run.log').write_bytes(p.stdout+p.stderr);results.append(dict(cfg=cfg,run_exit=p.returncode,text=p.stdout.decode(errors='replace')))
  except subprocess.TimeoutExpired as e:
   (out/'run.log').write_bytes((e.stdout or b'')+(e.stderr or b''));results.append(dict(cfg=cfg,timeout=True))
(r/'results.json').write_text(json.dumps(results,indent=2));print(results)
