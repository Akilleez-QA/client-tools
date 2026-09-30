from pathlib import Path
import hashlib,json,tarfile
r=Path('C:/file-executor33')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'private-inputs.tar')=='e9d396ac396c2c825db8f5519c17e8ffadcef6333e4f4ffca8f8cc17f1af10b0'
with tarfile.open(r/'private-inputs.tar') as t:
 members=t.getmembers()
 assert len(members)==9548
 for m in members:
  assert m.isfile() and not Path(m.name).is_absolute() and ':' not in m.name and '..' not in Path(m.name).parts
  assert not (r/m.name).exists(),m.name
 t.extractall(r)
assert sha(r/'input-manifest.json')=='ccd611ec70e592347954d0c5cb8cc2e01030e08503d54b705b446c244c304536'
assert sha(r/'run-native.py')=='27610569c54e4f82c4473099b299b3dd6011544e771db3e4ec313f67e496f7d3'
m=json.loads((r/'input-manifest.json').read_text())
for name,expected in m['sha256'].items():assert sha(r/name)==expected,name
(r/'before.json').write_text(json.dumps({'manifest':sha(r/'input-manifest.json'),'driver':sha(r/'run-native.py'),'verified_entries':len(m['sha256']),'sha256':m['sha256']},indent=2)+'\n')
print('Transferred manifest, exact runner and all 9547 inputs verified; no compiler invoked by staging.')
