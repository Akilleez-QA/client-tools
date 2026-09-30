#!/usr/bin/env python3
"""One explicitly authorized object-only matrix; no retries or product edits."""
from pathlib import Path
import hashlib,json,subprocess,tarfile
ROOT=Path(__file__).resolve().parent
INPUT=ROOT/'private-inputs-v1'
OUT=ROOT/'native-evidence-v1'
VM=Path('/home/akilleez/Work/swg-source-vm/winbuild')
PRODUCT=Path('/home/akilleez/Work/swg-source/client-build-next')
MANIFEST='13a7272cdf84d617ea82f70481da686ea4abefc8e198e77e9f3d501f6fc9538a'
DRIVER='e2fa5b240a6a1ba645897094fed236edfaf51bd863ff4947f30232626cec6135'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(INPUT/'input-manifest.json')==MANIFEST
assert sha(INPUT/'run-native35.py')==DRIVER
assert subprocess.check_output(['git','-C',str(PRODUCT),'rev-parse','HEAD']).decode().strip()=='49d0eeed4ddaa177d7a93ea396c37c3d9b9942da'
assert not subprocess.check_output(['git','-C',str(PRODUCT),'status','--porcelain=v1'])
for rel,expected in json.loads((INPUT/'input-manifest.json').read_text())['sha256'].items():assert sha(INPUT/rel)==expected,rel
OUT.mkdir(exist_ok=False)
commands=[]
def run(args,name,check=True):
 commands.append({'name':name,'argv':args})
 (OUT/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
 with (OUT/name).open('wb') as log:
  p=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  for line in p.stdout:
   log.write(line);log.flush()
   print(line.decode(errors='replace').rstrip(),flush=True)
  code=p.wait()
 commands[-1]['exit_code']=code
 (OUT/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
 print(name+' exit='+str(code),flush=True)
 if check and code:raise RuntimeError(name+' failed; no retry')
 return code
archive=OUT/'private-inputs.tar'
with tarfile.open(archive,'w') as t:
 for p in sorted(INPUT.rglob('*')):
  if p.is_file():t.add(p,arcname=str(p.relative_to(INPUT)),recursive=False)
archive_hash=sha(archive)
(OUT/'local-before.json').write_text(json.dumps({'manifest':MANIFEST,'driver':DRIVER,'archive':archive_hash,'product_head':'49d0eeed4ddaa177d7a93ea396c37c3d9b9942da','product_clean':True},indent=2)+'\n')
stage=OUT/'stage-inputs.py'
stage.write_text('''from pathlib import Path
import hashlib,json,tarfile
r=Path('C:/native-file-callbacks35')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'private-inputs.tar')=='''+repr(archive_hash)+'''
with tarfile.open(r/'private-inputs.tar') as t:
 members=t.getmembers()
 assert len(members)==9537
 for m in members:
  assert m.isfile() and not Path(m.name).is_absolute() and ':' not in m.name and '..' not in Path(m.name).parts
  assert not (r/m.name).exists(),m.name
 t.extractall(r)
assert sha(r/'input-manifest.json')=='''+repr(MANIFEST)+'''
assert sha(r/'run-native35.py')=='''+repr(DRIVER)+'''
m=json.loads((r/'input-manifest.json').read_text())
for name,expected in m['sha256'].items():assert sha(r/name)==expected,name
(r/'before.json').write_text(json.dumps({'manifest':sha(r/'input-manifest.json'),'driver':sha(r/'run-native35.py'),'verified_entries':len(m['sha256']),'sha256':m['sha256']},indent=2)+'\\n')
print('Transferred manifest, exact runner and all 9536 inputs verified; no compiler invoked by staging.')
''')
collect=OUT/'collect-evidence.py'
collect.write_text('''from pathlib import Path
import hashlib,json,struct,zipfile
r=Path('C:/native-file-callbacks35')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((r/'input-manifest.json').read_text())
actual={name:sha(r/name) for name in m['sha256']}
mismatches=[name for name in actual if actual[name]!=m['sha256'][name]]
objects={}
for p in (r/'results').glob('*/*.obj'):
 data=p.read_bytes()
 objects[str(p.relative_to(r))]={'sha256':sha(p),'bytes':len(data),'coff_machine':hex(struct.unpack_from('<H',data)[0])}
after={'manifest':sha(r/'input-manifest.json'),'driver':sha(r/'run-native35.py'),'sha256':actual,'input_mismatches':mismatches,'system_header_post_hashing_performed':False,'objects_rechecked':objects}
(r/'after.json').write_text(json.dumps(after,indent=2)+'\\n')
files=[r/'before.json',r/'after.json',r/'input-manifest.json']
for p in (r/'results').rglob('*'):
 if p.is_file() and p.name in ['results.json','command.json','compile.log','actual-includes.json','require-v120.h','symbols-command.json','symbols.log','inputs-after.json','environment.cmd']:files.append(p)
with zipfile.ZipFile(r/'curated-evidence.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(files):z.write(p,str(p.relative_to(r)))
print(json.dumps({'evidence_sha256':sha(r/'curated-evidence.zip'),'file_count':len(files),'input_mismatches':mismatches,'system_header_post_hashing_performed':False,'object_count':len(objects)}))
''')
scp=['scp','-q','-i',str(VM/'ssh/id_ed25519'),'-P','2223','-o','UserKnownHostsFile='+str(VM/'ssh/known_hosts')]
run([str(VM/'winps.sh'),"$ErrorActionPreference='Stop'; if(Test-Path 'C:/native-file-callbacks35'){throw 'Destination exists'}; if(Get-Process cl -ErrorAction SilentlyContinue){throw 'Compiler already running'}; New-Item -ItemType Directory 'C:/native-file-callbacks35'"],'01-create.log')
for p in [archive,stage,collect]:run(scp+[str(p),'builder@127.0.0.1:C:/native-file-callbacks35/'+p.name],'02-upload-'+p.name+'.log')
run([str(VM/'winps.sh'),"& C:/ci-dpvs-review/python/python.exe C:/native-file-callbacks35/stage-inputs.py; exit $LASTEXITCODE"],'03-stage.log')
# The exact authorized runner is invoked once. No code path retries it.
compile_code=run([str(VM/'winps.sh'),"& C:/ci-dpvs-review/python/python.exe C:/native-file-callbacks35/run-native35.py --approved-compile-only; exit $LASTEXITCODE"],'04-native-matrix.log',check=False)
run([str(VM/'winps.sh'),"& C:/ci-dpvs-review/python/python.exe C:/native-file-callbacks35/collect-evidence.py; exit $LASTEXITCODE"],'05-collect.log')
run(scp+['builder@127.0.0.1:C:/native-file-callbacks35/curated-evidence.zip',str(OUT/'curated-evidence.zip')],'06-download.log')
assert not subprocess.check_output(['git','-C',str(PRODUCT),'status','--porcelain=v1'])
for rel,expected in json.loads((INPUT/'input-manifest.json').read_text())['sha256'].items():assert sha(INPUT/rel)==expected,rel
(OUT/'local-after.json').write_text(json.dumps({'manifest':sha(INPUT/'input-manifest.json'),'driver':sha(INPUT/'run-native35.py'),'product_clean':True,'compile_exit_code':compile_code,'evidence_zip_sha256':sha(OUT/'curated-evidence.zip'),'runner_invocations':1},indent=2)+'\n')
print('Single matrix and curated collection complete. Compile exit='+str(compile_code),flush=True)
raise SystemExit(compile_code)
