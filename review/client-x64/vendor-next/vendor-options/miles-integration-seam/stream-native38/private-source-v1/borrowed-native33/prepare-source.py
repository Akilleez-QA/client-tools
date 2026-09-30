"""Compose frozen authored inputs and borrowed32 overlay; no compiler/VM invocation."""
from pathlib import Path
import hashlib,json,tarfile,ast,shutil
b=Path(__file__).resolve().parent;seam=b.parent
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
stage=b/'private-source-v1';stage.mkdir(exist_ok=False)
old=seam/'sample-live31'
if h(old/'source-manifest.json')!='e5a0e2e249226cc6e08bec7d7a2a86d7f5c6cf05b3bf283a604e22f09d5be734':raise RuntimeError('private31 manifest pin')
manifest=json.loads((old/'source-manifest.json').read_text())
# Frozen private implementation dependencies; compile only its renamed TU.
for n,v in manifest.items():
    if n.startswith('sample-live31/'):continue
    source=old/'private-source-v1'/n
    if h(source)!=v:raise RuntimeError('private31 changed '+n)
    target=stage/n;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
for group in ['native-sample27','native-playback28','native-stream28']:
    m=json.loads((seam/group/'source-manifest.json').read_text())
    for n,v in m.items():
        if not n.startswith(group+'/') or Path(n).suffix not in ['.h','.cpp']:continue
        source=seam/n
        if h(source)!=v:raise RuntimeError('native input changed '+n)
        target=stage/n;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
proposal=seam/'native-borrowed32'
if h(proposal/'source-manifest.json')!='0c76fc1457991c5e2f579c7cf108499a82f56011ffa1e7438a8f565a70c6da4a':raise RuntimeError('proposal32 pin')
for n,v in json.loads((proposal/'source-manifest.json').read_text()).items():
    source=proposal/n
    if h(source)!=v:raise RuntimeError('proposal changed '+n)
    dest=n[len('overlay/'):] if n.startswith('overlay/') else 'native-borrowed32/'+n
    target=stage/dest;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
for source in b.iterdir():
    if source.is_file() and source.suffix in ['.py','.json','.md'] and source.name!='source-manifest.json':
        if source.suffix=='.py':ast.parse(source.read_text())
        target=stage/'borrowed-native33'/source.name;target.parent.mkdir(exist_ok=True);shutil.copyfile(source,target)
expected=json.loads((b/'expected.json').read_text())
if len(expected)!=11 or [len(x['imports']) for x in expected[:3]]!=[5,19,9]:raise RuntimeError('prospective unit/import count')
for x in expected:
    if not (stage/x['source']).is_file():raise RuntimeError('missing TU')
entries={str(p.relative_to(stage)):h(p) for p in sorted(stage.rglob('*')) if p.is_file()}
with (b/'source-manifest.json').open('x') as f:json.dump(entries,f,indent=2);f.write('\n')
with tarfile.open(b/'source-v1.tar','x') as t:
    for n in entries:t.add(stage/n,arcname=n,recursive=False)
    t.add(b/'source-manifest.json',arcname='source-manifest.json',recursive=False)
print(json.dumps({'source':h(b/'source-v1.tar'),'manifest':h(b/'source-manifest.json'),'files':len(entries)},indent=2))
