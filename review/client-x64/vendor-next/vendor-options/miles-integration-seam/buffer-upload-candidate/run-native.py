from pathlib import Path
import subprocess,tarfile,hashlib,json
b=Path(__file__).resolve().parent; seam=b.parent; vm=Path('/home/akilleez/Work/swg-source-vm/winbuild'); remote='C:/miles-upload-parent17-v2'
files=['buffer-upload-candidate/buffer_upload.cpp','buffer-upload-candidate/buffer_upload.h','buffer-upload-candidate/tests.cpp','protocol-candidate/miles_wire.h']
manifest={n:hashlib.sha256((seam/n).read_bytes()).hexdigest() for n in files};(b/'input-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
with tarfile.open(b/'input.tar','w') as t:
 for n in files:t.add(seam/n,arcname=n)
script=r'''from pathlib import Path
import subprocess,tarfile,json,hashlib
r=Path('C:/miles-upload-parent17-v2')
with tarfile.open(r/'input.tar') as t:t.extractall(r)
src=r/'buffer-upload-candidate'; results=[]
actual=src/'buffer_upload.cpp'; mutant=src/'buffer_upload_mutant.cpp'
text=actual.read_text();needle='if(filled!=storage.size())return false;';assert text.count(needle)==1
mutant.write_text(text.replace(needle,'/* negative control: premature seal allowed */',1))
for arch in ['x86','amd64']:
 for cfg in ['Debug','Release']:
  for variant in ['actual','premature-seal']:
   out=r/(arch+'-'+cfg+'-'+variant);out.mkdir()
   cmd=out/'build.cmd';exe=out/'test.exe'
   cpp=actual if variant=='actual' else mutant
   cmd.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\nif errorlevel 1 exit /b 1\ncd /d "'+str(out)+'"\ncl /nologo /EHsc /W4 /WX '+('/MTd /Od' if cfg=='Debug' else '/MT /O2')+' "'+str(cpp)+'" "'+str(src/'tests.cpp')+'" /Fe"'+str(exe)+'"\nexit /b %errorlevel%\n')
   p=subprocess.run(['cmd','/d','/c',str(cmd)],capture_output=True,timeout=60);(out/'build.log').write_bytes(p.stdout+p.stderr)
   row=dict(arch=arch,config=cfg,variant=variant,build_exit=p.returncode)
   if not p.returncode:
    p=subprocess.run([str(exe)],capture_output=True,timeout=10);log=p.stdout+p.stderr;(out/'run.log').write_bytes(log)
    row.update(run_exit=p.returncode,expected_observed=(b'PASS 29 upload mechanism checks' in log) if variant=='actual' else (p.returncode==1 and b'FAIL line' in log))
   results.append(row)
manifest={str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for d in ['buffer-upload-candidate','protocol-candidate'] for p in (r/d).glob('*') if p.is_file()}
(r/'results.json').write_text(json.dumps(dict(results=results,source_sha256=manifest),indent=2));print(json.dumps(results,indent=2))
raise SystemExit(any(x['build_exit'] or not x.get('expected_observed',False) or (x['variant']=='actual' and x.get('run_exit')) for x in results))
'''
(b/'native.py').write_text(script);commands=[]
def run(args,log,timeout=90):
 commands.append(args); p=subprocess.run(args,capture_output=True,timeout=timeout);(b/log).write_bytes(p.stdout+p.stderr)
 (b/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
 if p.returncode:raise RuntimeError((log,p.returncode,p.stderr.decode(errors='replace')))
 return p
scp=['scp','-q','-i',str(vm/'ssh/id_ed25519'),'-P','2223','-o','UserKnownHostsFile='+str(vm/'ssh/known_hosts')]
run([str(vm/'winps.sh'),f"if(Test-Path '{remote}'){{throw 'already exists'}};New-Item -ItemType Directory '{remote}'"],'create.log')
run(scp+[str(b/'input.tar'),'builder@127.0.0.1:'+remote+'/input.tar'],'upload.log')
run(scp+[str(b/'native.py'),'builder@127.0.0.1:'+remote+'/run.py'],'upload-runner.log')
run([str(vm/'winps.sh'),f"& C:/ci-dpvs-review/python/python.exe '{remote}/run.py';exit $LASTEXITCODE"],'native.log',150)
(b/'results').mkdir(exist_ok=True)
run(scp+['builder@127.0.0.1:'+remote+'/results.json',str(b/'results/results.json')],'download.log')
for arch in ['x86','amd64']:
 for cfg in ['Debug','Release']:
  for variant in ['actual','premature-seal']:
   name=arch+'-'+cfg+'-'+variant; out=b/'results'/name;out.mkdir(exist_ok=True)
   for n in ['build.cmd','build.log','run.log']:run(scp+['builder@127.0.0.1:'+remote+'/'+name+'/'+n,str(out/n)],'download.log')
actual={k.replace(chr(92),'/'):v for k,v in json.loads((b/'results/results.json').read_text())['source_sha256'].items()}
assert all(actual[n]==v for n,v in manifest.items())
run([str(vm/'winps.sh'),f"Remove-Item -Recurse -Force '{remote}'; Write-Output (Test-Path '{remote}')"],'cleanup.log')
print((b/'results/results.json').read_text())
