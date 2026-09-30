"""Actual production ByteOrder TU, real headers and native v120; no SDK/header shims."""
from pathlib import Path
import subprocess,json,hashlib,struct
root=Path('C:/client-next-build')
source=root/'src/engine/shared/library/sharedFoundation/src/win32/ByteOrder.cpp'
project=root/'src/engine/shared/library/sharedFoundation/build/win32'
probe=Path('C:/assembly-next/byteorder-probe.cpp')
out=Path('C:/byteorder-next-v3');out.mkdir(exist_ok=False)
stock=Path('C:/assembly-next/stock-ByteOrder.cpp')
assert source.read_text().count('return _byteswap_ulong(hostLong);')==1
broken=out/'broken.cpp';broken.write_text(source.read_text().replace('return _byteswap_ulong(hostLong);','return hostLong;'))
def q(x):return '"'+str(x)+'"'
results=[]
for config in ['Debug','Release']:
 for platform,arch,machine in [('Win32','x86',0x14c),('x64','amd64',0x8664)]:
  audit=Path('C:/client-next-results')/('sharedFoundation-'+config+'-'+platform+'.audit.log')
  rows=[l.strip().split('|') for l in audit.read_text(encoding='utf-8-sig').splitlines() if l.strip().startswith('CL|')]
  row=next(r for r in rows if r[1].replace('\\','/').endswith('/ByteOrder.cpp'))
  defs=['/D'+q(v) for v in row[6].split(';') if v]
  inc=['/I'+q(v) for v in row[7].split(';') if v]
  for mode,tu in [('candidate',source),('stock',stock),('broken',broken)]:
   if mode=='broken' and platform=='Win32':continue
   name=config+'-'+platform+'-'+mode;d=out/name;d.mkdir()
   common=['/nologo','/EHsc','/Y-','/Zc:wchar_t-','/Gy','/MTd' if config=='Debug' else '/MT','/Od' if config=='Debug' else '/O2']+defs+inc
   commands=[]
   for label,path in [('production',tu),('probe',probe)]:
    rsp=d/(label+'.rsp');rsp.write_text(' '.join(common+['/c',q(path),'/Fo'+q(d/(label+'.obj'))]))
    commands.append('cl @'+q(rsp)+'\nif errorlevel 1 exit /b %errorlevel%')
   commands.append('link /nologo /NODEFAULTLIB:stlport_vc71_static.lib '+q(d/'production.obj')+' '+q(d/'probe.obj')+' /OUT:'+q(d/'probe.exe')+' /MAP:'+q(d/'probe.map'))
   bat=d/'build.cmd';bat.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\nif errorlevel 1 exit /b %errorlevel%\nwhere cl\n'+'\n'.join(commands)+'\nexit /b %errorlevel%\n')
   p=subprocess.run(['cmd','/c',str(bat)],cwd=str(project),stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'build.log').write_bytes(p.stdout)
   r=None;output='';objmachine=None
   if p.returncode==0:
    mapping=(d/'probe.map').read_text(errors='replace')
    assert all(any('?'+symbol+'@@' in line and 'production.obj' in line for line in mapping.splitlines()) for symbol in ['htonl','ntohl','htons','ntohs']),mapping
    objmachine=struct.unpack('<H',(d/'production.obj').read_bytes()[:2])[0]
    run=subprocess.run([str(d/'probe.exe')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);r=run.returncode;output=run.stdout.decode(errors='replace');(d/'run.log').write_bytes(run.stdout)
   expected_compile_failure=mode=='stock' and platform=='x64'
   okay=(p.returncode!=0 and ('C2485' in p.stdout.decode(errors='replace') or 'C4235' in p.stdout.decode(errors='replace'))) if expected_compile_failure else (p.returncode==0 and objmachine==machine and (r==1 and 'FAIL long' in output if mode=='broken' else r==0 and output.strip()=='PASS 166631 input cases (both directions)'))
   results.append(dict(name=name,compile=p.returncode,run=r,machine=objmachine,expected_outcome=okay,output=output,source_sha256=hashlib.sha256(tu.read_bytes()).hexdigest()))
(out/'results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results));raise SystemExit(0 if all(r['expected_outcome'] for r in results) else 1)
