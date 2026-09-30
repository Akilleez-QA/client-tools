from pathlib import Path
import hashlib,json,tarfile
r=Path('C:/native46-composition')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'private-inputs.tar')=='d62d5e362389a483bbbcd7e0f38642f415db477f9026e533ea1ed1c2d2e959a9'
with tarfile.open(r/'private-inputs.tar') as t:
 members=t.getmembers()
 assert len(members)==25
 for m in members:
  assert m.isfile() and not Path(m.name).is_absolute() and ':' not in m.name and '..' not in Path(m.name).parts
  assert not (r/m.name).exists(),m.name
 t.extractall(r)
assert sha(r/'input-manifest.json')=='d404be130dcad1d5876aeb90af7d3d76ba044668a6ff0a4192c9852d74eeb077'
assert sha(r/'run-native.py')=='118d3faf4d1dfeeb0fb5fdff27333d53ecf818c39abf3ce058f1df00ba2dcb0f'
m=json.loads((r/'input-manifest.json').read_text())
for name,expected in m['sha256'].items():assert sha(r/name)==expected,name
(r/'before.json').write_text(json.dumps({'manifest':sha(r/'input-manifest.json'),'driver':sha(r/'run-native.py'),'verified_entries':len(m['sha256']),'sha256':m['sha256']},indent=2)+'\n')
print('Transferred manifest, exact runner and all 24 inputs verified; no compiler invoked by staging.')
