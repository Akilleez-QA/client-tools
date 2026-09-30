from pathlib import Path
import subprocess, json, hashlib, platform, sys
r=Path('C:/pipe-drain23')
cases=['idle','exchange','late-read','late-peer-error','buffered-input','partial-input','queued-write','partial-write','backpressure','completed-write','first-fault','external-abort','timeout']
old_failure={'late-read','late-peer-error','buffered-input','partial-input','partial-write','backpressure','completed-write'}
results=[]
(r/'environment.json').write_text(json.dumps(dict(platform=platform.platform(),python=sys.version,architecture=platform.machine(),configuration='VS2013 v120 amd64 Debug /MTd /Od /W4 /WX'),indent=2))
manifest={str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(r.rglob('*')) if p.is_file() and p.suffix in {'.cpp','.h','.py','.md','.patch'}}
(r/'run-input-manifest.json').write_text(json.dumps(manifest,indent=2))
for variant in ['old','candidate']:
 out=r/(variant+'-amd64-Debug');out.mkdir(exist_ok=True)
 cmd=out/'build.cmd'
 flags='/nologo /EHsc /W4 /WX /D_WIN32_WINNT=0x0601 /MTd /Od '+('/DDRAIN23_CANDIDATE ' if variant=='candidate' else '')
 cmd.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" amd64 >nul\nif errorlevel 1 exit /b 1\ncl '+flags+' /I"'+str(r/variant)+'" "'+str(r/'endpoint-under-test.cpp')+'" "'+str(r/'drain-fixture.cpp')+'" "'+str(r/variant/'transport-candidate/codec.cpp')+'" /Fe"'+str(out/'fixture.exe')+'"\n')
 p=subprocess.run(['cmd','/d','/c',str(cmd)],cwd=out,capture_output=True,timeout=60)
 (out/'build.log').write_bytes(p.stdout+p.stderr)
 results.append(dict(variant=variant,stage='build',exit=p.returncode))
 if p.returncode:
  print((p.stdout+p.stderr).decode(errors='replace'));break
 for case in cases:
  try:
   p=subprocess.run([str(out/'fixture.exe'),case],cwd=out,capture_output=True,timeout=15)
   log=p.stdout+p.stderr;(out/(case+'.log')).write_bytes(log)
   expected=1 if variant=='old' and case in old_failure else 0
   results.append(dict(variant=variant,case=case,exit=p.returncode,expected=expected,matches=p.returncode==expected))
   print(variant,case,'exit',p.returncode,'expected',expected,flush=True)
   if p.returncode!=expected:print(log.decode(errors='replace'),flush=True)
  except subprocess.TimeoutExpired as e:
   (out/(case+'.log')).write_bytes((e.stdout or b'')+(e.stderr or b''));results.append(dict(variant=variant,case=case,timeout=True));break
 (r/'results.json').write_text(json.dumps(results,indent=2))
(r/'results.json').write_text(json.dumps(results,indent=2))
artifacts={str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(r.rglob('*')) if p.is_file() and p.suffix in {'.exe','.log','.cmd'}}
(r/'output-manifest.json').write_text(json.dumps(artifacts,indent=2))
print(json.dumps(results,indent=2))
