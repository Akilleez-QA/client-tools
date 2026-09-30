from pathlib import Path
import subprocess,json
out=Path('C:/crypto-pack-v2');out.mkdir(exist_ok=False);root=Path('C:/integration-current-v1/workspace/repo');rows=[]
for cfg in ['Release','Debug']:
 for platform,arch in [('Win32','x86'),('x64','amd64')]:
  d=out/(cfg+'-'+platform);d.mkdir();includes=[root/'src/external/3rd/library/stlport453/stlport',root/'src/external/ours/library/crypto/src/shared/core',root/'src/external/ours/library/crypto/src/shared/original']
  flags=['/nologo','/EHsc','/W3','/MTd' if cfg=='Debug' else '/MT','/Od' if cfg=='Debug' else '/O2','/D_DEBUG' if cfg=='Debug' else '/DNDEBUG','/D_CRT_SECURE_NO_DEPRECATE=1']+['/I"'+str(p)+'"' for p in includes]
  lib={('Release','Win32'):'C:/client-next-build/src/external/3rd/library/stlport453/lib/win32/stlport_vc71_static.lib',('Release','x64'):'C:/stlport-full-next-v2/stlport-v120-amd64-Release-full.lib',('Debug','Win32'):'C:/stlport-full-next-win32-debug-v1/stlport-v120-x86-Debug-full.lib',('Debug','x64'):'C:/stlport-full-next-x64-debug-v1/stlport-v120-amd64-Debug-full.lib'}[(cfg,platform)]
  bat=d/'build.cmd';bat.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\ncl '+' '.join(flags)+' C:/crypto-pack-probe.cpp /Fo"'+str(d/'probe.obj')+'" /Fe"'+str(d/'probe.exe')+'" /link /NODEFAULTLIB:stlport_vc71_static.lib /NODEFAULTLIB:stlport_vc71_stldebug_static.lib "'+lib+'"\nexit /b %errorlevel%\n')
  r=subprocess.run(['cmd','/c',str(bat)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'build.log').write_bytes(r.stdout);row=dict(configuration=cfg,platform=platform,compile=r.returncode);rows.append(row)
  if r.returncode==0:
   r=subprocess.run([str(d/'probe.exe')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'run.log').write_bytes(r.stdout);row.update(run=r.returncode,output=r.stdout.decode())
  (out/'results.json').write_text(json.dumps(rows,indent=2));print(row,flush=True)
