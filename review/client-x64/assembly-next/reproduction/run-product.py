from pathlib import Path
import subprocess,json,time
out=Path('C:/assembly-product');out.mkdir(exist_ok=False)
results=[]
for platform in ['Win32','x64']:
 cmd=['C:/Program Files (x86)/MSBuild/12.0/Bin/MSBuild.exe','C:/client-next-build/src/build/win32/swg.sln','/t:SwgClient','/p:Configuration=Release','/p:Platform='+platform,'/p:DXSDK_DIR=C:/SDKs/DXSDK','/m:2','/v:normal','/nologo']
 (out/(platform+'.cmd.json')).write_text(json.dumps(cmd))
 t=time.time()
 with (out/(platform+'.log')).open('w') as f: code=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT).returncode
 (out/(platform+'.exit')).write_text(str(code));results.append(dict(platform=platform,exit=code,seconds=time.time()-t));print(results[-1],flush=True)
(out/'results.json').write_text(json.dumps(results,indent=2))
