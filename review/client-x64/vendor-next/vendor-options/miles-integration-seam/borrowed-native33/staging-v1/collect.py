from pathlib import Path
import tarfile
root=Path('C:/borrowed-native33')
with tarfile.open(root/'text-evidence-v1.tar','x') as t:
 for p in sorted((root/'native-v1').rglob('*')):
  if p.is_file() and p.suffix.lower() in ['.log','.json','.sha256','.cmd']:
   t.add(p,arcname=str(p.relative_to(root/'native-v1')),recursive=False)
