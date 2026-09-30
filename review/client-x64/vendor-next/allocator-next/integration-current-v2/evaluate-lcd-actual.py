from pathlib import Path
import subprocess,json,shutil,hashlib
out=Path('C:/lcd-props-actual-v1');out.mkdir(exist_ok=False);subprocess.run(['subst','Q:','C:/integration-current-v1/workspace'],check=True);root=Path('Q:/repo');proj=root/'src/game/client/application/SwgClient/build/win32/SwgClient.vcxproj';ms='C:/Program Files (x86)/MSBuild/12.0/Bin/MSBuild.exe';rows=[]
paths=['tools/configure-client-x64/client-x64.props','tools/build-client-deps/logitech-lcd.props','tools/build-client-deps/validate-logitech-lcd.py'];original={p:(root/p).read_bytes() if (root/p).exists() else None for p in paths}
t=out/'audit.targets';t.write_text('<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003"><ItemGroup><Link Include="__audit"/></ItemGroup><Target Name="Audit"><Message Importance="High" Text="DIRS|%(Link.AdditionalLibraryDirectories)"/><Message Importance="High" Text="INPUTS|%(Link.AdditionalDependencies)"/></Target></Project>')
try:
 for candidate in [False,True]:
  if candidate:
   for p in paths:
    data=(Path('C:/lcd-actual-input')/Path(p).name).read_bytes();(root/p).write_bytes(data);(out/Path(p).name).write_bytes(data)
  for cfg in ['Release','Debug']:
   for platform in ['Win32','x64']:
    cmd=[ms,str(proj),'/t:'+('ValidateSwgLogitechLcd;Audit' if candidate and platform=='x64' else 'Audit'),'/p:Configuration='+cfg,'/p:Platform='+platform,'/p:ForceImportAfterCppTargets='+str(t),'/p:SwgLogitechLcdSdkDir=C:/lcd-props-eval-v1/LCDSDK','/p:SwgPythonExecutable=C:/ci-dpvs-review/python/python.exe','/p:DXSDK_DIR=C:/SDKs/DXSDK','/v:minimal','/nologo'];r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);name=cfg+'-'+platform+('-candidate' if candidate else '-baseline');(out/(name+'.log')).write_bytes(r.stdout);(out/(name+'.cmd.json')).write_text(json.dumps(cmd,indent=2));rows.append(dict(configuration=cfg,platform=platform,candidate=candidate,exit=r.returncode));print(rows[-1],flush=True)
 (out/'results.json').write_text(json.dumps(rows,indent=2))
finally:
 for p,data in original.items():
  if data is None:(root/p).unlink(missing_ok=True)
  else:(root/p).write_bytes(data)
