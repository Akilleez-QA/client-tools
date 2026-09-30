from pathlib import Path
import subprocess,json
out=Path('C:/crypto-pack-controls-v2');out.mkdir(exist_ok=False);root=Path('C:/integration-current-v1/workspace/repo');rows=[]
for cfg in ['Release','Debug']:
 for platform,arch in [('Win32','x86'),('x64','amd64')]:
  d=out/(cfg+'-'+platform);d.mkdir();includes=[root/'src/external/3rd/library/stlport453/stlport',root/'src/external/ours/library/crypto/src/shared/core',root/'src/external/ours/library/crypto/src/shared/original']
  flags=['/nologo','/EHsc','/W3','/MTd' if cfg=='Debug' else '/MT','/Od' if cfg=='Debug' else '/O2','/D_DEBUG' if cfg=='Debug' else '/DNDEBUG','/D_CRT_SECURE_NO_DEPRECATE=1']+['/I"'+str(p)+'"' for p in includes]
  lib={('Release','Win32'):'C:/client-next-build/src/external/3rd/library/stlport453/lib/win32/stlport_vc71_static.lib',('Release','x64'):'C:/stlport-full-next-v2/stlport-v120-amd64-Release-full.lib',('Debug','Win32'):'C:/stlport-full-next-win32-debug-v1/stlport-v120-x86-Debug-full.lib',('Debug','x64'):'C:/stlport-full-next-x64-debug-v1/stlport-v120-amd64-Debug-full.lib'}[(cfg,platform)]
  for kind in ['positive','negative']:
   src=d/(kind+'.cpp');src.write_text('#include "C:/crypto-packing-input/FirstCrypto.h"\n'+('#include "C:/crypto-packing-input/leaky-pack.h"\n' if kind=='negative' else ''))
   bat=d/(kind+'.cmd');bat.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\ncl '+' '.join(flags)+' /WX /c "'+str(src)+'" /Fo"'+str(d/(kind+'.obj'))+'"\nexit /b %errorlevel%\n')
   r=subprocess.run(['cmd','/c',str(bat)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/(kind+'.log')).write_bytes(r.stdout);row=dict(configuration=cfg,platform=platform,kind=kind,exit=r.returncode,expected=(r.returncode==0 if kind=='positive' else r.returncode!=0 and b'C4103' in r.stdout));rows.append(row)
  (out/'results.json').write_text(json.dumps(rows,indent=2));print(row,flush=True)
