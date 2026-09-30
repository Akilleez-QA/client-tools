from pathlib import Path
import hashlib,json,tarfile
r=Path('C:/native47-components')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'private-inputs.tar')=='3805cbeb211e62d966542bfc192ca3b648fe8bd4846a12719b09e9484ae1de88'
with tarfile.open(r/'private-inputs.tar') as t:
 members=t.getmembers()
 assert len(members)==30
 for m in members:
  assert m.isfile() and not Path(m.name).is_absolute() and ':' not in m.name and '..' not in Path(m.name).parts
  assert not (r/m.name).exists(),m.name
 t.extractall(r)
assert sha(r/'input-manifest.json')=='3414158ffd2ec9d6d9ba5d123b417eb13f54fe89b76ec1e850f9494cede82ffb'
assert sha(r/'run-native.py')=='ec1de45d21fe028e3f241e3563099ae411b937ec123548a8706dba5aa30fa34e'
m=json.loads((r/'input-manifest.json').read_text())
for name,expected in m['sha256'].items():assert sha(r/name)==expected,name
(r/'before.json').write_text(json.dumps({'manifest':sha(r/'input-manifest.json'),'driver':sha(r/'run-native.py'),'verified_entries':len(m['sha256']),'sha256':m['sha256']},indent=2)+'\n')
print('Transferred manifest, exact runner and all 29 inputs verified; no compiler invoked by staging.')
