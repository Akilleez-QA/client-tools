"""Local source composition only. Never contacts the VM or executes native code."""
from pathlib import Path
import ast,hashlib,json,re,shutil,subprocess,tarfile
base=Path(__file__).resolve().parent;root=base.parent
stage=base/'private-source-v1';stage.mkdir(exist_ok=False)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
frozen=root/'pipe-startup26/source-manifest.json'
if digest(frozen)!='09d5d3c749d4e2ac8e431c1d44788ae69804a1c9cfff5e5abb80be285db23bcf':raise RuntimeError('frozen26 manifest identity')
original=json.loads(frozen.read_text())
for n,h in original.items():
 if digest(root/n)!=h:raise RuntimeError('frozen26 source identity: '+n)
queue=[root/n for n in original]
queue += [root/'backend-boundary24/pipe/LiveChannel.cpp',base/'native/host_composition.cpp',
          root/'native-startup25/tests/portable_contract.cpp',base/'build-native.py',base/'prepare.py',base/'PLAN.md']
inputs={}
while queue:
 p=queue.pop().resolve();n=str(p.relative_to(root))
 if n in inputs:continue
 inputs[n]=digest(p);dest=stage/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
 for name in re.findall(r'^\s*#include\s+"([^"]+)"',p.read_text(),re.M):
  q=(p.parent/name).resolve()
  if q.is_file() and q.is_relative_to(root):queue.append(q)
logs=[]
for p in sorted((root/'pipe-startup26/patches').glob('*.patch')):
 command=['patch','--batch','--forward','--fuzz=0','-p1','-i',str(p)]
 result=subprocess.run(command,cwd=stage,capture_output=True,text=True,timeout=60)
 logs.append({'command':command,'exit':result.returncode,'output':result.stdout+result.stderr})
 if result.returncode:raise RuntimeError('overlay failed: '+p.name)
for p in (base/'build-native.py',base/'prepare.py',stage/'native-startup25/build-native.py'):ast.parse(p.read_text())
assert all(digest(root/n)==h for n,h in inputs.items())
(base/'original-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
(base/'composition-log.json').write_text(json.dumps(logs,indent=2)+'\n')
manifest={str(p.relative_to(stage)):digest(p) for p in sorted(stage.rglob('*')) if p.is_file()}
mp=stage/'pipe-native26/source-manifest.json';mp.write_text(json.dumps(manifest,indent=2)+'\n')
shutil.copyfile(mp,base/'source-manifest.json')
with tarfile.open(base/'source-v1.tar','w') as t:
 for p in sorted(stage.rglob('*')):
  if p.is_file():t.add(p,arcname=str(p.relative_to(stage)),recursive=False)
ids={n:digest(base/n) for n in ['PLAN.md','build-native.py','prepare.py','source-manifest.json','source-v1.tar','original-inputs.json','composition-log.json']}
(base/'FREEZE-v1.json').write_text(json.dumps(ids,indent=2)+'\n')
print(json.dumps(ids,indent=2))
