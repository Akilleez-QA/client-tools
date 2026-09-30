from pathlib import Path
import hashlib,json,tarfile
r=Path('C:/native-plain54')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'private-inputs.tar')=='1eb691836933c6cc18334c2b407e0615c12251b649791bf66abb4e7b6978e4d3'
with tarfile.open(r/'private-inputs.tar') as t:
 members=t.getmembers()
 assert len(members)==16
 for m in members:
  assert m.isfile() and not Path(m.name).is_absolute() and ':' not in m.name and '..' not in Path(m.name).parts
  assert not (r/m.name).exists(),m.name
 t.extractall(r)
assert sha(r/'input-manifest.json')=='c989f4a51ec69513018695ae3ae46eae56e332b559e306d7e092ac85d5de31b4'
assert sha(r/'run-native54.py')=='377bccba15a260c14143e495bfa72b14f9f94ec2234a9940155572bd04705a9e'
m=json.loads((r/'input-manifest.json').read_text())
for name,expected in m['sha256'].items():assert sha(r/name)==expected,name
(r/'before.json').write_text(json.dumps({'manifest':sha(r/'input-manifest.json'),'driver':sha(r/'run-native54.py'),'verified_entries':len(m['sha256']),'sha256':m['sha256']},indent=2)+'\n')
print('Transferred manifest, exact runner and all 15 inputs verified; no compiler invoked by staging.')
