from pathlib import Path
import hashlib,json,tarfile
r=Path('C:/native41-owner')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'private-inputs.tar')=='18bee103cdcf21ad7aa301377c6328f75cf31930110c61c48b45c47a94ed58db'
with tarfile.open(r/'private-inputs.tar') as t:
 members=t.getmembers()
 assert len(members)==22
 for m in members:
  assert m.isfile() and not Path(m.name).is_absolute() and ':' not in m.name and '..' not in Path(m.name).parts
  assert not (r/m.name).exists(),m.name
 t.extractall(r)
assert sha(r/'input-manifest.json')=='f16977da4ac842d3fcc57d0dc3c4c26024b585ed06b2ca8f182aa6b1e286e96e'
assert sha(r/'run-native.py')=='37d9175b200953b0f0462e663c0dbc7bbb482281954351b2b34995969d040aad'
m=json.loads((r/'input-manifest.json').read_text())
for name,expected in m['sha256'].items():assert sha(r/name)==expected,name
(r/'before.json').write_text(json.dumps({'manifest':sha(r/'input-manifest.json'),'driver':sha(r/'run-native.py'),'verified_entries':len(m['sha256']),'sha256':m['sha256']},indent=2)+'\n')
print('Transferred manifest, exact runner and all 21 inputs verified; no compiler invoked by staging.')
