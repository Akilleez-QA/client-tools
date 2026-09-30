from pathlib import Path
import zipfile,json,hashlib
roots=[Path('C:/stack-owner-Debug-v1'),Path('C:/stack-owner-Release-v1')];manifest={}
libs=json.loads(Path('C:/allocator-next/core-libraries-all.json').read_text())
for value in set(x for values in libs.values() for x in values):
 p=Path(value)
 if p.exists():manifest[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
for root in roots:
 for p in root.rglob('*'):
  if p.is_file() and p.suffix in ('.exe','.obj','.dll'):manifest[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
manifest['C:/stack-owner-probe.cpp']=hashlib.sha256(Path('C:/stack-owner-probe.cpp').read_bytes()).hexdigest()
with zipfile.ZipFile('C:/stack-owner-evidence.zip','w',zipfile.ZIP_DEFLATED) as z:
 for root in roots:
  for p in root.rglob('*'):
   if p.is_file() and p.suffix in ('.json','.log','.cmd','.map'):z.write(p,root.name+'/'+str(p.relative_to(root)))
 z.writestr('binary-and-input-sha256.json',json.dumps(manifest,indent=2))
