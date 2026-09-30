from pathlib import Path
import hashlib,json,tarfile
r=Path('C:/native-host49')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'private-inputs.tar')=='c81716c610ecc31dab884b2939aa349ccf46c2c6b1a8ee1e43ea48423b7f3e61'
with tarfile.open(r/'private-inputs.tar') as t:
 members=t.getmembers()
 assert len(members)==20
 for m in members:
  assert m.isfile() and not Path(m.name).is_absolute() and ':' not in m.name and '..' not in Path(m.name).parts
  assert not (r/m.name).exists(),m.name
 t.extractall(r)
assert sha(r/'input-manifest.json')=='19b5ed0340011f8eacc387f426e2cc7b06be2aff14435dd59cbcab08ebd85e4e'
assert sha(r/'run-native.py')=='6bc7d8ac683dda4949798957043961131018cc65c7d84ac29d236fa835bccdcd'
m=json.loads((r/'input-manifest.json').read_text())
for name,expected in m['sha256'].items():assert sha(r/name)==expected,name
(r/'before.json').write_text(json.dumps({'manifest':sha(r/'input-manifest.json'),'driver':sha(r/'run-native.py'),'verified_entries':len(m['sha256']),'sha256':m['sha256']},indent=2)+'\n')
print('Transferred manifest, exact runner and all 19 inputs verified; no compiler invoked by staging.')
