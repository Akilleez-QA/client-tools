from pathlib import Path
import hashlib,json,tarfile
r=Path('C:/native-file-callbacks35')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'private-inputs.tar')=='c284f2045d23491ed1e483d6812b18bce5a3c009e3f20326089736f3900db42c'
with tarfile.open(r/'private-inputs.tar') as t:
 members=t.getmembers()
 assert len(members)==9537
 for m in members:
  assert m.isfile() and not Path(m.name).is_absolute() and ':' not in m.name and '..' not in Path(m.name).parts
  assert not (r/m.name).exists(),m.name
 t.extractall(r)
assert sha(r/'input-manifest.json')=='13a7272cdf84d617ea82f70481da686ea4abefc8e198e77e9f3d501f6fc9538a'
assert sha(r/'run-native35.py')=='e2fa5b240a6a1ba645897094fed236edfaf51bd863ff4947f30232626cec6135'
m=json.loads((r/'input-manifest.json').read_text())
for name,expected in m['sha256'].items():assert sha(r/name)==expected,name
(r/'before.json').write_text(json.dumps({'manifest':sha(r/'input-manifest.json'),'driver':sha(r/'run-native35.py'),'verified_entries':len(m['sha256']),'sha256':m['sha256']},indent=2)+'\n')
print('Transferred manifest, exact runner and all 9536 inputs verified; no compiler invoked by staging.')
