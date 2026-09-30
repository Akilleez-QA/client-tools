import subprocess,json,tarfile
from pathlib import Path
root=Path('C:/socket-probe-source');root.mkdir(exist_ok=True)
with tarfile.open('C:/socket-candidate.tar') as a:a.extractall(root,filter='data')
out=Path('C:/socket-probe-results-v3');out.mkdir(exist_ok=True)
vc='C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat';results=[]
for arch in ['x86','amd64']:
 for sock,udp in [(1,0),(0,1),(0,2),(1,1),(1,2)]:
  for order in [0,1]:
   name=f'{arch}-s{sock}-u{udp}-w{order}';exe=out/(name+'.exe');obj=out/(name+'.obj')
   includes=[root/'src',root/'src/engine/shared/library/sharedNetwork/include/public',root/'src/external/3rd/library/soePlatform/VChatAPI/utils2.0/utils']
   bat=out/(name+'.cmd');cmd='cl /nologo /EHsc /W4 /DWIN32 /DSOCKET_PROBE_SOCK='+str(sock)+' /DSOCKET_PROBE_UDP='+str(udp)+' /DSOCKET_PROBE_WINSOCK_FIRST='+str(order)+' '+ ' '.join('/I"'+str(p)+'"' for p in includes)+' C:/socket-probe.cpp /Fo"'+str(obj)+'" /Fe"'+str(exe)+'" /link Ws2_32.lib'
   bat.write_text('@echo off\ncall "'+vc+'" '+arch+' >nul\n'+cmd+'\nexit /b %errorlevel%\n')
   p=subprocess.run(['cmd','/c',str(bat)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(out/(name+'.log')).write_bytes(p.stdout);run=None
   if p.returncode==0:
    p2=subprocess.run([str(exe)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=15);(out/(name+'.run.log')).write_bytes(p2.stdout);run=p2.returncode
   results.append({'name':name,'compile':p.returncode,'run':run})
(out/'results.json').write_text(json.dumps(results,indent=2)); print(json.dumps(results),flush=True)
