from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
root=Path('C:/vendor-lcd-integration')
with ZipFile(root/'evidence.zip','w',ZIP_DEFLATED) as z:
 for p in root.rglob('*'):
  if p.is_file() and p.suffix in ('.json','.log','.map','.txt','.cmd','.cpp'):
   z.write(p,p.relative_to(root))
