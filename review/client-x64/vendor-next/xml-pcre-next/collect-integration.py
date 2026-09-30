from pathlib import Path
import zipfile
with zipfile.ZipFile('C:/parser-integration-evidence.zip','w',zipfile.ZIP_DEFLATED) as z:
 for name in ['parser-integration-v3','parser-integration-reject-v1']:
  root=Path('C:/'+name)
  for p in root.rglob('*'):
   if p.is_file() and p.suffix in ['.json','.log']:
    z.write(p,name+'/'+p.relative_to(root).as_posix())
