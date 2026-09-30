from pathlib import Path
import subprocess,json,hashlib
r=Path('C:/miles-host-live-v3');results=[]
for cfg in ['Debug','Release']:
 out=r/cfg;out.mkdir(exist_ok=True);cmd=out/'build.cmd'
 cmd.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86 >nul\nif errorlevel 1 exit /b 1\ncd /d "'+str(out)+'"\ncl /nologo /EHsc /W4 /WX /DWIN32 /IC:/client-next-build/src/external/3rd/library/miles/include '+('/MTd /Od' if cfg=='Debug' else '/MT /O2')+' "'+str(r/'host-live-candidate/probe.cpp')+'" "'+str(r/'host-candidate/host_dispatch.cpp')+'" C:/client-next-build/src/external/3rd/library/miles/lib/win/Mss32.lib /Fe"'+str(out/'probe.exe')+'"\nif errorlevel 1 exit /b 1\ndumpbin /imports "'+str(out/'probe.exe')+'" > "'+str(out/'imports.txt')+'"\n')
 p=subprocess.run(['cmd','/d','/c',str(cmd)],capture_output=True,timeout=60);(out/'compile.log').write_bytes(p.stdout+p.stderr);results.append(dict(config=cfg,exit=p.returncode,exe_sha256=hashlib.sha256((out/'probe.exe').read_bytes()).hexdigest() if (out/'probe.exe').exists() else None))
(r/'build-results.json').write_text(json.dumps({'results':results,'source_sha256':{str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for d in ['host-live-candidate','host-candidate','transport-candidate','protocol-candidate'] for p in (r/d).glob('*') if p.is_file()}},indent=2));print(results)
raise SystemExit(any(x['exit'] for x in results))
