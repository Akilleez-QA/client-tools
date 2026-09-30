from pathlib import Path
import subprocess,json,hashlib,os,shutil,struct
out=Path('C:/vivox-wrapper-source-v1');out.mkdir(exist_ok=False);root=Path('C:/integration-current-v2/workspace/repo');vendor=root/'src/external/3rd/library';rows=[]
for cfg in ['Release','Debug']:
 for arch in ['x86','amd64']:
  d=out/(cfg+'-'+arch);d.mkdir();setup=d/'env.cmd';setup.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\nif errorlevel 1 exit /b %errorlevel%\nset\n');r=subprocess.run(['cmd','/d','/c',str(setup)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);assert r.returncode==0
  env={k.upper():v for k,v in os.environ.items()}
  for line in r.stdout.decode(errors='replace').splitlines():
   if '=' in line and not line.startswith('='):
    k,v=line.split('=',1);env[k.upper()]=v
  cl=shutil.which('cl.exe',path=env['PATH']);lib=shutil.which('lib.exe',path=env['PATH']);dump=shutil.which('dumpbin.exe',path=env['PATH'])
  flags=['/nologo','/c','/W4','/EHsc','/GR','/Zc:wchar_t-','/MTd' if cfg=='Debug' else '/MT','/Od' if cfg=='Debug' else '/O2','/D_DEBUG' if cfg=='Debug' else '/DNDEBUG','/DWIN32','/D_WINDOWS','/D_MBCS','/DVIVOX_VERSION=3','/I'+str(vendor/'stlport453/stlport'),'/I'+str(vendor/'vivox/include')]
  obj=d/'Vivox.obj';cmd=[cl]+flags+[str(vendor/'vivoxSharedWrapper/Vivox.cpp'),'/Fo'+str(obj)];(d/'compile.cmd.json').write_text(json.dumps(cmd,indent=2));r=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'compile.log').write_bytes(r.stdout);row=dict(configuration=cfg,arch=arch,compile_exit=r.returncode)
  if r.returncode==0:
   assert struct.unpack('<H',obj.read_bytes()[:2])[0]==(0x14c if arch=='x86' else 0x8664)
   target=d/'vivoxSharedWrapper.lib';cmd=[lib,'/nologo','/OUT:'+str(target),str(obj)];r=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'archive.log').write_bytes(r.stdout);row['archive_exit']=r.returncode;row['sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
   for flag in ['symbols','directives']:
    r=subprocess.run([dump,'/'+flag,str(obj)],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/(flag+'.txt')).write_bytes(r.stdout)
  rows.append(row);(out/'results.json').write_text(json.dumps(rows,indent=2));print(row,flush=True)
(out/'inputs.json').write_text(json.dumps({str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for base in [vendor/'vivox/include',vendor/'vivoxSharedWrapper'] for p in base.rglob('*') if p.is_file() and p.suffix in ['.h','.cpp','.inl']},indent=2))
