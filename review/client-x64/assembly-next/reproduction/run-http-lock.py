"""Native actual-header/TU HTTP lock probe. Diagnostic outputs never enter product checkout."""
from pathlib import Path
import subprocess,json,hashlib,struct,shutil
root=Path('C:/client-next-build');inputs=Path('C:/assembly-next')
source=root/'src/engine/client/library/clientGame/src/shared/HTTPpost/VeCritsec.cpp'
header=source.with_suffix('.hpp');project=root/'src/engine/client/library/clientGame/build/win32'
out=Path('C:/http-lock-next-v2');out.mkdir(exist_ok=False)
def q(v):return '"'+str(v)+'"'
results=[]
for config in ['Debug','Release']:
 for platform,arch,machine in [('Win32','x86',0x14c),('x64','amd64',0x8664)]:
  rows=[l.strip().split('|') for l in (Path('C:/client-next-results')/('clientGame-'+config+'-'+platform+'.audit.log')).read_text(encoding='utf-8-sig').splitlines() if l.strip().startswith('CL|')]
  row=next(r for r in rows if r[1].replace('\\','/').endswith('/VeCritsec.cpp'))
  modes=['candidate','stock']+(['broken-acquire','broken-release'] if config=='Release' and platform=='x64' else [])
  for mode in modes:
   d=out/(config+'-'+platform+'-'+mode);d.mkdir()
   text=(inputs/'stock-VeCritsec.hpp').read_text() if mode=='stock' else header.read_text()
   if mode.startswith('broken'):
    old,new=('_interlockedbittestandset( &m_iLock, 0 )','0') if mode=='broken-acquire' else ('_InterlockedExchange( &m_iLock, 0 );','/* diagnostic mutation: no release */')
    assert text.count(old)==1;text=text.replace(old,new)
   (d/'VeCritsec.hpp').write_text(text);shutil.copyfile(source,d/'VeCritsec.cpp');shutil.copyfile(inputs/'http-lock-probe.cpp',d/'probe.cpp')
   common=['/nologo','/EHsc','/Y-','/Zc:wchar_t-','/volatile:ms','/Gy','/MTd' if config=='Debug' else '/MT','/Od' if config=='Debug' else '/O2','/I'+q(root/'src'),'/I'+q(d)]
   common+=['/D'+q(v) for v in row[6].split(';') if v]+['/I'+q(v) for v in row[7].split(';') if v]
   cmds=[]
   for label,file in [('production','VeCritsec.cpp'),('probe','probe.cpp')]:
    rsp=d/(label+'.rsp');rsp.write_text(' '.join(common+['/c',q(d/file),'/Fo'+q(d/(label+'.obj'))]))
    cmds.append('cl @'+q(rsp)+'\nif errorlevel 1 exit /b %errorlevel%')
   cmds.append('link /nologo /NODEFAULTLIB:stlport_vc71_static.lib '+q(d/'probe.obj')+' /OUT:'+q(d/'probe.exe')+' /MAP:'+q(d/'probe.map')+' kernel32.lib')
   bat=d/'build.cmd';bat.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\nif errorlevel 1 exit /b %errorlevel%\nwhere cl\n'+'\n'.join(cmds)+'\nexit /b %errorlevel%\n')
   p=subprocess.run(['cmd','/c',str(bat)],cwd=str(project),stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'build.log').write_bytes(p.stdout)
   code=None;output='';actualmachine=None;binding=False
   if p.returncode==0:
    actualmachine=struct.unpack('<H',(d/'production.obj').read_bytes()[:2])[0]
    binding='yield_thread@VeCritsec' not in (d/'probe.map').read_text(errors='replace') # No substitute implementation linked; actual header operations only
    try:
     r=subprocess.run([str(d/'probe.exe')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=45);code=r.returncode;output=r.stdout.decode(errors='replace')
    except subprocess.TimeoutExpired as e: code='timeout';output=(e.stdout or b'').decode(errors='replace')
    (d/'run.log').write_text(output)
   if mode=='stock' and platform=='x64':okay=p.returncode!=0 and b'C4235' in p.stdout
   elif mode.startswith('broken'):okay=p.returncode==0 and code==1 and 'FAIL ' in output and binding and actualmachine==machine
   else:okay=p.returncode==0 and code==0 and output.splitlines().count('SUMMARY 27/27')==1 and sum(l.startswith('PASS ') for l in output.splitlines())==27 and binding and actualmachine==machine
   results.append(dict(name=d.name,compile=p.returncode,run=code,expected_outcome=okay,machine=actualmachine,binding=binding,header_sha256=hashlib.sha256((d/'VeCritsec.hpp').read_bytes()).hexdigest(),tu_sha256=hashlib.sha256((d/'VeCritsec.cpp').read_bytes()).hexdigest(),output=output))
(out/'results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results));raise SystemExit(0 if all(r['expected_outcome'] for r in results) else 1)
