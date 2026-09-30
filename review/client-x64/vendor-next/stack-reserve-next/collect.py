from pathlib import Path
import zipfile
r=Path('C:/stack-actual-position-v1')
with zipfile.ZipFile('C:/stack-actual-position-evidence.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in r.rglob('*'):
  if p.is_file() and p.suffix in ('.log','.json','.cmd','.c'):z.write(p,str(p.relative_to(r)))
