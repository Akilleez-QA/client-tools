from pathlib import Path
import subprocess,json,shutil
out=Path('C:/lcd-props-eval-v1');out.mkdir(exist_ok=False);sdk=out/'LCDSDK';(sdk/'Lib/x64').mkdir(parents=True);shutil.copy2('C:/vendor-reachability/lcd-legacy/amd64/lglcd.lib',sdk/'Lib/x64/lglcd.lib')
proj=Path('C:/integration-current-v2/workspace/repo/src/game/client/application/SwgClient/build/win32/SwgClient.vcxproj');ms='C:/Program Files (x86)/MSBuild/12.0/Bin/MSBuild.exe';rows=[]
for candidate in [False,True]:
 t=out/('candidate.targets' if candidate else 'baseline.targets');t.write_text('<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003">'+('<Import Project="C:/lcd-props-input/logitech-lcd.props"/>' if candidate else '')+'<ItemGroup><Link Include="__audit"/></ItemGroup><Target Name="Audit"><Message Importance="High" Text="DIRS|%(Link.AdditionalLibraryDirectories)"/><Message Importance="High" Text="INPUTS|%(Link.AdditionalDependencies)"/></Target></Project>')
 for cfg in ['Release','Debug']:
  for platform in ['Win32','x64']:
   cmd=[ms,str(proj),'/t:'+('ValidateSwgLogitechLcd;Audit' if candidate else 'Audit'),'/p:Configuration='+cfg,'/p:Platform='+platform,'/p:ForceImportAfterCppTargets='+str(t),'/p:SwgLogitechLcdSdkDir='+str(sdk),'/p:SwgPythonExecutable=C:/ci-dpvs-review/python/python.exe','/p:DXSDK_DIR=C:/SDKs/DXSDK','/v:minimal','/nologo']
   r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);name=cfg+'-'+platform+('-candidate' if candidate else '-baseline');(out/(name+'.log')).write_bytes(r.stdout);rows.append(dict(configuration=cfg,platform=platform,candidate=candidate,exit=r.returncode));print(rows[-1],flush=True)
(out/'results.json').write_text(json.dumps(rows,indent=2))
