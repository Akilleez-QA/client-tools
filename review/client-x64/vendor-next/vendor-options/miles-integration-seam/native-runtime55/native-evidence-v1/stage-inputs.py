from pathlib import Path
import hashlib,json,tarfile
r=Path('C:/native-runtime55')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'private-inputs.tar')=='7ab0e9cd40634b5117c019deb2939dd03877a5c8507064898ff5f0ddb32a763a'
with tarfile.open(r/'private-inputs.tar') as t:
 members=t.getmembers()
 assert len(members)==40
 for m in members:
  assert m.isfile() and not Path(m.name).is_absolute() and ':' not in m.name and '..' not in Path(m.name).parts
  assert not (r/m.name).exists(),m.name
 t.extractall(r)
assert sha(r/'input-manifest.json')=='bb30dfc441826ce315aacbdcda56ed1092a03e7369c22dabab4efe7ac47f5bb2'
assert sha(r/'run-native.py')=='72997ddd4187cee981e9bbbb1f8abf920694161917071dae88a4fe5e0e12d535'
m=json.loads((r/'input-manifest.json').read_text())
for name,expected in m['sha256'].items():assert sha(r/name)==expected,name
(r/'before.json').write_text(json.dumps({'manifest':sha(r/'input-manifest.json'),'driver':sha(r/'run-native.py'),'verified_entries':len(m['sha256']),'sha256':m['sha256']},indent=2)+'\n')
print('Transferred manifest, exact runner and all 39 inputs verified; no compiler invoked by staging.')
