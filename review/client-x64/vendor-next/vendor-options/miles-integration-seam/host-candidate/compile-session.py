from pathlib import Path
import tarfile,subprocess,json,hashlib
r=Path('C:/miles-session-v1');r.mkdir(exist_ok=True)
with tarfile.open('C:/miles-session-input-v1.tar') as t:t.extractall(r)
results=[]
for cfg in ['Debug','Release']:
 o=r/cfg;o.mkdir(exist_ok=True)
 flags='/nologo /EHsc /W4 /WX /DWIN32 '+('/MTd /Od' if cfg=='Debug' else '/MT /O2')+' /IC:/client-next-build/src/external/3rd/library/miles/include '
 b=o/'build.cmd';b.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86 >nul\nif errorlevel 1 exit /b 1\ncl '+flags+' /c '+str(r/'host-candidate/session_lifecycle.cpp')+' /Fo'+str(o/'host.obj')+'\nif errorlevel 1 exit /b 1\ncl '+flags+' '+str(r/'host-candidate/session_lifecycle_test.cpp')+' '+str(o/'host.obj')+' C:/client-next-build/src/external/3rd/library/miles/lib/win/Mss32.lib delayimp.lib /Fe'+str(o/'preflight.exe')+' /link /DELAYLOAD:mss32.dll\nif errorlevel 1 exit /b 1\ndumpbin /symbols '+str(o/'host.obj')+' > '+str(o/'symbols.txt')+'\n')
 p=subprocess.run(['cmd','/d','/c',str(b)],cwd=o,capture_output=True);(o/'build.log').write_bytes(p.stdout+p.stderr);entry=dict(cfg=cfg,build_exit=p.returncode);results.append(entry)
 if not p.returncode:
  p=subprocess.run([str(o/'preflight.exe')],cwd=o,capture_output=True,timeout=20);(o/'run.log').write_bytes(p.stdout+p.stderr);entry.update(run_exit=p.returncode,text=p.stdout.decode(errors='replace'))
(r/'results.json').write_text(json.dumps(results,indent=2));print(results)
