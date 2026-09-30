import os,subprocess,json,hashlib
from pathlib import Path
out=Path('C:/vendor-lcd-integration/real-wrapper-v4');out.mkdir(parents=True,exist_ok=False)
base=Path('C:/vendor-reachability/lcd-legacy-v2');minimum=Path('C:/allocator-minimum-v1');root=Path('C:/client-next-build')
core=json.loads(Path('C:/allocator-next/core-libraries-all.json').read_text());results=[]
for cfg in ['Release','Debug']:
 for platform in ['Win32','x64']:
  name=cfg+'-'+platform;d=out/name;d.mkdir();old=base/name;mm=minimum/name;rec=dict(name=name);results.append(rec)
  try:
   v=subprocess.run(['cmd','/d','/c',str(old/'env.cmd')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60);assert v.returncode==0
   env={k.upper():v for k,v in os.environ.items()}
   for l in v.stdout.decode(errors='replace').splitlines():
    if '=' in l and not l.startswith('='):k,val=l.split('=',1);env[k.upper()]=val
   # Real MemoryManager implementation, with the exact candidate header used in its accepted minimum-block probe; no test main or substitute symbols.
   bridge=d/'MemoryManager-real.cpp';bridge.write_text('#include "'+(mm/'MemoryManager-candidate.h').as_posix()+'"\n#include "'+(mm/'MemoryManager-diagnostic.cpp').as_posix()+'"\n')
   build=(mm/'build.cmd').read_text();compile_line=next(l for l in build.splitlines() if l.startswith('cl ') and str(mm/'probe.cpp').replace('\\','/') in l.replace('\\','/'))
   compile_line=compile_line.replace('\\','/').replace((mm/'probe.cpp').as_posix(),bridge.as_posix()).replace((mm/'probe.obj').as_posix(),(d/'MemoryManager.obj').as_posix()).replace((mm/'probe.pdb').as_posix(),(d/'MemoryManager.pdb').as_posix())
   assert str(mm/'probe.cpp').replace('\\','/') not in compile_line
   (d/'compile.command.txt').write_text(compile_line)
   project=root/'src/engine/shared/library/sharedMemoryManager/build/win32'
   bat=d/'compile.cmd';bat.write_text('@echo off\n'+compile_line+'\nexit /b %errorlevel%\n')
   v=subprocess.run(['cmd','/d','/c',str(bat)],cwd=project,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120);(d/'compile.log').write_bytes(v.stdout);rec['allocator_compile']=v.returncode
   if v.returncode:raise RuntimeError('real allocator compilation failed')
   cmd=json.loads((old/'link.command.json').read_text());cmd=[x for x in cmd if not x.startswith('/OUT:')]+['/OUT:'+str(d/'probe.exe'),'/MAP:'+str(d/'probe.map'),'/SUBSYSTEM:CONSOLE','/NODEFAULTLIB:stlport_vc71_static.lib','/NODEFAULTLIB:stlport_vc71_stldebug_static.lib',str(d/'MemoryManager.obj'),str(mm/'debughelp.obj'),str(mm/'installtimer.obj')]+core[name]+['kernel32.lib','shell32.lib','/VERBOSE:LIB']
   (d/'link.command.json').write_text(json.dumps(cmd,indent=2));rec['input_hashes']={x:hashlib.sha256(Path(x).read_bytes()).hexdigest() for x in cmd if Path(x).is_file()}
   v=subprocess.run(cmd,cwd=old,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120);(d/'link.log').write_bytes(v.stdout);rec['link']=v.returncode
   rec['executed']=False
   if not v.returncode:
    mapping=(d/'probe.map').read_text();rec['real_owner_allocator_in_map']='OsNewDel' in mapping or 'osnewdel' in mapping.lower();rec['real_memory_manager_in_map']='MemoryManager.obj' in mapping
  except Exception as e:rec['error']=str(e)
  (out/'results.json').write_text(json.dumps(results,indent=2));print(rec.get('name'),rec.get('allocator_compile'),rec.get('link'),rec.get('error'),flush=True)
