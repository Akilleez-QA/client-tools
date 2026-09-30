from pathlib import Path
import subprocess,json
b=Path(__file__).resolve().parent;vm=Path('/home/akilleez/Work/swg-source-vm/winbuild');scp=['scp','-q','-i',str(vm/'ssh/id_ed25519'),'-P','2223','-o','UserKnownHostsFile='+str(vm/'ssh/known_hosts')]
script=b/'staging-v1/collect.py';script.write_text('''from pathlib import Path
import tarfile
root=Path('C:/alias-native36')
with tarfile.open(root/'text-evidence-v1.tar','x') as t:
 for p in sorted((root/'native-v1').rglob('*')):
  if p.is_file() and p.suffix in ['.log','.json','.sha256','.cmd']:
   t.add(p,arcname=str(p.relative_to(root/'native-v1')),recursive=False)
''')
for args in [scp+[str(script),'builder@127.0.0.1:C:/alias-native36/collect.py'],[str(vm/'winps.sh'),"& C:/ci-dpvs-review/python/python.exe C:/alias-native36/collect.py;exit $LASTEXITCODE"],scp+['builder@127.0.0.1:C:/alias-native36/text-evidence-v1.tar',str(b/'text-evidence-v1.tar')]]:
 subprocess.run(args,check=True,capture_output=True,timeout=60)
import tarfile
out=b/'evidence-native-v1';out.mkdir(exist_ok=False)
with tarfile.open(b/'text-evidence-v1.tar') as t:
 for m in t.getmembers():
  assert m.isfile() and not m.name.startswith('/') and '..' not in Path(m.name).parts and Path(m.name).suffix in ['.log','.json','.sha256','.cmd']
 t.extractall(out)
r=json.loads((out/'receipt.json').read_text());print(json.dumps({'passed':r['passed'],'records':[{'source':x['source'],'machine':x['object']['machine'],'imports':x['imports']} for x in r['records']]},indent=2))
