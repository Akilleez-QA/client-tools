import subprocess,json
from pathlib import Path
out=Path('C:/client-next-probes');out.mkdir(exist_ok=True)
vc=Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat');results=[]
for arch in ['x86','amd64']:
 for variant,define in [('original','/DORIGINAL'),('body-only','/DBODY_ONLY'),('rename','')]:
  name=arch+'-'+variant;exe=out/(name+'.exe');obj=out/(name+'.obj')
  bat=out/(name+'.cmd');bat.write_text('@echo off\ncall "'+str(vc)+'" '+arch+' >nul\ncl /nologo /EHsc '+define+' C:\\memmove-rename-probe.cpp /Fo"'+str(obj)+'" /Fe"'+str(exe)+'"\nexit /b %errorlevel%\n')
  p=subprocess.run(['cmd','/c',str(bat)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(out/(name+'.log')).write_bytes(p.stdout)
  run=None
  if p.returncode==0:
   r=subprocess.run([str(exe)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(out/(name+'.run.log')).write_bytes(r.stdout);run=r.returncode
  results.append({'name':name,'compile':p.returncode,'run':run})
(out/'results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results))
