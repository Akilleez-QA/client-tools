"""Parent-authorized staging and object-only compile; no produced binary execution."""
from pathlib import Path
import hashlib, json, subprocess
base=Path(__file__).resolve().parent
vm=Path('/home/akilleez/Work/swg-source-vm/winbuild')
remote='C:/alias-native36'
archive=base/'source-v1.tar'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='0c7930e8675647eedebf41aba1ecab2dcab46c4310ef2474241be182121fc061'
logs=base/'staging-v1'; logs.mkdir(exist_ok=False)
commands=[]
def run(args,name,timeout=60):
 commands.append(args)
 (logs/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
 p=subprocess.run(args,capture_output=True,timeout=timeout)
 (logs/name).write_bytes(p.stdout+p.stderr)
 print(name,p.returncode,flush=True)
 if p.returncode: raise RuntimeError(name+': '+p.stderr.decode(errors='replace'))
 return p
stage=logs/'stage.py'
stage.write_text('''from pathlib import Path
import hashlib, tarfile, subprocess, sys
root=Path('C:/alias-native36')
archive=root/'source-v1.tar'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='0c7930e8675647eedebf41aba1ecab2dcab46c4310ef2474241be182121fc061'
with tarfile.open(archive) as t:
 for m in t.getmembers():
  assert m.isfile() and not m.name.startswith('/') and '..' not in Path(m.name).parts
 t.extractall(root)
p=subprocess.run([sys.executable,str(root/'alias-native36/build-native.py'),'--approved-compile-only'])
raise SystemExit(p.returncode)
''')
scp=['scp','-q','-i',str(vm/'ssh/id_ed25519'),'-P','2223','-o','UserKnownHostsFile='+str(vm/'ssh/known_hosts')]
run([str(vm/'winps.sh'),"if(Get-Process cl -ErrorAction SilentlyContinue){throw 'compiler active'};if(Test-Path 'C:/alias-native36'){throw 'exists'};New-Item -ItemType Directory 'C:/alias-native36'"],'create.log')
run(scp+[str(archive),'builder@127.0.0.1:'+remote+'/source-v1.tar'],'upload-source.log')
run(scp+[str(stage),'builder@127.0.0.1:'+remote+'/stage.py'],'upload-stage.log')
p=run([str(vm/'winps.sh'),"& C:/ci-dpvs-review/python/python.exe 'C:/alias-native36/stage.py';exit $LASTEXITCODE"],'compile.log',120)
print(p.stdout.decode(errors='replace'))
