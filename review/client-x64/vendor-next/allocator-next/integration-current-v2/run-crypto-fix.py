from pathlib import Path
import subprocess,json,hashlib
base=Path('C:/integration-current-v1');out=Path('C:/crypto-packing-fix-v1');out.mkdir(exist_ok=False);subprocess.run(['subst','Q:',str(base/'workspace')],check=True)
root=Path('Q:/repo');paths=['src/external/ours/library/crypto/src/shared/core/FirstCrypto.h'];original={p:(root/p).read_bytes() for p in paths};records=[]
ms='C:/Program Files (x86)/MSBuild/12.0/Bin/MSBuild.exe'
try:
 for p in paths:
  data=(Path('C:/crypto-packing-input')/Path(p).name).read_bytes();(root/p).write_bytes(data);(out/Path(p).name).write_bytes(data)
 for cfg in ['Release','Debug']:
  for platform in ['Win32','x64']:
   d=out/(cfg+'-'+platform);d.mkdir();t=d/'output.targets';t.write_text('<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003"><ItemDefinitionGroup><Lib><OutputFile>'+str(d/'crypto.lib')+'</OutputFile></Lib></ItemDefinitionGroup></Project>')
   cmd=[ms,str(root/'src/external/ours/library/crypto/build/win32/crypto.vcxproj'),'/t:Rebuild','/p:Configuration='+cfg,'/p:Platform='+platform,'/p:OutDir='+str(d)+'/', '/p:IntDir='+str(d/'obj')+'/', '/p:ForceImportAfterCppTargets='+str(t),'/p:DXSDK_DIR=C:/SDKs/DXSDK','/nologo','/v:normal']
   (d/'cmd.json').write_text(json.dumps(cmd,indent=2))
   with (d/'build.log').open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
   records.append(dict(configuration=cfg,platform=platform,exit=r.returncode));(out/'results.json').write_text(json.dumps(records,indent=2));print(records[-1],flush=True)
finally:
 for p,b in original.items():(root/p).write_bytes(b)
