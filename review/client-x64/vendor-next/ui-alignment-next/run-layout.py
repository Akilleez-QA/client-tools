from pathlib import Path
import subprocess,json,struct,hashlib
out=Path('C:/ui-alignment-readonly-v1');out.mkdir(exist_ok=False)
project=Path('C:/client-next-build/src/external/3rd/library/ui/build/win32')
source=Path('C:/ui-layout-probe.cpp');results=[]
q=lambda p:'"'+str(p)+'"'
for cfg in ['Debug','Release']:
 for plat,arch in [('Win32','x86'),('x64','amd64')]:
  name=cfg+'-'+plat;d=out/name;d.mkdir()
  audit=Path('C:/client-next-results')/('ui-'+name+'.audit.log')
  rows=[l.strip().split('|') for l in audit.read_text(encoding='utf-8-sig').splitlines() if l.strip().startswith('CL|')];row=next(r for r in rows if r[1].replace('\\','/').endswith('/UiMemoryBlockManager.cpp'))
  flags=['/nologo','/EHsc','/Y-','/Zc:wchar_t-','/MTd' if cfg=='Debug' else '/MT']+['/D'+q(x) for x in row[6].split(';') if x]+['/I'+q(x) for x in row[7].split(';') if x]
  rsp=d/'compile.rsp';rsp.write_text(' '.join(flags+['/c',q(source),'/Fo'+q(d/'layout.obj')]))
  bat=d/'compile.cmd';bat.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\ncl @'+q(rsp)+'\nexit /b %errorlevel%\n')
  p=subprocess.run(['cmd','/c',str(bat)],cwd=project,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'compile.log').write_bytes(p.stdout);r=dict(name=name,compile=p.returncode,audit_sha256=hashlib.sha256(audit.read_bytes()).hexdigest())
  if not p.returncode:
   b=(d/'layout.obj').read_bytes();machine,nsec=struct.unpack_from('<HH',b);opt=struct.unpack_from('<H',b,16)[0]
   for i in range(nsec):
    offset=20+opt+40*i
    if b[offset:offset+8].rstrip(b'\0')==b'.layout':
     length,ptr=struct.unpack_from('<II',b,offset+16);r['values']=list(struct.unpack_from('<12I',b,ptr));r['machine']=machine
  results.append(r)
(out/'results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results));raise SystemExit(0 if all('values' in r for r in results) else 1)
