from pathlib import Path
import hashlib,json,subprocess,tarfile,zipfile,io
r=Path('/home/akilleez/Work/swg-source/client-pr-evidence');b=r/'review/client-x64/vendor-next'
m=json.loads((b/'manifest.json').read_text());tracked=set(subprocess.check_output(['git','ls-tree','-r','--name-only','HEAD'],cwd=r,text=True).splitlines());checked=0
allowed={'.md','.json','.py','.cpp','.c','.h','.hpp','.patch','.diff','.txt','.log','.cmd','.sh','.ps1','.sha256','.yaml','.yml','.csv','.sln','.vcxproj','.props'}
def audit(name,data,depth=0):
 global checked
 q=Path(name)
 if q.is_absolute() or '..' in q.parts or q.name.lower()=='mss.h' or data.startswith((b'MZ',b'\x7fELF')):raise RuntimeError('forbidden '+name)
 if depth>4:raise RuntimeError('nested archive '+name)
 if q.suffix=='.tar':
  with tarfile.open(fileobj=io.BytesIO(data)) as t:
   for x in t.getmembers():
    if x.isdir():continue
    if not x.isfile():raise RuntimeError('archive link '+x.name)
    audit(x.name,t.extractfile(x).read(),depth+1)
 elif q.suffix=='.zip':
  with zipfile.ZipFile(io.BytesIO(data)) as z:
   for x in z.infolist():
    if not x.is_dir():audit(x.filename,z.read(x),depth+1)
 else:
  if q.suffix not in allowed and q.name != '.gitignore':raise RuntimeError('noncurated extension '+name)
  data.decode('utf8')
 checked+=1
new=[]
for rel,v in m.items():
 p=b/rel;d=p.read_bytes()
 if len(d)!=v['bytes'] or hashlib.sha256(d).hexdigest()!=v['sha256']:raise RuntimeError('manifest '+rel)
 if str(p.relative_to(r)) not in tracked:
  audit(rel,d);new.append(str(p.relative_to(r)))
print(json.dumps({'manifest_files':len(m),'new_files':len(new),'new_recursive_members_checked':checked,'result':'authored text/source only; all manifest bytes match'}))
