from pathlib import Path
import hashlib,json,tarfile
r=Path('C:/file-executor31')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'private-inputs.tar')=='87f0aec7b4a5cf2e4753b25b18c97281de0b087a63999966009f05037b466209'
with tarfile.open(r/'private-inputs.tar') as t:
 members=t.getmembers()
 assert len(members)==9548
 for m in members:
  assert m.isfile() and not Path(m.name).is_absolute() and ':' not in m.name and '..' not in Path(m.name).parts
  assert not (r/m.name).exists(),m.name
 t.extractall(r)
assert sha(r/'input-manifest.json')=='3296557d7c2c18c6b69f83a973fcdb93d8d318b20bbaf4ec0bea3bef9bbe8be7'
assert sha(r/'run-native.py')=='1080278829ce9798deae25a15338e81417ec2e349ddbe05f3105897434d86481'
m=json.loads((r/'input-manifest.json').read_text())
for name,expected in m['sha256'].items():assert sha(r/name)==expected,name
(r/'before.json').write_text(json.dumps({'manifest':sha(r/'input-manifest.json'),'driver':sha(r/'run-native.py'),'verified_entries':len(m['sha256']),'sha256':m['sha256']},indent=2)+'\n')
print('Transferred manifest, exact runner and all 9547 inputs verified; no compiler invoked by staging.')
