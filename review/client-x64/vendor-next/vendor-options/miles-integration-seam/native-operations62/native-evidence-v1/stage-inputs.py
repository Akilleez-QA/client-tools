from pathlib import Path
import hashlib,json,tarfile
r=Path('C:/native-operations62')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'private-inputs.tar')=='506a91a7f1ca2d751d77537be7ffeb480049a836ce45dcc209cb3a3b8171c537'
with tarfile.open(r/'private-inputs.tar') as t:
 members=t.getmembers()
 assert len(members)==12
 for m in members:
  assert m.isfile() and not Path(m.name).is_absolute() and ':' not in m.name and '..' not in Path(m.name).parts
  assert not (r/m.name).exists(),m.name
 t.extractall(r)
assert sha(r/'input-manifest.json')=='501cfc4fa5c1071d71f159bda37b90dc71c447466a60c63bdb1493fd620176f0'
assert sha(r/'run-native.py')=='fa9cd3e1c79e4ed2079e77000140d730791139d86be42909cb70580cfd4f63b8'
m=json.loads((r/'input-manifest.json').read_text())
for name,expected in m['sha256'].items():assert sha(r/name)==expected,name
(r/'before.json').write_text(json.dumps({'manifest':sha(r/'input-manifest.json'),'driver':sha(r/'run-native.py'),'verified_entries':len(m['sha256']),'sha256':m['sha256']},indent=2)+'\n')
print('Transferred manifest, exact runner and all 11 inputs verified; no compiler invoked by staging.')
