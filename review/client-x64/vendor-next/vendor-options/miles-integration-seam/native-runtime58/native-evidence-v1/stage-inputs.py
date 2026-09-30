from pathlib import Path
import hashlib,json,tarfile
r=Path('C:/native-runtime58')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'private-inputs.tar')=='7f616308b4ee9cd61d5527377b856737817ea03b6514fd00612cc1e646fe77ba'
with tarfile.open(r/'private-inputs.tar') as t:
 members=t.getmembers()
 assert len(members)==40
 for m in members:
  assert m.isfile() and not Path(m.name).is_absolute() and ':' not in m.name and '..' not in Path(m.name).parts
  assert not (r/m.name).exists(),m.name
 t.extractall(r)
assert sha(r/'input-manifest.json')=='70a555edcf098999e884e342c1b5f6b372e41e2904eedf054a3dc222eb5e6e2a'
assert sha(r/'run-native.py')=='597c70ac6f356d0617b6d45bba0a3116d92595a3afd30843bcd2ec4f4acab9bc'
m=json.loads((r/'input-manifest.json').read_text())
for name,expected in m['sha256'].items():assert sha(r/name)==expected,name
(r/'before.json').write_text(json.dumps({'manifest':sha(r/'input-manifest.json'),'driver':sha(r/'run-native.py'),'verified_entries':len(m['sha256']),'sha256':m['sha256']},indent=2)+'\n')
print('Transferred manifest, exact runner and all 39 inputs verified; no compiler invoked by staging.')
