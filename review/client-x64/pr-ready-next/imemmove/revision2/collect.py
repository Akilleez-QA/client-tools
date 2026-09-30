from pathlib import Path
import zipfile
root=Path('C:/pr-imemmove18-v2')
with zipfile.ZipFile('C:/pr-imemmove18-v2-text.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in root.rglob('*'):
  if p.is_file() and p.suffix in ['.log','.json','.rsp','.cmd']:z.write(p,str(p.relative_to(root)))
