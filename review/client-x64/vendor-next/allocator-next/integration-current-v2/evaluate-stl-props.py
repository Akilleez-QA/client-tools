from pathlib import Path
import subprocess,json,tarfile
out=Path('C:/stl-props-eval-v1');out.mkdir(exist_ok=False);subprocess.run(['subst','Q:','C:/integration-current-v1/workspace'],check=True);root=Path('Q:/repo');ms='C:/Program Files (x86)/MSBuild/12.0/Bin/MSBuild.exe';rows=[]
with tarfile.open('C:/stl-props-input.tar') as t:t.extractall(out/'input',filter='data')
paths=[str(p.relative_to(out/'input/candidate')) for p in (out/'input/candidate').rglob('*') if p.is_file()];original={p:(root/p).read_bytes() if (root/p).exists() else None for p in paths}
t=out/'audit.targets';t.write_text('<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003"><ItemGroup><Link Include="__audit"/><ClCompile Include="__audit"/></ItemGroup><Target Name="Audit"><Message Importance="High" Text="DIRS|%(Link.AdditionalLibraryDirectories)"/><Message Importance="High" Text="INPUTS|%(Link.AdditionalDependencies)"/><Message Importance="High" Text="IGNORE|%(Link.IgnoreSpecificDefaultLibraries)"/><Message Importance="High" Text="DEFINES|%(ClCompile.PreprocessorDefinitions)"/></Target></Project>')
try:
 for variant in ['baseline','candidate']:
  for p in paths:
   source=out/'input'/variant/p
   if source.exists():(root/p).write_bytes(source.read_bytes())
   else:(root/p).unlink(missing_ok=True)
  for name,project in [('SwgClient','src/game/client/application/SwgClient/build/win32/SwgClient.vcxproj'),('Direct3d9','src/engine/client/application/Direct3d9/build/win32/Direct3d9.vcxproj')]:
   for cfg in ['Release','Debug']:
    for platform in ['Win32','x64']:
     cmd=[ms,str(root/project),'/t:Audit','/p:Configuration='+cfg,'/p:Platform='+platform,'/p:ForceImportAfterCppTargets='+str(t),'/p:SwgLogitechLcdSdkDir=C:/lcd-props-eval-v1/LCDSDK','/p:SwgPythonExecutable=C:/ci-dpvs-review/python/python.exe','/p:DXSDK_DIR=C:/SDKs/DXSDK','/v:minimal','/nologo'];r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);label=name+'-'+cfg+'-'+platform+'-'+variant;(out/(label+'.log')).write_bytes(r.stdout);(out/(label+'.cmd.json')).write_text(json.dumps(cmd,indent=2));rows.append(dict(project=name,configuration=cfg,platform=platform,variant=variant,exit=r.returncode));print(rows[-1],flush=True)
 (out/'results.json').write_text(json.dumps(rows,indent=2))
finally:
 for p,data in original.items():
  if data is None:(root/p).unlink(missing_ok=True)
  else:(root/p).write_bytes(data)
