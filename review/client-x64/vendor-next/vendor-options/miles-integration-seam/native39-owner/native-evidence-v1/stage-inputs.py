from pathlib import Path
import hashlib,json,tarfile
r=Path('C:/native39-owner')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'private-inputs.tar')=='22a9041de881024487257ff4aad401013f9bc295c8b38fe29a75d5fea3f76b34'
with tarfile.open(r/'private-inputs.tar') as t:
 members=t.getmembers()
 assert len(members)==20
 for m in members:
  assert m.isfile() and not Path(m.name).is_absolute() and ':' not in m.name and '..' not in Path(m.name).parts
  assert not (r/m.name).exists(),m.name
 t.extractall(r)
assert sha(r/'input-manifest.json')=='96dc61ff4a9edd63c7c0597b2a1e6490382e5bbdd34e3e1bf3dc6fcc6c6e9d1a'
assert sha(r/'run-native.py')=='98cc93b04b8826aea577526658df90b313c4156af5c94f33980b7e42e8a42955'
m=json.loads((r/'input-manifest.json').read_text())
for name,expected in m['sha256'].items():assert sha(r/name)==expected,name
(r/'before.json').write_text(json.dumps({'manifest':sha(r/'input-manifest.json'),'driver':sha(r/'run-native.py'),'verified_entries':len(m['sha256']),'sha256':m['sha256']},indent=2)+'\n')
print('Transferred manifest, exact runner and all 19 inputs verified; no compiler invoked by staging.')
