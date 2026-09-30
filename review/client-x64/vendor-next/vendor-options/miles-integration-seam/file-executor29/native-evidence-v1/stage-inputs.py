from pathlib import Path
import hashlib,json,tarfile
r=Path('C:/file-executor29')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'private-inputs.tar')=='ff9b0bcf05a25aea5e83e10ddc8d8bc94f6bf2c7ffdc19aab680283b33f907c4'
with tarfile.open(r/'private-inputs.tar') as t:
 members=t.getmembers()
 assert len(members)==9539
 for m in members:
  assert m.isfile() and not Path(m.name).is_absolute() and ':' not in m.name and '..' not in Path(m.name).parts
  assert not (r/m.name).exists(),m.name
 t.extractall(r)
assert sha(r/'input-manifest.json')=='a02c162efe3dfd320f50cc4e0d8f56f236b99d770904c3c22e988e5dc48b135d'
assert sha(r/'run-native.py')=='ca93eb658f8dd70d78bfcd285385074d7ed34dd9a449ba5c32964099709bef73'
m=json.loads((r/'input-manifest.json').read_text())
for name,expected in m['sha256'].items():assert sha(r/name)==expected,name
(r/'before.json').write_text(json.dumps({'manifest':sha(r/'input-manifest.json'),'driver':sha(r/'run-native.py'),'verified_entries':len(m['sha256']),'sha256':m['sha256']},indent=2)+'\n')
print('Transferred manifest, exact runner and all 9538 inputs verified; no compiler invoked by staging.')
