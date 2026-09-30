from pathlib import Path
import subprocess,json,hashlib,re,struct
root=Path('C:/client-next-build');inp=Path('C:/allocator-minimum-input');out=Path('C:/allocator-minimum-v1');out.mkdir(exist_ok=False)
libs=json.loads((Path('C:/allocator-next')/'core-libraries-all.json').read_text());results=[]
source=inp/'MemoryManager-stats-candidate.cpp';project=root/'src/engine/shared/library/sharedMemoryManager/build/win32'
q=lambda s:'"'+str(s)+'"'
for cfg in ['Release','Debug']:
 for platform,arch,machine in [('Win32','x86',0x14c),('x64','amd64',0x8664)]:
  d=out/(cfg+'-'+platform);d.mkdir();item=dict(name=d.name);results.append(item)
  try:
   if cfg+'-'+platform not in libs:raise RuntimeError('No matching real dependency library list')
   text=source.read_text()
   for key in []:
    text,n=re.subn(r'(?m)^#define '+key+r' +0$', '#define '+key+(' 5' if key=='DO_TRACK' else ' 1'),text);assert n==1
   (d/'MemoryManager-diagnostic.cpp').write_text(text)
   probe=(inp/'probe.cpp').read_text()
   (d/'probe.cpp').write_text(probe)
   for extra in ['MemoryManager-candidate.h','InstallTimer-candidate.h','InstallTimer-candidate.cpp']:
    (d/extra).write_bytes((inp/extra).read_bytes())
   row=next(l.strip().split('|') for l in (Path('C:/client-next-results')/('sharedMemoryManager-'+cfg+'-'+platform+'.audit.log')).read_text(encoding='utf-8-sig').splitlines() if l.strip().startswith('CL|') and '/MemoryManager.cpp' in l.replace('\\','/'))
   flags=['/EHsc','/Y-','/Gy','/Zi','/Zc:wchar_t-','/MTd' if cfg=='Debug' else '/MT','/Od' if cfg=='Debug' else '/O2']+['/D'+q(x) for x in row[6].split(';') if x]+['/I'+q(x) for x in row[7].split(';') if x]
   deps=libs[cfg+'-'+platform]
   dbg=root/'src/engine/shared/library/sharedDebug/src/win32/DebugHelp.cpp'
   dbgrow=next(l.strip().split('|') for l in (Path('C:/client-next-results')/('sharedDebug-'+cfg+'-'+platform+'.audit.log')).read_text(encoding='utf-8-sig').splitlines() if l.strip().startswith('CL|') and '/DebugHelp.cpp' in l.replace('\\','/'))
   dbgflags=['/EHsc','/Y-','/Gy','/Zi','/Zc:wchar_t-','/MTd' if cfg=='Debug' else '/MT','/Od' if cfg=='Debug' else '/O2']+['/D'+q(x) for x in dbgrow[6].split(';') if x]+['/I'+q(x) for x in dbgrow[7].split(';') if x]
   # Resolve relative header paths against sharedDebug's own project.
   dbgcommand='cd /d '+q(root/'src/engine/shared/library/sharedDebug/build/win32')+'\n'+' '.join(['cl']+dbgflags+['/c',q(dbg),'/Fo'+q(d/'debughelp.obj')])+'\nif errorlevel 1 exit /b %errorlevel%\ncd /d '+q(project)+'\n'
   dbgcommand=dbgcommand.replace('cd /d '+q(project)+'\n', ' '.join(['cl']+dbgflags+['/c',q(d/'InstallTimer-candidate.cpp'),'/Fo'+q(d/'installtimer.obj')])+'\nif errorlevel 1 exit /b %errorlevel%\ncd /d '+q(project)+'\n')
   item['debughelp_sha256']=hashlib.sha256(dbg.read_bytes()).hexdigest()
   cmd=' '.join(['link /nologo /DEBUG /OPT:REF /INCREMENTAL:NO /NODEFAULTLIB:stlport_vc71_static.lib','/OUT:'+q(d/'probe.exe'),'/MAP:'+q(d/'probe.map'),q(d/'probe.obj'),q(d/'debughelp.obj'),q(d/'installtimer.obj')]+[q(x) for x in deps]+['kernel32.lib user32.lib advapi32.lib winmm.lib gdi32.lib shell32.lib'])
   bat=d/'build.cmd';bat.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\nif errorlevel 1 exit /b %errorlevel%\n'+' '.join(['cl']+flags+['/c',q(d/'probe.cpp'),'/Fo'+q(d/'probe.obj'),'/Fd'+q(d/'probe.pdb')])+'\nif errorlevel 1 exit /b %errorlevel%\n'+dbgcommand+cmd+'\nexit /b %errorlevel%\n')
   rr=subprocess.run(['cmd','/c',str(bat)],cwd=project,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180);(d/'build.log').write_bytes(rr.stdout);item['build']=rr.returncode
   item['source_sha256']=hashlib.sha256(source.read_bytes()).hexdigest();item['diagnostic_sha256']=hashlib.sha256((d/'MemoryManager-diagnostic.cpp').read_bytes()).hexdigest()
   if rr.returncode:raise RuntimeError('Real compilation/link failed')
   assert struct.unpack('<H',(d/'probe.obj').read_bytes()[:2])[0]==machine
   mapping=(d/'probe.map').read_text();assert any('getCallStack@DebugHelp' in x and 'debughelp.obj' in x for x in mapping.splitlines());assert 'OsNewDel.obj' in mapping or 'osnewdel.obj' in mapping.lower()
   if platform=='Win32':
    import shutil
    shutil.copyfile(Path('C:/allocator-next')/'dbghelp_6.3.17.0.dll',d/'dbghelp_6.3.17.0.dll')
   rr=subprocess.run([str(d/'probe.exe')],cwd=d,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60);(d/'run.log').write_bytes(rr.stdout);item.update(run=rr.returncode,output=rr.stdout.decode(errors='replace'))
   item['okay']=rr.returncode==0 and 'checks=1622 failures=0 expected=1622' in item['output']
  except Exception as exc:item['error']=str(exc)
  (out/'results.json').write_text(json.dumps(results,indent=2));print(item,flush=True)
