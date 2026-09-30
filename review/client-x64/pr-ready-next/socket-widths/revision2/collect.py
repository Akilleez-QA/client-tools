from pathlib import Path
import tarfile
roots=[Path('C:/pr-network18-v1-tus'),Path('C:/pr-network18-v1-tus-attempt2'),Path('C:/pr-network18-v2-all')]
with tarfile.open('C:/pr-network18-results-text.tar.gz','w:gz') as t:
 for root in roots:
  if not root.exists():continue
  for p in root.rglob('*'):
   if p.is_file() and p.suffix in ('.log','.json','.cmd','.py','.cpp','.h','.hpp'):
    t.add(p,arcname=root.name+'/'+p.relative_to(root).as_posix())
