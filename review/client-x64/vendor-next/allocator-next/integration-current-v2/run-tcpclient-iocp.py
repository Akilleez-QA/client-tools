from pathlib import Path
import subprocess,json
out=Path('C:/tcpclient-iocp-v1');out.mkdir(exist_ok=False);records=[]
for cfg in ['Release','Debug']:
 for platform,arch in [('Win32','x86'),('x64','amd64')]:
  d=out/(cfg+'-'+platform);d.mkdir();bat=d/'build.cmd';bat.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\ncl /nologo /EHsc '+('/MTd /Od' if cfg=='Debug' else '/MT /O2')+' /I"C:/integration-current-v1/workspace/repo/src/external/3rd/library/miles/include" C:/tcpclient-iocp-probe.cpp /Fo"'+str(d/'probe.obj')+'" /Fe"'+str(d/'probe.exe')+'"\nexit /b %errorlevel%\n')
  r=subprocess.run(['cmd','/c',str(bat)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'build.log').write_bytes(r.stdout);row=dict(configuration=cfg,platform=platform,compile=r.returncode);records.append(row)
  if r.returncode==0:
   r=subprocess.run([str(d/'probe.exe')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'run.log').write_bytes(r.stdout);row.update(run=r.returncode,output=r.stdout.decode())
  (out/'results.json').write_text(json.dumps(records,indent=2));print(row,flush=True)
