from pathlib import Path
import subprocess,json,hashlib,shutil,struct
r=Path('C:/client-next-build');inp=Path('C:/allocator-next');out=Path('C:/stack-owner-Debug-v1');out.mkdir(exist_ok=False)
libs=json.loads((inp/'core-libraries-all.json').read_text());results=[]
q=lambda x:'"'+str(x)+'"'
project=r/'src/engine/shared/library/sharedDebug/build/win32';source=r/'src/engine/shared/library/sharedDebug/src/win32/DebugHelp.cpp'
for platform,arch,machine in [('Win32','x86',0x14c),('x64','amd64',0x8664)]:
 d=out/platform;d.mkdir();rows=[x.strip().split('|') for x in (Path('C:/client-next-results')/('sharedDebug-Debug-'+platform+'.audit.log')).read_text(encoding='utf-8-sig').splitlines() if x.strip().startswith('CL|')];row=next(x for x in rows if x[1].replace('\\','/').endswith('/DebugHelp.cpp'))
 flags=['/EHsc','/Y-','/Gy','/MTd','/Od','/Zi','/Zc:wchar_t-']+['/D'+q(x) for x in row[6].split(';') if x]+['/I'+q(x) for x in row[7].split(';') if x]
 deps=libs['Debug-'+platform];cmd=' '.join(['link /nologo /DEBUG /OPT:REF /INCREMENTAL:NO /NODEFAULTLIB:stlport_vc71_static.lib','/OUT:'+q(d/'probe.exe'),'/MAP:'+q(d/'probe.map'),'/PDB:'+q(d/'probe.pdb')]+(['/BASE:0x140000000'] if platform=='x64' else [])+[q(d/'production.obj'),q(d/'probe.obj')]+[q(x) for x in deps]+['kernel32.lib user32.lib advapi32.lib winmm.lib gdi32.lib shell32.lib'])
 bat=d/'build.cmd';bat.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\nif errorlevel 1 exit /b %errorlevel%\n'+' '.join(['cl']+flags+['/c',q(source),'/Fo'+q(d/'production.obj')])+'\nif errorlevel 1 exit /b %errorlevel%\n'+' '.join(['cl']+flags+['/c',q(Path('C:/stack-owner-probe.cpp')),'/Fo'+q(d/'probe.obj')])+'\nif errorlevel 1 exit /b %errorlevel%\n'+cmd+'\nexit /b %errorlevel%\n')
 rr=subprocess.run(['cmd','/c',str(bat)],cwd=project,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'build.log').write_bytes(rr.stdout)
 item=dict(platform=platform,build=rr.returncode,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest());results.append(item)
 if not rr.returncode:
  assert struct.unpack('<H',(d/'production.obj').read_bytes()[:2])[0]==machine
  mapping=(d/'probe.map').read_text();assert any('getCallStack@DebugHelp' in x and 'production.obj' in x for x in mapping.splitlines())
  if platform=='Win32':shutil.copyfile(inp/'dbghelp_6.3.17.0.dll',d/'dbghelp_6.3.17.0.dll')
  try:
   rr=subprocess.run([str(d/'probe.exe')],cwd=d,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90);(d/'run.log').write_bytes(rr.stdout);item.update(run=rr.returncode,text=rr.stdout.decode(errors='replace'),exe_sha256=hashlib.sha256((d/'probe.exe').read_bytes()).hexdigest())
  except subprocess.TimeoutExpired as exc:item['run']='TIMEOUT';(d/'run.log').write_bytes(exc.stdout or b'')
 (out/'results.json').write_text(json.dumps(results,indent=2));print(item,flush=True)
raise SystemExit(any(x['build'] or x.get('run')!=0 for x in results))
