"""Freeze exact playback-pipe34 composition plus3 owned-playback overlays."""
from pathlib import Path
import hashlib,json,shutil,difflib,tarfile,ast
b=Path(__file__).resolve().parent;prior=b.parent/'alias-native36';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if h(prior/'source-manifest.json')!='ae42fe85b0484d904b8987c8966285792983e439e882b9fb3ef92912521873a1':raise RuntimeError('prior manifest mismatch')
m=json.loads((prior/'source-manifest.json').read_text());stage=b/'private-source-v1';stage.mkdir(exist_ok=False);patches=b/'patches';patches.mkdir(exist_ok=False)
changed=['backend-boundary24/pipe/ClientMilesPipe.cpp','startup-bridge23/reply.h','protocol-candidate/API-MAP.md']
for n,v in m.items():
 source=prior/'private-source-v1'/n
 if h(source)!=v:raise RuntimeError('prior input changed '+n)
 target=stage/n;target.parent.mkdir(parents=True,exist_ok=True)
 if n in changed:
  newer=b/'overlay'/n
  patch=''.join(difflib.unified_diff(source.read_text().splitlines(True),newer.read_text().splitlines(True),fromfile='a/'+n,tofile='b/'+n))
  (patches/(str(changed.index(n)+1)+'-'+Path(n).stem+'.patch')).write_text(patch);source=newer
 shutil.copyfile(source,target)
for source in (b/'overlay').rglob('*'):
 if source.is_file():
  target=stage/source.relative_to(b/'overlay');target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
for source in list(b.iterdir())+list(patches.iterdir()):
 if source.is_file() and source.suffix in ['.py','.cpp','.md','.patch']:
  if source.suffix=='.py':ast.parse(source.read_text())
  n='stream-proxy37/'+str(source.relative_to(b));target=stage/n;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
entries={str(p.relative_to(stage)):h(p) for p in sorted(stage.rglob('*')) if p.is_file()}
with (b/'source-manifest.json').open('x') as f:json.dump(entries,f,indent=2);f.write('\n')
with tarfile.open(b/'source-v1.tar','x') as t:
 for n in entries:t.add(stage/n,arcname=n,recursive=False)
 t.add(b/'source-manifest.json',arcname='source-manifest.json',recursive=False)
print(json.dumps({'source':h(b/'source-v1.tar'),'manifest':h(b/'source-manifest.json'),'files':len(entries)},indent=2))
