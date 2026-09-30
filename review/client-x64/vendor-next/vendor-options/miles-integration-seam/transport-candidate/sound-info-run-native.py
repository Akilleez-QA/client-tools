from pathlib import Path
import subprocess,json,hashlib
r=Path('C:/miles-sound-info-v2');src=r/'transport-candidate';results=[]
for arch in ['x86','amd64']:
 for cfg in ['Debug','Release']:
  out=r/(arch+'-'+cfg);out.mkdir(exist_ok=True)
  cmd=out/'run.cmd';exe=out/'tests.exe'
  cmd.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\nif errorlevel 1 exit /b 1\ncd /d "'+str(out)+'"\ncl /nologo /EHsc /W4 /WX '+('/MTd /Od' if cfg=='Debug' else '/MT /O2')+' "'+str(src/'sound-info-codec.cpp')+'" "'+str(src/'sound-info-tests.cpp')+'" /Fe"'+str(exe)+'"\nif errorlevel 1 exit /b 1\n"'+str(exe)+'"\n')
  p=subprocess.run(['cmd','/d','/c',str(cmd)],capture_output=True,timeout=60)
  log=p.stdout+p.stderr;(out/'run.log').write_bytes(log)
  results.append(dict(arch=arch,config=cfg,exit=p.returncode,exact_count=((b'92/92 sound-info checks passed' in log and b'SKIP retained size' in log) if arch=='x86' else b'93/93 sound-info checks passed' in log)))
(r/'results.json').write_text(json.dumps({'results':results,'source_sha256':{str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for d in ['transport-candidate','protocol-candidate'] for p in (r/d).glob('*') if p.is_file()}},indent=2));print(results)
raise SystemExit(any(x['exit'] or not x['exact_count'] for x in results))
