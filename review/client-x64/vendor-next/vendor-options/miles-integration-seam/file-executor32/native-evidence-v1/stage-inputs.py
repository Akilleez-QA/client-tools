from pathlib import Path
import hashlib,json,tarfile
r=Path('C:/file-executor32')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'private-inputs.tar')=='153cd763aafddd4c048ced93eecaf56e675eb854e5f12298415fffff32f1b37f'
with tarfile.open(r/'private-inputs.tar') as t:
 members=t.getmembers()
 assert len(members)==9548
 for m in members:
  assert m.isfile() and not Path(m.name).is_absolute() and ':' not in m.name and '..' not in Path(m.name).parts
  assert not (r/m.name).exists(),m.name
 t.extractall(r)
assert sha(r/'input-manifest.json')=='949d56d8a0d23efe1e4f0ed9461a2e19cdafd36d7849469fdc66f4f259e1c2e1'
assert sha(r/'run-native.py')=='a0ec2996dd06364697e975665f698f6b95b009f4e2403b2ca0a0952c72b02a31'
m=json.loads((r/'input-manifest.json').read_text())
for name,expected in m['sha256'].items():assert sha(r/name)==expected,name
(r/'before.json').write_text(json.dumps({'manifest':sha(r/'input-manifest.json'),'driver':sha(r/'run-native.py'),'verified_entries':len(m['sha256']),'sha256':m['sha256']},indent=2)+'\n')
print('Transferred manifest, exact runner and all 9547 inputs verified; no compiler invoked by staging.')
