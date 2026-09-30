from pathlib import Path
import json,hashlib,zipfile
b=Path('C:/miles-engine-fixture-v1');r=Path('C:/integration-current-v2/workspace/repo');records={}
for name in ['clientAudio','sharedFoundation','sharedMemoryManager','sharedUtility','sharedFile','sharedMath','sharedRandom','sharedThread','sharedDebug','sharedSynchronization','fileInterface','unicode','archive']:
 p=r/('src/compile/win32/'+name+'/Release/'+name+'.lib')
 if p.exists():records[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
for rel in ['src/engine/client/library/clientAudio/src/win32/Audio.cpp','src/engine/client/library/clientAudio/src/win32/Sound2d.cpp','src/engine/client/library/clientAudio/src/win32/SetupClientAudio.cpp','src/engine/client/library/clientAudio/src/win32/Sound2dTemplate.cpp']:
 p=r/rel;records[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
(b/'real-input-hashes.json').write_text(json.dumps(records,indent=2))
with zipfile.ZipFile(b/'evidence.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in b.iterdir():
  if p.suffix in ['.json','.log','.map','.cpp','.py','.cmd']:z.write(p,p.name)
