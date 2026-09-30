from pathlib import Path
import subprocess,json
r=Path('C:/miles-schema-check-v2');r.mkdir(exist_ok=True);results=[]
for arch in ['x86','amd64']:
 out=r/arch;out.mkdir(exist_ok=True)
 b=out/'compile.cmd';b.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\nif errorlevel 1 exit /b 1\ncl /nologo /c /EHsc /DWIN32 /IC:/client-next-build/src/external/3rd/library/miles/include C:/sdk-declarations-v2.cpp /Fo'+str(out/'schema.obj')+'\n')
 p=subprocess.run(['cmd','/d','/c',str(b)],capture_output=True);(out/'compile.log').write_bytes(p.stdout+p.stderr);results.append(dict(arch=arch,exit=p.returncode))
(r/'results.json').write_text(json.dumps(results,indent=2));print(results)
