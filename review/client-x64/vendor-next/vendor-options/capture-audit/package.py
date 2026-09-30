from pathlib import Path
import zipfile
root=Path('C:/capture-poll-candidate-v2')
with zipfile.ZipFile('C:/capture-poll-evidence-v2.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in root.rglob('*'):
  if p.is_file() and p.suffix.lower() in ['.log','.txt','.json','.rsp','.cmd']:
   z.write(p,str(p.relative_to(root)))
 z.write('C:/capture-poll-CuiIoWin.cpp','candidate-CuiIoWin.cpp')
