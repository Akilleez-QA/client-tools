from pathlib import Path
import hashlib,json,struct,zipfile
r=Path('C:/file-executor31')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((r/'input-manifest.json').read_text())
actual={name:sha(r/name) for name in m['sha256']}
mismatches=[name for name in actual if actual[name]!=m['sha256'][name]]
objects={}
for p in (r/'results').glob('*/*.obj'):
 data=p.read_bytes()
 objects[str(p.relative_to(r))]={'sha256':sha(p),'bytes':len(data),'coff_machine':hex(struct.unpack_from('<H',data)[0])}
after={'manifest':sha(r/'input-manifest.json'),'driver':sha(r/'run-native.py'),'sha256':actual,'input_mismatches':mismatches,'system_header_post_hashing_performed':False,'objects_rechecked':objects}
(r/'after.json').write_text(json.dumps(after,indent=2)+'\n')
files=[r/'before.json',r/'after.json',r/'input-manifest.json']
for p in (r/'results').rglob('*'):
 if p.is_file() and p.name in ['results.json','command.json','compile.log','actual-includes.json','require-v120.h']:files.append(p)
with zipfile.ZipFile(r/'curated-evidence.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(files):z.write(p,str(p.relative_to(r)))
print(json.dumps({'evidence_sha256':sha(r/'curated-evidence.zip'),'file_count':len(files),'input_mismatches':mismatches,'system_header_post_hashing_performed':False,'object_count':len(objects)}))
