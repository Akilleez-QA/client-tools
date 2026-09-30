from pathlib import Path
import hashlib,json,tarfile
r=Path('C:/native38-owner')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'private-inputs.tar')=='e67b26a7a1c4373f76e6f98e2a18e6b5422d2646e322ecf77f3c0c3bfc699302'
with tarfile.open(r/'private-inputs.tar') as t:
 members=t.getmembers()
 assert len(members)==20
 for m in members:
  assert m.isfile() and not Path(m.name).is_absolute() and ':' not in m.name and '..' not in Path(m.name).parts
  assert not (r/m.name).exists(),m.name
 t.extractall(r)
assert sha(r/'input-manifest.json')=='4647bf4ad00dcdc1e80c082ac454eeba491e2d459710726ec8b87659f2a007c4'
assert sha(r/'run-native.py')=='0e9e60ef8af2b4308130d07999cf13f65bcfd535633591514ccd941d8898b95b'
m=json.loads((r/'input-manifest.json').read_text())
for name,expected in m['sha256'].items():assert sha(r/name)==expected,name
(r/'before.json').write_text(json.dumps({'manifest':sha(r/'input-manifest.json'),'driver':sha(r/'run-native.py'),'verified_entries':len(m['sha256']),'sha256':m['sha256']},indent=2)+'\n')
print('Transferred manifest, exact runner and all 19 inputs verified; no compiler invoked by staging.')
