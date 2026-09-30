from pathlib import Path
import json,hashlib,shutil,tarfile,ast
b=Path(__file__).resolve().parent;prior=b.parent/'alias-pipe35';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if h(prior/'source-manifest.json')!='71e13b03df1ddd336ff243ed168717ca78df042a87b483b1dc40cc0df98fbd87':raise RuntimeError('prior mismatch')
m=json.loads((prior/'source-manifest.json').read_text());stage=b/'private-source-v1';stage.mkdir(exist_ok=False)
for n,v in m.items():
 p=prior/'private-source-v1'/n
 if h(p)!=v:raise RuntimeError('changed '+n)
 q=stage/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
for p in b.iterdir():
 if p.is_file() and p.suffix in ['.py','.md','.cpp','.json']:
  if p.suffix=='.py':ast.parse(p.read_text())
  q=stage/'alias-native36'/p.name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
m={str(p.relative_to(stage)):h(p) for p in sorted(stage.rglob('*')) if p.is_file()}
with (b/'source-manifest.json').open('x') as f:json.dump(m,f,indent=2);f.write('\n')
with tarfile.open(b/'source-v1.tar','x') as t:
 for n in m:t.add(stage/n,arcname=n,recursive=False)
 t.add(b/'source-manifest.json',arcname='source-manifest.json',recursive=False)
print(json.dumps({'source':h(b/'source-v1.tar'),'manifest':h(b/'source-manifest.json'),'files':len(m)},indent=2))
