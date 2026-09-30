from pathlib import Path
import tarfile,subprocess,json,hashlib
b=Path(__file__).resolve().parent;seam=b.parent
vm=Path('/home/akilleez/Work/swg-source-vm/winbuild');remote='C:/miles-preflight-parent15'
files=['host-candidate/host_dispatch.cpp','host-candidate/host_dispatch.h','host-candidate/preflight.cpp','host-candidate/registry_resolver.h','transport-candidate/resource_registry.h','protocol-candidate/miles_wire.h']
(b/'preflight-input-manifest.json').write_text(json.dumps({n:hashlib.sha256((seam/n).read_bytes()).hexdigest() for n in files},indent=2)+'\n')
with tarfile.open(b/'preflight-input.tar','w') as t:
 for n in files:t.add(seam/n,arcname=n)
script=r'''from pathlib import Path
import tarfile,subprocess,json
b=Path('C:/miles-preflight-parent15')
with tarfile.open(b/'input.tar') as t:t.extractall(b)
source=b/'host-candidate/host_dispatch.cpp';original=source.read_text();needle='memset(&out,0,sizeof(out));'
assert needle in original
source_mutant=b/'host-candidate/host_dispatch_mutant.cpp';source_mutant.write_text(original.replace(needle,'/* negative control: output clear omitted */',1))
results=[]
for cfg in ['Debug','Release']:
 for variant in ['actual','mutant']:
  out=b/(cfg+'-'+variant);out.mkdir()
  flags='/nologo /EHsc /DWIN32 '+('/MTd /Od' if cfg=='Debug' else '/MT /O2')+' /IC:/client-next-build/src/external/3rd/library/miles/include '
  src=source if variant=='actual' else source_mutant
  cmd=out/'build.cmd';cmd.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86 >nul\nif errorlevel 1 exit /b 1\ncl '+flags+str(src)+' '+str(b/'host-candidate/preflight.cpp')+' C:/client-next-build/src/external/3rd/library/miles/lib/win/Mss32.lib delayimp.lib /Fe'+str(out/'probe.exe')+' /link /DELAYLOAD:mss32.dll\nexit /b %errorlevel%\n')
  p=subprocess.run(['cmd','/c',str(cmd)],cwd=out,capture_output=True);(out/'build.log').write_bytes(p.stdout+p.stderr)
  row={'cfg':cfg,'variant':variant,'build_exit':p.returncode}
  if not p.returncode:
   p=subprocess.run([str(out/'probe.exe')],cwd=out,capture_output=True,timeout=15);(out/'run.log').write_bytes(p.stdout+p.stderr);row.update(run_exit=p.returncode,stdout=p.stdout.decode(errors='replace'))
  results.append(row)
(b/'results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
'''
(b/'native-preflight.py').write_text(script)
commands=[]
def run(args,name):
 commands.append(args);p=subprocess.run(args,capture_output=True,timeout=60);(b/name).write_bytes(p.stdout+p.stderr)
 (b/'preflight-commands.json').write_text(json.dumps(commands,indent=2)+'\n')
 if p.returncode:raise RuntimeError((name,p.returncode,p.stderr.decode(errors='replace')))
 return p
scp=['scp','-q','-i',str(vm/'ssh/id_ed25519'),'-P','2223','-o','UserKnownHostsFile='+str(vm/'ssh/known_hosts')]
run([str(vm/'winps.sh'),f"if(Test-Path '{remote}'){{throw 'exists'}};New-Item -ItemType Directory '{remote}'"],'preflight-create.log')
run(scp+[str(b/'preflight-input.tar'),'builder@127.0.0.1:'+remote+'/input.tar'],'preflight-upload.log')
run(scp+[str(b/'native-preflight.py'),'builder@127.0.0.1:'+remote+'/run.py'],'preflight-runner-upload.log')
run([str(vm/'winps.sh'),f"& C:/ci-dpvs-review/python/python.exe '{remote}/run.py';exit $LASTEXITCODE"],'preflight-native.log')
for cfg in ['Debug','Release']:
 for v in ['actual','mutant']:
  d=b/'preflight-native'/(cfg+'-'+v);d.mkdir(parents=True,exist_ok=True)
  for n in ['build.log','run.log','build.cmd']:
   run(scp+['builder@127.0.0.1:'+remote+'/'+cfg+'-'+v+'/'+n,str(d/n)],'preflight-download.log')
run(scp+['builder@127.0.0.1:'+remote+'/results.json',str(b/'preflight-native/results.json')],'preflight-download-results.log')
print((b/'preflight-native/results.json').read_text())
