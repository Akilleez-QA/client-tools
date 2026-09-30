from pathlib import Path
import zipfile
with zipfile.ZipFile('C:/pr-pcre18-text.zip','w',zipfile.ZIP_DEFLATED) as z:
 for name in ['pr-pcre18-revision2','pr-pcre18-tu']:
  root=Path('C:/')/name
  for p in root.rglob('*'):
   if p.is_file() and p.suffix in ['.log','.json','.rsp','.cmd','.py']:
    z.write(p,name+'/'+str(p.relative_to(root)))
