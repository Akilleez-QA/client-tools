from pathlib import Path
import tarfile,subprocess,json,hashlib
r=Path('C:/miles-host-candidate-v1');r.mkdir(exist_ok=True)
with tarfile.open('C:/miles-host-input.tar') as t:t.extractall(r)
results=[]
for cfg in ['Debug','Release']:
 o=r/cfg;o.mkdir(exist_ok=True);b=o/'compile.cmd';b.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86 >nul\nif errorlevel 1 exit /b 1\ncl /nologo /c /EHsc /DWIN32 '+('/MTd /Od' if cfg=='Debug' else '/MT /O2')+' /IC:/client-next-build/src/external/3rd/library/miles/include '+str(r/'host-candidate/host_dispatch.cpp')+' /Fo'+str(o/'host.obj')+'\nif errorlevel 1 exit /b 1\ndumpbin /symbols '+str(o/'host.obj')+' > '+str(o/'symbols.txt')+'\n')
 p=subprocess.run(['cmd','/d','/c',str(b)],capture_output=True);(o/'compile.log').write_bytes(p.stdout+p.stderr);results.append(dict(cfg=cfg,exit=p.returncode,source_sha256=hashlib.sha256((r/'host-candidate/host_dispatch.cpp').read_bytes()).hexdigest()))
(r/'results.json').write_text(json.dumps(results,indent=2));print(results)
