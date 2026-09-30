from pathlib import Path
import zipfile,json,struct
root=Path('C:/null-realloc-compile-v1');r=json.loads((root/'results.json').read_text())
for row in r:
 d=root/(row['configuration']+'-'+row['platform'])/({'MemoryManager.cpp':'sharedMemoryManager','SetupSharedXml.cpp':'sharedXml','OciSession.cpp':'sharedDatabaseInterface'}[row['source']])/row['variant']
 row['machine']=struct.unpack('<H',(d/'source.obj').read_bytes()[:2])[0]
 assert row['compile_exit']==0 and row['machine']==(0x14c if row['platform']=='win32' else 0x8664)
(root/'verified-results.json').write_text(json.dumps(r,indent=2))
with zipfile.ZipFile('C:/null-realloc-compile-v1.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in root.rglob('*'):
  if p.is_file() and p.suffix.lower() in ['.json','.cpp','.cmd','.rsp','.log']:z.write(p,str(p.relative_to(root)))
print('16/16 actual TU compile checks, architecture verified; no executables built or run')
