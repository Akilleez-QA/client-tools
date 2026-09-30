"""Compose immutable live27 source with two reviewed authored overlays; no execution."""
from pathlib import Path
import hashlib,json,shutil,difflib,tarfile
b=Path(__file__).resolve().parent
base=b.parent/'pipe-live27'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if h(base/'source-manifest.json')!='a91c57521828ca3bd94963593d19747a802de7f3da64a6dbe71d37f9f8bb5902':raise RuntimeError('live27 manifest mismatch')
old=json.loads((base/'source-manifest.json').read_text())
paths=['transport-candidate/resource_registry.h','startup-bridge23/backend.h']
patches=b/'patches';patches.mkdir(exist_ok=False)
for i,n in enumerate(paths,1):
    original=base/'private-source-v1'/n
    if h(original)!=old[n]:raise RuntimeError('original mismatch')
    patch=''.join(difflib.unified_diff(original.read_text().splitlines(True),(b/'overlay'/n).read_text().splitlines(True),fromfile='a/'+n,tofile='b/'+n))
    (patches/('%02d-'%i+Path(n).stem+'.patch')).write_text(patch)
prepared=b/'prepared';prepared.mkdir(exist_ok=False)
for n,v in old.items():
    if Path(n).suffix not in ('.h','.cpp'):continue
    original=base/'private-source-v1'/n
    if h(original)!=v:raise RuntimeError('source mismatch '+n)
    source=b/'overlay'/n if n in paths else original
    target=prepared/n;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
for p in b.iterdir():
    if p.is_file() and p.suffix in ('.py','.cpp','.md'):
        target=prepared/'sample-host29'/p.name;target.parent.mkdir(exist_ok=True);shutil.copyfile(p,target)
for p in patches.iterdir():
    target=prepared/'sample-host29/patches'/p.name;target.parent.mkdir(exist_ok=True);shutil.copyfile(p,target)
manifest={str(p.relative_to(prepared)):h(p) for p in sorted(prepared.rglob('*')) if p.is_file()}
with (b/'source-manifest.json').open('x') as f:json.dump(manifest,f,indent=2);f.write('\n')
with tarfile.open(b/'source-v1.tar','x') as t:
    for n in manifest:t.add(prepared/n,arcname=n,recursive=False)
    t.add(b/'source-manifest.json',arcname='sample-host29/source-manifest.json',recursive=False)
print(json.dumps({'manifest':h(b/'source-manifest.json'),'source':h(b/'source-v1.tar'),'files':len(manifest)},indent=2))
