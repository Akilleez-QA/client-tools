from pathlib import Path
import tarfile
root=Path('C:/sample-live31')
with tarfile.open(root/'text-evidence-v1.tar','x') as t:
 for p in sorted((root/'build-v1').rglob('*')):
  if p.is_file() and p.suffix.lower() in ['.log','.json','.sha256']:
   t.add(p,arcname=str(p.relative_to(root/'build-v1')),recursive=False)
with tarfile.open(root/'private-pair-v1.tar','x') as t:
 for name in ['x86-Release/host.exe','amd64-Release/controller.exe']:
  p=root/'build-v1'/name
  if p.is_file():t.add(p,arcname=name,recursive=False)
