from pathlib import Path
import zipfile,json,hashlib,struct
summary={}
with zipfile.ZipFile('C:/miles-pipe-text-evidence.zip','w',zipfile.ZIP_DEFLATED) as z:
 for version in range(1,6):
  root=Path('C:/miles-pipe-transport-v'+str(version));name='native-v'+str(version)
  for f in root.rglob('*'):
   if f.is_file() and (f.suffix=='.log' or f.name=='results.json'):z.write(f,name+'/'+str(f.relative_to(root)).replace('\\','/'))
  for f in root.glob('*/fixture.exe'):
   b=f.read_bytes();offset=struct.unpack_from('<I',b,0x3c)[0];machine=struct.unpack_from('<H',b,offset+4)[0]
   summary[name+'/'+f.parent.name]={'sha256':hashlib.sha256(b).hexdigest(),'machine':hex(machine),'bytes':len(b)}
 z.writestr('binary-identities.json',json.dumps(summary,indent=2))
print(summary)
