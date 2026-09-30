from pathlib import Path
import hashlib,json,tarfile
r=Path('C:/native40-owner')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'private-inputs.tar')=='dd9b09dd970dc1020967a812d507918838dc16f8a76ecdcc83710bd9828ed9f3'
with tarfile.open(r/'private-inputs.tar') as t:
 members=t.getmembers()
 assert len(members)==22
 for m in members:
  assert m.isfile() and not Path(m.name).is_absolute() and ':' not in m.name and '..' not in Path(m.name).parts
  assert not (r/m.name).exists(),m.name
 t.extractall(r)
assert sha(r/'input-manifest.json')=='d1315d34017519fa396e0f40884b577a14ac423bf2ce574360cbe9f06bbdbbe1'
assert sha(r/'run-native.py')=='840f26662cb74134efdc60ef044b745024dd589255d8599d0cd71987ccdcf98a'
m=json.loads((r/'input-manifest.json').read_text())
for name,expected in m['sha256'].items():assert sha(r/name)==expected,name
(r/'before.json').write_text(json.dumps({'manifest':sha(r/'input-manifest.json'),'driver':sha(r/'run-native.py'),'verified_entries':len(m['sha256']),'sha256':m['sha256']},indent=2)+'\n')
print('Transferred manifest, exact runner and all 21 inputs verified; no compiler invoked by staging.')
