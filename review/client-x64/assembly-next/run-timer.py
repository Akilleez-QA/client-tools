from pathlib import Path
import subprocess,json,hashlib,struct
r=Path('C:/client-next-build');inp=Path('C:/allocator-next');out=Path('C:/timer-next-v2');out.mkdir(exist_ok=False)
source=r/'src/engine/shared/library/sharedDebug/src/win32/ProfilerTimer.cpp';project=r/'src/engine/shared/library/sharedDebug/build/win32'
def q(v):return '"'+str(v)+'"'
results=[]
for config in ['Debug','Release']:
 for platform,arch,machine in [('Win32','x86',0x14c),('x64','amd64',0x8664)]:
  rows=[l.strip().split('|') for l in (Path('C:/client-next-results')/('sharedDebug-'+config+'-'+platform+'.audit.log')).read_text(encoding='utf-8-sig').splitlines() if l.strip().startswith('CL|')]
  row=next(x for x in rows if x[1].replace('\\','/').endswith('/ProfilerTimer.cpp'))
  for mode in ['candidate','stock']+(['zero'] if platform=='x64' else []):
   d=out/(config+'-'+platform+'-'+mode);d.mkdir()
   tu=source if mode=='candidate' else inp/'stock-ProfilerTimer.cpp'
   if mode=='zero':
    text=source.read_text();assert text.count('return static_cast<__int64>(__rdtsc());')==1;tu=d/'zero.cpp';tu.write_text(text.replace('return static_cast<__int64>(__rdtsc());','return 0;'))
   text=tu.read_text()
   start=text.index('#if defined(_M_X64)') if '#if defined(_M_X64)' in text else text.index('static __int64 __declspec(naked)')
   end=text.index('\n#endif',start)+len('\n#endif') if '#if defined(_M_X64)' in text else text.index('// ======================================================================',start)
   helper=text[start:end]
   probe=d/'probe.cpp';probe.write_text('#include <windows.h>\n#include <intrin.h>\n'+helper+'\n'+(inp/'timer-probe.cpp').read_text())
   flags=['/EHsc','/Y-','/Gy','/Zc:wchar_t-','/MTd' if config=='Debug' else '/MT','/Od' if config=='Debug' else '/O2']+['/D'+q(v) for v in row[6].split(';') if v]+['/I'+q(v) for v in row[7].split(';') if v]
   tu_rsp=d/'production.rsp';tu_rsp.write_text(' '.join(flags+['/c',q(tu),'/Fo'+q(d/'production.obj')]))
   rsp=d/'probe.rsp';rsp.write_text(' '.join(flags+['/c',q(probe),'/Fo'+q(d/'probe.obj')]))
   bat=d/'build.cmd';bat.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\nif errorlevel 1 exit /b %errorlevel%\ncl @'+q(tu_rsp)+'\nif errorlevel 1 exit /b %errorlevel%\ncl @'+q(rsp)+'\nif errorlevel 1 exit /b %errorlevel%\nlink /nologo /OPT:REF /NODEFAULTLIB:stlport_vc71_static.lib '+q(d/'probe.obj')+' kernel32.lib /OUT:'+q(d/'probe.exe')+'\nexit /b %errorlevel%\n')
   p=subprocess.run(['cmd','/c',str(bat)],cwd=str(project),stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'build.log').write_bytes(p.stdout)
   code=None;output='';objmachine=None
   if p.returncode==0:
    objmachine=struct.unpack('<H',(d/'probe.obj').read_bytes()[:2])[0]
    rr=subprocess.run([str(d/'probe.exe')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=30);code=rr.returncode;output=rr.stdout.decode(errors='replace');(d/'run.log').write_text(output)
   okay=(p.returncode!=0 and (b'C2485' in p.stdout or b'C4235' in p.stdout)) if mode=='stock' and platform=='x64' else p.returncode==0 and objmachine==machine and ((code==1 and 'FAIL timestamp' in output) if mode=='zero' else code==0 and output.strip()=='PASS 10000 bracketed TSC samples')
   results.append(dict(name=d.name,compile=p.returncode,run=code,output=output,expected_outcome=okay,source_sha256=hashlib.sha256(tu.read_bytes()).hexdigest()))
(out/'results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results));raise SystemExit(not all(x['expected_outcome'] for x in results))
